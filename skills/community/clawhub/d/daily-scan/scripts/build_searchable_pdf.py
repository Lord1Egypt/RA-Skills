from pathlib import Path
import sys
import json
import cv2
from PIL import Image
from datetime import datetime
import re
import subprocess


def enhance_document(image_path: str, output_path: str) -> str:
    img = cv2.imread(image_path)
    if img is None:
        raise FileNotFoundError(image_path)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.fastNlMeansDenoising(gray, None, 10, 7, 21)

    thresh = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 15
    )

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
    cleaned = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

    cv2.imwrite(output_path, cleaned)
    return output_path


def run_ocr(image_path: str, lang: str = 'kor+eng') -> str:
    result = subprocess.run(
        ['tesseract', image_path, 'stdout', '-l', lang, '--psm', '6'],
        capture_output=True,
        text=True,
        encoding='utf-8',
        errors='ignore'
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or 'tesseract failed')
    return result.stdout.strip()


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


def build_image_pdf(image_paths: list[str], pdf_path: str) -> str:
    images = []
    for image_path in image_paths:
        img = Image.open(image_path).convert('RGB')
        images.append(img)

    first, rest = images[0], images[1:]
    first.save(pdf_path, save_all=True, append_images=rest)
    return pdf_path


def apply_ocrmypdf(input_pdf: str, output_pdf: str) -> str:
    result = subprocess.run(
        ['ocrmypdf', '--force-ocr', '-l', 'kor+eng', input_pdf, output_pdf],
        capture_output=True,
        text=True,
        encoding='utf-8',
        errors='ignore'
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or result.stdout.strip() or 'ocrmypdf failed')
    return output_pdf


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('usage: python build_searchable_pdf.py <output_dir> <image1> [image2 ... imageN]')
        sys.exit(1)

    output_dir = Path(sys.argv[1])
    if output_dir.name == 'AUTO':
        output_dir = Path.cwd() / 'daily-scan-storage' / datetime.now().strftime('%Y-%m')
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
    image_pdf = output_dir / 'temp_image.pdf'
    pdf_out = output_dir / filename
    build_image_pdf(enhanced_paths, str(image_pdf))
    apply_ocrmypdf(str(image_pdf), str(pdf_out))

    result = {
        'pdf': str(pdf_out),
        'headline': extract_headline(joined_ocr),
        'ocr_failed': not bool(joined_ocr.strip())
    }
    print(json.dumps(result, ensure_ascii=False))
