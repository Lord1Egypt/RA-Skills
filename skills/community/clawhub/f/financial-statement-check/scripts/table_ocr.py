#!/usr/bin/env python3
"""
Tencent Cloud Table OCR (High Precision) - RecognizeTableAccurateOCR

Extracts structured table data from financial statement PDF/images.
Requires env vars: TENCENTCLOUD_SECRET_ID, TENCENTCLOUD_SECRET_KEY

Usage:
    # Single image
    python table_ocr.py --image-url <url>
    python table_ocr.py --image-base64 <base64_or_filepath>

    # PDF with built-in page rendering (requires PyMuPDF)
    python table_ocr.py --pdf /path/to/report.pdf --pdf-pages 6,7,8,9
    python table_ocr.py --pdf /path/to/report.pdf --pdf-pages 1

Note:
    RecognizeTableAccurateOCR does NOT support IsPdf/PdfPageNumber params.
    PDF files are converted to PNG images internally via PyMuPDF before OCR.
"""

import argparse
import base64
import io
import json
import os
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed

# SDK max image size limit (10MB)
MAX_IMAGE_SIZE_BYTES = 10 * 1024 * 1024
# Default DPI for PDF→PNG rendering
DEFAULT_PDF_DPI = 200
# Max parallel OCR workers
MAX_OCR_WORKERS = 4


def validate_env() -> tuple:
    """Validate and return Tencent Cloud API credentials."""
    secret_id = os.environ.get("TENCENTCLOUD_SECRET_ID")
    secret_key = os.environ.get("TENCENTCLOUD_SECRET_KEY")
    if not secret_id or not secret_key:
        print(
            "错误: 请设置环境变量 TENCENTCLOUD_SECRET_ID 和 TENCENTCLOUD_SECRET_KEY",
            file=sys.stderr,
        )
        sys.exit(1)
    return secret_id, secret_key


def load_image_base64(value: str) -> str:
    """
    Load Base64 image content.
    If value is an existing file path, read and encode the file;
    otherwise treat it as a Base64 string directly.
    """
    if os.path.isfile(value):
        with open(value, "rb") as f:
            raw = f.read()
        # If file content is already Base64 text, use directly
        try:
            raw_str = raw.decode("utf-8").strip()
            base64.b64decode(raw_str, validate=True)
            return raw_str
        except (UnicodeDecodeError, ValueError):
            pass
        # Otherwise encode binary file to Base64
        if len(raw) > MAX_IMAGE_SIZE_BYTES:
            print(
                f"错误: 文件大小超过 {MAX_IMAGE_SIZE_BYTES // (1024 * 1024)}MB 限制",
                file=sys.stderr,
            )
            sys.exit(1)
        return base64.b64encode(raw).decode("utf-8")
    else:
        # Treat as Base64 string directly
        try:
            decoded = base64.b64decode(value, validate=True)
            if len(decoded) > MAX_IMAGE_SIZE_BYTES:
                print(
                    f"错误: 图片大小超过 {MAX_IMAGE_SIZE_BYTES // (1024 * 1024)}MB 限制",
                    file=sys.stderr,
                )
                sys.exit(1)
        except ValueError:
            print(
                "错误: 提供的 ImageBase64 不是合法的 Base64 编码，也不是有效的文件路径",
                file=sys.stderr,
            )
            sys.exit(1)
        return value


def pdf_page_to_base64(pdf_path: str, page_number: int, dpi: int = DEFAULT_PDF_DPI) -> str:
    """
    Render a single PDF page to PNG and return as Base64 string.

    Args:
        pdf_path: Path to the PDF file.
        page_number: 1-based page number.
        dpi: Resolution for rendering (default 200).

    Returns:
        Base64-encoded PNG image string.
    """
    try:
        import fitz  # PyMuPDF
    except ImportError:
        print(
            "错误: 缺少依赖 PyMuPDF，请执行: pip install PyMuPDF",
            file=sys.stderr,
        )
        sys.exit(1)

    if not os.path.isfile(pdf_path):
        print(f"错误: PDF文件不存在: {pdf_path}", file=sys.stderr)
        sys.exit(1)

    doc = fitz.open(pdf_path)
    total_pages = len(doc)

    if page_number < 1 or page_number > total_pages:
        print(
            f"错误: 页码 {page_number} 超出范围，PDF共 {total_pages} 页",
            file=sys.stderr,
        )
        doc.close()
        sys.exit(1)

    # fitz uses 0-based page index
    page = doc[page_number - 1]
    zoom = dpi / 72.0
    mat = fitz.Matrix(zoom, zoom)
    pix = page.get_pixmap(matrix=mat)

    # Convert to PNG bytes
    png_bytes = pix.tobytes("png")
    doc.close()

    if len(png_bytes) > MAX_IMAGE_SIZE_BYTES:
        print(
            f"警告: 第{page_number}页渲染后图片大小 {len(png_bytes) / (1024 * 1024):.1f}MB，"
            f"超过 {MAX_IMAGE_SIZE_BYTES // (1024 * 1024)}MB 限制，尝试降低DPI重新渲染",
            file=sys.stderr,
        )
        # Retry with lower DPI
        lower_dpi = int(dpi * 0.6)
        doc = fitz.open(pdf_path)
        page = doc[page_number - 1]
        zoom = lower_dpi / 72.0
        mat = fitz.Matrix(zoom, zoom)
        pix = page.get_pixmap(matrix=mat)
        png_bytes = pix.tobytes("png")
        doc.close()

    return base64.b64encode(png_bytes).decode("utf-8")


def format_response(resp) -> dict:
    """Format SDK response object, extract table data and text.

    Args:
        resp: RecognizeTableAccurateOCRResponse object from SDK.

    Returns:
        dict with tables (HTML list), raw_text, and metadata.
    """
    table_detections = resp.TableDetections or []

    if not table_detections:
        return {
            "tables": [],
            "raw_text": "",
            "table_count": 0,
            "message": "No tables detected in the image/PDF.",
            "RequestId": resp.RequestId or "",
        }

    tables = []
    all_text_parts = []

    for i, table in enumerate(table_detections):
        table_info = {
            "index": i,
            "html": "",
            "cells": [],
        }

        # Extract HTML table content
        if hasattr(table, "Table") and table.Table:
            table_info["html"] = table.Table

        # Extract cell-level data
        if hasattr(table, "Cells") and table.Cells:
            for cell in table.Cells:
                cell_data = {
                    "row": cell.RowTl if hasattr(cell, "RowTl") else None,
                    "col": cell.ColTl if hasattr(cell, "ColTl") else None,
                    "text": cell.Text if hasattr(cell, "Text") else "",
                }
                table_info["cells"].append(cell_data)
                if cell_data["text"]:
                    all_text_parts.append(cell_data["text"])

        tables.append(table_info)

    raw_text = "\n".join(all_text_parts)

    return {
        "tables": tables,
        "raw_text": raw_text,
        "table_count": len(tables),
        "RequestId": resp.RequestId or "",
    }


def create_ocr_client(args: argparse.Namespace):
    """Create and return a Tencent Cloud OCR client."""
    try:
        from tencentcloud.common import credential
        from tencentcloud.common.profile.client_profile import ClientProfile
        from tencentcloud.common.profile.http_profile import HttpProfile
        from tencentcloud.ocr.v20181119 import ocr_client
    except ImportError:
        print(
            "错误: 缺少依赖 tencentcloud-sdk-python，请执行: pip install tencentcloud-sdk-python",
            file=sys.stderr,
        )
        sys.exit(1)

    secret_id, secret_key = validate_env()

    cred = credential.Credential(secret_id, secret_key)
    http_profile = HttpProfile()
    http_profile.endpoint = "ocr.tencentcloudapi.com"
    client_profile = ClientProfile()
    client_profile.httpProfile = http_profile
    client_profile.request_client = args.user_agent
    region = args.region if args.region else "ap-guangzhou"
    client = ocr_client.OcrClient(cred, region, client_profile)
    return client


def call_ocr_single(client, image_base64: str = None, image_url: str = None) -> dict:
    """
    Call RecognizeTableAccurateOCR for a single image.

    Note: This API does NOT support IsPdf/PdfPageNumber parameters.
    PDF files must be converted to images before calling this function.

    Args:
        client: OcrClient instance.
        image_base64: Base64-encoded image string.
        image_url: Image URL.

    Returns:
        Formatted response dict.
    """
    from tencentcloud.common.exception.tencent_cloud_sdk_exception import (
        TencentCloudSDKException,
    )
    from tencentcloud.ocr.v20181119 import models

    req = models.RecognizeTableAccurateOCRRequest()

    if image_url:
        req.ImageUrl = image_url
    elif image_base64:
        req.ImageBase64 = image_base64
    else:
        raise ValueError("必须提供 image_base64 或 image_url 之一")

    # NOTE: Do NOT set req.IsPdf or req.PdfPageNumber here.
    # RecognizeTableAccurateOCR does not support these params and will
    # return "UnknownParameter: SPdf" error if they are set.

    try:
        resp = client.RecognizeTableAccurateOCR(req)
    except TencentCloudSDKException as e:
        return {
            "error": True,
            "error_code": e.code,
            "error_message": e.message,
            "RequestId": e.requestId or "",
        }

    return format_response(resp)


def call_table_ocr(args: argparse.Namespace) -> None:
    """Call Tencent Cloud RecognizeTableAccurateOCR API (single image mode)."""
    client = create_ocr_client(args)

    if args.image_url:
        result = call_ocr_single(client, image_url=args.image_url)
    elif args.image_base64:
        b64 = load_image_base64(args.image_base64)
        result = call_ocr_single(client, image_base64=b64)
    else:
        print("错误: 必须提供 --image-url 或 --image-base64 之一", file=sys.stderr)
        sys.exit(1)

    if result.get("error"):
        print(
            f"API调用失败 [{result['error_code']}]: {result['error_message']}",
            file=sys.stderr,
        )
        sys.exit(1)

    print(json.dumps(result, ensure_ascii=False, indent=2))


def call_pdf_ocr(args: argparse.Namespace) -> None:
    """
    PDF mode: render specified pages to PNG, then call OCR in parallel.

    Uses PyMuPDF for PDF→PNG conversion and ThreadPoolExecutor for
    concurrent API calls to minimize total wait time.
    """
    pdf_path = args.pdf
    if not os.path.isfile(pdf_path):
        print(f"错误: PDF文件不存在: {pdf_path}", file=sys.stderr)
        sys.exit(1)

    # Parse page numbers
    pages = parse_page_numbers(args.pdf_pages, pdf_path)
    if not pages:
        print("错误: 未指定有效的页码", file=sys.stderr)
        sys.exit(1)

    print(f"📄 PDF: {pdf_path}", file=sys.stderr)
    print(f"📑 待识别页码: {pages} (共{len(pages)}页)", file=sys.stderr)

    # Step 1: Render all pages to PNG (sequential, CPU-bound)
    print("🖼️  渲染PDF页面为PNG...", file=sys.stderr)
    page_images = {}
    for pg in pages:
        print(f"  - 渲染第{pg}页...", file=sys.stderr)
        page_images[pg] = pdf_page_to_base64(pdf_path, pg, args.dpi)

    # Step 2: Call OCR in parallel (IO-bound, benefits from concurrency)
    client = create_ocr_client(args)
    workers = min(len(pages), MAX_OCR_WORKERS)
    print(f"🔍 并行调用OCR (workers={workers})...", file=sys.stderr)

    results = {}

    def ocr_task(page_num, img_b64):
        return page_num, call_ocr_single(client, image_base64=img_b64)

    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = {
            executor.submit(ocr_task, pg, img_b64): pg
            for pg, img_b64 in page_images.items()
        }
        for future in as_completed(futures):
            pg = futures[future]
            try:
                page_num, result = future.result()
                results[page_num] = result
                if result.get("error"):
                    print(
                        f"  ⚠️ 第{page_num}页OCR失败: [{result['error_code']}] {result['error_message']}",
                        file=sys.stderr,
                    )
                else:
                    print(
                        f"  ✅ 第{page_num}页识别完成 (检测到{result.get('table_count', 0)}个表格)",
                        file=sys.stderr,
                    )
            except Exception as e:
                results[pg] = {"error": True, "error_message": str(e)}
                print(f"  ❌ 第{pg}页异常: {e}", file=sys.stderr)

    # Step 3: Assemble output sorted by page number
    output = {
        "pdf_path": pdf_path,
        "pages": [],
        "total_tables": 0,
    }

    for pg in sorted(results.keys()):
        page_result = results[pg]
        page_result["page_number"] = pg
        output["pages"].append(page_result)
        if not page_result.get("error"):
            output["total_tables"] += page_result.get("table_count", 0)

    print(json.dumps(output, ensure_ascii=False, indent=2))


def parse_page_numbers(pages_str: str, pdf_path: str) -> list:
    """
    Parse page number string into a sorted list of unique page numbers.

    Supports:
        - Comma-separated: "1,3,5"
        - Ranges: "1-5"
        - Mixed: "1,3-5,8"
        - "all" for all pages

    Args:
        pages_str: Page number specification string.
        pdf_path: Path to PDF (for total page count).

    Returns:
        Sorted list of 1-based page numbers.
    """
    try:
        import fitz
    except ImportError:
        print("错误: 缺少依赖 PyMuPDF，请执行: pip install PyMuPDF", file=sys.stderr)
        sys.exit(1)

    doc = fitz.open(pdf_path)
    total_pages = len(doc)
    doc.close()

    if pages_str.strip().lower() == "all":
        return list(range(1, total_pages + 1))

    pages = set()
    for part in pages_str.split(","):
        part = part.strip()
        if "-" in part:
            try:
                start, end = part.split("-", 1)
                start, end = int(start.strip()), int(end.strip())
                for p in range(start, end + 1):
                    if 1 <= p <= total_pages:
                        pages.add(p)
            except ValueError:
                print(f"警告: 无法解析页码范围 '{part}'，已跳过", file=sys.stderr)
        else:
            try:
                p = int(part)
                if 1 <= p <= total_pages:
                    pages.add(p)
                else:
                    print(
                        f"警告: 页码 {p} 超出范围 (1-{total_pages})，已跳过",
                        file=sys.stderr,
                    )
            except ValueError:
                print(f"警告: 无法解析页码 '{part}'，已跳过", file=sys.stderr)

    return sorted(pages)


def build_parser() -> argparse.ArgumentParser:
    """Build command-line argument parser."""
    parser = argparse.ArgumentParser(
        description="Tencent Cloud Table OCR (High Precision) - RecognizeTableAccurateOCR",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Recognize table from image URL
  python table_ocr.py --image-url "https://example.com/financial_report.jpg"

  # Recognize table from local image file
  python table_ocr.py --image-base64 ./financial_report.jpg

  # Recognize PDF pages (built-in PDF→PNG conversion + parallel OCR)
  python table_ocr.py --pdf ./report.pdf --pdf-pages 6,7,8,9

  # Recognize specific page range
  python table_ocr.py --pdf ./report.pdf --pdf-pages 1-5

  # Recognize all pages
  python table_ocr.py --pdf ./report.pdf --pdf-pages all

  # Customize rendering DPI (default: 200)
  python table_ocr.py --pdf ./report.pdf --pdf-pages 1,2,3 --dpi 300
        """,
    )

    # Image input mode (mutually exclusive with PDF mode)
    img_group = parser.add_argument_group("Image mode (single image)")
    img_exclusive = img_group.add_mutually_exclusive_group()
    img_exclusive.add_argument(
        "--image-url",
        type=str,
        help="Image URL (HTTP/HTTPS), max 10MB",
    )
    img_exclusive.add_argument(
        "--image-base64",
        type=str,
        help="Image Base64 string, or path to image file",
    )

    # PDF input mode
    pdf_group = parser.add_argument_group("PDF mode (multi-page, parallel OCR)")
    pdf_group.add_argument(
        "--pdf",
        type=str,
        help="Path to PDF file (pages will be rendered to PNG internally)",
    )
    pdf_group.add_argument(
        "--pdf-pages",
        type=str,
        default="1",
        help="Page numbers to recognize: comma-separated (1,3,5), range (1-5), "
             "mixed (1,3-5,8), or 'all' (default: 1)",
    )
    pdf_group.add_argument(
        "--dpi",
        type=int,
        default=DEFAULT_PDF_DPI,
        help=f"DPI for PDF→PNG rendering (default: {DEFAULT_PDF_DPI})",
    )

    # Common optional parameters
    parser.add_argument(
        "--region",
        type=str,
        default=None,
        help="Tencent Cloud region (default: ap-guangzhou)",
    )
    parser.add_argument(
        "--user-agent",
        type=str,
        default="Skills",
        help="Client identifier for tracking, fixed as 'Skills'",
    )

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    # Determine mode: PDF or single image
    if args.pdf:
        call_pdf_ocr(args)
    elif args.image_url or args.image_base64:
        call_table_ocr(args)
    else:
        parser.print_help()
        print("\n错误: 请指定 --pdf、--image-url 或 --image-base64 之一", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
