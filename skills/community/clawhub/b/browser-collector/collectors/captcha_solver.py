#!/usr/bin/env python3
"""
collectors/captcha_solver.py - 验证码识别模块
增强版：支持ddddocr预处理 + Tesseract fallback + 滑块轨迹生成

与 base.py 的 StructuredItem 兼容：
    识别结果 → StructuredItem.content
    质量分数 → StructuredItem.quality_score
"""

import io
import time
import random
import hashlib
from pathlib import Path
from typing import Optional, List, Tuple, Union
from dataclasses import dataclass, field

import cv2
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter

# DdddOcr - 主引擎
try:
    from ddddocr import DdddOcr as _DdddOcr
    DDDDOCR_AVAILABLE = True
except ImportError:
    _DdddOcr = None
    DDDDOCR_AVAILABLE = False

# Tesseract - Fallback引擎
try:
    import pytesseract
    PYTESSERACT_AVAILABLE = True
except ImportError:
    pytesseract = None
    PYTESSERACT_AVAILABLE = False

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from collectors.base import StructuredItem


@dataclass
class CaptchaResult(StructuredItem):
    """验证码识别结果（兼容StructuredItem）"""
    platform: str = "captcha"
    raw_id: Optional[str] = None

    # CaptchaSolver 特有字段
    captcha_type: Optional[str] = None        # image / slider / chinese
    confidence: Optional[float] = None        # 识别置信度 0-1
    preprocess_applied: bool = False          # 是否使用了预处理
    ocr_engine: Optional[str] = None           # 使用的OCR引擎
    processing_time_ms: Optional[float] = None

    @property
    def quality_score(self) -> Optional[float]:
        return self.confidence

    @quality_score.setter
    def quality_score(self, v: float):
        self.confidence = v


class CaptchaSolver:
    """
    验证码识别器

    支持：
    - ddddocr（主引擎，纯Python，无需额外模型）
    - Tesseract OCR（Fallback，需安装tesseract）
    - 图像预处理（灰度、去噪、二值化）

    Usage:
        solver = CaptchaSolver()
        result = solver.solve_image(image_bytes)        # bytes → str
        result = solver.solve_with_preprocess(path)    # 文件 → str（带预处理）

        # 也可直接获取StructuredItem
        item = solver.solve_as_item(image_bytes, platform="github")
    """

    def __init__(self, beta: bool = False, show_ad: bool = False):
        self.beta = beta
        self.show_ad = show_ad
        self._ocr = None
        self._init_engine()

    def _init_engine(self):
        """初始化ddddocr引擎"""
        if DDDDOCR_AVAILABLE:
            try:
                self._ocr = _DdddOcr(beta=self.beta, show_ad=self.show_ad)
            except Exception as e:
                print(f"[CaptchaSolver] DdddOcr init failed: {e}")
                self._ocr = None
        else:
            print("[CaptchaSolver] ddddocr not available")

    # ---- 核心识别API ----

    def solve_image(self, image_bytes: bytes) -> str:
        """
        识别字节流中的验证码文字

        Args:
            image_bytes: 图片原始字节

        Returns:
            识别出的文字（已strip）
        """
        if self._ocr is None:
            return self._fallback_tesseract_bytes(image_bytes)
        try:
            return self._ocr.classification(image_bytes).strip()
        except Exception as e:
            print(f"[CaptchaSolver] ddddocr failed: {e}")
            return self._fallback_tesseract_bytes(image_bytes)

    def solve_with_preprocess(self, image_path: str) -> str:
        """
        图像预处理后识别

        预处理流程：灰度 → 对比度增强 → 中值滤波去噪 → 自适应二值化 → 形态学闭操作

        Args:
            image_path: 图片文件路径

        Returns:
            识别出的文字
        """
        processed_bytes = self._preprocess_image(image_path)
        return self.solve_image(processed_bytes)

    def solve_as_item(self, image_bytes: bytes, platform: str = "captcha",
                      image_path: Optional[str] = None) -> CaptchaResult:
        """
        以StructuredItem格式返回识别结果

        与 base.py 的 StructuredItem 完全兼容
        """
        start = time.time()
        raw_text = self.solve_image(image_bytes)

        # 估算置信度（基于ddddocr内部机制，简单用长度一致性）
        confidence = self._estimate_confidence(raw_text)

        item = CaptchaResult(
            title="captcha",
            url="",
            platform=platform,
            content=raw_text,
            captcha_type="image",
            confidence=confidence,
            ocr_engine="ddddocr" if self._ocr else "tesseract",
            processing_time_ms=(time.time() - start) * 1000,
            preprocess_applied=False,
        )

        return item

    # ---- 图像预处理 ----

    def _preprocess_image(self, image_path: str) -> bytes:
        """
        完整的图像预处理流程

        Returns:
            处理后的PNG字节流
        """
        img = Image.open(image_path)

        # 1. 灰度化
        img = img.convert('L')

        # 2. 对比度增强（2x）
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(2.0)

        # 3. 中值滤波去噪
        img = img.filter(ImageFilter.MedianFilter(size=3))

        # 4. 转为numpy处理
        arr = np.array(img)

        # 5. 自适应阈值二值化（高斯）
        arr = cv2.adaptiveThreshold(
            arr, 255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY, 21, 10
        )

        # 6. 形态学闭操作（去孤立噪点）
        kernel = np.ones((2, 2), np.uint8)
        arr = cv2.morphologyEx(arr, cv2.MORPH_CLOSE, kernel)

        # 转回PIL → bytes
        result = Image.fromarray(arr)
        buf = io.BytesIO()
        result.save(buf, format='PNG')
        return buf.getvalue()

    def _estimate_confidence(self, text: str) -> float:
        """
        估算识别置信度

        启发式：字符种类多样性 + 长度合理性
        """
        if not text:
            return 0.0
        unique_ratio = len(set(text)) / max(len(text), 1)
        length_score = 1.0 if 4 <= len(text) <= 8 else max(0, 1.0 - abs(len(text) - 6) / 6)
        return round(min(1.0, (unique_ratio * 0.6 + length_score * 0.4) * 0.85 + 0.1), 3)

    # ---- Tesseract Fallback ----

    def _fallback_tesseract_bytes(self, image_bytes: bytes) -> str:
        """ddddocr失败时，用Tesseract处理字节流"""
        if not PYTESSERACT_AVAILABLE:
            return ""
        try:
            img = Image.open(io.BytesIO(image_bytes)).convert('L')
            return pytesseract.image_to_string(
                img,
                config='--psm 7 --oem 3'
            ).strip()
        except Exception as e:
            print(f"[CaptchaSolver] Tesseract fallback failed: {e}")
            return ""

    def set_beta(self, beta: bool):
        """切换beta模式（启用滑动验证码模型）"""
        self.beta = beta
        self._ocr = None
        self._init_engine()


class SliderCaptchaSolver:
    """
    滑块验证码识别器

    功能：
    1. 缺口位置检测（边缘密度法 + 模板匹配）
    2. 人类轨迹生成（慢启动 + 抖动 + 回退）

    Usage:
        slider = SliderCaptchaSolver()
        gap_ratio = slider.detect_gap(full_image_path)       # 0.0-1.0
        track = slider.generate_track(gap_ratio, total_width) # [(x,y,delay_ms), ...]
        steps = slider.solve_slider(full_image_path)         # 完整流程
    """

    def __init__(self):
        pass

    def detect_gap(self, full_image_path: str,
                   slider_image_path: Optional[str] = None) -> float:
        """
        检测缺口位置（相对于图片宽度的比例）

        算法：
        1. 尝试边缘检测 + 轮廓分析法（找最大轮廓）
        2. Fallback：边缘密度法（统计每列边缘点数量）

        Args:
            full_image_path: 完整背景图路径
            slider_image_path: 滑块图路径（可选，用于模板匹配）

        Returns:
            float: 缺口中心x坐标相对于图片宽度的比例 (0.0-1.0)
                   失败返回 -1.0
        """
        full_img = cv2.imread(full_image_path, cv2.IMREAD_GRAYSCALE)
        if full_img is None:
            return -1.0

        # 方法1：边缘检测 + 轮廓分析
        blurred = cv2.GaussianBlur(full_img, (5, 5), 0)
        edges = cv2.Canny(blurred, 50, 150)
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if contours:
            largest = max(contours, key=cv2.contourArea)
            x, y, w, h = cv2.boundingRect(largest)
            # 排除过大/过小的轮廓（通常是边框或噪点）
            area_ratio = (w * h) / (full_img.shape[1] * full_img.shape[0])
            if 0.01 < area_ratio < 0.3:
                gap_center_x = x + w // 2
                return gap_center_x / full_img.shape[1]

        # 方法2：边缘密度法（Fallback）
        return self._edge_density_method(full_img)

    def _edge_density_method(self, gray_img: np.ndarray) -> float:
        """
        边缘密度法：计算每列的边缘点数量

        原理：缺口处有明显的边缘（左右边界），所以边缘点数量峰值就是缺口位置
        """
        edges = cv2.Canny(gray_img, 50, 150)
        col_sums = np.sum(edges, axis=0)

        # 只在中间80%范围内找峰值（排除图片边缘）
        mid_start = int(len(col_sums) * 0.1)
        mid_end = int(len(col_sums) * 0.9)
        mid_section = col_sums[mid_start:mid_end]

        peak_idx = np.argmax(mid_section) + mid_start
        return peak_idx / len(col_sums)

    def _edge_match_method(self, full_img: np.ndarray,
                           template: np.ndarray) -> float:
        """
        滑块模板匹配法（当有滑块图时使用）

        使用 TM_CCOEFF_NORMED 模板匹配
        """
        if template is None or len(template.shape) != 2:
            return -1.0
        full_gray = cv2.cvtColor(full_img, cv2.COLOR_RGB2GRAY) if len(full_img.shape) == 3 else full_img
        result = cv2.matchTemplate(full_gray, template, cv2.TM_CCOEFF_NORMED)
        _, _, _, max_loc = cv2.minMaxLoc(result)
        return max_loc[0] / full_img.shape[1]

    def generate_track(self, distance: float,
                       total_width: int,
                       total_steps: int = 50) -> List[Tuple[int, int, int]]:
        """
        生成模拟人类滑动的轨迹

        轨迹特点：
        1. 慢启动（开始20%距离慢速）
        2. 中速前进有抖动（中间60%）
        3. 接近目标减速（最后20%）
        4. 5%概率出现小幅回退（模拟松手习惯）

        Args:
            distance: 缺口距离占图片宽度的比例 (0.0-1.0)
            total_width: 图片总宽度（像素）
            total_steps: 总步数

        Returns:
            List[(x_offset, y_offset, delay_ms)]
            x_offset: 相对起始点的x位移
            y_offset: y方向微抖动
            delay_ms: 距离上次的时间间隔
        """
        target_x = int(distance * total_width)
        track: List[Tuple[int, int, int]] = []
        x = 0
        y = 0
        current_time = 0

        # 阶段1：慢启动（0-30%）
        phase1_end = int(target_x * 0.3)
        while x < phase1_end:
            step = random.randint(3, 8)
            delay = random.randint(30, 80)
            x = min(x + step, phase1_end)
            current_time += delay
            track.append((x, y, current_time))

        # 阶段2：中速前进+抖动（30%-80%）
        phase2_end = int(target_x * 0.8)
        while x < phase2_end:
            jitter = random.randint(-3, 12)
            step = random.randint(10, 25)
            delay = random.randint(15, 40)
            x = min(x + step + jitter, phase2_end)
            y = random.randint(-2, 2)
            current_time += delay
            track.append((x, y, current_time))

            # 5%概率小幅回退
            if random.random() < 0.05:
                back_x = max(x - random.randint(5, 15), phase1_end)
                track.append((back_x, y, current_time + random.randint(10, 30)))

        # 阶段3：接近目标减速（80%-100%）
        while x < target_x:
            step = random.randint(2, 6)
            delay = random.randint(60, 120)
            x = min(x + step, target_x)
            current_time += delay
            track.append((x, y, current_time))

        # 阶段4：过冲回调（模拟人推到位的习惯）
        if target_x - x < 5:
            overshoot = min(x + random.randint(3, 8), total_width)
            track.append((overshoot, y, current_time + 50))
            current_time += 50
            track.append((x, y, current_time + random.randint(30, 80)))

        return track

    def solve_slider(self, full_image_path: str,
                     slider_image_path: Optional[str] = None) -> List[dict]:
        """
        完整滑块解决流程

        Args:
            full_image_path: 背景图路径
            slider_image_path: 滑块图路径（可选）

        Returns:
            List[dict]: 轨迹步骤列表，每步包含 {'x': int, 'y': int, 'delay': int}
        """
        gap_ratio = self.detect_gap(full_image_path, slider_image_path)
        if gap_ratio < 0:
            return []

        full_img = cv2.imread(full_image_path)
        if full_img is None:
            return []

        total_width = full_img.shape[1]
        track_tuples = self.generate_track(gap_ratio, total_width)

        return [
            {'x': x, 'y': y, 'delay': delay}
            for x, y, delay in track_tuples
        ]

    def solve_slider_as_item(self, full_image_path: str,
                              slider_image_path: Optional[str] = None,
                              platform: str = "slider") -> CaptchaResult:
        """
        以StructuredItem格式返回滑块识别结果
        """
        start = time.time()
        track = self.solve_slider(full_image_path, slider_image_path)
        gap_ratio = self.detect_gap(full_image_path, slider_image_path)

        item = CaptchaResult(
            title="slider_captcha",
            url=full_image_path,
            platform=platform,
            content=str(track),
            captcha_type="slider",
            confidence=0.8 if gap_ratio >= 0 else 0.0,
            raw_id=f"gap_{int(gap_ratio * 1000)}" if gap_ratio >= 0 else None,
            processing_time_ms=(time.time() - start) * 1000,
        )
        return item


def solve_slider_with_playwright(page, slider_selector: str, track: List[dict], by: str = 'css'):
    """
    在Playwright中执行滑块轨迹

    Args:
        page: playwright.Page 对象
        slider_selector: 滑块元素选择器
        track: generate_track() 返回的轨迹列表
        by: 选择器类型 ('css' 或 'xpath')
    """
    locator = page.locator(f'xpath={slider_selector}') if by == 'xpath' else page.locator(slider_selector)

    for step in track:
        if step['delay'] > 0:
            time.sleep(step['delay'] / 1000)
        locator.hover(position={'x': 5, 'y': 5})
        page.mouse.down()
        page.mouse.move(step['x'], step['y'])

    page.mouse.up()


# ---- CLI Entrance ----

def main():
    import argparse
    parser = argparse.ArgumentParser(description='Captcha Solver CLI')
    parser.add_argument('command', choices=['recognize', 'slider', 'test'],
                        help='子命令')
    parser.add_argument('image_path', nargs='?', help='图片路径')
    parser.add_argument('--beta', action='store_true', help='启用beta模型')
    parser.add_argument('--preprocess', action='store_true', help='使用预处理')
    args = parser.parse_args()

    if args.command == 'test':
        print(f"ddddocr available: {DDDDOCR_AVAILABLE}")
        print(f"pytesseract available: {PYTESSERACT_AVAILABLE}")
        return 0

    if not args.image_path:
        parser.print_help()
        return 1

    if args.command == 'recognize':
        solver = CaptchaSolver(beta=args.beta)
        if args.preprocess:
            result = solver.solve_with_preprocess(args.image_path)
        else:
            with open(args.image_path, 'rb') as f:
                result = solver.solve_image(f.read())
        print(f"Result: {result}")
        return 0

    if args.command == 'slider':
        slider = SliderCaptchaSolver()
        track = slider.solve_slider(args.image_path)
        print(f"Gap ratio: {slider.detect_gap(args.image_path):.3f}")
        print(f"Track steps: {len(track)}")
        for step in track[:5]:
            print(f"  {step}")
        return 0


if __name__ == '__main__':
    import sys
    sys.exit(main())
