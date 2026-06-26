#!/usr/bin/env python3
"""
PDF Converter - PDF 转换脚本
支持: PDF转图片、图片合并为PDF、PDF拆分/合并

依赖:
  pip install Pillow PyMuPDF (fitz)
  # 或
  pip install Pillow pdf2image

用法:
  python convert_pdf.py <command> [args]
  
命令:
  to-image     PDF 转图片
  from-image   图片合并为 PDF
  merge        合并多个 PDF
  split        拆分 PDF 为单页
  info         查看 PDF 信息
  
示例:
  python convert_pdf.py to-image document.pdf --format png --dpi 200
  python convert_pdf.py from-image ./photos/ output.pdf
  python convert_pdf.py merge part1.pdf part2.pdf -o merged.pdf
  python convert_pdf.py split document.pdf --output-dir ./pages/
"""

import argparse
import os
import sys
from pathlib import Path
from typing import Optional, List, Tuple

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    print("错误: 需要安装 Pillow 库")
    print("请执行: pip install Pillow PyMuPDF")
    sys.exit(1)

# 尝试导入 fitz (PyMuPDF)，优先使用（性能更好）
try:
    import fitz  # PyMuPDF
    HAS_FITZ = True
except ImportError:
    HAS_FITZ = False

# 备用方案: pdf2image
try:
    from pdf2image import convert_from_path as pdf2img_convert
    HAS_PDF2IMAGE = True
except ImportError:
    HAS_PDF2IMAGE = False


def _format_size(size_bytes: int) -> str:
    """格式化文件大小"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024:
            return f'{size_bytes:.1f} {unit}'
        size_bytes /= 1024
    return f'{size_bytes:.1f} TB'


def pdf_to_images(
    pdf_path: str,
    output_dir: str,
    fmt: str = 'png',
    dpi: int = 200,
    page_range: Optional[Tuple[int, int]] = None,
    first_page_only: bool = False,
    quality: int = 85,
) -> List[dict]:
    """将 PDF 转换为图片"""
    
    pdf_path = Path(pdf_path)
    if not pdf_path.exists():
        return [{'success': False, 'error': f'文件不存在: {pdf_path}'}]
    
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    results = []
    
    if HAS_FITZ:
        # 使用 PyMuPDF (更快更准确)
        doc = fitz.open(str(pdf_path))
        
        total_pages = len(doc)
        start_page = (page_range[0] - 1) if page_range else 0
        end_page = (page_range[1]) if page_range else total_pages
        
        if first_page_only:
            end_page = min(start_page + 1, total_pages)
        
        for i in range(start_page, min(end_page, total_pages)):
            page = doc[i]
            
            # 根据格式选择渲染方式
            if fmt.lower() in ('jpg', 'jpeg'):
                mat = fitz.Matrix(dpi / 72, dpi / 72)
                pix = page.get_pixmap(matrix=mat, alpha=False)
                img_data = pix.tobytes('jpeg')
            else:
                mat = fitz.Matrix(dpi / 72, dpi / 72)
                pix = page.get_pixmap(matrix=mat, alpha=(fmt.lower() == 'png'))
                img_data = pix.tobytes(fmt.lower())
            
            # 构建输出文件名
            base_name = pdf_path.stem
            if total_pages > 1 or not first_page_only:
                output_name = f"{base_name}_page{i+1}.{fmt.lower()}"
            else:
                output_name = f"{base_name}.{fmt.lower()}"
            
            output_path = output_dir / output_name
            
            with open(output_path, 'wb') as f:
                f.write(img_data)
            
            file_size = output_path.stat().st_size
            results.append({
                'success': True,
                'page': i + 1,
                'output_path': str(output_path),
                'size': file_size,
                'size_human': _format_size(file_size),
                'dimensions': (pix.width, pix.height),
            })
        
        doc.close()
    
    elif HAS_PDF2IMAGE:
        # 使用 pdf2image 作为备选
        kwargs = {
            'dpi': dpi,
            'fmt': fmt.upper(),
        }
        if page_range:
            kwargs['first_page'] = page_range[0]
            kwargs['last_page'] = page_range[1]
        
        images = pdf2img_convert(str(pdf_path), **kwargs)
        
        base_name = pdf_path.stem
        for i, img in enumerate(images):
            output_name = f"{base_name}_page{i+1}.{fmt.lower()}" if len(images) > 1 else f"{base_name}.{fmt.lower()}"
            output_path = output_dir / output_name
            
            save_kwargs = {}
            if fmt.lower() in ('jpg', 'jpeg'):
                save_kwargs['quality'] = quality
            
            img.save(str(output_path), **save_kwargs)
            
            file_size = output_path.stat().st_size
            results.append({
                'success': True,
                'page': i + 1,
                'output_path': str(output_path),
                'size': file_size,
                'size_human': _format_size(file_size),
                'dimensions': img.size,
            })
    else:
        return [{
            'success': False,
            'error': '需要安装 PDF 处理库。请执行: pip install PyMuPDF 或 pip install pdf2image'
        }]
    
    return results


def images_to_pdf(
    input_paths: List[str] | str,
    output_path: str,
    sort_by_name: bool = True,
    image_quality: int = 85,
    page_size: Optional[Tuple[float, float]] = None,
) -> dict:
    """
    将图片合并为 PDF
    
    Args:
        input_paths: 图片路径列表或包含图片的目录
        output_path: 输出 PDF 路径
        sort_by_name: 是否按名称排序
        image_quality: 图片质量（仅对 JPG 格式有效）
        page_size: 自定义页面大小 (宽, 高)，单位英寸，如 (8.5, 11) 为 Letter
    """
    
    # 如果传入目录，收集其中所有图片
    if isinstance(input_paths, str):
        input_dir = Path(input_paths)
        if input_dir.is_dir():
            supported_exts = {'.png', '.jpg', '.jpeg', '.webp', '.gif', '.bmp', '.tiff'}
            paths = []
            for ext in supported_exts:
                paths.extend(input_dir.glob(f'*{ext}'))
                paths.extend(input_dir.glob(f'*{ext.upper()}'))
            input_paths = [str(p) for p in sorted(paths)]
        else:
            input_paths = [input_paths]
    
    if not input_paths:
        return {'success': False, 'error': '没有找到图片文件'}
    
    if sort_by_name:
        input_paths = sorted(input_paths, key=lambda x: Path(x).name.lower())
    
    images = []
    valid_paths = []
    
    for path_str in input_paths:
        path = Path(path_str)
        if not path.exists():
            continue
        try:
            img = Image.open(path)
            # RGB 模式转换
            if img.mode not in ('RGB', 'L'):
                if img.mode == 'RGBA':
                    # 创建白色背景
                    background = Image.new('RGB', img.size, (255, 255, 255))
                    background.paste(img, mask=img.split()[3])
                    img = background
                elif img.mode == 'P' and 'transparency' in img.info:
                    img = img.convert('RGBA')
                    background = Image.new('RGB', img.size, (255, 255, 255))
                    background.paste(img, mask=img.split()[3])
                    img = background
                else:
                    img = img.convert('RGB')
            images.append(img)
            valid_paths.append(path)
        except Exception as e:
            print(f"警告: 无法打开 {path}: {e}")
    
    if not images:
        return {'success': False, 'error': '没有有效的图片可以转换'}
    
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # 确定页面大小
    if page_size:
        page_width, page_height = page_size
    else:
        # 使用第一张图片的尺寸作为默认
        page_width = images[0].width / 72  # 转换为英寸
        page_height = images[0].height / 72
    
    # 创建 PDF
    try:
        images[0].save(
            str(output_path),
            'PDF',
            resolution=100.0,
            save_all=True,
            append_images=images[1:] if len(images) > 1 else [],
        )
        
        file_size = output_path.stat().st_size
        
        return {
            'success': True,
            'output_path': str(output_path),
            'pages_count': len(valid_paths),
            'size': file_size,
            'size_human': _format_size(file_size),
            'images': [str(p) for p in valid_paths],
        }
    except Exception as e:
        return {'success': False, 'error': str(e)}


def merge_pdfs(
    input_pdfs: List[str],
    output_path: str,
    bookmarks: bool = True,
) -> dict:
    """合并多个 PDF 文件"""
    
    if HAS_FITZ:
        merged_doc = fitz.open()
        
        for pdf_path in input_pdfs:
            path = Path(pdf_path)
            if not path.exists():
                continue
            
            doc = fitz.open(str(path))
            merged_doc.insert_pdf(doc)
            
            if bookmarks:
                # 添加书签
                toc_item = [1, path.stem, len(merged_doc) - len(doc)]
                merged_doc.set_toc([toc_item])
            
            doc.close()
        
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        merged_doc.save(str(output_path))
        merged_doc.close()
        
        return {
            'success': True,
            'output_path': str(output_path),
            'size_human': _format_size(output_path.stat().st_size),
        }
    else:
        return {
            'success': False,
            'error': 'PDF 合并功能需要 PyMuPDF 库。请执行: pip install PyMuPDF'
        }


def split_pdf(
    pdf_path: str,
    output_dir: str,
    page_ranges: Optional[List[Tuple[int, int]]] = None,
) -> List[dict]:
    """拆分 PDF"""
    
    if not HAS_FITZ:
        return [{
            'success': False,
            'error': 'PDF 拆分功能需要 PyMuPDF 库。请执行: pip install PyMuPDF'
        }]
    
    pdf_path = Path(pdf_path)
    if not pdf_path.exists():
        return [{'success': False, 'error': f'文件不存在: {pdf_path}'}]
    
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    doc = fitz.open(str(pdf_path))
    results = []
    
    if page_ranges:
        # 按指定范围拆分
        for idx, (start, end) in enumerate(page_ranges):
            new_doc = fitz.new()
            new_doc.insert_pdf(doc, from_page=start-1, to_page=end-1)
            
            output_name = f"{pdf_path.stem}_{idx+1}.pdf"
            output_path = output_dir / output_name
            new_doc.save(str(output_path))
            new_doc.close()
            
            results.append({
                'success': True,
                'output_path': str(output_path),
                'pages': f"{start}-{end}",
                'size_human': _format_size(output_path.stat().st_size),
            })
    else:
        # 每页单独拆分
        for i in range(len(doc)):
            new_doc = fitz.new()
            new_doc.insert_pdf(doc, from_page=i, to_page=i)
            
            output_name = f"{pdf_path.stem}_page{i+1}.pdf"
            output_path = output_dir / output_name
            new_doc.save(str(output_path))
            new_doc.close()
            
            results.append({
                'success': True,
                'output_path': str(output_path),
                'pages': f"第 {i+1} 页",
                'size_human': _format_size(output_path.stat().st_size),
            })
    
    doc.close()
    return results


def get_pdf_info(pdf_path: str) -> dict:
    """获取 PDF 详细信息"""
    
    pdf_path = Path(pdf_path)
    if not pdf_path.exists():
        return {'success': False, 'error': f'文件不存在: {pdf_path}'}
    
    stat = pdf_path.stat()
    
    result = {
        'filename': pdf_path.name,
        'size': stat.st_size,
        'size_human': _format_size(stat.st_size),
    }
    
    if HAS_FITZ:
        doc = fitz.open(str(pdf_path))
        result['success'] = True
        result['pages'] = len(doc)
        result['title'] = doc.metadata.get('title', '')
        result['author'] = doc.metadata.get('author', '')
        result['creator'] = doc.metadata.get('creator', '')
        
        # 计算每页尺寸
        first_page = doc[0]
        rect = first_page.rect
        result['page_width'] = round(rect.width, 2)
        result['page_height'] = round(rect.height, 2)
        
        # 判断纸张类型
        w, h = rect.width, rect.height
        if (abs(w - 595) < 10 and abs(h - 842) < 10) or (abs(w - 612) < 10 and abs(h - 792) < 10):
            result['paper'] = 'A4/Letter'
        else:
            result['paper'] = f'{w:.0f}x{h:.0f} pt'
        
        doc.close()
    else:
        result['success'] = True
        result['note'] = '安装 PyMuPDF 可获取更多信息: pip install PyMuPDF'
    
    return result


def main():
    parser = argparse.ArgumentParser(
        description='PDF 转换工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
示例:
  %(prog)s to-image document.pdf --format png --dpi 300
  %(prog)s to-image report.pdf --first-page --quality 95
  %(prog)s from-image ./photos/ output.pdf
  %(prog)s from-image img1.png img2.jpg img3.webp merged.pdf
  %(prog)s merge a.pdf b.pdf c.pdf -o complete.pdf
  %(prog)s split document.pdf --output-dir ./pages/
  %(prog)s info document.pdf
'''
    )
    
    subparsers = parser.add_subparsers(dest='command', help='可用命令')
    
    # to-image 子命令
    p_to_img = subparsers.add_parser('to-image', help='PDF 转图片')
    p_to_img.add_argument('input', help='输入 PDF 文件路径')
    p_to_img.add_argument('--output-dir', '-o', default='.', help='输出目录（默认当前目录）')
    p_to_img.add_argument('--format', '-f', choices=['png', 'jpg', 'jpeg', 'webp'], default='png',
                          help='输出图片格式（默认png）')
    p_to_img.add_argument('--dpi', '-d', type=int, default=200, help='分辨率 DPI（默认200）')
    p_to_img.add_argument('--pages', '-p', metavar='M-N', help='页码范围，如 1-5')
    p_to_img.add_argument('--first-page', action='store_true', help='仅转换第一页')
    p_to_img.add_argument('--quality', '-q', type=int, default=85, help='JPG/WebP 质量 (1-100)')
    
    # from-image 子命令
    p_from_img = subparsers.add_parser('from-image', help='图片合并为 PDF')
    p_from_img.add_argument('inputs', nargs='+', help='图片路径或目录')
    p_from_img.add_argument('output', help='输出 PDF 路径')
    p_from_img.add_argument('--no-sort', action='store_true', help='不按名称排序')
    p_from_img.add_argument('--quality', '-q', type=int, default=85, help='图片质量')
    p_from_img.add_argument('--page-size', metavar='WxH', help='页面大小(英寸)，如 8.5x11')
    
    # merge 子命令
    p_merge = subparsers.add_parser('merge', help='合并多个 PDF')
    p_merge.add_argument('inputs', nargs='+', help='要合并的 PDF 文件')
    p_merge.add_argument('-o', '--output', required=True, help='输出文件路径')
    p_merge.add_argument('--no-bookmarks', action='store_true', help='不添加书签')
    
    # split 子命令
    p_split = subparsers.add_parser('split', help='拆分 PDF')
    p_split.add_argument('input', help='输入 PDF 文件路径')
    p_split.add_argument('--output-dir', '-o', default='./split_output/', help='输出目录')
    p_split.add_argument('--ranges', '-r', nargs='+', metavar='M-N', help='页码范围，如 1-3 5-7')
    
    # info 子命令
    p_info = subparsers.add_parser('info', help='查看 PDF 信息')
    p_info.add_argument('input', help='输入 PDF 文件路径')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(0)
    
    if args.command == 'to-image':
        page_range = None
        if args.pages:
            parts = args.pages.split('-')
            page_range = (int(parts[0]), int(parts[1]))
        
        results = pdf_to_images(
            args.input,
            args.output_dir,
            fmt=args.format,
            dpi=args.dpi,
            page_range=page_range,
            first_page_only=args.first_page,
            quality=args.quality,
        )
        
        success = sum(1 for r in results if r.get('success'))
        print(f'\n转换完成: {success}/{len(results)} 页')
        for r in results:
            if r.get('success'):
                print(f"  ✓ 第 {r['page']} 页 → {Path(r['output_path']).name} ({r['size_human']})")
            else:
                print(f"  ✗ 错误: {r.get('error')}")
    
    elif args.command == 'from-image':
        page_size = None
        if getattr(args, 'page_size', None):
            parts = args.page_size.split('x')
            page_size = (float(parts[0]), float(parts[1]))
        
        result = images_to_pdf(
            args.inputs,
            args.output,
            sort_by_name=not getattr(args, 'no_sort', False),
            image_quality=getattr(args, 'quality', 85),
            page_size=page_size,
        )
        
        if result.get('success'):
            print(f"\n✓ PDF 已生成: {result['output_path']}")
            print(f"  共 {result['pages_count']} 页，大小: {result['size_human']}")
        else:
            print(f"\n✗ 错误: {result.get('error')}")
    
    elif args.command == 'merge':
        result = merge_pdfs(
            args.inputs,
            args.output,
            bookmarks=not args.no_bookmarks,
        )
        
        if result.get('success'):
            print(f"\n✓ PDF 已合并: {result['output_path']}")
            print(f"  大小: {result['size_human']}")
        else:
            print(f"\n✗ 错误: {result.get('error')}")
    
    elif args.command == 'split':
        ranges = None
        if args.ranges:
            ranges = []
            for r in args.ranges:
                parts = r.split('-')
                ranges.append((int(parts[0]), int(parts[1])))
        
        results = split_pdf(args.input, args.output_dir, ranges)
        
        success = sum(1 for r in results if r.get('success'))
        print(f"\n拆分完成: {success}/{len(results)} 个文件")
        for r in results:
            if r.get('success'):
                print(f"  ✓ {r['pages']:>15s} → {Path(r['output_path']).name} ({r['size_human']})")
            else:
                print(f"  ✗ 错误: {r.get('error')}")
    
    elif args.command == 'info':
        info = get_pdf_info(args.input)
        if info.get('success'):
            print(f"\n{'='*50}")
            print(f"文件: {info['filename']}")
            print(f"大小: {info['size_human']}")
            if 'pages' in info:
                print(f"页数: {info['pages']}")
            if 'page_width' in info:
                print(f"页面: {info['page_width']} x {info['page_height']} pt ({info['paper']})")
            if info.get('title'):
                print(f"标题: {info['title']}")
            if info.get('author'):
                print(f"作者: {info['author']}")
            print('='*50)
        else:
            print(f"错误: {info.get('error')}")


if __name__ == '__main__':
    main()
