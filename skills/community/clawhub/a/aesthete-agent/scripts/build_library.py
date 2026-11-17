#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""build_library.py — 扩库流水线(随包发布)。

从收割的原始 JSON(源站排序页卡片数据,格式见 references/harvest-playbook.md)
构建调色板库:去重、HSL 风格标签、点赞分层、客观质量门(平坦明度/无可读对拒,
色盲碰撞/slop/窄明度打旗)。

用法:
  python build_library.py --raw <目录含 *_raw.json> --out <库文件.json>
原始 JSON 格式: [{"name":..., "likes":"34.9K", "hexes":[{"hex":"780000","light":false},...]}, ...]
或 {"palettes":[同上]}。
"""
import argparse, colorsys, glob, json, math, os, sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

TAILWIND = {"3B82F6", "6366F1", "8B5CF6", "A855F7", "EC4899", "4F46E5", "0EA5E9", "22D3EE"}

def rgb(h):
    h = h.lstrip("#"); return tuple(int(h[i:i+2], 16)/255 for i in (0, 2, 4))
def hsl(h):
    hh, ll, ss = colorsys.rgb_to_hls(*rgb(h)); return hh*360, ll, ss
def oklab(h):
    lin = lambda c: c/12.92 if c <= 0.04045 else ((c+0.055)/1.055)**2.4
    r, g, b = (lin(c) for c in rgb(h))
    l = 0.4122214708*r + 0.5363325363*g + 0.0514459929*b
    m = 0.2119034982*r + 0.6806995451*g + 0.1073969566*b
    s = 0.0883024619*r + 0.2817188376*g + 0.6299787005*b
    l_, m_, s_ = l**(1/3), m**(1/3), s**(1/3)
    return (0.2104542553*l_+0.7936177850*m_-0.0040720468*s_,
            1.9779984951*l_-2.4285922050*m_+0.4505937099*s_,
            0.0259040371*l_+0.7827717662*m_-0.8086757660*s_)
def rlum(h):
    lin = lambda c: c/12.92 if c <= 0.04045 else ((c+0.055)/1.055)**2.4
    r, g, b = (lin(c) for c in rgb(h))
    return 0.2126*r + 0.7152*g + 0.0722*b
def contrast(a, b):
    l1, l2 = sorted((rlum(a), rlum(b)), reverse=True)
    return (l1+0.05)/(l2+0.05)
def deutan(h):
    r, g, b = rgb(h)
    m = (0.367322, 0.860646, -0.227968, 0.280085, 0.672501, 0.047413, -0.011820, 0.042940, 0.968881)
    o = tuple(min(1, max(0, m[i]*r+m[i+1]*g+m[i+2]*b)) for i in (0, 3, 6))
    return oklab("".join("%02X" % round(c*255) for c in o))
def mind(cols, fn):
    labs = [fn(c) for c in cols]
    return min(math.dist(labs[i], labs[j]) for i in range(len(labs)) for j in range(i+1, len(labs)))
def likes(s):
    s = (s or "").strip().upper()
    try:
        return int(float(s[:-1]) * {"K": 1e3, "M": 1e6}[s[-1]]) if s[-1] in "KM" else int(s)
    except Exception:
        return 0

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--raw", required=True, help="收割 JSON 所在目录")
    ap.add_argument("--out", required=True, help="输出库文件")
    a = ap.parse_args()

    store = {}
    for fp in sorted(glob.glob(os.path.join(a.raw, "*_raw.json"))):
        d = json.load(open(fp, encoding="utf-8"))
        for p in (d.get("palettes") if isinstance(d, dict) else d):
            hexes = [h["hex"].upper() for h in p.get("hexes", []) if h.get("hex")]
            if len(hexes) < 3:
                continue
            store.setdefault("#".join(sorted(hexes)), []).append((os.path.basename(fp), p))

    kept, rej = [], []
    for key, grp in store.items():
        fp0, p = grp[-1]
        hexes = [h.upper() for h in p.get("hexes", [])]
        Ls = [hsl(h)[1] for h in hexes]
        span = max(Ls) - min(Ls)
        bestc = max(contrast(x, y) for i, x in enumerate(hexes) for y in hexes[i+1:])
        if span < 0.15:
            rej.append((hexes[0], f"平坦明度 {span:.2f}")); continue
        if bestc < 4.5:
            rej.append((hexes[0], f"无可读对 {bestc:.2f}:1")); continue
        pairs = [(i, j) for i in range(len(hexes)) for j in range(i+1, len(hexes))]
        cb = min(min(mind([hexes[i], hexes[j]], oklab), mind([hexes[i], hexes[j]], deutan)) for i, j in pairs)
        purples = [oklab(h) for h in hexes
                   if 275 <= (math.degrees(math.atan2(oklab(h)[2], oklab(h)[1])) % 360) <= 330
                   and math.hypot(*oklab(h)[1:]) > 0.12]
        flags = (["CB-COLLISION-RISK"] if cb < 0.02 else []) + \
                (["SLOP-SIGNATURE"] if set(hexes) & TAILWIND or len(purples) >= 2 else []) + \
                (["NARROW-LIGHTNESS"] if span < 0.25 else [])
        hues = [hsl(h)[0] for h in hexes]
        sin_s = sum(math.sin(math.radians(x)) for x in hues) / len(hues)
        cos_s = sum(math.cos(math.radians(x)) for x in hues) / len(hues)
        spread = (1 - math.hypot(sin_s, cos_s)) * 360
        ml, ms = sum(Ls)/len(Ls), sum(hsl(h)[2] for h in hexes)/len(hexes)
        tags = ["warm" if sum(1 for x in hues if x >= 310 or x < 70) >= len(hues)/2 else "cool",
                "dark" if ml < 0.35 else "light" if ml > 0.65 else "mid"]
        if ms < 0.40 and ml > 0.60: tags.append("pastel")
        if ms > 0.55: tags.append("vivid")
        if spread < 40: tags.append("monochromatic")
        if spread > 120: tags.append("multihue")
        lk = likes(p.get("likes"))
        kept.append({"name": p.get("name") or f"Unnamed ({hexes[0].lower()}…)",
                     "hexes": hexes, "text_hint": [h["hex"].upper() for h in p["hexes"] if h.get("light")],
                     "likes": lk, "tier": 3 if lk >= 50000 else 2 if lk >= 20000 else 1 if lk > 0 else 0,
                     "computed_styles": sorted(set(tags)), "occurrences": len(grp),
                     "metrics": {"lightness_span": round(span, 3), "max_contrast": round(bestc, 2),
                                 "cb_min_separation": round(cb, 3)},
                     "flags": sorted(set(flags)), "sources": sorted({g[0] for g in grp}),
                     "origin": "harvest"})
    kept.sort(key=lambda x: (-x["tier"], -x["likes"], -x["occurrences"]))
    meta = {"_meta": {"schema": 2, "counts": {"kept": len(kept), "rejected": len(rej)},
                      "style_vocab": ["warm", "cool", "dark", "light", "mid", "pastel", "vivid",
                                      "monochromatic", "multihue", "deep"]},
            "palettes": kept}
    json.dump(meta, open(a.out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"kept {len(kept)} / rejected {len(rej)}")
    print("flags:", {f: sum(1 for k in kept if f in k["flags"]) for f in
                     ("CB-COLLISION-RISK", "SLOP-SIGNATURE", "NARROW-LIGHTNESS")})

if __name__ == "__main__":
    main()
