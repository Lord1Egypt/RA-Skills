#!/usr/bin/env python3
"""微信表情素材机检 —— 上架前自检,拦截高频拒因。

对照官方规范(references/中文平台表情包尺寸规范.md)逐项判定,分三级:
  FAIL  必须修(不修必被驳回/无法上传)
  WARN  人工确认(可能被驳回,视素材类型)
  OK    合规
退出码 = FAIL 条数(0 = 可提交)。

检查项:
  1. 尺寸 / 格式 / 体积 / 张数(主图 8-24,单品 1)
  2. 透明底: 封面/图标必须透明(FAIL);横幅/赞赏图官方用「避免」非禁止
     → 仅 WARN(2026-10-26 对齐官方原文: 避免使用透明背景);
     主图不强制透明(照片型合法,插画型建议透明 → 仅 WARN)
  3. 白描边: 轮廓明显比主体内部更白 → WARN(官方:形象不应有白色描边)
  4. 整套差异: 主图两两差分哈希(dhash)汉明距离过小 → FAIL(官方明文第一大拒因)
  5. 动静统一: 主图混有 GIF/PNG → FAIL(官方:同一套须统一动/静)
  6. 含义词(--meanings): ≤4 汉字 / 无标点 / 同套不重复 / 条数与主图对应

用法:
  python3 check_assets.py ./wechat_pack                     # 只机检素材
  python3 check_assets.py ./wechat_pack --meanings meanings.txt
  python3 check_assets.py ./wechat_pack --json               # 机器可读输出

目录结构需与 resize_stickers.py --wechat 输出一致:
  主图/ 聊天面板图标/ 封面图/ 详情页横幅/ 赞赏引导图/ 赞赏致谢图/
"""
import argparse
import glob
import json
import os
import sys

try:
    from PIL import Image, ImageFilter
except ImportError:
    sys.stderr.write("缺少依赖 Pillow,请先运行: pip install Pillow\n")
    sys.exit(2)

# ---- 官方规格(references 尺寸规范) ----
# alpha: "must"=官方明文须透明→FAIL; "prefer"=未强制但插画型建议→WARN;
#        "no"=官方明文「避免」透明→WARN(不是禁止,2026-10-26 按官方原文降级)
SPEC = {
    "主图":      {"size": (240, 240), "max_kb": 500, "fmt": ("PNG", "JPEG", "GIF"), "alpha": "prefer", "count": (1, 24)},
    "聊天面板图标": {"size": (50, 50),   "max_kb": 100, "fmt": ("PNG",),             "alpha": "must"},
    "封面图":    {"size": (240, 240), "max_kb": 500, "fmt": ("PNG",),             "alpha": "must"},
    "详情页横幅":  {"size": (750, 400), "max_kb": 500, "fmt": ("PNG", "JPEG"),        "alpha": "no"},
    # 「缩略图」已于 v3.1.9 删除: 官方素材总表(4 项)不含此项,官方全文仅在赞赏开通
    # 条件里出现名词「赞赏缩略图」且无任何规格 → 无出处,不再产出/不再校验。
    "赞赏引导图":  {"size": (750, 560), "max_kb": 500, "fmt": ("PNG", "GIF"),         "alpha": "no"},
    "赞赏致谢图":  {"size": (750, 750), "max_kb": 500, "fmt": ("PNG", "GIF"),         "alpha": "no"},
}
PUNCT = set("，。！？、；：""''（）()【】《》<>…—·~!?,.:;'\"[]{}|-_=+/\\@$%^&*#`")


class Report:
    def __init__(self):
        self.rows = []

    def add(self, level, target, msg):
        self.rows.append({"level": level, "target": target, "msg": msg})

    def fail(self, t, m): self.add("FAIL", t, m)
    def warn(self, t, m): self.add("WARN", t, m)
    def ok(self, t, m): self.add("OK", t, m)

    @property
    def fails(self):
        return sum(1 for r in self.rows if r["level"] == "FAIL")


def load(path):
    im = Image.open(path)
    frames = getattr(im, "n_frames", 1)
    return im, im.format, frames


def alpha_stats(im):
    """返回 (有透明像素比例, 全不透明与否)。"""
    if im.mode != "RGBA":
        return 0.0
    a = im.getchannel("A").resize((64, 64))
    transparent = sum(1 for v in a.tobytes() if v < 250)
    return transparent / (64 * 64)


def white_fringe(im):
    """白描边检测: 轮廓带 vs 主体内部的近白比例差。只看封面/图标类小图,够用。"""
    if im.mode != "RGBA":
        return 0.0, 0.0
    im = im.convert("RGBA")
    mask = im.getchannel("A").point(lambda v: 255 if v > 16 else 0)
    inner = mask.filter(ImageFilter.MinFilter(7))  # 腐蚀 3px
    rgb = im.convert("L")
    rim_px, inner_px = [], []
    w, h = im.size
    step = max(1, min(w, h) // 64)  # 采样降开销
    for y in range(0, h, step):
        for x in range(0, w, step):
            if not mask.getpixel((x, y)):
                continue
            v = rgb.getpixel((x, y))
            (inner_px if inner.getpixel((x, y)) else rim_px).append(v)
    if not rim_px or not inner_px:
        return 0.0, 0.0
    frac = lambda vs: sum(1 for v in vs if v >= 235) / len(vs)
    return frac(rim_px), frac(inner_px)


def subject_box(im):
    """主体外接框: 优先 alpha,全不透明(照片型)按非白像素。"""
    if im.mode == "RGBA":
        box = im.getchannel("A").point(lambda v: 255 if v > 16 else 0).getbbox()
        if box and box != (0, 0, *im.size):
            return box
    return im.convert("L").point(lambda v: 255 if v < 235 else 0).getbbox() or (0, 0, *im.size)


def dhash(im):
    """差分哈希(64bit): 裁到主体再算,背景大片白/透明不会干扰。"""
    g = im.crop(subject_box(im)).convert("L").resize((9, 8))
    px = list(g.tobytes())
    bits = 0
    for y in range(8):
        for x in range(8):
            if px[y * 9 + x] > px[y * 9 + x + 1]:
                bits |= 1 << (y * 8 + x)
    return bits


def hamming(a, b):
    return bin(a ^ b).count("1")


def find_dir(root, name):
    for cand in (name, name.replace("图", ""), name.replace("面板", "")):
        p = os.path.join(root, cand)
        if os.path.isdir(p):
            return p
    return None


def check_kind(root, kind, rep, dhashes):
    spec = SPEC[kind]
    d = find_dir(root, kind)
    if not d:
        if kind in ("主图",):
            rep.fail(kind, "缺少目录")
        else:
            rep.warn(kind, "缺少目录(赞赏图非必填,封面/图标/横幅必填)")
        return []

    files = sorted(
        f for f in os.listdir(d)
        if f.lower().endswith((".png", ".jpg", ".jpeg", ".gif")) and not f.startswith(".")
    )
    if not files:
        rep.fail(kind, "目录为空")
        return []

    # 张数
    if "count" in spec:
        lo, hi = spec["count"]
        n = len(files)
        if n == 1:
            rep.ok(kind, "单品模式(1 张)")
        elif lo <= n <= hi:
            rep.ok(kind, f"张数 {n}(8-24 合规)")
        else:
            rep.fail(kind, f"张数 {n} 不在 8-24 范围(单品请只放 1 张)")

    sizes = set()
    fails_before = rep.fails   # v3.1.9: 本类逐图检查前的 FAIL 数,用于防止「既 FAIL 又 OK」
    for f in files:
        path = os.path.join(d, f)
        try:
            im, fmt, frames = load(path)
        except Exception as e:
            rep.fail(f"{kind}/{f}", f"无法读取: {e}")
            continue

        # 尺寸
        ok_sizes = [spec["size"]] + ([spec["alt_size"]] if spec.get("alt_size") else [])
        if (im.width, im.height) not in ok_sizes:
            rep.fail(f"{kind}/{f}", f"尺寸 {im.width}x{im.height},应为 {' 或 '.join(f'{w}x{h}' for w, h in ok_sizes)}")
        else:
            sizes.add((im.width, im.height))

        # 格式
        if fmt not in spec["fmt"]:
            rep.fail(f"{kind}/{f}", f"格式 {fmt},应为 {'/'.join(spec['fmt'])}")

        # 体积
        kb = os.path.getsize(path) / 1024
        if kb > spec["max_kb"]:
            rep.fail(f"{kind}/{f}", f"体积 {kb:.0f}KB > {spec['max_kb']}KB")

        # 透明底
        alpha_spec = spec["alpha"]
        if frames == 1:
            t = alpha_stats(im)
            if alpha_spec == "must" and t < 0.05:
                rep.fail(f"{kind}/{f}", "不透明(官方明文须透明背景)")
            elif alpha_spec == "no" and t > 0.05:
                rep.warn(f"{kind}/{f}", "透明背景(官方用「避免」非禁止;确认底色与微信底可区分)")
            elif alpha_spec == "prefer" and t < 0.05:
                rep.warn(f"{kind}/{f}", "不透明(照片型合法;插画型建议透明)")

        # 白描边(只查强制透明的类别)
        if alpha_spec == "must" and frames == 1:
            rim, inner = white_fringe(im)
            if rim - inner > 0.4:
                rep.warn(f"{kind}/{f}", f"疑似白描边(轮廓白度 {rim:.0%} vs 内部 {inner:.0%})")

        # dhash(只查主图)
        if kind == "主图":
            dhashes.append((f, dhash(im)))

        # 动静统一
        if kind == "主图":
            kinds = {os.path.splitext(f)[1].lower() for f in files}
            if ".gif" in kinds and len(kinds) > 1:
                rep.fail(kind, "混有 GIF 与静态图(官方:同一套须统一动态或静态)")

    # v3.1.9: 只有本类零 FAIL 才打 OK——旧版只看 sizes 是否唯一,
    # 导致「格式错但尺寸对」的图同时出现 [✗ FAIL] 和 [✓ OK],会误导 agent 放过问题。
    if len(sizes) == 1 and rep.fails == fails_before:
        rep.ok(kind, f"{len(files)} 张,尺寸/体积/格式合规")
    return files


def check_meanings(rep, mpath, main_files):
    try:
        words = [w.strip() for w in open(mpath, encoding="utf-8") if w.strip()]
    except OSError as e:
        rep.fail("含义词", f"无法读取 {mpath}: {e}")
        return

    if main_files is not None and len(words) != len(main_files):
        rep.fail("含义词", f"条数 {len(words)} ≠ 主图 {len(main_files)} 张(须一一对应)")

    seen = {}
    for i, w in enumerate(words, 1):
        han = sum(1 for ch in w if "\u4e00" <= ch <= "\u9fff")
        other = len(w) - han
        if len(w) > 4 or other > 2:
            rep.fail(f"含义词#{i}", f"「{w}」超 4 汉字(官方:≤4 汉字)")
        if any(ch in PUNCT for ch in w):
            rep.warn(f"含义词#{i}", f"「{w}」含标点(官方:尽量避免)")
        if w in seen:
            rep.fail(f"含义词#{i}", f"「{w}」与 #{seen[w]} 重复(官方:同套避免重复)")
        seen[w] = i
    if words and all(len(w) <= 4 for w in words) and len(set(words)) == len(words):
        rep.ok("含义词", f"{len(words)} 条合规")


def main():
    ap = argparse.ArgumentParser(description="微信表情素材机检(上架前自检)")
    ap.add_argument("dir", help="素材根目录(resize_stickers.py --wechat 的输出目录)")
    ap.add_argument("--meanings", help="含义词文件路径(每行一条,与主图一一对应)", default=None)
    ap.add_argument("--json", action="store_true", help="输出 JSON(机器可读)")
    args = ap.parse_args()

    if not os.path.isdir(args.dir):
        sys.stderr.write(f"目录不存在: {args.dir}\n")
        sys.exit(2)

    rep = Report()
    dhashes = []
    main_files = None
    for kind in SPEC:
        files = check_kind(args.dir, kind, rep, dhashes)
        if kind == "主图":
            main_files = files

    # 整套差异(第一大拒因)
    if len(dhashes) >= 2:
        dup = []
        for i in range(len(dhashes)):
            for j in range(i + 1, len(dhashes)):
                d = hamming(dhashes[i][1], dhashes[j][1])
                if d <= 6:
                    dup.append((dhashes[i][0], dhashes[j][0], d))
        for a, b, d in dup:
            rep.fail("整套差异", f"{a} 与 {b} 过于相似(汉明距离 {d};官方:整套差异不足为明文不通过)")
        if not dup:
            rep.ok("整套差异", f"{len(dhashes)} 张两两差异充分")

    if args.meanings:
        check_meanings(rep, args.meanings, main_files)

    if args.json:
        print(json.dumps(rep.rows, ensure_ascii=False, indent=2))
    else:
        for r in rep.rows:
            mark = {"FAIL": "✗ FAIL", "WARN": "△ WARN", "OK": "✓ OK"}[r["level"]]
            print(f"[{mark}] {r['target']}: {r['msg']}")
        n_fail = rep.fails
        print(f"\nFAIL {n_fail} / WARN {sum(1 for r in rep.rows if r['level']=='WARN')} / OK {sum(1 for r in rep.rows if r['level']=='OK')}")
        if n_fail:
            print("FAIL 必须清零后再提交;WARN 请人工确认(照片型主图不透明属正常)。")
    sys.exit(rep.fails or 0)


if __name__ == "__main__":
    main()
