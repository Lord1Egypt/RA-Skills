#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
品牌资产SVG转PNG一站式渲染器，基于Edge headless + Pillow LANCZOS。

用法：
  python render_svg_to_png.py <项目根目录>          # 仅核心标志（标准PNG + 多尺寸 + ICO）
  python render_svg_to_png.py <项目根目录> --all   # 完整模式（核心 + 批量VI + 全部多尺寸 + ICO）
  python render_svg_to_png.py <项目根目录> --all --timeout 120

--all: 完整模式，渲染全部SVG
--timeout: 单个SVG渲染超时时间(秒)，默认90

环境要求：
  - Edge浏览器路径：C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe
    或通过环境变量 EDGE 指定，例如：set EDGE=C:\\Path\\To\\msedge.exe
  - Python虚拟环境：C:\\Users\\<用户>\\.workbuddy\\binaries\\python\\envs\\default\\Scripts\\python.exe
    （Windows下Python可执行文件位于Scripts子目录下）
"""
import os
import re
import struct
import subprocess
import tempfile
import argparse
from io import BytesIO
from PIL import Image

EDGE = os.environ.get("EDGE", r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe")

# 检查Edge路径
if not os.path.exists(EDGE):
    EDGE = None
    print("  警告：未找到Edge浏览器，SVG→PNG渲染将不可用")
    print("  可通过环境变量 EDGE 指定路径，例如：")
    print("  set EDGE=C:\\Path\\To\\msedge.exe")


# ============================================================
# 公共辅助函数
# ============================================================

def find_icon_dir(root):
    """在项目根目录查找 01_核心标志 目录。"""
    for d in os.listdir(root):
        full = os.path.join(root, d)
        if os.path.isdir(full) and "核心" in d:
            return full
    return None


def get_viewbox_size(svg_path):
    """从SVG文件提取viewBox宽高。"""
    with open(svg_path, "r", encoding="utf-8") as f:
        content = f.read()
    m = re.search(r'viewBox="([^"]*)"', content)
    if not m:
        return None, None
    parts = m.group(1).split()
    if len(parts) >= 4:
        try:
            return int(float(parts[2])), int(float(parts[3]))
        except (ValueError, IndexError):
            return None, None
    return None, None


def calc_timeout(view_w, view_h):
    """根据SVG尺寸自动计算渲染超时时间。"""
    if not view_w or not view_h:
        return 90
    area = view_w * view_h
    if area > 1_500_000:   # >1225x1225 大图（如信纸1588×2246≈3.57M）
        return 120
    if area > 500_000:     # >707x707 中图（如Banner 1920×600=1152000）
        return 90
    return 60


def wrap_svg_to_html(svg_content, target_w, target_h):
    """将SVG包装为可截图的HTML。"""
    svg = svg_content
    svg = re.sub(
        r'(<svg[^>]*?)\swidth="[^"]*"',
        r'\1 width="%d"' % target_w, svg, count=1
    )
    svg = re.sub(
        r'(<svg[^>]*?)\sheight="[^"]*"',
        r'\1 height="%d"' % target_h, svg, count=1
    )
    if "preserveAspectRatio" in svg:
        svg = re.sub(
            r'preserveAspectRatio="[^"]*"',
            'preserveAspectRatio="xMidYMid meet"', svg, count=1
        )
    else:
        svg = svg.replace(
            "<svg",
            '<svg preserveAspectRatio="xMidYMid meet"', 1
        )
    return (
        '<!DOCTYPE html><html><head><meta charset="UTF-8">'
        '<style>*{margin:0;padding:0;box-sizing:border-box}'
        'html,body{width:%dpx;height:%dpx;overflow:hidden}</style>'
        '</head><body>%s</body></html>' % (target_w, target_h, svg)
    )


def render_svg_to_png(svg_path, target_w, target_h, tmp_dir, timeout=90):
    """将SVG通过Edge headless渲染为指定尺寸PNG，返回PNG路径或None。"""
    if EDGE is None:
        print("  错误：Edge浏览器不可用，无法渲染 %s" % os.path.basename(svg_path))
        return None
    with open(svg_path, "r", encoding="utf-8") as f:
        svg_content = f.read()
    html = wrap_svg_to_html(svg_content, target_w, target_h)

    html_path = os.path.join(tmp_dir, "render.html")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html)
    url = "file:///" + html_path.replace("\\", "/")

    png_path = os.path.join(tmp_dir, "large.png")
    for mode in ["--headless=new", "--headless"]:
        cmd = [
            EDGE, mode, "--disable-gpu", "--no-sandbox",
            "--hide-scrollbars", "--screenshot=" + png_path,
            "--window-size=%d,%d" % (target_w, target_h),
            "--default-background-color=00000000", url
        ]
        try:
            subprocess.run(cmd, capture_output=True, timeout=timeout)
        except subprocess.TimeoutExpired:
            continue
        if os.path.exists(png_path) and os.path.getsize(png_path) > 0:
            return png_path
    return None


def resize_png(src_path, dst_path, target_w, target_h):
    """用Pillow LANCZOS高质量缩放PNG。"""
    img = Image.open(src_path).convert("RGBA")
    if img.size != (target_w, target_h):
        img = img.resize((target_w, target_h), Image.LANCZOS)
    img.save(dst_path, "PNG")
    return os.path.getsize(dst_path)


def build_ico(ico_path, png_sources):
    """手动构建多尺寸ICO文件（png_sources: [(size, png_path), ...]）。"""
    data_list = []
    for size, png_path in png_sources:
        if not os.path.exists(png_path):
            print("  警告：%s 不存在，跳过 %dpx" % (png_path, size))
            continue
        img = Image.open(png_path).convert("RGBA").resize((size, size), Image.LANCZOS)
        buf = BytesIO()
        img.save(buf, format="PNG")
        data_list.append((size, buf.getvalue()))

    if not data_list:
        print("  错误：未找到ICO所需的PNG源文件")
        return

    header = struct.pack("<HHH", 0, 1, len(data_list))
    offset = 6 + 16 * len(data_list)
    ico = bytearray(header)
    for size, data in data_list:
        w = size if size < 256 else 0
        entry = struct.pack("<BBBBHHII", w, w, 0, 0, 1, 32, len(data), offset)
        ico += entry
        offset += len(data)
    for _, data in data_list:
        ico += data
    with open(ico_path, "wb") as f:
        f.write(bytes(ico))
    print("  ICO: %dB（%d个尺寸）" % (len(ico), len(data_list)))


def extract_ico_pngs(ico_path, icon_dir):
    """从ICO二进制提取4个内嵌PNG（16×16/32×32/48×48/64×64）存入01_核心标志目录。

    ICO格式：
    - 6字节header: reserved(2) + type(2) + count(2)
    - count × 16字节entry: width(1)+height(1)+pal(1)+rsv(1)+planes(2)+bpp(2)+size(4)+offset(4)
    - 图像数据按entry顺序排列

    返回提取成功的文件名列表。
    """
    if not os.path.exists(ico_path):
        print("  警告：ICO文件 %s 不存在，跳过PNG提取" % ico_path)
        return []

    extracted = []
    try:
        with open(ico_path, "rb") as f:
            data = f.read()

        reserved, ico_type, count = struct.unpack_from("<HHH", data, 0)
        if reserved != 0 or ico_type != 1:
            print("  错误：ICO header 无效 (reserved=%d, type=%d)" % (reserved, ico_type))
            return []

        offset = 6
        entries = []
        for i in range(count):
            w, h, pal, rsv, planes, bpp, size, data_off = struct.unpack_from("<BBBBHHII", data, offset)
            actual_w = w if w != 0 else 256
            actual_h = h if h != 0 else 256
            entries.append((actual_w, actual_h, size, data_off))
            offset += 16

        for w, h, size, data_off in entries:
            img_data = data[data_off:data_off + size]
            if img_data[:4] == b'\x89PNG':
                # 内嵌的是PNG数据，直接提取
                dst_name = "favicon_%dx%d.png" % (w, h)
                dst_path = os.path.join(icon_dir, dst_name)
                with open(dst_path, "wb") as f:
                    f.write(img_data)
                extracted.append(dst_name)
                print("  提取: %s (%dx%d, %dB)" % (dst_name, w, h, len(img_data)))
            else:
                # 内嵌的是BMP数据，用PIL转PNG
                try:
                    img = Image.open(BytesIO(img_data))
                    img = img.convert("RGBA")
                    dst_name = "favicon_%dx%d.png" % (w, h)
                    dst_path = os.path.join(icon_dir, dst_name)
                    img.save(dst_path, "PNG")
                    extracted.append(dst_name)
                    print("  提取(BMP→PNG): %s (%dx%d, %dB)" % (dst_name, w, h, os.path.getsize(dst_path)))
                except Exception as e:
                    print("  提取失败: %dx%d BMP→PNG - %s" % (w, h, e))

    except Exception as e:
        print("  错误：ICO PNG提取失败 - %s" % e)

    return extracted


# ============================================================
# BA3-01: 核心标志标准PNG渲染
# ============================================================

def render_core_standard(root, timeout=90):
    """渲染01_核心标志目录中的3个SVG为标准PNG。"""
    icon_dir = find_icon_dir(root)
    if not icon_dir:
        print("  错误：找不到图标目录（01_核心标志）")
        return False

    tmp_dir = tempfile.gettempdir()
    rendered = 0

    # 定义3个标准SVG及其渲染尺寸
    # 注意：03_纯图标.png 由 render_icon_sizes() 负责渲染（更精细的多尺寸管线），此处不重复
    standards = [
        ("01_横版标志", 600, 240),
        ("02_竖版标志", 400, 480),
    ]

    for fname, target_w, target_h in standards:
        svg_path = None
        for f in os.listdir(icon_dir):
            if f.endswith(".svg") and f.startswith(fname) and "小尺寸" not in f:
                svg_path = os.path.join(icon_dir, f)
                break
        if not svg_path:
            print("  警告：未找到 %s SVG，跳过" % fname)
            continue

        png_path = os.path.join(icon_dir, fname + ".png")
        if os.path.exists(png_path) and os.path.getsize(png_path) > 0:
            print("  跳过（已存在）: %s.png" % fname)
            rendered += 1
            continue

        # 从SVG提取viewBox做auto timeout
        vb_w, vb_h = get_viewbox_size(svg_path)
        t = max(timeout, calc_timeout(vb_w, vb_h))

        large_png = render_svg_to_png(svg_path, target_w, target_h, tmp_dir, timeout=t)
        if large_png:
            sz_bytes = resize_png(large_png, png_path, target_w, target_h)
            print("  OK: %s.png (%dx%d, %dB)" % (fname, target_w, target_h, sz_bytes))
            rendered += 1
        else:
            print("  失败: %s.svg → %s.png" % (fname, fname))

    print("  核心标准渲染完成: %d/%d" % (rendered, len(standards)))
    return rendered == len(standards)


# ============================================================
# BA3-02A: 横版/竖版多尺寸生成
# ============================================================

def render_horizontal_multi(root):
    """横版标志多尺寸生成（从标准PNG 600×240）。"""
    icon_dir = find_icon_dir(root)
    if not icon_dir:
        print("  警告：找不到图标目录，跳过横版多尺寸")
        return

    std_path = os.path.join(icon_dir, "01_横版标志.png")
    if not os.path.exists(std_path):
        print("  警告：01_横版标志.png 不存在，跳过横版多尺寸")
        return

    print("  横版标准: %s" % std_path)
    for suffix, ratio in [
        ("_1200", 2.0), ("_300", 0.5),
        ("_150", 0.25), ("_75", 0.125),
    ]:
        img = Image.open(std_path).convert("RGBA")
        w, h = round(img.width * ratio), round(img.height * ratio)
        out = os.path.join(icon_dir, "01_横版标志%s.png" % suffix)
        img.resize((w, h), Image.LANCZOS).save(out, "PNG")
        print("    -> %s (%dx%d, %dB)" % (
            os.path.basename(out), w, h, os.path.getsize(out)))


def render_vertical_multi(root):
    """竖版标志多尺寸生成（从标准PNG 400×480）。"""
    icon_dir = find_icon_dir(root)
    if not icon_dir:
        print("  警告：找不到图标目录，跳过竖版多尺寸")
        return

    std_path = os.path.join(icon_dir, "02_竖版标志.png")
    if not os.path.exists(std_path):
        print("  警告：02_竖版标志.png 不存在，跳过竖版多尺寸")
        return

    print("  竖版标准: %s" % std_path)
    for suffix, ratio in [
        ("_960", 2.0), ("_240", 0.5),
        ("_120", 0.25), ("_60", 0.125),
    ]:
        img = Image.open(std_path).convert("RGBA")
        w, h = round(img.width * ratio), round(img.height * ratio)
        out = os.path.join(icon_dir, "02_竖版标志%s.png" % suffix)
        img.resize((w, h), Image.LANCZOS).save(out, "PNG")
        print("    -> %s (%dx%d, %dB)" % (
            os.path.basename(out), w, h, os.path.getsize(out)))


# ============================================================
# BA3-03: 纯图标多尺寸渲染
# ============================================================

def render_icon_sizes(root, small_svg_path=None, timeout=90):
    """渲染纯图标多尺寸（16/32/64/128/256/512）+ 480标准PNG。"""
    icon_dir = find_icon_dir(root)
    if not icon_dir:
        print("  错误：找不到图标目录（01_核心标志）")
        return

    tmp_dir = tempfile.gettempdir()

    # 找SVG源文件
    full_svg = None
    small_svg = small_svg_path
    for f in os.listdir(icon_dir):
        if not f.endswith(".svg"):
            continue
        fp = os.path.join(icon_dir, f)
        if "小尺寸" in f:
            small_svg = fp
        elif "纯图标" in f and "小尺寸" not in f:
            full_svg = fp

    if not full_svg:
        print("  错误：找不到主图标SVG文件")
        return

    print("图标目录: %s" % icon_dir)
    print("完整版SVG: %s" % os.path.basename(full_svg))
    print("简化版SVG: %s" % os.path.basename(small_svg or full_svg))

    # 1. 小尺寸（16/32/64/128）使用简化版SVG
    small_source = small_svg if small_svg else full_svg
    vb_w, vb_h = get_viewbox_size(small_source)
    t = max(timeout, calc_timeout(vb_w, vb_h))
    print("\n[小尺寸 16/32/64/128] 来源: %s (timeout=%ds)" % (os.path.basename(small_source), t))

    large_png = render_svg_to_png(small_source, 1024, 1024, tmp_dir, timeout=t)
    if large_png:
        print("  基础1024x1024: %dB" % os.path.getsize(large_png))
        for sz in [16, 32, 64, 128]:
            dst = os.path.join(icon_dir, "03_纯图标_%d.png" % sz)
            if os.path.exists(dst) and os.path.getsize(dst) > 0:
                print("    -> %dx%d: 已存在，跳过" % (sz, sz))
                continue
            sz_bytes = resize_png(large_png, dst, sz, sz)
            print("  -> %dx%d: %dB" % (sz, sz, sz_bytes))

    # 2. 大尺寸（256/512/480）使用完整版SVG
    vb_w2, vb_h2 = get_viewbox_size(full_svg)
    t2 = max(timeout, calc_timeout(vb_w2, vb_h2))
    print("\n[大尺寸 256/512/480] 来源: %s (timeout=%ds)" % (os.path.basename(full_svg), t2))

    large_png = render_svg_to_png(full_svg, 1024, 1024, tmp_dir, timeout=t2)
    if large_png:
        for sz in [256, 512]:
            dst = os.path.join(icon_dir, "03_纯图标_%d.png" % sz)
            if os.path.exists(dst) and os.path.getsize(dst) > 0:
                print("  -> %dx%d: 已存在，跳过" % (sz, sz))
                continue
            sz_bytes = resize_png(large_png, dst, sz, sz)
            print("  -> %dx%d: %dB" % (sz, sz, sz_bytes))
        dst = os.path.join(icon_dir, "03_纯图标.png")
        if os.path.exists(dst) and os.path.getsize(dst) > 0:
            print("  -> 480x480: 已存在，跳过")
        else:
            sz_bytes = resize_png(large_png, dst, 480, 480)
            print("  -> 480x480: %dB" % sz_bytes)


# ============================================================
# BA3-04: 构建favicon.ico
# ============================================================

def build_favicon(root):
    """构建favicon.ico（多尺寸嵌入）。"""
    icon_dir = find_icon_dir(root)
    if not icon_dir:
        return

    ico_path = os.path.join(icon_dir, "favicon.ico")
    # 48px ICO条目从64px PNG源缩小（ICO格式中48px是标准尺寸之一）
    # build_ico()内部会统一resize到目标尺寸，这里只需保证源PNG≥目标尺寸即可
    src_map = {16: 16, 32: 32, 48: 64, 64: 64}
    png_sources = []
    for s in [16, 32, 48, 64]:
        src_sz = src_map[s]
        src_png = os.path.join(icon_dir, "03_纯图标_%d.png" % src_sz)
        if os.path.exists(src_png):
            png_sources.append((s, src_png))
    build_ico(ico_path, png_sources)


# ============================================================
# BA3-02B: 批量SVG渲染
# ============================================================

def render_batch_svg(root, timeout=90):
    """批量SVG渲染（02_商标注册~09_多媒体模板）。

    遍历所有子目录，逐一渲染SVG→PNG。
    跳过01_核心标志（已由render_core_standard处理）。
    自动跳过已存在且非空的PNG（增量渲染）。
    """
    if EDGE is None:
        print("  错误：Edge浏览器不可用，批量VI渲染跳过")
        return 0

    tmp_dir = tempfile.gettempdir()
    subdirs = [
        "02_商标注册", "03_数字化应用",
        "04_办公文具", "05_宣传物料",
        "06_品牌规范", "07_环境应用",
        "08_产品周边", "09_多媒体模板"
    ]
    rendered = 0
    failed = 0
    skipped = 0

    for subdir in subdirs:
        dirpath = os.path.join(root, subdir)
        if not os.path.isdir(dirpath):
            continue

        for f in sorted(os.listdir(dirpath)):
            if not f.endswith(".svg"):
                continue
            svg_path = os.path.join(dirpath, f)
            fname = f[:-4]
            out_png = os.path.join(dirpath, fname + ".png")
            if os.path.exists(out_png) and os.path.getsize(out_png) > 0:
                skipped += 1
                continue

            w, h = get_viewbox_size(svg_path)
            if not w or not h:
                print("    SKIP (无viewBox): %s" % f)
                continue

            # 限制渲染尺寸上限（当前所有SVG的viewBox ≤ 2400，A0海报约2480×3508）
            # 上限4000px覆盖A0海报等超大尺寸场景，同时避免渲染过慢
            MAX_RENDER = 4000
            render_w = min(w, MAX_RENDER)
            render_h = min(h, MAX_RENDER)
            t = max(timeout, calc_timeout(w, h))

            with open(svg_path, "r", encoding="utf-8") as sf:
                svg = sf.read()
            html = wrap_svg_to_html(svg, render_w, render_h)

            html_path = os.path.join(tmp_dir, "b.html")
            with open(html_path, "w", encoding="utf-8") as hf:
                hf.write(html)

            ok = False
            for mode in ["--headless=new", "--headless"]:
                try:
                    cmd = [
                        EDGE, mode, "--disable-gpu", "--no-sandbox",
                        "--hide-scrollbars", "--screenshot=" + out_png,
                        "--window-size=%d,%d" % (render_w, render_h),
                        "--default-background-color=00000000",
                        "file:///" + html_path.replace("\\", "/")
                    ]
                    subprocess.run(cmd, capture_output=True, timeout=t)
                    if os.path.exists(out_png) and os.path.getsize(out_png) > 0:
                        print("    OK: %s (%dx%d, %dB)" % (
                            fname, render_w, render_h, os.path.getsize(out_png)))
                        rendered += 1
                        ok = True
                        break
                except subprocess.TimeoutExpired:
                    continue
            if not ok:
                print("    失败: %s (%d×%d, timeout=%ds)" % (f, render_w, render_h, t))
                failed += 1

    print("\n  批量SVG渲染完成: %d 成功, %d 失败, %d 跳过" % (rendered, failed, skipped))
    return rendered


# ============================================================
# 入口
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        description="品牌资产SVG转PNG一站式渲染器"
    )
    parser.add_argument("project_root", help="项目根目录（包含SVG文件的目录）")
    parser.add_argument("--small-svg", help="小图标（16-128px）使用的简化版SVG路径")
    parser.add_argument("--all", action="store_true",
                        help="完整模式：核心标准PNG + 多尺寸 + 批量VI + ICO + ICO内嵌PNG提取")
    parser.add_argument("--timeout", type=int, default=90,
                        help="单个SVG渲染超时时间(秒)，默认90，大图自动延长")
    args = parser.parse_args()

    root = os.path.abspath(args.project_root)
    print("=== 品牌资产渲染器 ===")
    print("项目目录: %s" % root)
    print("默认超时: %ds（大图自动延长）" % args.timeout)
    print()

    if args.all:
        print("--- 完整模式：核心标志 + 批量SVG ---")
        print()

        # [1] 核心标志标准PNG渲染（必须先做，多尺寸依赖它）
        print("[1] 核心标志标准PNG...")
        render_core_standard(root, timeout=args.timeout)

        # [2] 横版/竖版多尺寸（依赖标准PNG）
        print("\n[2] 横版标志多尺寸...")
        render_horizontal_multi(root)

        print("\n[3] 竖版标志多尺寸...")
        render_vertical_multi(root)

        # [4] 纯图标多尺寸
        print("\n[4] 纯图标多尺寸...")
        render_icon_sizes(root, args.small_svg, timeout=args.timeout)

        # [5] favicon.ico
        print("\n[5] favicon.ico...")
        build_favicon(root)

        # [5B] 从ICO提取内嵌PNG（HTML展示页需要）
        print("\n[5B] 从ICO提取内嵌PNG...")
        icon_dir = find_icon_dir(root)
        if icon_dir:
            ico_path = os.path.join(icon_dir, "favicon.ico")
            if os.path.exists(ico_path):
                extract_ico_pngs(ico_path, icon_dir)

        # [6] 批量SVG渲染（02~09）
        # 注意：06~09目录（品牌规范+扩展应用）在首次运行--all时可能不存在
        # （BA5/BA6的SVG在核心管线之后才生成）。目录不存在时自动跳过，
        # 后续生成SVG后再次运行--all会增量渲染。
        print("\n[6] 批量SVG渲染...")
        render_batch_svg(root, timeout=args.timeout)

        print("\n=== 全部完成 ===")
        return

    # 非 --all 模式：仅渲染核心标志
    print("--- 仅核心标志模式 ---")
    print("提示：使用 --all 可同时渲染批量VI系统")
    print()

    render_core_standard(root, timeout=args.timeout)
    render_horizontal_multi(root)
    render_vertical_multi(root)
    render_icon_sizes(root, args.small_svg, timeout=args.timeout)
    build_favicon(root)

    # 从ICO提取内嵌PNG（HTML展示页需要）
    icon_dir = find_icon_dir(root)
    if icon_dir:
        ico_path = os.path.join(icon_dir, "favicon.ico")
        if os.path.exists(ico_path):
            extract_ico_pngs(ico_path, icon_dir)

    print("\n=== 核心标志完成 ===")


if __name__ == "__main__":
    main()