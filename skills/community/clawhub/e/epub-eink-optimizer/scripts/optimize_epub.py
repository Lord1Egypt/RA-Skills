#!/usr/bin/env python3
"""
epub-eink-optimizer: 墨水屏电子书图片优化工具

用法:
  python optimize_epub.py <epub_path> [选项]

选项:
  --max-width   INT    图片最大宽度像素 (默认: 800)
  --quality     INT    JPEG压缩质量 1-95 (默认: 70)
  --min-size    INT    清除低于此字节数的图片 (默认: 10240 即10KB)
  --no-dedup         跳过重复图片合并
  --no-resize        跳过宽度缩放
  --no-recompress    跳过JPEG重压缩
  --no-clean-small   跳过小图清除
  --dry-run          仅分析，不修改文件
"""
import argparse, zipfile, hashlib, collections, os, io, re, sys, shutil
from PIL import Image

# ──────────────────────────────────────────────
# 工具函数
# ──────────────────────────────────────────────
def read_epub(path):
    files = {}
    with zipfile.ZipFile(path, 'r') as z:
        for name in z.namelist():
            files[name] = z.read(name)
    return files

def write_epub(files, path):
    tmp = path + ".tmp"
    with zipfile.ZipFile(tmp, 'w', zipfile.ZIP_DEFLATED) as zout:
        mimetype = files.pop('mimetype', None)
        if mimetype:
            zout.writestr(zipfile.ZipInfo('mimetype'), mimetype, compress_type=zipfile.ZIP_STORED)
        for name, data in sorted(files.items()):
            zout.writestr(name, data)
    os.replace(tmp, path)

def is_image(name):
    return name.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp'))

def is_jpeg(name):
    return name.lower().endswith(('.jpg', '.jpeg'))

def epub_size_mb(path):
    return os.path.getsize(path) / 1024 / 1024

# ──────────────────────────────────────────────
# 步骤1: 去重复图片
# ──────────────────────────────────────────────
def dedup_images(files, dry_run=False):
    img_names = [n for n in files if is_image(n)]
    hash_to_files = collections.defaultdict(list)
    for img in img_names:
        h = hashlib.md5(files[img]).hexdigest()
        hash_to_files[h].append(img)

    duplicates = {h: f for h, f in hash_to_files.items() if len(f) > 1}
    if not duplicates:
        print("  [去重] 无重复图片")
        return files, 0

    replace_map = {}
    to_delete = set()
    saved = 0
    for h, flist in duplicates.items():
        canonical = sorted(flist)[0]
        for f in flist[1:]:
            replace_map[f] = canonical
            to_delete.add(f)
            saved += len(files[f])
            print(f"  [去重] {os.path.basename(f)} -> {os.path.basename(canonical)}")

    if dry_run:
        print(f"  [去重] 可节省 {saved//1024}KB ({len(to_delete)} 张副本)")
        return files, saved

    # 更新XHTML引用
    for xhtml_name in [n for n in files if n.endswith(('.xhtml', '.html'))]:
        content = files[xhtml_name].decode('utf-8', errors='replace')
        for dup, canon in replace_map.items():
            content = content.replace(os.path.basename(dup), os.path.basename(canon))
        files[xhtml_name] = content.encode('utf-8')

    # 更新OPF
    for opf_name in [n for n in files if n.endswith('.opf')]:
        content = files[opf_name].decode('utf-8', errors='replace')
        for dup in to_delete:
            basename = os.path.basename(dup)
            content = re.sub(r'\s*<item\b[^>]*href="[^"]*' + re.escape(basename) + r'"[^>]*/>\s*', '\n', content)
        files[opf_name] = content.encode('utf-8')

    for f in to_delete:
        del files[f]

    print(f"  [去重] 节省 {saved//1024}KB，删除 {len(to_delete)} 张副本")
    return files, saved

# ──────────────────────────────────────────────
# 步骤2: 清除小图（及其XHTML引用）
# ──────────────────────────────────────────────
def remove_small_images(files, min_size=10240, dry_run=False):
    small = [n for n in files if is_image(n) and len(files[n]) < min_size]
    if not small:
        print(f"  [清小图] 无 {min_size//1024}KB 以下图片")
        return files, 0

    saved = sum(len(files[n]) for n in small)
    print(f"  [清小图] 发现 {len(small)} 张，共 {saved//1024}KB")

    if dry_run:
        return files, saved

    # 删除XHTML中的img标签
    removed_tags = 0
    for xhtml_name in [n for n in files if n.endswith(('.xhtml', '.html'))]:
        content = files[xhtml_name].decode('utf-8', errors='replace')
        original = content
        for img_path in small:
            basename = os.path.basename(img_path)
            content = re.sub(r'<img\b[^>]*src="[^"]*' + re.escape(basename) + r'"[^>]*/?>',  '', content)
        content = re.sub(r'<p>\s*</p>', '', content)
        content = re.sub(r'<div[^>]*>\s*</div>', '', content)
        if content != original:
            removed_tags += original.count('<img') - content.count('<img')
            files[xhtml_name] = content.encode('utf-8')

    # 更新OPF
    for opf_name in [n for n in files if n.endswith('.opf')]:
        content = files[opf_name].decode('utf-8', errors='replace')
        for img_path in small:
            basename = os.path.basename(img_path)
            content = re.sub(r'\s*<item\b[^>]*href="[^"]*' + re.escape(basename) + r'"[^>]*/>\s*', '\n', content)
        files[opf_name] = content.encode('utf-8')

    for n in small:
        del files[n]

    print(f"  [清小图] 删除 {len(small)} 张图，清除 {removed_tags} 个img标签")
    return files, saved

# ──────────────────────────────────────────────
# 步骤3: 缩放宽度超限图片
# ──────────────────────────────────────────────
def resize_images(files, max_width=800, quality=85, dry_run=False):
    img_names = [n for n in files if is_image(n)]
    total_before = sum(len(files[n]) for n in img_names)
    count = 0

    for name in sorted(img_names):
        data = files[name]
        try:
            img = Image.open(io.BytesIO(data))
            w, h = img.size
            if w <= max_width:
                continue
            new_h = int(h * max_width / w)
            img = img.resize((max_width, new_h), Image.LANCZOS)
            buf = io.BytesIO()
            fmt = 'JPEG' if is_jpeg(name) else 'PNG'
            if fmt == 'JPEG':
                img.convert('RGB').save(buf, format='JPEG', quality=quality, optimize=True)
            else:
                img.save(buf, format='PNG', optimize=True)
            new_data = buf.getvalue()
            print(f"  [缩放] {os.path.basename(name)}: {w}x{h} -> {max_width}x{new_h}  {len(data)//1024}KB -> {len(new_data)//1024}KB")
            if not dry_run:
                files[name] = new_data
            count += 1
        except Exception as e:
            print(f"  [缩放] 跳过 {name}: {e}")

    total_after = sum(len(files[n]) for n in img_names)
    saved = total_before - total_after
    if count == 0:
        print(f"  [缩放] 无超过 {max_width}px 的图片")
    else:
        print(f"  [缩放] 缩放 {count} 张，节省 {saved//1024}KB")
    return files, saved

# ──────────────────────────────────────────────
# 步骤4: JPEG重压缩
# ──────────────────────────────────────────────
def recompress_jpegs(files, quality=70, dry_run=False):
    jpg_names = [n for n in files if is_jpeg(n)]
    if not jpg_names:
        print("  [重压] 无JPEG图片")
        return files, 0

    total_before = sum(len(files[n]) for n in jpg_names)

    if not dry_run:
        for name in sorted(jpg_names):
            try:
                img = Image.open(io.BytesIO(files[name])).convert('RGB')
                buf = io.BytesIO()
                img.save(buf, format='JPEG', quality=quality, optimize=True)
                files[name] = buf.getvalue()
            except Exception as e:
                print(f"  [重压] 跳过 {name}: {e}")

    total_after = sum(len(files[n]) for n in jpg_names)
    saved = total_before - total_after
    print(f"  [重压] {len(jpg_names)} 张JPEG quality={quality}，节省 {saved//1024}KB ({saved/total_before*100:.1f}%)")
    return files, saved

# ──────────────────────────────────────────────
# 主流程
# ──────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description='epub墨水屏优化工具')
    parser.add_argument('epub', help='epub文件路径')
    parser.add_argument('--max-width',      type=int,   default=800,   help='图片最大宽度 (默认800)')
    parser.add_argument('--quality',        type=int,   default=70,    help='JPEG质量 (默认70)')
    parser.add_argument('--min-size',       type=int,   default=10240, help='最小图片字节数 (默认10240=10KB)')
    parser.add_argument('--no-dedup',       action='store_true', help='跳过去重')
    parser.add_argument('--no-resize',      action='store_true', help='跳过缩放')
    parser.add_argument('--no-recompress',  action='store_true', help='跳过重压缩')
    parser.add_argument('--no-clean-small', action='store_true', help='跳过清小图')
    parser.add_argument('--dry-run',        action='store_true', help='仅分析，不修改')
    args = parser.parse_args()

    if not os.path.exists(args.epub):
        print(f"错误: 文件不存在: {args.epub}")
        sys.exit(1)

    size_before = epub_size_mb(args.epub)
    print(f"\n{'='*50}")
    print(f"epub墨水屏优化器")
    print(f"{'='*50}")
    print(f"输入: {args.epub}")
    print(f"原始大小: {size_before:.1f}MB")
    if args.dry_run:
        print("模式: 仅分析（dry-run）")
    print(f"{'='*50}\n")

    files = read_epub(args.epub)
    total_saved = 0

    if not args.no_dedup:
        print("步骤1: 去重复图片")
        files, saved = dedup_images(files, args.dry_run)
        total_saved += saved

    if not args.no_clean_small:
        print(f"\n步骤2: 清除 {args.min_size//1024}KB 以下小图")
        files, saved = remove_small_images(files, args.min_size, args.dry_run)
        total_saved += saved

    if not args.no_resize:
        print(f"\n步骤3: 缩放宽度超过 {args.max_width}px 的图片")
        files, saved = resize_images(files, args.max_width, args.quality, args.dry_run)
        total_saved += saved

    if not args.no_recompress:
        print(f"\n步骤4: JPEG重压缩 quality={args.quality}")
        files, saved = recompress_jpegs(files, args.quality, args.dry_run)
        total_saved += saved

    if not args.dry_run:
        print(f"\n{'='*50}")
        print("写入epub...")
        write_epub(files, args.epub)
        size_after = epub_size_mb(args.epub)
        print(f"{'='*50}")
        print(f"完成！")
        print(f"  原始大小: {size_before:.1f}MB")
        print(f"  优化后:   {size_after:.1f}MB")
        print(f"  压缩率:   {(1-size_after/size_before)*100:.1f}%")
        print(f"{'='*50}\n")
    else:
        print(f"\n{'='*50}")
        print(f"[dry-run] 预计可节省约 {total_saved//1024}KB")
        print(f"{'='*50}\n")

if __name__ == '__main__':
    main()
