#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
品牌资产完整性校验器。

检查项：
  1. 每个实际文件都在HTML中被引用（无孤儿）
  2. 每个HTML引用都指向真实存在的文件（无悬空链接）
  3. PNG尺寸标注与实际像素一致（可选）
  4. 总文件数与预期一致（核心62个，全量87个）

用法：
  python verify_assets.py <项目根目录> [--html <文件名.html>] [--full]

退出码：
  0 = 全部检查通过
  1 = 发现问题
"""
import os, re, argparse, sys
from PIL import Image


def find_html_file(root, html_name):
    """在项目根目录查找HTML展示页文件。

    优先返回品牌资产展示页（排除VI手册等辅助HTML），
    当有多个HTML文件时按以下优先级：
      1. 文件名不含"VI/手册/manual"的（即展示页）
      2. 按文件名排序取第一个
    """
    if html_name:
        path = os.path.join(root, html_name)
        if os.path.exists(path):
            return path
    # 自动检测：在根目录查找.html文件（不含子目录）
    html_files = []
    for f in sorted(os.listdir(root)):
        if f.endswith(".html") and os.path.isfile(os.path.join(root, f)):
            html_files.append(f)
    if not html_files:
        return None
    # 优先选择展示页（排除VI手册等辅助HTML）
    for f in html_files:
        name_lower = f.lower()
        if 'vi' not in name_lower and '手册' not in name_lower and 'manual' not in name_lower:
            return os.path.join(root, f)
    # 回退：返回第一个
    return os.path.join(root, html_files[0])


def get_actual_files(root, exclude_html=True):
    """获取根目录下所有文件的相对路径，排除HTML文件本身。"""
    files = set()
    for dirpath, dirs, filenames in os.walk(root):
        for fname in filenames:
            if exclude_html and fname.endswith(".html"):
                continue
            full = os.path.join(dirpath, fname)
            rel = os.path.relpath(full, root).replace("\\", "/")
            files.add(rel)
    return files


def get_referenced_files(html_path):
    """从HTML中提取所有src/href文件引用。"""
    with open(html_path, "r", encoding="utf-8") as f:
        html = f.read()
    # 先移除<code>...</code>块——其中包含示例代码
    # （如 <code>&lt;link rel="icon" href="favicon.ico"&gt;</code>）
    # 其中的src/href是示例，不是真实文件引用。按BA4-02要求：
    # "排除<code>标签内示例代码"。
    html = re.sub(r'<code[^>]*>.*?</code>', '', html, flags=re.DOTALL)
    # 匹配 src="..." 和 href="..."，排除锚点(#)和外部URI
    refs = set()
    for match in re.finditer(r'(?:src|href)="([^"]+)"', html):
        ref = match.group(1)
        if ref.startswith("#") or ref.startswith("http") or ref.startswith("data:"):
            continue
        # 跳过不像真实文件路径的引用
        if "." not in ref:
            continue
        # 排除外部 CSS/JS 引用（展示页使用内联样式，不应将外部资源引用视为资产文件）
        if ref.endswith(".css") or ref.endswith(".js"):
            continue
        refs.add(ref)
    return refs


def check_png_dimensions(root, html_path):
    """检查HTML中标注的PNG尺寸是否与实际文件一致。

    三种扫描方式覆盖不同标注形式：
      方式1：逐行扫描——src 和尺寸标注在同一行内（原有逻辑）
      方式2：块级扫描——按 img/div/figure 拆分，跨行匹配（修复：标注在图片下方时也能校验）
      方式3：属性扫描——检查 img 标签的 alt/title 属性中的尺寸标注
    """
    issues = []
    with open(html_path, "r", encoding="utf-8") as f:
        html = f.read()

    dim_pattern = re.compile(r'(\d+)[×x](\d+)')
    src_pattern = re.compile(r'src="([^"]+\.png)"')
    checked = set()

    # ---------- 方式1：逐行扫描（原有逻辑，src 和 dim 在同一行）----------
    for line in html.split("\n"):
        src_match = src_pattern.search(line)
        dim_match = dim_pattern.search(line)
        if src_match and dim_match:
            png_rel = src_match.group(1)
            png_path = os.path.join(root, png_rel)
            if os.path.exists(png_path):
                try:
                    img = Image.open(png_path)
                    actual_w, actual_h = img.size
                    labeled_w = int(dim_match.group(1))
                    labeled_h = int(dim_match.group(2))
                    if actual_w != labeled_w or actual_h != labeled_h:
                        issues.append(
                            "  不匹配: %s 标注 %dx%d 但实际 %dx%d"
                            % (png_rel, labeled_w, labeled_h, actual_w, actual_h)
                        )
                except Exception as e:
                    issues.append("  读取错误 %s: %s" % (png_rel, e))

    # ---------- 方式2：块级扫描（跨行匹配）----------
    # 将HTML按 img/div/figure/li 块拆分，在每个块内查找 src + dim
    blocks = re.split(
        r'(?=<\s*(?:img|div|figure|li|span)\b)',
        html,
        flags=re.IGNORECASE,
    )
    for block in blocks:
        src_match = src_pattern.search(block)
        dim_match = dim_pattern.search(block)
        if src_match and dim_match:
            png_rel = src_match.group(1)
            if png_rel in checked:
                continue
            checked.add(png_rel)
            png_path = os.path.join(root, png_rel)
            if os.path.exists(png_path):
                try:
                    img = Image.open(png_path)
                    actual_w, actual_h = img.size
                    labeled_w = int(dim_match.group(1))
                    labeled_h = int(dim_match.group(2))
                    if actual_w != labeled_w or actual_h != labeled_h:
                        issues.append(
                            "  不匹配: %s 标注 %dx%d 但实际 %dx%d"
                            % (png_rel, labeled_w, labeled_h, actual_w, actual_h)
                        )
                except Exception as e:
                    issues.append("  读取错误 %s: %s" % (png_rel, e))

    # ---------- 方式3：属性扫描（alt / title 中的尺寸标注）----------
    alt_title_pattern = re.compile(r'(?:alt|title)="[^"]*?(\d+[×x]\d+)[^"]*?"')
    img_tag_pattern = re.compile(r'<img[^>]+src="([^"]+\.png)"[^>]*>', re.IGNORECASE)
    for img_match in img_tag_pattern.finditer(html):
        img_tag = img_match.group(0)
        png_rel = img_match.group(1)
        alt_match = alt_title_pattern.search(img_tag)
        if alt_match:
            if png_rel in checked:
                continue
            checked.add(png_rel)
            png_path = os.path.join(root, png_rel)
            if os.path.exists(png_path):
                try:
                    img = Image.open(png_path)
                    actual_w, actual_h = img.size
                    dim_str = alt_match.group(1)
                    dim_parts = re.match(r'(\d+)[×x](\d+)', dim_str)
                    if dim_parts:
                        labeled_w = int(dim_parts.group(1))
                        labeled_h = int(dim_parts.group(2))
                        if actual_w != labeled_w or actual_h != labeled_h:
                            issues.append(
                                "  不匹配: %s 标注 %dx%d 但实际 %dx%d"
                                % (png_rel, labeled_w, labeled_h, actual_w, actual_h)
                            )
                except Exception as e:
                    issues.append("  读取错误 %s: %s" % (png_rel, e))

    return issues


def check_render_quality(root):
    """BA3-04: 检查PNG渲染质量——边缘截断、内容居中、ICO结构有效性。"""
    import struct
    issues = []

    # 1. 检查所有PNG的边缘是否clean（无截断）
    for dirpath, dirs, files in os.walk(root):
        for f in files:
            if not f.endswith(".png"):
                continue
            png_path = os.path.join(dirpath, f)
            try:
                img = Image.open(png_path).convert("RGBA")
                w, h = img.size
                # 检查四角像素一致性（判断是否有截断），不限制颜色
                corners = [
                    img.getpixel((0, 0)),
                    img.getpixel((w - 1, 0)),
                    img.getpixel((0, h - 1)),
                    img.getpixel((w - 1, h - 1)),
                ]
                # 允许透明背景
                bg = corners[0]
                bg_is_transparent = bg[3] <= 10
                bg_color = (bg[0], bg[1], bg[2]) if not bg_is_transparent else None
                # 检查四角是否一致（容差10）
                inconsistent_corners = []
                for i, c in enumerate(corners):
                    if bg_is_transparent and c[3] > 10:
                        inconsistent_corners.append(i)
                    elif not bg_is_transparent:
                        rdiff = abs(c[0] - bg_color[0])
                        gdiff = abs(c[1] - bg_color[1])
                        bdiff = abs(c[2] - bg_color[2])
                        adiff = abs(c[3] - bg[3])
                        if rdiff > 10 or gdiff > 10 or bdiff > 10 or adiff > 10:
                            inconsistent_corners.append(i)
                if inconsistent_corners:
                    rel = os.path.relpath(png_path, root)
                    issues.append("  四角不一致（可能截断）: %s (%dx%d) - 角 %s 与角0(%s) 不一致" % (rel, w, h, inconsistent_corners, bg))
            except Exception as e:
                issues.append("  读取错误 %s: %s" % (f, e))

    # 2. 检查ICO文件结构有效性
    for dirpath, dirs, files in os.walk(root):
        for f in files:
            if not f.endswith(".ico"):
                continue
            ico_path = os.path.join(dirpath, f)
            try:
                with open(ico_path, "rb") as fp:
                    data = fp.read()
                # 解析ICO header
                reserved, ico_type, count = struct.unpack_from("<HHH", data, 0)
                if reserved != 0 or ico_type != 1:
                    issues.append("  ICO header错误: %s (reserved=%d, type=%d)" % (f, reserved, ico_type))
                    continue
                # 解析每个entry
                sizes_found = []
                offset = 6
                for i in range(count):
                    w_b, h_b, pal, rsv, planes, bpp, size, data_off = struct.unpack_from("<BBBBHHII", data, offset)
                    actual_w = w_b if w_b != 0 else 256
                    actual_h = h_b if h_b != 0 else 256
                    sizes_found.append(actual_w)
                    # 检查数据偏移量是否在文件范围内
                    if data_off + size > len(data):
                        issues.append("  ICO偏移量错误: %s entry %d (offset=%d, size=%d, file=%d)" % (f, i, data_off, size, len(data)))
                    offset += 16
                rel = os.path.relpath(ico_path, root)
                print("  ICO正常: %s（%d个尺寸: %s）" % (rel, count, sizes_found))
            except Exception as e:
                issues.append("  ICO错误: %s - %s" % (f, e))

    return issues


def check_duplicates(root):
    """BA4-03: 检查重复文件——字节级比对同尺寸PNG。"""
    import hashlib
    issues = []

    # 按文件大小分组，同大小的再比hash
    size_map = {}
    for dirpath, dirs, files in os.walk(root):
        for f in files:
            if not f.endswith(".png"):
                continue
            fp = os.path.join(dirpath, f)
            sz = os.path.getsize(fp)
            if sz not in size_map:
                size_map[sz] = []
            size_map[sz].append(fp)

    # 同大小的文件比MD5
    for sz, paths in size_map.items():
        if len(paths) < 2:
            continue
        hash_map = {}
        for fp in paths:
            with open(fp, "rb") as f:
                md5 = hashlib.md5(f.read()).hexdigest()
            if md5 not in hash_map:
                hash_map[md5] = []
            hash_map[md5].append(fp)

        for md5, dups in hash_map.items():
            if len(dups) >= 2:
                rels = [os.path.relpath(p, root) for p in dups]
                issues.append("  重复: %s (MD5=%s, %d bytes)" % (" == ".join(rels), md5[:8], sz))

    return issues


def main():
    parser = argparse.ArgumentParser(description="品牌资产完整性校验器")
    parser.add_argument("project_root", help="项目根目录")
    parser.add_argument("--html", help="HTML文件名（省略时自动检测）")
    parser.add_argument("--render-check", action="store_true", help="同时检查渲染质量（边缘、ICO）")
    parser.add_argument("--dup-check", action="store_true", help="同时检查重复文件")
    parser.add_argument("--full", action="store_true", help="全量模式：校验87个全量文件（默认核心62个）")
    args = parser.parse_args()

    root = os.path.abspath(args.project_root)
    html_path = find_html_file(root, args.html)

    if not html_path:
        print("错误：在 %s 中未找到HTML文件" % root)
        sys.exit(1)

    print("=== 品牌资产校验 ===")
    print("项目: %s" % root)
    print("HTML: %s" % os.path.basename(html_path))
    print()

    actual = get_actual_files(root, exclude_html=False)
    referenced = get_referenced_files(html_path)
    # HTML文件是独立交付物，不应当出现在"孤儿"列表中（它本身就是主文件而非被引用的资产）
    referenced.add(os.path.basename(html_path))

    print("实际文件数:   %d" % len(actual))
    print("HTML引用数:   %d" % len(referenced))
    print()

    # 检查孤儿（存在但未被引用）
    orphans = actual - referenced
    if orphans:
        print("孤儿文件（存在但HTML未引用）:")
        for f in sorted(orphans):
            print("  " + f)
    else:
        print("孤儿文件: 0")

    # 检查悬空（引用但不存在）
    dangling = referenced - actual
    if dangling:
        print("\n悬空引用（HTML引用但文件不存在）:")
        for f in sorted(dangling):
            print("  " + f)
    else:
        print("悬空引用: 0")

    # 检查PNG尺寸标注
    print("\nPNG尺寸标注校验:")
    dim_issues = check_png_dimensions(root, html_path)
    if dim_issues:
        for issue in dim_issues:
            print(issue)
    else:
        print("  所有PNG尺寸标注与实际像素一致")

    # 可选：渲染质量检查（BA3-04）
    if args.render_check:
        print("\n渲染质量检查:")
        render_issues = check_render_quality(root)
        if render_issues:
            for issue in render_issues:
                print(issue)
        else:
            print("  所有PNG边缘干净，ICO结构有效")

    # 可选：重复文件检查（BA4-03）
    if args.dup_check:
        print("\n重复文件检查:")
        dup_issues = check_duplicates(root)
        if dup_issues:
            for issue in dup_issues:
                print(issue)
        else:
            print("  未发现重复文件")

    # 文件数硬校验（事实纪律#15）
    expected_total = 87 if args.full else 62
    actual_total = len(actual)
    print("\n文件数硬校验:")
    if actual_total == expected_total:
        print("  文件数正确：%d个（%s模式，预期%d个）" % (actual_total, "全量" if args.full else "核心", expected_total))
    else:
        print("  文件数不匹配：实际%d个，预期%d个（%s模式）" % (actual_total, expected_total, "全量" if args.full else "核心"))

    # 汇总
    print("\n=== 汇总 ===")
    total_issues = len(orphans) + len(dangling) + len(dim_issues)
    if args.render_check:
        total_issues += len(render_issues)
    if args.dup_check:
        total_issues += len(dup_issues)
    if actual_total != expected_total:
        total_issues += 1
    if total_issues == 0:
        print("全部检查通过")
        sys.exit(0)
    else:
        print("发现 %d 个问题" % total_issues)
        sys.exit(1)


if __name__ == "__main__":
    main()
