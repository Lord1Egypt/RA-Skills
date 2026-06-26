#!/usr/bin/env python3
"""
image_batch.py — 图像批处理工具（标准库 + pillow 可选）
覆盖：缩放/压缩/水印/格式转换/裁剪/旋转/批量重命名/信息查看

用法：
  python image_batch.py info photo.jpg
  python image_batch.py batch-resize ./photos -w 1920 -h 1080 -o ./resized
  python image_batch.py compress ./images --quality 70 -o ./compressed
  python image_batch.py watermark ./photos --text "Copyright 2025" -o ./marked
  python image_batch.py convert ./images png jpg -o ./converted
  python image_batch.py crop ./photos --left 100 --top 50 --width 800 --height 600
  python image_batch.py rotate ./photos --angle 90 -o ./rotated
  python image_batch.py thumbnail ./photos --size 256 -o ./thumbs
  python image_batch.py grid ./photos --cols 4 --spacing 10 -o collage.png
"""

import sys
import os
import json
import struct
import math
from typing import Optional, Tuple, List


# ─── CLI ──────────────────────────────────────────────────────

def parse_args(argv=None):
    argv = argv or sys.argv[1:]
    if not argv or '-h' in argv or '--help' in argv:
        print(__doc__)
        sys.exit(0)
    cmd = argv[0]
    args = {'_cmd': cmd, '_pos': []}
    i = 1
    while i < len(argv):
        a = argv[i]
        if a.startswith('-'):
            key = a.lstrip('-').replace('-', '_')
            if i + 1 < len(argv) and not argv[i+1].startswith('-'):
                args[key] = argv[i + 1]
                i += 2
            else:
                args[key] = True
                i += 1
        else:
            args['_pos'].append(a)
            i += 1
    return args


def color(text: str, fg: str = '') -> str:
    codes = {'red': 31, 'green': 32, 'yellow': 33, 'blue': 34, 'cyan': 36}
    code = codes.get(fg, '')
    if not code:
        return text
    if hasattr(sys.stdout, 'isatty') and sys.stdout.isatty():
        return f'\033[{code}m{text}\033[0m'
    return text


def echo(text: str, fg: str = ''):
    print(color(text, fg))


def ensure_pillow():
    """确保 Pillow 可用"""
    try:
        from PIL import Image
        return Image
    except ImportError:
        echo('⚠️ 需要安装 Pillow: pip install pillow', fg='yellow')
        echo('   部分功能将不可用（仅支持基本信息读取）', fg='yellow')
        return None


# ─── 图像文件扫描 ───────────────────────────────────────────

IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp',
                    '.tiff', '.tif', '.ico', '.ppm', '.pgm', '.pbm'}


def scan_images(directory: str, recursive: bool = False) -> List[str]:
    """扫描目录中的图像文件"""
    images = []
    if recursive:
        for root, dirs, files in os.walk(directory):
            dirs[:] = [d for d in dirs if d not in ('.git', '__pycache__', 'node_modules')]
            for f in files:
                ext = os.path.splitext(f)[1].lower()
                if ext in IMAGE_EXTENSIONS:
                    images.append(os.path.join(root, f))
    else:
        if os.path.isdir(directory):
            for f in os.listdir(directory):
                full = os.path.join(directory, f)
                if os.path.isfile(full):
                    ext = os.path.splitext(f)[1].lower()
                    if ext in IMAGE_EXTENSIONS:
                        images.append(full)
        elif os.path.isfile(directory) and os.path.splitext(directory)[1].lower() in IMAGE_EXTENSIONS:
            images.append(directory)
    return sorted(images)


def _fmt_size(b: int) -> str:
    for u in ['B', 'KB', 'MB']:
        if b < 1024:
            return f'{b:.1f} {u}'
        b /= 1024
    return f'{b:.1f} GB'


# ══════════════════════════════════════════════════════════════
#  命令实现
# ══════════════════════════════════════════════════════════════

def cmd_info(args):
    """查看图像详细信息"""
    target = args['_pos'][0] if args.get('_pos') else ''

    Image = ensure_pillow()

    # 单个文件
    if os.path.isfile(target):
        _print_image_info(target, Image)

    # 目录
    elif os.path.isdir(target):
        images = scan_images(target)
        echo(f'📂 扫描目录: {target} ({len(images)} 张图像)', fg='cyan')

        from scripts.table_format import tabulate
        rows = []
        total_size = 0
        for img_path in images:
            info = get_image_meta(img_path, Image)
            if info:
                total_size += info.get('size', 0)
                rows.append({
                    '名称': os.path.basename(info['path']),
                    '格式': info.get('format', '?'),
                    '尺寸': info.get('dimensions', ''),
                    '大小': _fmt_size(info.get('size', 0)),
                    '模式': info.get('mode', ''),
                })
        print(tabulate(rows, tablefmt='grid'))
        echo(f'总计: {len(images)} 张图像, {_fmt_size(total_size)}', fg='cyan')


def get_image_meta(path: str, Image=None) -> dict:
    """获取图像元数据"""
    result = {
        'path': path,
        'format': None,
        'dimensions': '',
        'mode': '',
        'size': 0,
    }

    try:
        result['size'] = os.path.getsize(path)
    except OSError:
        pass

    if Image is None:
        # 仅从文件头解析基本信息
        try:
            with open(path, 'rb') as f:
                header = f.read(32)
                if header[:8] == b'\x89PNG\r\n\x1a\n':
                    result['format'] = 'PNG'
                    w = struct.unpack('>I', header[16:20])[0]
                    h = struct.unpack('>I', header[20:24])[0]
                    result['dimensions'] = f'{w}x{h}'
                elif header[:2] == b'\xff\xd8':
                    result['format'] = 'JPEG'
                elif header[:6] == b'GIF87a' or header[:6] == b'GIF89a':
                    result['format'] = 'GIF'
                    w = struct.unpack('<H', header[6:8])[0]
                    h = struct.unpack('<H', header[8:10])[0]
                    result['dimensions'] = f'{w}x{h}'
                elif header[:2] == b'BM':
                    result['format'] = 'BMP'
        except (OSError, IndexError):
            pass
        return result

    try:
        with Image.open(path) as img:
            result['format'] = img.format or '?'
            w, h = img.size
            result['dimensions'] = f'{w}x{h}'
            result['mode'] = img.mode
            result['exif'] = {}
            if hasattr(img, '_getexif'):
                exif_data = img._getexif()
                if exif_data:
                    from PIL.ExifTags import TAGS
                    result['exif'] = {
                        TAGS.get(k, str(k)): v
                        for k, v in list(exif_data.items())[:20]
                    }
    except Exception as e:
        result['error'] = str(e)

    return result


def _print_image_info(path: str, Image=None):
    info = get_image_meta(path, Image)
    from scripts.table_format import tabulate
    echo(f'🖼 图像信息: {os.path.basename(path)}', fg='cyan', bold=True)
    meta_rows = [
        ['路径', path],
        ['格式', str(info.get('format', '?'))],
        ['尺寸', str(info.get('dimensions', ''))],
        ['色彩模式', str(info.get('mode', ''))],
        ['文件大小', _fmt_size(info.get('size', 0))],
    ]
    if info.get('error'):
        meta_rows.append(['错误', info['error']])
    print(tabulate(meta_rows, tablefmt='grid'))

    if info.get('exif') and info['exif']:
        echo('\nEXIF 信息:', fg='cyan')
        exif_rows = [[k, str(v)[:80]] for k, v in list(info['exif'].items())[:15]]
        print(tabulate(exif_rows, tablefmt='grid'))


def cmd_batch_resize(args):
    """批量缩放"""
    src_dir = args['_pos'][0] if args.get('_pos') else ''
    width = int(args.get('width', 0))
    height = int(args.get('height', 0))
    ratio = args.get('ratio', '')  # 如 "50%" 或 "0.5"
    maintain_aspect = args.get('keep_aspect', True)
    output_dir = args.get('o', '')
    recursive = args.get('recursive', False)

    Image = ensure_pillow()
    if Image is None:
        sys.exit(1)

    images = scan_images(src_dir, recursive=recursive)
    if not images:
        echo('❌ 未找到图像文件', fg='red')
        sys.exit(1)

    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    processed = 0
    for idx, img_path in enumerate(images):
        sys.stderr.write(f'\r  处理中: {idx+1}/{len(images)}')
        sys.stderr.flush()

        try:
            with Image.open(img_path) as img:
                orig_w, orig_h = img.size

                if ratio:
                    scale = float(ratio.rstrip('%')) / 100 if '%' in ratio else float(ratio)
                    new_w, new_h = int(orig_w * scale), int(orig_h * scale)
                elif width and height and not maintain_aspect:
                    new_w, new_h = width, height
                elif width:
                    new_w = width
                    new_h = int(orig_h * (width / orig_w))
                elif height:
                    new_h = height
                    new_w = int(orig_w * (height / orig_h))
                else:
                    continue

                resized = img.resize((new_w, new_h), Image.LANCZOS)

                out_name = f'resized_{os.path.basename(img_path)}' if not output_dir else os.path.basename(img_path)
                dest = os.path.join(output_dir, out_name) if output_dir else \
                    os.path.join(os.path.dirname(img_path), out_name)
                resized.save(dest, quality=95)
                processed += 1
        except Exception as e:
            echo(f'\n  ⚠️ {img_path}: {e}', fg='yellow')

    print(f'\n✅ 已缩放 {processed}/{len(images)} 张图像', fg='green')


def cmd_compress(args):
    """压缩图像"""
    src_dir = args['_pos'][0] if args.get('_pos') else ''
    quality = int(args.get('quality', 75))
    output_dir = args.get('o', '')

    Image = ensure_pillow()
    if Image is None:
        sys.exit(1)

    images = scan_images(src_dir)
    if not images:
        echo('❌ 未找到图像文件', fg='red')
        sys.exit(1)

    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    total_orig = 0
    total_compressed = 0
    processed = 0

    for idx, img_path in enumerate(images):
        sys.stderr.write(f'\r  压缩中: {idx+1}/{len(images)}')
        sys.stderr.flush()

        try:
            orig_size = os.path.getsize(img_path)
            total_orig += orig_size

            with Image.open(img_path) as img:
                out_name = os.path.basename(img_path)
                dest = os.path.join(output_dir, out_name) if output_dir else img_path

                # 根据格式选择保存参数
                fmt = img.format or 'JPEG'
                if fmt.upper() in ('JPEG', 'JPG'):
                    # 转换 RGBA → RGB
                    if img.mode == 'RGBA':
                        bg = Image.new('RGB', img.size, (255, 255, 255))
                        bg.paste(img, mask=img.split()[3])
                        img = bg
                    img.save(dest, format='JPEG', quality=quality, optimize=True)
                elif fmt == 'PNG':
                    img.save(dest, format='PNG', optimize=True)
                elif fmt == 'WEBP':
                    img.save(dest, format='WEBP', quality=quality)
                else:
                    img.save(dest, quality=quality)

                comp_size = os.path.getsize(dest)
                total_compressed += comp_size
                processed += 1
        except Exception as e:
            echo(f'\n  ⚠️ {img_path}: {e}', fg='yellow')

    saved_pct = ((total_orig - total_compressed) / total_orig * 100) if total_orig > 0 else 0
    print(f'\n✅ 压缩完成: {processed} 张 | '
          f'{_fmt_size(total_orig)} → {_fmt_size(total_compressed)} (节省 {saved_pct:.1f}%)', fg='green')


def cmd_watermark(args):
    """添加文字或图片水印"""
    src_dir = args['_pos'][0] if args.get('_pos') else ''
    text = args.get('text', '')
    text_color = args.get('color', '#ffffff80')  # 半透明白色
    font_size = int(args.get('font_size', 36))
    position = args.get('position', 'bottom-right')  # top-left, center, bottom-right, etc.
    opacity = float(args.get('opacity', 0.5))
    image_watermark = args.get('image', '')  # 图片水印路径
    output_dir = args.get('o', '')

    Image = ensure_pillow()
    if Image is None:
        sys.exit(1)

    try:
        from PIL import ImageDraw, ImageFont
    except ImportError:
        echo('❌ 缺少 PIL 组件', fg='red')
        sys.exit(1)

    images = scan_images(src_dir)
    if not images:
        echo('❌ 未找到图像', fg='red')
        return

    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    # 尝试加载字体
    font = None
    for font_path in [
        '/System/Library/Fonts/Helvetica.ttc',
        '/Windows/Fonts/msyh.ttc',
        '/Windows/Fonts/simhei.ttf',
        '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
    ]:
        if os.path.exists(font_path):
            try:
                font = ImageFont.truetype(font_path, font_size)
                break
            except Exception:
                pass
    if not font:
        try:
            font = ImageFont.load_default()
        except Exception:
            pass

    processed = 0
    for idx, img_path in enumerate(images):
        sys.stderr.write(f'\r  水印: {idx+1}/{len(images)}')
        sys.stderr.flush()

        try:
            with Image.open(img_path).convert('RGBA') as img:
                overlay = Image.new('RGBA', img.size, (0, 0, 0, 0))

                if image_watermark and os.path.isfile(image_watermark):
                    with Image.open(image_watermark) as wm:
                        wm = wm.resize(
                            (img.size[0] // 4, img.size[1] // 4),
                            Image.LANCZOS
                        )
                        wm.putalpha(int(255 * opacity))

                        pos_x = (img.size[0] - wm.size[0]) // 2 if position == 'center' else \
                                img.size[0] - wm.size[0] - 10 if position == 'bottom-right' else 10
                        pos_y = (img.size[1] - wm.size[1]) // 2 if position == 'center' else \
                                img.size[1] - wm.size[1] - 10 if position == 'bottom-right' else 10
                        overlay.paste(wm, (pos_x, pos_y), wm if wm.mode == 'RGBA' else None)
                elif text:
                    draw = ImageDraw.Draw(overlay)
                    bbox = draw.textbbox((0, 0), text, font=font)
                    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]

                    margin = 15
                    if position == 'bottom-right':
                        x, y = img.size[0] - tw - margin, img.size[1] - th - margin
                    elif position == 'top-left':
                        x, y = margin, margin
                    elif position == 'center':
                        x, y = (img.size[0] - tw) // 2, (img.size[1] - th) // 2
                    elif position == 'bottom-left':
                        x, y = margin, img.size[1] - th - margin
                    else:  # top-right
                        x, y = img.size[0] - tw - margin, margin

                    # 解析颜色
                    r, g, b = 255, 255, 255
                    alpha = int(opacity * 255)
                    if text_color.startswith('#') and len(text_color) >= 7:
                        r = int(text_color[1:3], 16)
                        g = int(text_color[3:5], 16)
                        b = int(text_color[5:7], 16)
                        if len(text_color) > 7:
                            alpha = int(text_color[7:9], 16) if text_color[7:9] else int(text_color[7], 16)

                    draw.text((x, y), text, fill=(r, g, b, alpha), font=font)

                watermarked = Image.alpha_composite(img, overlay)
                result = watermarked.convert('RGB')

                dest = os.path.join(output_dir, os.path.basename(img_path)) if output_dir else img_path
                fmt = img.format or 'JPEG'
                if fmt == 'PNG':
                    result.save(dest, 'PNG')
                else:
                    result.save(dest, 'JPEG', quality=95)
                processed += 1
        except Exception as e:
            echo(f'\n  ⚠️ {img_path}: {e}', fg='yellow')

    print(f'\n✅ 已添加水印: {processed}/{len(images)} 张', fg='green')


def cmd_convert_format(args):
    """批量转换格式"""
    src_dir = args['_pos'][0] if args.get('_pos') else ''
    from_fmt = args['_pos'][1] if len(args.get('_pos', [])) > 1 else ''
    to_fmt = args['_pos'][2] if len(args.get('_pos', [])) > 2 else ''
    to_ext_arg = args.get('to', '')
    output_dir = args.get('o', '')

    Image = ensure_pillow()
    if Image is None:
        sys.exit(1)

    images = scan_images(src_dir)

    # 确定目标格式
    target_ext = to_fmt.lower() if to_fmt else (to_ext_arg or 'jpg').lstrip('.')
    target_format = target_ext.upper().replace('JPG', 'JPEG').replace('TIF', 'TIFF')

    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    processed = 0
    for idx, img_path in enumerate(images):
        sys.stderr.write(f'\r  转换: {idx+1}/{len(images)}')
        sys.stderr.flush()
        try:
            with Image.open(img_path) as img:
                base_name = os.path.splitext(os.path.basename(img_path))[0]
                dest = os.path.join(output_dir, f'{base_name}.{target_ext}') if output_dir else \
                    os.path.join(os.path.dirname(img_path), f'{base_name}.{target_ext}')

                # 特殊处理：RGBA→RGB for JPEG
                if target_format == 'JPEG' and img.mode in ('RGBA', 'P', 'LA'):
                    bg = Image.new('RGB', img.size, (255, 255, 255))
                    if img.mode == 'P':
                        img = img.convert('RGBA')
                    if img.mode in ('RGBA', 'LA'):
                        bg.paste(img, mask=img.split()[-1])
                        img = bg
                    else:
                        img = img.convert('RGB')

                img.save(dest, format=target_format, quality=95)
                processed += 1
        except Exception as e:
            echo(f'\n  ⚠️ {img_path}: {e}', fg='yellow')

    print(f'\n✅ 格式转换: {processed}/{len(images)} → .{target_ext}', fg='green')


def cmd_crop(args):
    """裁剪图像"""
    src_dir = args['_pos'][0] if args.get('_pos') else ''
    left = int(args.get('left', 0))
    top = int(args.get('top', 0))
    width = int(args.get('width', 0))
    height = int(args.get('height', 0))
    center = args.get('center', False)  # 居中裁剪
    output_dir = args.get('o', '')

    Image = ensure_pillow()
    if Image is None:
        sys.exit(1)

    images = scan_images(src_dir)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    processed = 0
    for idx, img_path in enumerate(images):
        sys.stderr.write(f'\r  裁剪: {idx+1}/{len(images)}')
        sys.stderr.flush()
        try:
            with Image.open(img_path) as img:
                w, h = img.size
                if center and width and height:
                    left = (w - width) // 2
                    top = (h - height) // 2
                box = (left, top, min(left + width, w), min(top + height, h))
                cropped = img.crop(box)

                dest = os.path.join(output_dir, os.path.basename(img_path)) if output_dir else img_path
                cropped.save(dest)
                processed += 0
        except Exception as e:
            echo(f'\n  ⚠️ {img_path}: {e}', fg='yellow')

    print(f'\n✅ 裁剪完成: {processed}/{len(images)}', fg='green')


def cmd_rotate(args):
    """批量旋转"""
    src_dir = args['_pos'][0] if args.get('_pos') else ''
    angle = float(args.get('angle', 90))  # 角度或 auto
    output_dir = args.get('o', '')
    auto_exif = args.get('auto', False)

    Image = ensure_pillow()
    if Image is None:
        sys.exit(1)

    images = scan_images(src_dir)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    processed = 0
    for idx, img_path in enumerate(images):
        try:
            with Image.open(img_path) as img:
                if auto_exif:
                    rotated = img
                    for orientation_key in [274]:  # EXIF Orientation tag
                        if hasattr(img, '_getexif'):
                            exif = img._getexif()
                            if exif and orientation_key in exif:
                                rot_val = exif[orientation_key]
                                rotation_map = {
                                    3: 180, 6: 270, 8: 90,
                                    1: 0, 2: 0, 4: 180, 5: 270, 7: 90,
                                }
                                actual_angle = rotation_map.get(rot_val, 0)
                                rotated = img.rotate(actual_angle, expand=True)
                                break
                else:
                    expanded = angle % 180 != 0
                    rotated = img.rotate(angle, expand=expanded)

                dest = os.path.join(output_dir, os.path.basename(img_path)) if output_dir else img_path
                rotated.save(dest)
                processed += 1
        except Exception as e:
            echo(f'⚠️ {img_path}: {e}', fg='yellow')

    echo(f'✅ 旋转完成: {processed}/{len(images)}', fg='green')


def cmd_thumbnail(args):
    """生成缩略图"""
    src_dir = args['_pos'][0] if args.get('_pos') else ''
    size = int(args.get('size', 200))
    output_dir = args.get('o', './thumbnails')

    Image = ensure_pillow()
    if Image is None:
        sys.exit(1)

    images = scan_images(src_dir)
    os.makedirs(output_dir, exist_ok=True)

    processed = 0
    for idx, img_path in enumerate(images):
        sys.stderr.write(f'\r  缩略图: {idx+1}/{len(images)}')
        sys.stderr.flush()
        try:
            with Image.open(img_path) as img:
                img.thumbnail((size, size), Image.LANCZOS)
                base = os.path.splitext(os.path.basename(img_path))[0]
                dest = os.path.join(output_dir, f'{base}_thumb.jpg')
                img.convert('RGB').save(dest, 'JPEG', quality=85)
                processed += 1
        except Exception:
            pass

    print(f'\n✅ 生成 {processed} 个缩略图 → {output_dir}/', fg='green')


def cmd_grid_collage(args):
    """将多张图拼成网格/拼贴画"""
    src_dir = args['_pos'][0] if args.get('_pos') else ''
    cols = int(args.get('cols', 4))
    spacing = int(args.get('spacing', 5))
    bg_color = args.get('bg', '#ffffff')
    thumb_size = int(args.get('thumb_size', 300))
    output_file = args.get('o', 'collage.png')

    Image = ensure_pillow()
    if Image is None:
        sys.exit(1)

    images = scan_images(src_dir)

    # 加载并统一尺寸
    thumbs = []
    for img_path in images:
        try:
            with Image.open(img_path) as img:
                t = img.copy()
                t.thumbnail((thumb_size, thumb_size), Image.LANCZOS)
                thumbs.append(t)
        except Exception:
            pass

    if not thumbs:
        echo('❌ 无可用图像', fg='red')
        return

    n = len(thumbs)
    rows_count = (n + cols - 1) // cols

    cell_size = thumb_size + spacing
    canvas_w = cols * thumb_size + (cols + 1) * spacing
    canvas_h = rows_count * thumb_size + (rows_count + 1) * spacing

    # 解析背景色
    if bg_color.startswith('#'):
        r, g, b = int(bg_color[1:3], 16), int(bg_color[3:5], 16), int(bg_color[5:7], 16)
        bg = (r, g, b)
    else:
        bg = (255, 255, 255)

    canvas = Image.new('RGB', (canvas_w, canvas_h), bg)

    for idx, thumb in enumerate(thumbs):
        row = idx // cols
        col = idx % cols
        x = spacing + col * (thumb_size + spacing)
        y = spacing + row * (thumb_size + spacing)

        # 居中放置在单元格内
        offset_x = (thumb_size - thumb.width) // 2
        offset_y = (thumb_size - thumb.height) // 2

        paste_img = thumb.convert('RGB') if thumb.mode != 'RGB' else thumb
        canvas.paste(paste_img, (x + offset_x, y + offset_y))

    canvas.save(output_file, quality=95)
    echo(f'✅ 拼贴画已生成: {output_file} ({canvas_w}x{canvas_h}, {n}张图)', fg='green')


# ══════════════════════════════════════════════════════════════
#  主入口
# ══════════════════════════════════════════════════════════════

COMMANDS = {
    'info': cmd_info,
    'batch-resize': cmd_batch_resize,
    'resize': cmd_batch_resize,
    'compress': cmd_compress,
    'watermark': cmd_watermark,
    'convert': cmd_convert_format,
    'crop': cmd_crop,
    'rotate': cmd_rotate,
    'thumbnail': cmd_thumbnail,
    'grid': cmd_grid_collage,
}

ALIASES = {
    'ls': 'info', 'show': 'info',
    'scale': 'batch-resize',
    'optimize': 'compress', 'shrink': 'compress',
    'mark': 'watermark', 'stamp': 'watermark',
    'convert-format': 'convert',
    'cut': 'crop',
    'turn': 'rotate', 'auto-rotate': lambda a: (a.__setitem__('auto', True), cmd_rotate(a))[1],
    'thumb': 'thumbnail', 'preview': 'thumbnail',
    'collage': 'grid', 'mosaic': 'grid',
}


def main():
    args = parse_args()
    cmd = args['_cmd']
    cmd = ALIASES.get(cmd, cmd)

    if cmd not in COMMANDS:
        available = ', '.join(sorted(set(list(COMMANDS.keys()) + [k for k, v in ALIASES.items() if k in COMMANDS])))
        echo(f'❌ 未知命令: {cmd}', fg='red')
        echo(f'可用命令: {available}', fg='cyan')
        sys.exit(1)

    COMMANDS[cmd](args)


if __name__ == '__main__':
    main()
