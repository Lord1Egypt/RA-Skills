#!/usr/bin/env python3
"""
Process relatedLinks attachments for a book card (generalized version).
1. Download file links (pdf/docx/xlsx/pptx/png/jpg/gif/webp...) from payload.relatedLinks
2. Convert PNG to JPG (high quality, white background for transparency)
3. Skip images already embedded in the PDF (payload.image / payload.images)
4. Emit renamed files + attachments.json ready for upload (IMA or Feishu API)

Usage:
  python process_attachments.py --payload /tmp/b2l_payload.json --date 2026-08-23 --card-id ch01-12 --out-dir /tmp/b2l_attachments [--prefix BOOK]

Notes:
- Download failures are recorded in attachments.json `skipped` (never crash the push).
- No emoji in output (weasyprint/console-safe).
"""
import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
from urllib.parse import urlparse

EXTENSIONS = {'.pdf', '.docx', '.xlsx', '.doc', '.ppt', '.pptx',
              '.png', '.jpg', '.jpeg', '.gif', '.webp'}
IMAGE_EXTS = {'.png', '.jpg', '.jpeg', '.gif', '.webp'}
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"


def run_curl(url, out_path, referer=""):
    """Download file with curl. Return True if file exists and is not an HTML error page."""
    cmd = ["curl", "-sL", "--fail", "--max-time", "60",
           "-A", USER_AGENT,
           "-H", "Accept: image/*,application/pdf,*/*"]
    if referer:
        cmd += ["-e", referer]
    cmd += [url, "-o", out_path]
    try:
        r = subprocess.run(cmd, capture_output=True, timeout=90)
    except subprocess.TimeoutExpired:
        if os.path.exists(out_path):
            os.unlink(out_path)
        return False
    if r.returncode != 0:
        # curl 失败（--max-time 截断 / DNS / TLS / HTTP>=400）：残留的半截文件必须删掉
        if os.path.exists(out_path):
            os.unlink(out_path)
        return False
    if not os.path.exists(out_path):
        return False
    min_size = 16 if os.path.splitext(out_path)[1].lower() in IMAGE_EXTS else 64
    if os.path.getsize(out_path) < min_size:
        os.unlink(out_path)
        return False
    # Detect HTML error pages (403/404 bodies served as 200)
    try:
        with open(out_path, 'rb') as f:
            head = f.read(256).lstrip().lower()
        if head.startswith(b'<!doctype html') or head.startswith(b'<html'):
            os.unlink(out_path)
            return False
    except Exception:
        pass
    return True


def png_to_jpg(png_path, quality=95):
    """Convert PNG to JPG with white background. Returns new path. Requires Pillow."""
    from PIL import Image
    img = Image.open(png_path)
    jpg_path = os.path.splitext(png_path)[0] + '.jpg'
    if img.mode in ('RGBA', 'LA'):
        background = Image.new('RGB', img.size, (255, 255, 255))
        mask = img.split()[-1] if img.mode == 'RGBA' else img.split()[1]
        background.paste(img, mask=mask)
        img = background
    elif img.mode != 'RGB':
        img = img.convert('RGB')
    img.save(jpg_path, 'JPEG', quality=quality)
    os.unlink(png_path)
    return jpg_path


def sanitize_filename(name):
    name = re.sub(r'[^\w\-\. ]', '_', name)
    name = re.sub(r'\s+', '_', name)
    return name


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--payload', required=True, help='Path to push payload JSON')
    ap.add_argument('--date', required=True, help='Date for filename (YYYY-MM-DD)')
    ap.add_argument('--card-id', required=True, help='Card ID (e.g. ch01-12)')
    ap.add_argument('--out-dir', default='/tmp/b2l_attachments', help='Output directory')
    ap.add_argument('--prefix', default=None, help='Filename prefix (default: book cardPrefix from config)')
    args = ap.parse_args()

    os.makedirs(args.out_dir, exist_ok=True)
    if not shutil.which('curl'):
        print(json.dumps({'ok': False, 'error': '未找到 curl 命令（process_attachments 依赖 curl 下载附件）'}))
        raise SystemExit(1)

    with open(args.payload, encoding='utf-8') as f:
        payload = json.load(f)

    prefix = args.prefix or os.environ.get('B2L_PREFIX') or (payload.get('bookSlug') or 'B2L').upper()

    # Collect already embedded image srcs to skip duplicates
    embedded_srcs = set()
    img = payload.get('image', '') or ''
    if img and not img.startswith('data:'):
        embedded_srcs.add(img)   # URL 型主配图：链接相同则跳过重复上传
    # data URI 主配图无法与链接 URL 匹配（原 __EMBEDDED__ 哨兵永远匹配不上，是死逻辑）
    for im in payload.get('images', []) or []:
        src = im.get('src', '') if isinstance(im, dict) else ''
        if src:
            embedded_srcs.add(src)

    processed, skipped = [], []

    for link in payload.get('relatedLinks', []):
        if isinstance(link, dict):
            href = link.get('href', '')
        else:
            href = str(link)
        parsed = urlparse(href)
        ext = os.path.splitext(parsed.path)[1].lower()

        if ext not in EXTENSIONS:
            continue
        if href in embedded_srcs and ext in IMAGE_EXTS:
            skipped.append(('already_embedded', href))
            continue

        orig_name = sanitize_filename(os.path.basename(parsed.path)) or ('file' + ext)
        print("Processing: %s" % href)

        tmp_path = os.path.join(args.out_dir, orig_name)
        if not run_curl(href, tmp_path):
            print("  [WARN] Download failed or invalid file (likely 403/404)")
            skipped.append(('download_failed', href))
            continue

        final_path = tmp_path
        if ext == '.png':
            try:
                final_path = png_to_jpg(tmp_path)
                orig_name = os.path.splitext(orig_name)[0] + '.jpg'
            except Exception as e:
                print("  [WARN] PNG->JPG conversion failed: %s" % e)
                skipped.append(('convert_failed', href))
                if os.path.exists(tmp_path):
                    os.unlink(tmp_path)
                continue

        short_hash = hashlib.md5(href.encode()).hexdigest()[:6]
        final_name = f"{prefix}_{args.date}_{args.card_id}_{short_hash}_{orig_name}"
        final_renamed = os.path.join(args.out_dir, final_name)
        if final_path != final_renamed:
            os.rename(final_path, final_renamed)

        processed.append({
            'href': href,
            'local_path': final_renamed,
            'filename': final_name,
            'converted_from_png': ext == '.png',
        })
        print("  [OK] Ready: %s" % final_name)

    print("=" * 60)
    print("Processed %d files, skipped %d" % (len(processed), len(skipped)))
    for p in processed:
        status = " (PNG->JPG)" if p['converted_from_png'] else ""
        print("  [OK] %s%s" % (p['filename'], status))
    for reason, url in skipped:
        print("  [SKIP] (%s): %s" % (reason, url))

    result = {
        'date': args.date,
        'card_id': args.card_id,
        'processed': processed,
        'skipped': skipped,
        'out_dir': args.out_dir,
    }
    with open(os.path.join(args.out_dir, 'attachments.json'), 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    print("Result saved to %s" % os.path.join(args.out_dir, 'attachments.json'))


if __name__ == '__main__':
    main()
