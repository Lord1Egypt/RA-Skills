from pathlib import Path
import sys
import json
import cv2
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from PIL import Image
from datetime import datetime
import re
from paddleocr import PaddleOCR

ocr_engine = PaddleOCR(use_textline_orientation=True, lang='korean')


def enhance_document(image_path: str, output_path: str) -> str:
    img = cv2.imread(image_path)
    if img is None:
        raise FileNotFoundError(image_path)

    h, w = img.shape[:2]
    if h > w:
        img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)

    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    l2 = clahe.apply(l)
    enhanced = cv2.merge((l2, a, b))
    enhanced = cv2.cvtColor(enhanced, cv2.COLOR_LAB2BGR)

    cv2.imwrite(output_path, enhanced)
    return output_path


def run_ocr(image_path: str) -> str:
    result = ocr_engine.predict(image_path)
    lines = []
    for item in result:
        if isinstance(item, dict):
            lines.extend(item.get('rec_texts', []))
    return '\n'.join([str(line).strip() for line in lines if str(line).strip()])


def sanitize_filename(text: str) -> str:
    text = re.sub(r'\s+', ' ', text).strip()
    text = re.sub(r'[\\/:*?"<>|]', '', text)
    return text[:80] or 'untitled'


def extract_headline(ocr_text: str) -> str:
    lines = [line.strip() for line in ocr_text.splitlines() if line.strip()]
    headline = ' '.join(lines[:3])
    return sanitize_filename(headline)


def make_filename(ocr_text: str) -> str:
    date_part = datetime.now().strftime('%Y-%m-%d')
    headline = extract_headline(ocr_text)
    return f'{date_part}_{headline}.pdf'


def build_searchable_pdf(image_paths: list[str], pdf_path: str, ocr_texts: list[str]) -> str:
    c = None
    for idx, image_path in enumerate(image_paths):
        img = Image.open(image_path)
        width, height = img.size
        if c is None:
            c = canvas.Canvas(pdf_path, pagesize=(width, height))
        else:
            c.setPageSize((width, height))

        c.drawImage(ImageReader(img), 0, 0, width=width, height=height)
        text = c.beginText(0, height)
        text.setTextRenderMode(3)
        text.setFont('Helvetica', 10)
        for line in ocr_texts[idx].splitlines():
            text.textLine(line[:500])
        c.drawText(text)
        c.showPage()

    c.save()
    return pdf_path


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('usage: python build_searchable_pdf_paddle.py <output_dir> <image1> [image2 ... imageN]')
        sys.exit(1)

    output_dir = Path(sys.argv[1])
    source_images = [Path(p) for p in sys.argv[2:]]
    output_dir.mkdir(parents=True, exist_ok=True)

    enhanced_paths = []
    ocr_texts = []

    for img_path in source_images:
        enhanced_path = output_dir / f'enhanced_{img_path.name}'
        enhance_document(str(img_path), str(enhanced_path))
        enhanced_paths.append(str(enhanced_path))
        ocr_texts.append(run_ocr(str(enhanced_path)))

    joined_ocr = '\n'.join(ocr_texts)
    filename = make_filename(joined_ocr)
    pdf_out = output_dir / filename
    build_searchable_pdf(enhanced_paths, str(pdf_out), ocr_texts)

    result = {
        'pdf': str(pdf_out),
        'headline': extract_headline(joined_ocr),
        'ocr_failed': not bool(joined_ocr.strip())
    }
    print(json.dumps(result, ensure_ascii=False))
