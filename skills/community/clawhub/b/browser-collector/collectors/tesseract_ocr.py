#!/usr/bin/env python3
"""
collectors/tesseract_ocr.py - Tesseract OCR优化模块
独立于ddddocr，提供高精度OCR能力

与 base.py 的 StructuredItem 兼容：
    识别结果 → StructuredItem.content
    置信度   → StructuredItem.quality_score
"""

import sys
import time
from pathlib import Path
from typing import Optional, Tuple, List

import cv2
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter

try:
    import pytesseract
    TESSERACT_AVAILABLE = True
except ImportError:
    pytesseract = None
    TESSERACT_AVAILABLE = False

sys.path.insert(0, str(Path(__file__).parent.parent))
from collectors.base import StructuredItem


# Tesseract 语言代码常量
TESS_LANG = {
    'eng': 'eng',
    'chi_sim': 'chi_sim',      # 简体中文
    'chi_tra': 'chi_tra',      # 繁体中文
    'jpn': 'jpn',              # 日语
    'kor': 'kor',              # 韩语
    'eng_chi': 'eng+chi_sim',  # 中英混合
}

# PSM (Page Segmentation Mode) 常用模式
PSM_MODES = {
    'auto': 3,       # 完全自动分页（可能不稳定）
    'single_line': 6,    # 假设图像包含单行文本
    'single_word': 7,    # 假设图像包含单个单词
    'single_char': 8,    # 假设图像包含单个字符
    'raw_line': 13,      # 原始文本行（不分组）
    'single_block': 4,   # 单一文本块
}


class TesseractOCR:
    """
    Tesseract OCR 识别器

    与 CaptchaSolver 的区别：
    - CaptchaSolver: 专门针对验证码优化（ddddocr主引擎）
    - TesseractOCR: 通用OCR，适合长文本、文档、混合语言

    Usage:
        ocr = TesseractOCR(lang='eng+chi_sim')
        text = ocr.recognize('document.png')
        text, conf = ocr.get_confidence('document.png')
        img = ocr.preprocess_for_tesseract('document.png')  # 获取预处理后的PIL.Image
    """

    def __init__(self, lang: str = 'eng', psm: int = 7):
        """
        Args:
            lang: 语言代码，参见 TESS_LANG 常量
            psm: Page Segmentation Mode，参见 PSM_MODES
        """
        if not TESSERACT_AVAILABLE:
            raise RuntimeError("pytesseract not installed. Run: pip install pytesseract && apt install tesseract-ocr")

        self.lang = lang
        self.psm = psm
        self._config = f'--psm {psm} --oem 3'

    def preprocess_for_tesseract(self, image_path: str) -> Image.Image:
        """
        文字识别前预处理

        处理流程：
        1. 灰度化
        2. 非局部均值去噪（fastNlMeansDenoising）
        3. 锐化（卷积核）
        4. 自适应二值化
        5. 去除边框线干扰

        Args:
            image_path: 原始图片路径

        Returns:
            PIL.Image: 预处理后的图像
        """
        img = cv2.imread(image_path)
        if img is None:
            raise ValueError(f"Cannot read image: {image_path}")

        # 1. 灰度化
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # 2. 非局部均值去噪（对文字效果比高斯滤波好）
        denoised = cv2.fastNlMeansDenoising(gray, None, 10, 7, 21)

        # 3. 锐化
        kernel = np.array([[-1, -1, -1],
                           [-1,  9, -1],
                           [-1, -1, -1]])
        sharpened = cv2.filter2D(denoised, -1, kernel)

        # 4. 自适应二值化
        binary = cv2.adaptiveThreshold(
            sharpened, 255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY, 15, 11
        )

        # 5. 去除边框线（反向二值化 → 找轮廓 → 排除大轮廓 → 填回）
        result = 255 - binary
        contours, _ = cv2.findContours(result, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        img_h, img_w = img.shape[:2]
        for cnt in contours:
            x, y, w, h = cv2.boundingRect(cnt)
            area_ratio = (w * h) / (img_w * img_h)
            # 排除占图片80%以上的超大轮廓（通常是边框）
            if area_ratio > 0.8:
                cv2.rectangle(binary, (x - 2, y - 2), (x + w + 2, y + h + 2), 255, -1)
        binary = 255 - binary

        return Image.fromarray(binary)

    def recognize(self, image_path: str,
                 use_preprocess: bool = True) -> str:
        """
        识别文字

        Args:
            image_path: 图片路径
            use_preprocess: 是否使用预处理

        Returns:
            识别出的文字（已strip）
        """
        start = time.time()

        if use_preprocess:
            img = self.preprocess_for_tesseract(image_path)
        else:
            img = Image.open(image_path)

        text = pytesseract.image_to_string(
            img,
            lang=self.lang,
            config=self._config
        ).strip()

        self._last_processing_time = (time.time() - start) * 1000
        return text

    def get_confidence(self, image_path: str) -> Tuple[str, float]:
        """
        识别并返回置信度

        Args:
            image_path: 图片路径

        Returns:
            (识别文字, 平均置信度 0-100)
        """
        img = Image.open(image_path)
        data = pytesseract.image_to_data(
            img,
            lang=self.lang,
            config=self._config,
            output_type=pytesseract.Output.DICT
        )

        # 计算非空白字符的平均置信度
        confidences = [int(c) for c in data['conf'] if int(c) > 0]
        avg_conf = sum(confidences) / len(confidences) if confidences else 0.0

        # 拼接文字（非空白）
        text = ''.join(c for c in data['text'] if c.strip())

        return text, round(avg_conf, 2)

    def recognize_as_item(self, image_path: str,
                         platform: str = "ocr",
                         use_preprocess: bool = True) -> StructuredItem:
        """
        以StructuredItem格式返回识别结果

        与 base.py 完全兼容
        """
        start = time.time()
        text, conf = self.get_confidence(image_path)

        item = StructuredItem(
            title=f"ocr_{Path(image_path).stem}",
            url=image_path,
            platform=platform,
            content=text,
            quality_score=conf / 100.0,  # 归一化到0-1
        )
        return item

    def recognize_with_boxes(self, image_path: str) -> List[dict]:
        """
        识别并返回每个字符/单词的位置信息

        Returns:
            List[dict]: 每个文本块的信息，包含 bounding box、text、conf
        """
        img = Image.open(image_path)
        data = pytesseract.image_to_data(
            img,
            lang=self.lang,
            config=self._config,
            output_type=pytesseract.Output.DICT
        )

        results = []
        n = len(data['text'])
        for i in range(n):
            text = data['text'][i].strip()
            conf = int(data['conf'][i])
            if not text or conf <= 0:
                continue
            results.append({
                'text': text,
                'conf': conf,
                'left': data['left'][i],
                'top': data['top'][i],
                'width': data['width'][i],
                'height': data['height'][i],
            })
        return results


# ---- CLI Entrance ----

def main():
    import argparse
    parser = argparse.ArgumentParser(description='Tesseract OCR CLI')
    parser.add_argument('command', choices=['recognize', 'confidence', 'boxes', 'test'],
                        help='子命令')
    parser.add_argument('image_path', nargs='?', help='图片路径')
    parser.add_argument('--lang', default='eng', help='语言代码 (eng/chi_sim/eng+chi_sim)')
    parser.add_argument('--psm', type=int, default=7, help='PSM模式')
    parser.add_argument('--no-preprocess', action='store_true', help='禁用预处理')
    args = parser.parse_args()

    if args.command == 'test':
        print(f"pytesseract available: {TESSERACT_AVAILABLE}")
        if TESSERACT_AVAILABLE:
            print(f"Available languages: {list(TESS_LANG.keys())}")
            print(f"PSM modes: {PSM_MODES}")
        return 0

    if not args.image_path:
        parser.print_help()
        return 1

    ocr = TesseractOCR(lang=args.lang, psm=args.psm)

    if args.command == 'recognize':
        text = ocr.recognize(args.image_path, use_preprocess=not args.no_preprocess)
        print(f"Result: {text}")

    elif args.command == 'confidence':
        text, conf = ocr.get_confidence(args.image_path)
        print(f"Text: {text}")
        print(f"Confidence: {conf}%")

    elif args.command == 'boxes':
        boxes = ocr.recognize_with_boxes(args.image_path)
        print(f"Found {len(boxes)} text blocks:")
        for b in boxes:
            print(f"  [{b['conf']:3d}] {b['text']!r:20s} at ({b['left']:4d},{b['top']:4d}) {b['width']}x{b['height']}")

    return 0


if __name__ == '__main__':
    sys.exit(main())
