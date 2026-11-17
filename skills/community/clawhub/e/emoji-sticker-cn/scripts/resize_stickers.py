#!/usr/bin/env python3
"""批量将表情原图裁切/缩放为指定平台尺寸并规范命名、可选打包 ZIP。

依赖: Pillow  (缺失时: pip install Pillow)
设计: 本脚本只做机械的「缩放 + 居中贴合 + 顺序命名 + 打包」,
      平台尺寸规范以 emoji-sticker-cn/references/中文平台表情包尺寸规范.md 为准(单一事实源)。

用法:
  # 单尺寸批量处理:主图 240x240 透明底,命名 01.png…24.png
  python3 resize_stickers.py ./raw --size 240x240 --bg transparent --format png --out ./wechat --zip

  # 微信四件套一次生成(主图/图标/封面/横幅,自动建目录)
  # (赞赏引导图/致谢图需自行制作:官方要求风格须与表情一致,机械派生不合格)
  python3 resize_stickers.py ./raw --wechat --out ./wechat_pack --zip

  # 自定义前缀 + 非透明底(横幅场景)
  python3 resize_stickers.py ./raw --size 750x400 --bg white --format png --prefix banner --out ./out
"""
import argparse
import os
import sys
import zipfile

try:
    from PIL import Image, ImageSequence
    from PIL.Image import Resampling
except ImportError:
    sys.stderr.write("缺少依赖 Pillow,请先运行: pip install Pillow\n")
    sys.exit(2)

# 兼容新旧 Pillow(新版推荐 Resampling.LANCZOS,旧版常量已弃用)
LANCZOS = Resampling.LANCZOS
BICUBIC = Resampling.BICUBIC

# 微信表情开放平台「可自动派生」的四类素材(单一事实源: references/中文平台表情包尺寸规范.md)
# 说明: 官方素材总表只有 4 项(表情图/横幅/封面/图标)+ 赞赏 2 图。
#       「缩略图」无官方出处(全文仅赞赏开通条件里出现名词「赞赏缩略图」,无规格),v3.1.9 已删除。
#       赞赏引导图/致谢图官方要求「风格须与表情一致」,机械派生不合格,故不在此生成。
WECHAT_ASSETS = [
    ("主图", "240x240", "png", "transparent"),
    ("聊天面板图标", "50x50", "png", "transparent"),
    ("封面图", "240x240", "png", "transparent"),
    ("详情页横幅", "750x400", "png", "#F2F3F5"),  # 禁纯白底,给浅灰底
]

INPUT_EXTS = (".png", ".jpg", ".jpeg", ".webp", ".gif", ".bmp")


def parse_size(s: str):
    w, h = s.lower().split("x")
    w, h = int(w), int(h)
    if w <= 0 or h <= 0:
        raise ValueError(f"非法尺寸: {s}")
    return w, h


def hex_bg(hex_color: str):
    """#RRGGBB / #RRGGBBAA → RGBA 元组。"""
    v = hex_color.lstrip("#")
    if len(v) == 6:
        return tuple(int(v[i:i + 2], 16) for i in (0, 2, 4)) + (255,)
    if len(v) == 8:
        return tuple(int(v[i:i + 2], 16) for i in (0, 2, 4, 6))
    raise ValueError(f"非法颜色: {hex_color}")


def make_bg(w, h, bg):
    """生成画布:transparent → RGBA 全透明;white/black 或 #hex → 不透明纯色。"""
    if bg == "transparent":
        return Image.new("RGBA", (w, h), (0, 0, 0, 0))
    if bg == "white":
        return Image.new("RGBA", (w, h), (255, 255, 255, 255))
    if bg == "black":
        return Image.new("RGBA", (w, h), (0, 0, 0, 255))
    if bg.startswith("#"):
        return Image.new("RGBA", (w, h), hex_bg(bg))
    raise ValueError(f"未知背景: {bg}")


def fit_frame(frame, size, bg, fit):
    """单帧缩放 + 居中贴合 + 铺底色。始终在 RGBA 空间合成,避免透明区变黑。"""
    w, h = size
    img = frame.convert("RGBA")
    if fit == "cover":
        # 裁切填满:先等比放大到铺满,再居中裁到目标框
        scale = max(w / max(img.width, 1), h / max(img.height, 1))
        nw, nh = max(1, round(img.width * scale)), max(1, round(img.height * scale))
        img = img.resize((nw, nh), LANCZOS)
        left = (nw - w) // 2
        top = (nh - h) // 2
        img = img.crop((left, top, left + w, top + h))
        return img
    # contain:等比缩到目标框内,居中留边(默认)
    img.thumbnail((w, h), LANCZOS)
    canvas = make_bg(w, h, bg)
    off_x = (w - img.width) // 2
    off_y = (h - img.height) // 2
    canvas.paste(img, (off_x, off_y), img)
    return canvas


def process_one(src_path, size, bg, fmt, out_path, fit="contain"):
    """处理单张静态图。返回 (输出路径, 字节数)。"""
    src = Image.open(src_path)
    frame = src.convert("RGBA")
    canvas = fit_frame(frame, size, bg, fit)
    save_frame(canvas, out_path, fmt, bg)
    return out_path, os.path.getsize(out_path)


def process_gif(src_path, size, bg, fmt, out_path, fit="contain"):
    """GIF 动画:逐帧处理并保留动画(仅输出 gif 时有效)。"""
    src = Image.open(src_path)
    frames = [fit_frame(f.convert("RGBA"), size, bg, fit) for f in ImageSequence.Iterator(src)]
    duration = src.info.get("duration", 80) or 80
    ps = [rgba_to_p(f) for f in frames]
    ps[0].save(
        out_path, format="GIF", save_all=True, append_images=ps[1:],
        duration=duration, loop=0, transparency=255, disposal=2,
    )
    return out_path, os.path.getsize(out_path)


def rgba_to_p(frame):
    """RGBA → 带透明索引的 P 模式(GIF 1-bit 透明经典配方)。"""
    alpha = frame.getchannel("A")
    p = frame.convert("RGB").quantize(colors=255, method=2)
    mask = alpha.point(lambda a: 255 if a < 128 else 0)
    p.paste(255, mask)
    p.info["transparency"] = 255
    return p


def save_frame(canvas, out_path, fmt, bg):
    """落盘单帧,针对格式做必要转换:jpg 去透明;gif 转 P 模式保透明。"""
    if fmt == "jpg":
        canvas.convert("RGB").save(out_path, "JPEG", quality=92)
    elif fmt == "gif":
        rgba_to_p(canvas).save(out_path, "GIF", transparency=255, disposal=2)
    elif fmt == "webp":
        canvas.save(out_path, "WEBP", quality=90, lossless=(bg == "transparent"))
    else:  # png
        canvas.save(out_path, "PNG", optimize=True)


def collect_inputs(path):
    if os.path.isdir(path):
        return sorted(
            os.path.join(path, f)
            for f in os.listdir(path)
            if f.lower().endswith(INPUT_EXTS)
        )
    return [path]


def main():
    ap = argparse.ArgumentParser(description="表情包批量裁切/缩放/命名/打包")
    ap.add_argument("input", help="原图文件或目录")
    ap.add_argument("--size", help="目标尺寸,如 240x240(--wechat 时忽略)")
    ap.add_argument("--bg", default="transparent",
                    help="背景: transparent / white / black / #RRGGBB,默认 transparent")
    ap.add_argument("--format", dest="fmt", choices=["png", "jpg", "gif", "webp"], default="png")
    ap.add_argument("--prefix", default="", help="输出文件名前缀(默认空,直接 01.png…24.png,对齐微信规范)")
    ap.add_argument("--start", type=int, default=1, help="起始序号,默认 1")
    ap.add_argument("--pad", type=int, default=2, help="序号位宽,默认 2(01,02…)")
    ap.add_argument("--fit", choices=["contain", "cover"], default="contain",
                    help="contain=等比缩放留边(默认);cover=裁切填满")
    ap.add_argument("--wechat", action="store_true", help="微信四件套预设(主图/图标/封面/横幅)")
    ap.add_argument("--banner-bg", default="#F2F3F5", help="微信横幅底色(禁纯白),默认浅灰 #F2F3F5")
    ap.add_argument("--out", default="./out", help="输出目录")
    ap.add_argument("--zip", action="store_true", help="额外打包成 ZIP")
    ap.add_argument("--max-kb", type=int, default=0, help="单文件体积上限 KB,超限警告并返回退出码 3")
    args = ap.parse_args()

    if args.wechat and args.size:
        sys.stderr.write("--wechat 与 --size 互斥,请二选一\n")
        sys.exit(2)
    if not args.wechat and not args.size:
        sys.stderr.write("必须提供 --size 或 --wechat\n")
        sys.exit(2)

    # 微信四件套计划(横幅底色可用 --banner-bg 覆盖,默认浅灰而非纯白)
    wechat_assets = [
        (n, s, f, args.banner_bg if n == "详情页横幅" else b)
        for n, s, f, b in WECHAT_ASSETS
    ]

    size = None if args.wechat else parse_size(args.size)
    os.makedirs(args.out, exist_ok=True)
    files = collect_inputs(args.input)
    if not files:
        sys.stderr.write("未找到输入图片\n")
        sys.exit(1)

    over_limit = []
    total = 0
    zip_list = []

    def run_batch(out_dir, size_, bg_, fmt_, prefix_):
        nonlocal total
        os.makedirs(out_dir, exist_ok=True)
        paths = []
        for i, fp in enumerate(files, args.start):
            out_name = f"{prefix_}{i:0{args.pad}d}.{fmt_}"
            out_path = os.path.join(out_dir, out_name)
            is_gif = fp.lower().endswith(".gif") and fmt_ == "gif"
            (process_gif if is_gif else process_one)(fp, size_, bg_, fmt_, out_path, args.fit)
            kb = os.path.getsize(out_path) / 1024
            flag = ""
            if args.max_kb and kb > args.max_kb:
                over_limit.append((out_name, kb, args.max_kb))
                flag = " ⚠ 超限"
            print(f"[{i:0{args.pad}d}] {os.path.basename(fp)} -> {os.path.relpath(out_path)} {kb:.1f}KB{flag}")
            paths.append(out_path)
            total += 1
        return paths

    if args.wechat:
        for name, size_, fmt_, bg_ in wechat_assets:
            out_dir = os.path.join(args.out, name)
            print(f"── {name} ({size_}, {bg_})")
            paths = run_batch(out_dir, parse_size(size_), bg_, fmt_, args.prefix)
            if args.zip:
                zf = os.path.join(out_dir, f"{name}.zip")
                with zipfile.ZipFile(zf, "w", zipfile.ZIP_DEFLATED) as z:
                    for p in paths:
                        z.write(p, os.path.basename(p))
                zip_list.append(zf)
                print(f"已打包: {zf}")
    else:
        paths = run_batch(args.out, size, args.bg, args.fmt, args.prefix)
        if args.zip:
            zip_name = os.path.join(args.out, f"{args.prefix or 'stickers'}_{args.size}.zip")
            with zipfile.ZipFile(zip_name, "w", zipfile.ZIP_DEFLATED) as z:
                for p in paths:
                    z.write(p, os.path.basename(p))
            zip_list.append(zip_name)
            print(f"已打包: {zip_name}")

    if over_limit:
        sys.stderr.write("\n体积超限(超过上限将面临驳回):\n")
        for name, kb, limit in over_limit:
            sys.stderr.write(f"  {name}: {kb:.1f}KB > {limit}KB\n")
        sys.stderr.write("建议: 缩小主体占比 / 降低 --format 质量 / 使用 animate_sticker.py 的降色抽帧\n")
    print(f"\n完成,共 {total} 张,输出目录: {args.out}")
    sys.exit(3 if over_limit else 0)


if __name__ == "__main__":
    main()
