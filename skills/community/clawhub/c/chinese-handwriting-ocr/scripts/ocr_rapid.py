"""
ocr_rapid.py — RapidOCR 手写体文本提取工具
专门用于从PDF指定区域提取手写文本(工号、姓名、日期、签名等)

用法:
  # 从PDF提取指定区域文本
  python ocr_rapid.py input.pdf --region 0.1 0.4 0.9 0.6 -o output.txt

  # 提取全页文本
  python ocr_rapid.py input.pdf --page 2 -o output.txt

  # 批量提取PDF目录中的手写签名区域
  python ocr_rapid.py ./pdfs --batch --region 0.1 0.4 0.9 0.6

  # 提取日期(预置区域)
  python ocr_rapid.py input.pdf --date-mode
"""
import sys, os, json, re, argparse
from pathlib import Path
from rapidocr_onnxruntime import RapidOCR

def extract_regions(pdf_path: Path, regions: dict, dpi: int = 400) -> dict:
    """
    从PDF指定区域提取文本
    regions: { "name": (x1, y1, x2, y2) } 百分比坐标(0-1)
    返回: { page_num: { "region_name": "text" } }
    """
    import fitz
    engine = RapidOCR()
    doc = fitz.open(str(pdf_path))
    results = {}

    for page_idx in range(len(doc)):
        page = doc[page_idx]
        r = page.rect
        page_result = {}

        for name, (x1, y1, x2, y2) in regions.items():
            crop = fitz.Rect(r.width * x1, r.height * y1,
                             r.width * x2, r.height * y2)
            pix = page.get_pixmap(dpi=dpi, clip=crop)
            tmp = str(pdf_path.parent / f"_rapid_{page_idx}_{name}.png")
            pix.save(tmp)

            result, _ = engine(tmp)
            os.remove(tmp)

            texts = [t for _, t, c in (result or []) if c > 0.3]
            page_result[name] = " ".join(texts) if texts else ""

        results[page_idx] = page_result

    doc.close()
    return results


def extract_full(pdf_path: Path, dpi: int = 300) -> dict:
    """全页文本提取"""
    import fitz
    engine = RapidOCR()
    doc = fitz.open(str(pdf_path))
    results = {}

    for page_idx in range(len(doc)):
        page = doc[page_idx]
        pix = page.get_pixmap(dpi=dpi)
        tmp = str(pdf_path.parent / f"_rapid_full_{page_idx}.png")
        pix.save(tmp)

        result, _ = engine(tmp)
        os.remove(tmp)

        # 按Y坐标归并行
        if result:
            lines = sorted(
                [(bbox[0][1], text) for bbox, text, _ in result],
                key=lambda x: x[0]
            )
            grouped = []
            current_y = None
            current_line = []
            for y, text in lines:
                if current_y is None or abs(y - current_y) < 20:
                    current_line.append(text)
                else:
                    grouped.append(" ".join(current_line))
                    current_line = [text]
                current_y = y
            if current_line:
                grouped.append(" ".join(current_line))
            results[page_idx] = "\n".join(grouped)
        else:
            results[page_idx] = ""

    doc.close()
    return results


def parse_date(text: str) -> str:
    """从文本中提取日期"""
    m = re.search(r'(\d{4})\s*年\s*(\d{1,2})\s*月\s*(\d{1,2})\s*日', text)
    if m:
        return f"{m.group(1)}年{m.group(2)}月{m.group(3)}日"
    m = re.search(r'(\d{1,2})\s*月\s*(\d{1,2})\s*日', text)
    if m:
        yr = ""
        ym = re.search(r'(20\d{2})\s*年', text)
        if ym:
            yr = f"{ym.group(1)}年"
        return f"{yr}{m.group(1)}月{m.group(2)}日"
    m = re.search(r'(\d{4})\s*年\s*(\d{1,2})\s*月', text)
    if m:
        return f"{m.group(1)}年{m.group(2)}月"
    m = re.search(r'(\d{1,2})\s*月', text)
    if m:
        return f"{m.group(1)}月"
    return ""


# 预置区域配置
PRESET_REGIONS = {
    "date": (0.1, 0.46, 0.9, 0.64),       # 日期区域
    "signature": (0.25, 0.30, 0.75, 0.55), # 签名区域(承诺人+部门)
    "id_top": (0, 0, 0.4, 0.12),           # 左上角(工号/编号)
    "full_bottom": (0.05, 0.40, 0.95, 0.70), # 下半部分(综合手写区)
}


def main(argv):
    parser = argparse.ArgumentParser(description="RapidOCR 手写体文本提取")
    parser.add_argument("input", help="输入PDF文件或目录(--batch)")
    parser.add_argument("-o", "--output", help="输出文件路径(默认 stdout)")
    parser.add_argument("--page", type=int, default=None,
                        help="指定页码(1-based), 默认所有页")
    parser.add_argument("--region", nargs=4, type=float,
                        metavar=("X1", "Y1", "X2", "Y2"),
                        help="自定义区域: --region 0.1 0.4 0.9 0.6")
    parser.add_argument("--date-mode", action="store_true",
                        help="日期提取模式(自动提取日期并格式化)")
    parser.add_argument("--signature-mode", action="store_true",
                        help="签名区域提取(承诺人+部门)")
    parser.add_argument("--batch", action="store_true",
                        help="批量处理目录下的所有PDF")
    parser.add_argument("--dpi", type=int, default=400,
                        help="OCR分辨率(默认400)")
    parser.add_argument("--json", action="store_true",
                        help="JSON格式输出")
    args = parser.parse_args(argv)

    # 确定区域
    regions = {}
    if args.region:
        regions["custom"] = tuple(args.region)
    elif args.date_mode:
        regions["date"] = PRESET_REGIONS["date"]
    elif args.signature_mode:
        regions["signature"] = PRESET_REGIONS["signature"]
        regions["date"] = PRESET_REGIONS["date"]
    else:
        regions["full_bottom"] = PRESET_REGIONS["full_bottom"]

    inputs = []
    if args.batch:
        dir_path = Path(args.input)
        if dir_path.is_dir():
            inputs = sorted(dir_path.glob("*.pdf"))
    else:
        inputs = [Path(args.input)]

    all_results = {}

    for pdf_path in inputs:
        if not pdf_path.exists():
            print(f"文件不存在: {pdf_path}", file=sys.stderr)
            continue

        if args.date_mode:
            # 专注于日期提取
            r = extract_regions(pdf_path, {"date": PRESET_REGIONS["date"]}, args.dpi)
            label = pdf_path.stem
            dates = {}
            for page_num, page_data in r.items():
                text = page_data.get("date", "")
                dates[str(page_num + 1)] = {
                    "raw": text[:100],
                    "parsed": parse_date(text)
                }
            all_results[label] = dates
        elif args.signature_mode:
            r = extract_regions(pdf_path, regions, args.dpi)
            all_results[pdf_path.stem] = r
        else:
            r = extract_regions(pdf_path, regions, args.dpi)
            all_results[pdf_path.stem] = r

    # 输出
    output_text = ""
    if args.json:
        output_text = json.dumps(all_results, ensure_ascii=False, indent=2)
    else:
        for label, pages in all_results.items():
            output_text += f"=== {label} ===\n"
            if isinstance(pages, dict):
                for page_num, data in pages.items():
                    if isinstance(data, dict):
                        for region_name, text in data.items():
                            if text:
                                output_text += f"  页{page_num}[{region_name}]: {text}\n"
                    else:
                        output_text += f"  页{page_num}: {data}\n"
            output_text += "\n"

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output_text)
        print(f"结果已保存到: {args.output}")
    else:
        # stdout
        sys.stdout.reconfigure(encoding="utf-8")
        print(output_text)


if __name__ == "__main__":
    main(sys.argv[1:])
