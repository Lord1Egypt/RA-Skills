#!/usr/bin/env python3
"""
文件格式转换工具
支持图片格式转换、文档格式转换等
"""

import os
from pathlib import Path
from typing import List, Optional, Tuple
import sys


class FormatConverter:
    """文件格式转换器"""

    def __init__(self, dry_run: bool = False):
        self.dry_run = dry_run
        self.convert_operations = []

    def convert_images(
        self,
        directory: str,
        target_format: str,
        files: Optional[List[str]] = None,
        quality: int = 95,
        keep_original: bool = True
    ):
        """
        转换图片格式
        支持: JPG, PNG, WEBP, BMP, TIFF 等
        """
        try:
            from PIL import Image
        except ImportError:
            raise ImportError(
                "Pillow library required. Install with: pip install Pillow"
            )

        dir_path = Path(directory)
        file_list = self._get_file_list(dir_path, files, extensions=[".jpg", ".jpeg", ".png", ".webp", ".bmp", ".tiff", ".tif"])

        # 标准化目标格式
        target_format = target_format.lower().lstrip(".")

        for file_path in file_list:
            if file_path.suffix.lower().lstrip(".") == target_format:
                print(f"⚠️  Skip: {file_path.name} already in target format")
                continue

            new_name = f"{file_path.stem}.{target_format}"
            new_path = dir_path / new_name

            self.convert_operations.append({
                "type": "image",
                "source": file_path,
                "target": new_path,
                "quality": quality
            })

    def convert_pdf_to_images(
        self,
        pdf_path: str,
        output_dir: str,
        format: str = "png",
        dpi: int = 300
    ):
        """
        将 PDF 转换为图片
        支持: PNG, JPG
        """
        try:
            from pdf2image import convert_from_path
        except ImportError:
            raise ImportError(
                "pdf2image library required. Install with: pip install pdf2image"
            )

        pdf_file = Path(pdf_path)
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        self.convert_operations.append({
            "type": "pdf_to_image",
            "source": pdf_file,
            "output_dir": output_path,
            "format": format,
            "dpi": dpi
        })

    def convert_images_to_pdf(
        self,
        directory: str,
        output_pdf: str,
        files: Optional[List[str]] = None,
        sort: bool = True
    ):
        """
        将图片转换为 PDF
        """
        try:
            from PIL import Image
        except ImportError:
            raise ImportError(
                "Pillow library required. Install with: pip install Pillow"
            )

        dir_path = Path(directory)
        file_list = self._get_file_list(dir_path, files, extensions=[".jpg", ".jpeg", ".png", ".webp", ".bmp"])

        if sort:
            file_list = sorted(file_list, key=lambda x: x.name)

        self.convert_operations.append({
            "type": "images_to_pdf",
            "sources": file_list,
            "target": Path(output_pdf)
        })

    def convert_docx_to_pdf(
        self,
        docx_path: str,
        output_pdf: str
    ):
        """
        将 DOCX 转换为 PDF
        """
        try:
            from docx2pdf import convert
        except ImportError:
            raise ImportError(
                "docx2pdf library required. Install with: pip install docx2pdf"
            )

        self.convert_operations.append({
            "type": "docx_to_pdf",
            "source": Path(docx_path),
            "target": Path(output_pdf)
        })

    def convert_markdown_to_pdf(
        self,
        md_path: str,
        output_pdf: str
    ):
        """
        将 Markdown 转换为 PDF
        """
        try:
            from markdown import markdown
            from weasyprint import HTML
        except ImportError:
            raise ImportError(
                "markdown and weasyprint libraries required. Install with: pip install markdown weasyprint"
            )

        self.convert_operations.append({
            "type": "md_to_pdf",
            "source": Path(md_path),
            "target": Path(output_pdf)
        })

    def _get_file_list(
        self,
        directory: Path,
        files: Optional[List[str]],
        extensions: List[str]
    ) -> List[Path]:
        """获取文件列表"""
        if files:
            return [directory / f for f in files if (directory / f).exists()]
        else:
            return [
                f for f in directory.iterdir()
                if f.is_file() and f.suffix.lower() in extensions
            ]

    def execute(self):
        """执行转换操作"""
        if not self.convert_operations:
            print("No files to convert")
            return

        print(f"\n{'='*60}")
        print(f"{'DRY RUN' if self.dry_run else 'EXECUTE'}: {len(self.convert_operations)} conversion operations")
        print(f"{'='*60}\n")

        # 显示操作预览
        for idx, op in enumerate(self.convert_operations, 1):
            if op["type"] == "image":
                print(f"{idx}. Image: {op['source'].name} -> {op['target'].name}")
            elif op["type"] == "pdf_to_image":
                print(f"{idx}. PDF to Images: {op['source'].name} -> {op['output_dir']}/")
            elif op["type"] == "images_to_pdf":
                print(f"{idx}. Images to PDF: {len(op['sources'])} images -> {op['target'].name}")
            elif op["type"] == "docx_to_pdf":
                print(f"{idx}. DOCX to PDF: {op['source'].name} -> {op['target'].name}")
            elif op["type"] == "md_to_pdf":
                print(f"{idx}. Markdown to PDF: {op['source'].name} -> {op['target'].name}")

        if self.dry_run:
            print("\n🔍 Dry run complete. No files were converted.")
            return

        print("\n⚙️  Executing conversions...")

        # 执行转换
        for op in self.convert_operations:
            try:
                self._execute_single_operation(op)
            except Exception as e:
                print(f"❌ Error: {e}")
                continue

        print(f"\n✅ Conversion complete")

    def _execute_single_operation(self, op: dict):
        """执行单个转换操作"""
        from PIL import Image

        if op["type"] == "image":
            # 图片格式转换
            img = Image.open(op["source"])
            img.save(
                op["target"],
                format=op["target"].suffix[1:].upper(),
                quality=op["quality"],
                optimize=True
            )
            print(f"✅ Converted: {op['source'].name} -> {op['target'].name}")

        elif op["type"] == "pdf_to_image":
            # PDF 转图片
            from pdf2image import convert_from_path
            images = convert_from_path(str(op["source"]), dpi=op["dpi"])
            for idx, img in enumerate(images, 1):
                output_path = op["output_dir"] / f"{op['source'].stem}_{idx:03d}.{op['format']}"
                img.save(output_path, format=op["format"].upper())
            print(f"✅ Converted PDF: {op['source'].name} -> {len(images)} images")

        elif op["type"] == "images_to_pdf":
            # 图片转 PDF
            images = [Image.open(img).convert("RGB") for img in op["sources"]]
            images[0].save(op["target"], save_all=True, append_images=images[1:])
            print(f"✅ Converted: {len(op['sources'])} images -> {op['target'].name}")

        elif op["type"] == "docx_to_pdf":
            # DOCX 转 PDF
            from docx2pdf import convert
            convert(str(op["source"]), str(op["target"]))
            print(f"✅ Converted: {op['source'].name} -> {op['target'].name}")

        elif op["type"] == "md_to_pdf":
            # Markdown 转 PDF
            from markdown import markdown
            from weasyprint import HTML

            with open(op["source"], "r", encoding="utf-8") as f:
                md_content = f.read()

            html_content = markdown(md_content)
            HTML(string=html_content).write_pdf(str(op["target"]))
            print(f"✅ Converted: {op['source'].name} -> {op['target'].name}")


def main():
    """命令行入口"""
    import argparse

    parser = argparse.ArgumentParser(description="文件格式转换工具")
    parser.add_argument("--dry-run", action="store_true", help="预览模式,不实际执行")

    subparsers = parser.add_subparsers(dest="operation", help="操作类型")

    # 图片格式转换
    image_parser = subparsers.add_parser("images", help="转换图片格式")
    image_parser.add_argument("directory", help="图片目录")
    image_parser.add_argument("format", help="目标格式 (png/jpg/webp/bmp/tiff)")
    image_parser.add_argument("--quality", type=int, default=95, help="图片质量 (1-100)")
    image_parser.add_argument("--no-keep-original", action="store_true", help="不保留原文件")

    # PDF 转图片
    pdf_to_img_parser = subparsers.add_parser("pdf-to-images", help="PDF转图片")
    pdf_to_img_parser.add_argument("pdf_path", help="PDF文件路径")
    pdf_to_img_parser.add_argument("output_dir", help="输出目录")
    pdf_to_img_parser.add_argument("--format", default="png", help="输出格式 (png/jpg)")
    pdf_to_img_parser.add_argument("--dpi", type=int, default=300, help="DPI")

    # 图片转 PDF
    img_to_pdf_parser = subparsers.add_parser("images-to-pdf", help="图片转PDF")
    img_to_pdf_parser.add_argument("directory", help="图片目录")
    img_to_pdf_parser.add_argument("output_pdf", help="输出PDF路径")
    img_to_pdf_parser.add_argument("--no-sort", action="store_true", help="不按名称排序")

    # DOCX 转 PDF
    docx_to_pdf_parser = subparsers.add_parser("docx-to-pdf", help="DOCX转PDF")
    docx_to_pdf_parser.add_argument("docx_path", help="DOCX文件路径")
    docx_to_pdf_parser.add_argument("output_pdf", help="输出PDF路径")

    # Markdown 转 PDF
    md_to_pdf_parser = subparsers.add_parser("md-to-pdf", help="Markdown转PDF")
    md_to_pdf_parser.add_argument("md_path", help="Markdown文件路径")
    md_to_pdf_parser.add_argument("output_pdf", help="输出PDF路径")

    args = parser.parse_args()

    if not args.operation:
        parser.print_help()
        return

    converter = FormatConverter(dry_run=args.dry_run)

    # 执行操作
    if args.operation == "images":
        converter.convert_images(
            args.directory,
            args.format,
            quality=args.quality,
            keep_original=not args.no_keep_original
        )
    elif args.operation == "pdf-to-images":
        converter.convert_pdf_to_images(
            args.pdf_path,
            args.output_dir,
            format=args.format,
            dpi=args.dpi
        )
    elif args.operation == "images-to-pdf":
        converter.convert_images_to_pdf(
            args.directory,
            args.output_pdf,
            sort=not args.no_sort
        )
    elif args.operation == "docx-to-pdf":
        converter.convert_docx_to_pdf(args.docx_path, args.output_pdf)
    elif args.operation == "md-to-pdf":
        converter.convert_markdown_to_pdf(args.md_path, args.output_pdf)

    converter.execute()


if __name__ == "__main__":
    main()
