#!/usr/bin/env python3
"""
CAD批量处理
功能：批量转PDF、批量重命名、自动备份、添加水印
"""

import os
import sys
import shutil
import subprocess
from typing import List, Tuple

def batch_rename(folder_path: str, prefix: str, start_num: int = 1):
    """批量重命名"""
    count = 0
    files = sorted([f for f in os.listdir(folder_path) if f.lower().endswith(('.dwg', '.dxf'))])
    
    for f in files:
        ext = os.path.splitext(f)[1]
        new_name = f"{prefix}_{start_num + count:03d}{ext}"
        old_path = os.path.join(folder_path, f)
        new_path = os.path.join(folder_path, new_name)
        os.rename(old_path, new_path)
        print(f"✅ {f} → {new_name}")
        count += 1
    
    print(f"\n📊 总计重命名: {count} 个文件")
    return count

def auto_backup(folder_path: str, backup_folder: str = None):
    """自动备份整个文件夹"""
    if backup_folder is None:
        backup_folder = os.path.join(os.path.dirname(folder_path), f"{os.path.basename(folder_path)}_backup")
    
    os.makedirs(backup_folder, exist_ok=True)
    count = 0
    
    for root, dirs, files in os.walk(folder_path):
        for f in files:
            if f.lower().endswith(('.dwg', '.dxf', '.pdf')):
                src = os.path.join(root, f)
                # 保持相对路径
                rel_path = os.path.relpath(src, folder_path)
                dst = os.path.join(backup_folder, rel_path)
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                shutil.copy2(src, dst)
                count += 1
                print(f"✅ 备份: {rel_path}")
    
    print(f"\n📊 总计备份: {count} 个文件到 {backup_folder}")
    return count

def add_watermark_to_pdf(input_pdf: str, output_pdf: str, watermark_text: str = "温州隐室空间设计"):
    """给PDF添加水印（需要PyPDF2和reportlab）"""
    try:
        from PyPDF2 import PdfReader, PdfWriter
        from reportlab.pdfgen import canvas
        from reportlab.lib.pagesizes import letter
        import io
        
        packet = io.BytesIO()
        can = canvas.Canvas(packet, pagesize=letter)
        can.setFont("Helvetica", 50)
        can.setFillColorRGB(0.8, 0.8, 0.8, 0.3)
        can.rotate(45)
        can.drawString(300, 100, watermark_text)
        can.save()
        
        packet.seek(0)
        watermark = PdfReader(packet)
        existing_pdf = PdfReader(open(input_pdf, "rb"))
        output = PdfWriter()
        
        for page in existing_pdf.pages:
            page.merge_page(watermark.pages[0])
            output.add_page(page)
        
        with open(output_pdf, "wb") as f:
            output.write(f)
        
        print(f"✅ 水印添加完成: {output_pdf}")
        return True
    except ImportError:
        print("⚠️ 需要安装依赖: pip install PyPDF2 reportlab")
        return False

def batch_export_pdf(input_folder: str, output_folder: str, add_watermark: bool = False, watermark_text: str = "温州隐室空间设计"):
    """
    批量导出PDF
    注意：需要AutoCAD/LibreCAD/DwgSee支持命令行转换
    这里封装通用框架，可根据实际CAD软件调整
    """
    os.makedirs(output_folder, exist_ok=True)
    count = 0
    dxf_files = [f for f in os.listdir(input_folder) if f.lower().endswith('.dxf')]
    
    print(f"找到 {len(dxf_files)} 个DXF文件需要导出PDF")
    print("提示: 导出PDF需要本地CAD软件支持，可通过以下方式之一：")
    print("  1. AutoCAD 命令行: /Applications/Autodesk/AutoCAD.app/Contents/MacOS/AutoCAD")
    print("  2. LibreCAD: librecad --export")
    
    for f in dxf_files:
        base_name = os.path.splitext(f)[0]
        input_path = os.path.join(input_folder, f)
        output_path = os.path.join(output_folder, f"{base_name}.pdf")
        
        # 这里留空，实际转换命令根据你本地CAD调整
        # 示例：librecad --export-format pdf --output $output_path $input_path
        print(f"📝 待转换: {input_path} → {output_path}")
        count += 1
    
    print(f"\n📊 准备转换 {count} 个文件")
    return count


def main():
    if len(sys.argv) < 2:
        print("""
CAD批量处理工具

Usage:
  1. 批量重命名:
     python batch_export.py rename <folder> <prefix> [start_num]

  2. 自动备份:
     python batch_export.py backup <source_folder> [backup_folder]

  3. 添加水印到PDF:
     python batch_export.py watermark <input.pdf> <output.pdf> [watermark_text]

  4. 批量导出PDF:
     python batch_export.py pdf <input_folder> <output_folder> [--watermark]
""")
        sys.exit(1)
    
    mode = sys.argv[1]
    
    if mode == "rename":
        folder = sys.argv[2]
        prefix = sys.argv[3]
        start = int(sys.argv[4]) if len(sys.argv) > 4 else 1
        batch_rename(folder, prefix, start)
    elif mode == "backup":
        source = sys.argv[2]
        backup = sys.argv[3] if len(sys.argv) > 3 else None
        auto_backup(source, backup)
    elif mode == "watermark":
        input_pdf = sys.argv[2]
        output_pdf = sys.argv[3]
        text = sys.argv[4] if len(sys.argv) > 4 else "温州隐室空间设计"
        add_watermark_to_pdf(input_pdf, output_pdf, text)
    elif mode == "pdf":
        input_folder = sys.argv[2]
        output_folder = sys.argv[3]
        do_watermark = len(sys.argv) > 4 and sys.argv[4] == "--watermark"
        batch_export_pdf(input_folder, output_folder, do_watermark)
    else:
        print(f"❌ 未知模式: {mode}")
        sys.exit(1)


if __name__ == "__main__":
    main()
