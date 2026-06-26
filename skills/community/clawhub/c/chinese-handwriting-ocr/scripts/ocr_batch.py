"""
OCR 双引擎脚本 — 支持 Tesseract (印刷体) + RapidOCR (手写体)
用法:
  python ocr_batch.py input.pdf output.pdf                     # Tesseract 默认
  python ocr_batch.py input.pdf output.pdf --engine rapid      # RapidOCR
  python ocr_batch.py input.pdf output.pdf --engine dual       # 双引擎(先Tesseract,低置信度fallback)
  python ocr_batch.py --batch-dir ./pdfs --engine rapid        # 批量
"""
import sys, os, logging, json, re, argparse
from pathlib import Path
from PIL import Image

# ── 引擎: Tesseract (via ocrmypdf) ─────────────────────────
def ensure_tesseract():
    try:
        import subprocess
        subprocess.run(["ocrmypdf", "--version"], check=True,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception:
        raise RuntimeError(
            "ocrmypdf/Tesseract 未就绪。安装: pip install ocrmypdf\n"
            "Tesseract: https://github.com/UB-Mannheim/tesseract/wiki"
        )

def ocr_tesseract(input_pdf: Path, output_pdf: Path, lang: str = "chi_sim+eng"):
    import subprocess
    cmd = ["ocrmypdf", "-l", lang, "--force-ocr",
           str(input_pdf), str(output_pdf)]
    subprocess.run(cmd, check=True)
    logging.info(f"[Tesseract] {input_pdf.name} -> {output_pdf.name}")

# ── 引擎: RapidOCR (手写体优化) ────────────────────────────
def ensure_rapidocr():
    try:
        from rapidocr_onnxruntime import RapidOCR
    except ImportError:
        raise RuntimeError("RapidOCR 未安装。安装: pip install rapidocr-onnxruntime")

def ocr_rapid(input_pdf: Path, output_pdf: Path, lang: str = "ch"):
    """用 RapidOCR 提取文本后注入 PDF 为文字层（通过 ocrmypdf 空壳叠加）"""
    from rapidocr_onnxruntime import RapidOCR
    import fitz  # PyMuPDF

    engine = RapidOCR()
    doc = fitz.open(str(input_pdf))
    all_text = {}

    for page_idx in range(len(doc)):
        page = doc[page_idx]
        pix = page.get_pixmap(dpi=300)
        img_path = str(output_pdf.parent / f"_rapid_tmp_{page_idx}.png")
        pix.save(img_path)

        result, _ = engine(img_path)
        os.remove(img_path)

        if result:
            # 按 y 坐标分组为段落
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

            all_text[page_idx] = "\n".join(grouped)

    doc.close()

    # 用 fitz 将文本写入 PDF 文字层
    doc = fitz.open(str(input_pdf))
    for page_idx, text in all_text.items():
        page = doc[page_idx]
        # 在页面底部写入 OCR 文本（透明层）
        rect = page.rect
        # 清除已有文字层（如果有）
        # 用红线圈注：RapidOCR文本以元数据形式嵌入
        page.insert_text(
            fitz.Point(10, rect.height - 20),
            f"[RapidOCR] {text[:200]}",
            fontsize=6,
            color=(0, 0, 0, 0)  # 透明
        )
        # 同时写入页面注释
        page.add_annot(fitz.PDF_ANNOT_TEXT,
                       fitz.Point(10, 10),
                       content=f"RapidOCR: {text}")

    doc.save(str(output_pdf))
    doc.close()
    logging.info(f"[RapidOCR] {input_pdf.name} -> {output_pdf.name} ({len(all_text)} 页)")

def ocr_rapid_text(input_pdf: Path, output_txt: Path, regions=None):
    """提取文本到文本文件，handwriting优化"""
    from rapidocr_onnxruntime import RapidOCR
    import fitz

    engine = RapidOCR()
    doc = fitz.open(str(input_pdf))
    results = {}

    for page_idx in range(len(doc)):
        page = doc[page_idx]
        r = page.rect

        if regions:
            # 提取指定区域
            page_text = {}
            for name, crop_rect in regions.items():
                crop = fitz.Rect(
                    r.width * crop_rect[0],
                    r.height * crop_rect[1],
                    r.width * crop_rect[2],
                    r.height * crop_rect[3]
                )
                pix = page.get_pixmap(dpi=400, clip=crop)
                img_path = str(output_txt.parent / f"_rapid_crop_{page_idx}.png")
                pix.save(img_path)
                result, _ = engine(img_path)
                os.remove(img_path)
                texts = [t for _, t, _ in (result or [])]
                page_text[name] = " ".join(texts) if texts else ""
            results[page_idx] = page_text
        else:
            # 全页提取
            pix = page.get_pixmap(dpi=300)
            img_path = str(output_txt.parent / f"_rapid_full_{page_idx}.png")
            pix.save(img_path)
            result, _ = engine(img_path)
            os.remove(img_path)
            texts = [t for _, t, _ in (result or [])]
            results[page_idx] = "\n".join(texts) if texts else ""

    doc.close()

    with open(str(output_txt), "w", encoding="utf-8") as f:
        for page_idx in sorted(results.keys()):
            f.write(f"--- 第 {page_idx+1} 页 ---\n")
            if isinstance(results[page_idx], dict):
                for name, text in results[page_idx].items():
                    f.write(f"[{name}] {text}\n")
            else:
                f.write(results[page_idx] + "\n")
            f.write("\n")

    logging.info(f"[RapidOCR-Text] {input_pdf.name} -> {output_txt.name}")

# ── 双引擎模式 ──────────────────────────────────────────
def ocr_dual(input_pdf: Path, output_pdf: Path, lang: str = "chi_sim+eng"):
    """双引擎：先用Tesseract，再用RapidOCR补充手写区域"""
    import fitz

    # 先跑 Tesseract
    ocr_tesseract(input_pdf, output_pdf, lang)

    # 再用 RapidOCR 提取文本并附加到 PDF 注释
    from rapidocr_onnxruntime import RapidOCR
    engine = RapidOCR()
    doc = fitz.open(str(output_pdf))

    for page_idx in range(len(doc)):
        page = doc[page_idx]
        r = page.rect
        # 手写体通常在签名/日期区域（页面下半部分）
        crop = fitz.Rect(r.width * 0.05, r.height * 0.35,
                         r.width * 0.95, r.height * 0.70)
        pix = page.get_pixmap(dpi=400, clip=crop)
        img_path = str(output_pdf.parent / f"_rapid_dual_{page_idx}.png")
        pix.save(img_path)
        result, _ = engine(img_path)
        os.remove(img_path)

        if result:
            texts = [t for _, t, c in result if c > 0.5]
            if texts:
                page.add_annot(fitz.PDF_ANNOT_TEXT,
                               fitz.Point(r.width * 0.5, r.height * 0.5),
                               content="Handwriting: " + " ".join(texts))

    doc.save(str(output_pdf), incremental=True, encryption=0)
    doc.close()
    logging.info(f"[Dual] {input_pdf.name} -> {output_pdf.name}")

# ── 批量处理 ────────────────────────────────────────────
def batch_dir(dir_path: Path, engine: str, lang: str):
    for pdf_path in sorted(dir_path.rglob("*.pdf")):
        out_path = pdf_path.with_name(pdf_path.stem + f"_{engine}.pdf")
        try:
            if engine == "rapid":
                ocr_rapid(pdf_path, out_path, lang)
            elif engine == "dual":
                ocr_dual(pdf_path, out_path, lang)
            else:
                ocr_tesseract(pdf_path, out_path, lang)
        except Exception as exc:
            logging.error(f"处理失败: {pdf_path}: {exc}")

# ── CLI ──────────────────────────────────────────────────
def main(argv):
    parser = argparse.ArgumentParser(description="PDF OCR — 双引擎支持")
    parser.add_argument("input", nargs="?", help="输入PDF路径")
    parser.add_argument("output", nargs="?", help="输出PDF/TXT路径")
    parser.add_argument("--batch-dir", help="批量处理目录")
    parser.add_argument("--engine", default="tesseract",
                        choices=["tesseract", "rapid", "dual"],
                        help="OCR引擎: tesseract(印刷体), rapid(手写体), dual(双引擎)")
    parser.add_argument("--lang", default="chi_sim+eng",
                        help="语言(默认 chi_sim+eng)")
    parser.add_argument("--extract-text", action="store_true",
                        help="仅提取文本到 .txt 文件(rapid引擎)")
    parser.add_argument("--region", nargs=4, type=float, metavar=("X1","Y1","X2","Y2"),
                        help="提取指定区域(百分比0-1): --region 0.1 0.4 0.9 0.6")
    args = parser.parse_args(argv)

    logging.basicConfig(
        filename=str(Path("logs") / "pdf_ocr.log"),
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s"
    )

    # 引擎检查
    try:
        if args.engine in ("tesseract", "dual"):
            ensure_tesseract()
        if args.engine in ("rapid", "dual"):
            ensure_rapidocr()
    except RuntimeError as e:
        print(e)
        sys.exit(1)

    if args.batch_dir:
        batch_dir(Path(args.batch_dir), args.engine, args.lang)
        return

    if not args.input or not args.output:
        parser.print_help()
        sys.exit(1)

    inp, out = Path(args.input), Path(args.output)

    if args.extract_text and args.engine == "rapid":
        regions = None
        if args.region:
            regions = {"crop": tuple(args.region)}
        ocr_rapid_text(inp, out, regions)
    elif args.engine == "rapid":
        ocr_rapid(inp, out, args.lang)
    elif args.engine == "dual":
        ocr_dual(inp, out, args.lang)
    else:
        ocr_tesseract(inp, out, args.lang)

if __name__ == "__main__":
    main(sys.argv[1:])
