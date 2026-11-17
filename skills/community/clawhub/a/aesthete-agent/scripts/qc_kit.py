# -*- coding: utf-8 -*-
"""qc_kit.py — qc 命令实现体:渲染实况对声明令牌的机械对账(渲染反馈闭环的闸)。

纯 stdlib PNG 解码(8bit/RGB·RGBA·调色板/非隔行)→像素网格采样→颜色聚类→
与 tokens.json 或声明色板对账:大底是否真被渲染、板外色入侵(带面积份额)、
三方对账(页面声明 vs 令牌 vs 实测)。双哈希类 bug(变量失效/覆盖丢失导致
页面实际颜色静默漂移)在这里现形。被 palette_forge.py 的 cmd_qc 调用。
"""
import hashlib
import json
import math
import os
import struct
import sys
import zlib


# ------------------------------------------------------------- PNG 解析(纯 stdlib)

def _paeth(a, b, c):
    p = a + b - c
    pa, pb, pc = abs(p - a), abs(p - b), abs(p - c)
    if pa <= pb and pa <= pc:
        return a
    return b if pb <= pc else c


def decode_png(path):
    """8bit/非隔行 PNG → (width, height, pixels(list of (r,g,b)))。
    不支持的形态(16bit/隔行/灰度外色彩)如实抛 ValueError。"""
    raw = open(path, "rb").read()
    if raw[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("不是 PNG")
    pos, idat, w = 8, b"", 0
    height = bitdepth = colortype = interlace = 0
    palette = []
    while pos < len(raw):
        ln, typ = struct.unpack(">I4s", raw[pos:pos + 8])
        data = raw[pos + 8:pos + 8 + ln]
        pos += 12 + ln
        if typ == b"IHDR":
            w, height, bitdepth, colortype, comp, filt, interlace = struct.unpack(">IIBBBBB", data)
        elif typ == b"PLTE":
            palette = [tuple(data[i:i + 3]) for i in range(0, len(data), 3)]
        elif typ == b"IDAT":
            idat += data
        elif typ == b"IEND":
            break
    if bitdepth != 8:
        raise ValueError(f"仅支持 8bit(得到 {bitdepth}bit)")
    if interlace != 0:
        raise ValueError("不支持隔行(Adam7)")
    channels = {0: 1, 2: 3, 3: 1, 4: 2, 6: 4}.get(colortype)
    if channels is None:
        raise ValueError(f"不支持的色彩类型 {colortype}")
    if colortype == 3 and not palette:
        raise ValueError("调色板图缺 PLTE")
    stride = w * channels
    flat = zlib.decompress(idat)
    out = bytearray(stride * height)
    prev = bytearray(stride)
    for y in range(height):
        ft = flat[y * (stride + 1)]
        line = bytearray(flat[y * (stride + 1) + 1:(y + 1) * (stride + 1)])
        if ft == 1:
            for i in range(channels, stride):
                line[i] = (line[i] + line[i - channels]) & 0xFF
        elif ft == 2:
            for i in range(stride):
                line[i] = (line[i] + prev[i]) & 0xFF
        elif ft == 3:
            for i in range(stride):
                left = line[i - channels] if i >= channels else 0
                line[i] = (line[i] + ((left + prev[i]) >> 1)) & 0xFF
        elif ft == 4:
            for i in range(stride):
                left = line[i - channels] if i >= channels else 0
                ul = prev[i - channels] if i >= channels else 0
                line[i] = (line[i] + _paeth(left, prev[i], ul)) & 0xFF
        out[y * stride:(y + 1) * stride] = line
        prev = line
    pixels = []
    for y in range(height):
        row = out[y * stride:(y + 1) * stride]
        for x in range(w):
            p = row[x * channels:(x + 1) * channels]
            if colortype == 3:
                pixels.append(palette[p[0]])
            elif colortype == 0:
                v = p[0]
                pixels.append((v, v, v))
            elif colortype == 4:
                v = p[0]
                pixels.append((v, v, v))
            else:
                pixels.append((p[0], p[1], p[2]))
    return w, height, pixels


# ------------------------------------------------------------- 聚类与对账

def _hexof(rgb):
    return "%02X%02X%02X" % rgb


def clusters(pixels, max_px=60000):
    """网格采样 → 近邻合并聚类 → [(hex, share), ...] 按份额降序。"""
    step = max(1, int(math.sqrt(len(pixels) / max_px)))
    sample = pixels[::step]
    counts = {}
    for p in sample:
        counts.setdefault(_hexof(p), 0)
        counts[_hexof(p)] += 1
    total = sum(counts.values())
    ordered = sorted(counts.items(), key=lambda kv: -kv[1])
    merged = []
    from palette_forge import oklch_from_hex
    for h, c in ordered:
        L, a, b = oklch_from_hex(h)
        for m in merged:
            L2, a2, b2 = m["_lab"]
            if math.sqrt((L - L2) ** 2 + (a - a2) ** 2 + (b - b2) ** 2) < 0.06:
                m["share"] += c / total
                break
        else:
            merged.append({"hex": h, "share": c / total, "_lab": (L, a, b)})
    return [{k: (round(v, 4) if k == "share" else v) for k, v in m.items() if k != "_lab"}
            for m in merged[:14]]


def _nearest_declared(h, declared):
    from palette_forge import oklch_from_hex
    L, a, b = oklch_from_hex(h)
    best, bestd = None, 1e9
    for d in declared:
        L2, a2, b2 = oklch_from_hex(d)
        dd = math.sqrt((L - L2) ** 2 + (a - a2) ** 2 + (b - b2) ** 2)
        if dd < bestd:
            best, bestd = d, dd
    return best, bestd


def qc_image(png, declared, bg=None, min_share=0.015):
    """→ (payload dict)。declared = 声明色 hex 列表;bg = 声明大底(可空)。"""
    w, h, pixels = decode_png(png)
    cls = clusters(pixels)
    chroma = [c for c in cls if not (max(int(c["hex"][i:i + 2], 16) for i in (0, 2, 4)) -
                                     min(int(c["hex"][i:i + 2], 16) for i in (0, 2, 4))) < 30]
    findings = []
    bg_ok = None
    if bg:
        bg = bg.upper().lstrip("#")
        top = cls[0]
        _, d = _nearest_declared(top["hex"], [bg])
        bg_ok = d < 0.08
        if not bg_ok:
            near, dn = _nearest_declared(top["hex"], declared)
            findings.append({
                "sev": "P0", "check": "bg_mismatch",
                "msg": "大底漂移:渲染主色 #%s(占 %.0f%%)≠ 声明大底 #%s" % (
                    top["hex"], top["share"] * 100, bg),
                "fix": "查令牌是否真被引用(变量被覆盖/未加载是常见根因);实测最近声明色 #%s(ΔE %.2f)" % (near, dn)})
    intruders = []
    for c in chroma:
        _, d = _nearest_declared(c["hex"], declared)
        if d >= 0.10 and c["share"] >= min_share:
            near, _ = _nearest_declared(c["hex"], declared)
            intruders.append({"hex": c["hex"], "share": c["share"], "nearest": near})
    for it in sorted(intruders, key=lambda x: -x["share"])[:5]:
        sev = "P1" if it["share"] >= 0.03 else "P2"
        findings.append({
            "sev": sev, "check": "off_palette",
            "msg": "板外入侵:#%s 占 %.1f%%(渲染实测)" % (it["hex"], it["share"] * 100),
            "fix": "改用最近声明色 #%s,或把它正式补进声明(有语义的私货色须登记)" % it["nearest"]})
    n_p0 = sum(1 for f in findings if f["sev"] == "P0")
    n_p1 = sum(1 for f in findings if f["sev"] == "P1")
    verdict = "FAIL" if (n_p0 or n_p1 >= 1) else ("PASS" if not findings else "WARN")
    with open(png, "rb") as f:
        img_fp = hashlib.sha256(f.read()).hexdigest()
    payload = {
        "image": os.path.abspath(png), "image_sha256": img_fp,
        "size": [w, h], "sampled_pixels": min(len(pixels), 60000),
        "declared": [d.upper().lstrip("#") for d in declared],
        "declared_bg": (bg or "").upper().lstrip("#") or None,
        "clusters": cls, "findings": findings, "verdict": verdict,
    }
    payload["fingerprint"] = hashlib.sha256(
        ("aesthete-qc/v1|" + img_fp + "|" + ",".join(payload["declared"]) + "|" + verdict)
        .encode("utf-8")).hexdigest()
    return payload
