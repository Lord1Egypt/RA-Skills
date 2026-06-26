#!/usr/bin/env python3
"""
图表识别扩展模块
支持饼图、柱状图、折线图、表格等图表的数据提取。

这一版重点提升：
- 更稳的图表类型检测
- 对大图中的多图表场景做分块识别
- 饼图/柱状图/折线图以“结构线索 + OCR 文本”联合提取
- 保持原有 CLI 兼容
"""

from __future__ import annotations

import argparse
import json
import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Tuple
import math

import cv2
import numpy as np
import pytesseract


@dataclass
class ChartRegion:
    x: int
    y: int
    w: int
    h: int
    chart_type: str
    score: float

    def as_dict(self) -> Dict[str, Any]:
        return {
            "x": self.x,
            "y": self.y,
            "w": self.w,
            "h": self.h,
            "chart_type": self.chart_type,
            "score": round(self.score, 3),
        }


class ChartOCR:
    def __init__(self, lang: str = "chi_sim+eng", psm: int = 6):
        self.lang = lang
        self.psm = psm

        # 自定义 OCR 配置：不要在中文场景对白名单过度收窄，否则标题/图例中文会被误杀。
        lang_part = f"-l {lang}"
        self.digit_config = f"--psm 6 --oem 3 {lang_part} -c tessedit_char_whitelist=0123456789.,-% -c preserve_interword_spaces=1"
        self.axis_config = f"--psm 7 --oem 3 {lang_part} -c preserve_interword_spaces=1"
        self.legend_config = f"--psm 6 --oem 3 {lang_part} -c preserve_interword_spaces=1"
        self.title_config = f"--psm 6 --oem 3 {lang_part} -c preserve_interword_spaces=1"

        # 原有配置
        self.config = f"--psm {psm} --oem 3 -l {lang}"
        self.sparse_config = f"--psm 11 --oem 3 -l {lang}"
        self.line_config = f"--psm 6 --oem 3 -l {lang}"
        self.num_pattern = re.compile(r"-?\d+(?:\.\d+)?")


    def _split_card_regions(self, image: np.ndarray) -> Dict[str, np.ndarray]:
        h, w = image.shape[:2]
        title = image[0:int(h * 0.16), :]
        bottom = image[int(h * 0.80):h, :]
        right = image[:, int(w * 0.62):w]
        left = image[:, 0:int(w * 0.18)]
        plot = image[int(h * 0.14):int(h * 0.82), int(w * 0.12):int(w * 0.95)]
        return {
            "title": title,
            "bottom": bottom,
            "right": right,
            "left": left,
            "plot": plot,
        }

    def _sanitize_ocr_label(self, text: str) -> str:
        text = re.sub(r"[|/\\_=*~`'\"]+", " ", text)
        text = re.sub(r"\s+", " ", text).strip(" :-—_.,，。:：")
        return text

    def _is_probable_axis_tick(self, text: str) -> bool:
        t = text.strip()
        if not t:
            return True
        if re.fullmatch(r"[0-9.,%]+", t):
            return True
        if re.fullmatch(r"[0-9.,%-]+[kKmMwW万千百]?", t):
            return True
        return False

    def _find_dominant_circle(self, image: np.ndarray) -> Tuple[Tuple[int, int] | None, int | None]:
        gray = self._gray(image)
        h, w = gray.shape[:2]
        circles = cv2.HoughCircles(
            gray,
            cv2.HOUGH_GRADIENT,
            dp=1.2,
            minDist=max(20, min(h, w) // 6),
            param1=80,
            param2=24,
            minRadius=max(18, min(h, w) // 10),
            maxRadius=max(28, min(h, w) // 2),
        )
        if circles is None or len(circles[0]) == 0:
            return None, None
        best = max(circles[0], key=lambda c: c[2])
        return (int(best[0]), int(best[1])), int(best[2])

    def _collect_pie_legend_lines(self, parts: Dict[str, np.ndarray], center: Tuple[int, int] | None, radius: int | None) -> List[str]:
        lines: List[str] = []
        lines.extend(self._ocr_lines(parts["right"], self.sparse_config))
        lines.extend(self._ocr_lines(parts["bottom"], self.sparse_config))
        if center is not None and radius is not None:
            plot = parts["plot"]
            ph, pw = plot.shape[:2]
            mask = np.ones((ph, pw), dtype=np.uint8) * 255
            cv2.circle(mask, center, int(radius * 1.08), 0, -1)
            outside = cv2.bitwise_and(plot, plot, mask=mask)
            lines.extend(self._ocr_lines(outside, self.sparse_config))
        # 去重保序
        seen = set()
        out = []
        for line in lines:
            s = line.strip()
            if s and s not in seen:
                seen.add(s)
                out.append(s)
        return out

    def _estimate_line_points_from_plot(self, plot: np.ndarray) -> List[Dict[str, float]]:
        gray = self._gray(plot)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        edges = cv2.Canny(blur, 50, 150)
        lines = cv2.HoughLinesP(
            edges,
            1,
            np.pi / 180,
            threshold=35,
            minLineLength=max(20, min(plot.shape[:2]) // 8),
            maxLineGap=18,
        )
        points: List[Tuple[float, float]] = []
        if lines is not None:
            for line in lines[:, 0]:
                x1, y1, x2, y2 = map(float, line)
                dx = abs(x2 - x1)
                dy = abs(y2 - y1)
                if dx < 10:
                    continue
                if dy < 4:
                    continue
                if dx > dy * 6:
                    continue
                points.append((x1, y1))
                points.append((x2, y2))
        if not points:
            return []
        points.sort(key=lambda p: (p[0], p[1]))
        merged: List[Tuple[float, float]] = []
        for x, y in points:
            if not merged or abs(x - merged[-1][0]) > 18:
                merged.append((x, y))
            else:
                px, py = merged[-1]
                merged[-1] = ((px + x) / 2.0, min(py, y))
        ph = max(1, plot.shape[0] - 1)
        result = []
        for i, (x, y) in enumerate(merged, start=1):
            result.append({
                "x": float(i),
                "y": round(float((ph - y) / ph), 4),
                "pixel_x": round(x, 2),
                "pixel_y": round(y, 2),
            })
        return result

    def preprocess_image(self, image_path: str) -> np.ndarray:
        img = cv2.imread(image_path)
        if img is None:
            raise ValueError(f"无法加载图像: {image_path}")
        return img

    def _gray(self, image: np.ndarray) -> np.ndarray:
        if len(image.shape) == 2:
            return image
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    def _binary(self, image: np.ndarray) -> np.ndarray:
        gray = self._gray(image)
        blur = cv2.GaussianBlur(gray, (3, 3), 0)
        return cv2.adaptiveThreshold(
            blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 31, 8
        )

    def _ocr_text(self, image: np.ndarray, config: str | None = None) -> str:
        cfg = config or self.config
        return pytesseract.image_to_string(image, config=cfg).strip()

    def _ocr_confidence(self, image: np.ndarray, config: str | None = None) -> Dict[str, Any]:
        cfg = config or self.config
        try:
            data = pytesseract.image_to_data(image, config=cfg, output_type=pytesseract.Output.DICT)
        except Exception:
            return {"avg_conf": None, "word_count": 0, "low_conf_words": 0}
        confs = []
        low = 0
        for text, conf_raw in zip(data.get("text", []), data.get("conf", [])):
            if not str(text).strip():
                continue
            try:
                conf = float(conf_raw)
            except Exception:
                continue
            if conf < 0:
                continue
            confs.append(conf)
            if conf < 55:
                low += 1
        if not confs:
            return {"avg_conf": None, "word_count": 0, "low_conf_words": 0}
        return {"avg_conf": round(sum(confs) / len(confs), 2), "word_count": len(confs), "low_conf_words": low}

    def _quality_notes(self, result: Dict[str, Any]) -> List[str]:
        notes: List[str] = []
        region = result.get("selected_region") or result.get("region")
        if region and float(region.get("score", 0)) < 0.35:
            notes.append("图表类型判断分数偏低，建议查看 --visualize 输出并人工确认区域/类型")
        raw_text = "\n".join(result.get("raw_lines", []) or [])
        if not raw_text and not result.get("title"):
            notes.append("OCR 文本较少，建议提高图片分辨率或裁剪到图表主体")
        if result.get("chart_type") in {"bar", "line", "pie"}:
            numbers = []
            for line in result.get("raw_lines", []) or []:
                numbers.extend(self._extract_numbers(line))
            if len(numbers) < 2 and not result.get("data_points") and not result.get("series"):
                notes.append("数值提取偏少，建议使用更清晰图片或手动指定 --chart-type")
        return notes

    def _ocr_lines(self, image: np.ndarray, config: str | None = None) -> List[str]:
        text = self._ocr_text(image, config=config)
        return [line.strip() for line in text.splitlines() if line.strip()]

    def _extract_numbers(self, text: str) -> List[float]:
        out: List[float] = []
        for item in self.num_pattern.findall(text):
            try:
                out.append(float(item))
            except Exception:
                pass
        return out

    def _find_chart_regions(self, image: np.ndarray) -> List[ChartRegion]:
        h, w = image.shape[:2]
        candidates: List[ChartRegion] = []

        # 固定分块：适合示例图这类 dashboard / collage 图片
        grid = [
            (0.00, 0.00, 0.50, 0.52),
            (0.50, 0.00, 0.50, 0.52),
            (0.00, 0.52, 0.50, 0.48),
            (0.50, 0.52, 0.50, 0.48),
        ]
        for idx, (rx, ry, rw, rh) in enumerate(grid):
            x = int(w * rx)
            y = int(h * ry)
            ww = int(w * rw)
            hh = int(h * rh)
            roi = image[y:y + hh, x:x + ww]
            chart_type, score = self._classify_region(roi)
            # 对四宫格区域轻微加权，避免整图候选抢分
            score += 0.08
            candidates.append(ChartRegion(x, y, ww, hh, chart_type, score))

        # 如果整图更像单图，也补一个全图候选，但默认降权
        chart_type, score = self._classify_region(image)
        score *= 0.72
        candidates.append(ChartRegion(0, 0, w, h, chart_type, score))

        return sorted(candidates, key=lambda r: r.score, reverse=True)

    def _classify_region(self, image: np.ndarray) -> Tuple[str, float]:
        parts = self._split_card_regions(image)
        gray = self._gray(parts["plot"])
        binary = self._binary(parts["plot"])
        h, w = gray.shape[:2]

        # 圆检测：偏饼图
        circles = cv2.HoughCircles(
            gray,
            cv2.HOUGH_GRADIENT,
            dp=1.2,
            minDist=max(20, min(h, w) // 6),
            param1=80,
            param2=24,
            minRadius=max(18, min(h, w) // 10),
            maxRadius=max(28, min(h, w) // 2),
        )
        circle_count = 0
        largest_circle_ratio = 0.0
        if circles is not None and len(circles[0]) > 0:
            circle_count = len(circles[0])
            largest_r = max(c[2] for c in circles[0])
            largest_circle_ratio = float(largest_r) / max(1.0, min(h, w))

        # 直线检测：偏柱状图/折线图/表格
        lines = cv2.HoughLinesP(
            binary,
            1,
            np.pi / 180,
            threshold=60,
            minLineLength=max(18, min(h, w) // 10),
            maxLineGap=10,
        )
        horizontal = 0
        vertical = 0
        diagonal = 0
        if lines is not None:
            for line in lines[:, 0]:
                x1, y1, x2, y2 = line
                dx = x2 - x1
                dy = y2 - y1
                if abs(dx) > abs(dy) * 3:
                    horizontal += 1
                elif abs(dy) > abs(dx) * 3:
                    vertical += 1
                else:
                    diagonal += 1

        # 文本辅助线索：主要看标题 + 底部 + 右侧图例
        lines_text = []
        lines_text.extend(self._ocr_lines(parts["title"], self.line_config))
        lines_text.extend(self._ocr_lines(parts["bottom"], self.sparse_config))
        lines_text.extend(self._ocr_lines(parts["right"], self.sparse_config))
        text_blob = " ".join(lines_text)
        numeric_lines = sum(1 for line in lines_text if len(self._extract_numbers(line)) >= 1)
        pair_lines = sum(1 for line in lines_text if len(self._extract_numbers(line)) >= 2)

        pie_keywords = ["饼", "占比", "%", "进度", "分布", "状态分布"]
        bar_keywords = ["柱", "统计", "数量", "排行", "TOP", "top", "监控"]
        line_keywords = ["折线", "趋势", "曲线", "周", "月", "日", "走势"]

        pie_kw = sum(1 for kw in pie_keywords if kw in text_blob)
        bar_kw = sum(1 for kw in bar_keywords if kw in text_blob)
        line_kw = sum(1 for kw in line_keywords if kw in text_blob)

        pie_score = 0.0
        if circle_count > 0 and largest_circle_ratio >= 0.12:
            pie_score = min(1.0, 0.42 + 0.16 * min(circle_count, 2) + 0.65 * min(largest_circle_ratio, 0.35))
        pie_score += min(0.24, pie_kw * 0.08)

        table_score = 0.0
        if horizontal >= 6 and vertical >= 6:
            table_score = min(1.0, 0.3 + 0.04 * min(horizontal, 10) + 0.04 * min(vertical, 10))

        bar_score = 0.0
        if vertical >= 3 and horizontal >= 2:
            bar_score = min(1.0, 0.24 + 0.05 * min(vertical, 10) + 0.03 * min(horizontal, 8))
        if numeric_lines >= 3:
            bar_score += 0.05
        bar_score += min(0.22, bar_kw * 0.08)

        line_score = 0.0
        if diagonal >= 2 and horizontal >= 1:
            line_score = min(1.0, 0.24 + 0.08 * min(diagonal, 10) + 0.03 * min(horizontal, 5))
        if pair_lines >= 2:
            line_score += 0.08
        line_score += min(0.28, line_kw * 0.1)

        if "状态分布" in text_blob:
            pie_score += 0.18
        if any(kw in text_blob for kw in ["折线图", "趋势图", "趋势", "走势"]):
            line_score += 0.24
            pie_score *= 0.45

        # 没有明显大圆时，别轻易判饼图
        if largest_circle_ratio < 0.14:
            pie_score *= 0.28
        # 有连续斜线和时间关键词时，更像趋势图
        if diagonal >= 4:
            line_score += 0.12
        # 竖线显著但斜线弱，更像柱状图
        if vertical >= 5 and diagonal <= 2:
            bar_score += 0.08

        scores = {
            "pie": pie_score,
            "table": table_score,
            "bar": bar_score,
            "line": line_score,
        }
        chart_type = max(scores, key=scores.get)
        best_score = scores[chart_type]
        if best_score < 0.2:
            chart_type = "unknown"
        return chart_type, float(best_score)

    def detect_chart_type(self, image: np.ndarray) -> str:
        return self._classify_region(image)[0]

    def extract_text_from_regions(self, image: np.ndarray, regions: List[Tuple[int, int, int, int]]) -> List[str]:
        texts = []
        for (x, y, w, h) in regions:
            roi = image[y:y + h, x:x + w]
            texts.append(self._ocr_text(roi))
        return texts

    def _find_pie_legend_pairs(self, image: np.ndarray, center: Tuple[int, int] | None, radius: int | None) -> List[Tuple[str, float]]:
        """
        在饼图周围区域寻找图例 marker 与文本的配对
        返回: [(label, value), ...]
        """
        if center is None or radius is None:
            return []

        h, w = image.shape[:2]
        ph, pw = h, w

        # 定义图例区域（右侧和底部）
        legend_regions = []
        if pw > 0:
            right_region = image[:, int(pw * 0.65):pw]
            legend_regions.append(("right", right_region, int(pw * 0.65), 0))
        if ph > 0:
            bottom_region = image[int(ph * 0.75):ph, :]
            legend_regions.append(("bottom", bottom_region, 0, int(ph * 0.75)))

        pairs = []
        for region_name, region_img, offset_x, offset_y in legend_regions:
            if region_img.size == 0:
                continue
            gray = self._gray(region_img)
            # 二值化找 marker
            _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
            contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            markers = []
            for cnt in contours:
                area = cv2.contourArea(cnt)
                if 8 < area < 120:
                    x, y, w_box, h_box = cv2.boundingRect(cnt)
                    if 2 < w_box < 22 and 2 < h_box < 22:
                        markers.append((x + w_box // 2, y + h_box // 2))

            # OCR 文本
            lines = self._ocr_lines(region_img, self.sparse_config)
            text_blocks = []
            for i, line in enumerate(lines):
                clean = line.strip()
                if not clean or len(clean) > 24:
                    continue
                text_blocks.append({
                    "text": clean,
                    "y": i * 18,
                    "index": i,
                })

            # 简单配对：按垂直位置对齐 marker 与文本
            for mx, my in markers:
                best_text = None
                best_dist = float('inf')
                for tb in text_blocks:
                    dist = abs(my - tb["y"])
                    if dist < best_dist and dist < 24:
                        best_dist = dist
                        best_text = tb["text"]
                if best_text:
                    numbers = self._extract_numbers(best_text)
                    value = numbers[0] if numbers else 0.0
                    pairs.append((best_text, value))

        return pairs

    def _find_chart_body(self, image: np.ndarray) -> Tuple[np.ndarray, Tuple[int, int, int, int]]:
        """
        基于边缘/颜色/纹理检测图表主体
        返回: (chart_body, (x, y, w, h))
        """
        h, w = image.shape[:2]
        if h == 0 or w == 0:
            return image, (0, 0, w, h)

        gray = self._gray(image)
        # 边缘检测
        edges = cv2.Canny(gray, 50, 150)
        # 形态学操作
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        closed = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)
        # 找轮廓
        contours, _ = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        best_box = None
        best_score = 0

        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area < 200:
                continue
            x, y, w_box, h_box = cv2.boundingRect(cnt)
            # 过滤太小的区域
            if w_box < w * 0.2 or h_box < h * 0.2:
                continue
            # 过滤太细长的区域
            if w_box > h_box * 8 or h_box > w_box * 8:
                continue
            # 评分：面积占比 + 位置权重
            area_ratio = area / (w * h)
            center_x = x + w_box // 2
            center_y = y + h_box // 2
            center_score = 1.0 - abs(center_x - w // 2) / w - abs(center_y - h // 2) / h
            score = area_ratio * 0.7 + center_score * 0.3
            if score > best_score:
                best_score = score
                best_box = (x, y, w_box, h_box)

        if best_box is None:
            return image, (0, 0, w, h)

        x, y, w_box, h_box = best_box
        chart_body = image[y:y + h_box, x:x + w_box]
        return chart_body, best_box

    def _perspective_correct(self, image: np.ndarray) -> np.ndarray:
        """
        基于角点检测进行透视矫正
        """
        h, w = image.shape[:2]
        if h == 0 or w == 0:
            return image

        gray = self._gray(image)
        # 找角点
        corners = cv2.goodFeaturesToTrack(gray, 20, 0.01, 10)
        if corners is None or len(corners) < 4:
            return image

        corners = np.intp(corners)
        points = [(corner[0][0], corner[0][1]) for corner in corners]
        # 找四个角点
        points = sorted(points, key=lambda p: p[0] + p[1])
        tl = points[0]
        br = points[-1]
        points = sorted(points, key=lambda p: p[0] - p[1])
        tr = points[-1]
        bl = points[0]

        # 目标点
        max_width = max(int(br[0] - tl[0]), int(tr[0] - bl[0]))
        max_height = max(int(br[1] - tl[1]), int(tr[1] - bl[1]))
        dst_points = np.float32([[0, 0], [max_width, 0], [0, max_height], [max_width, max_height]])
        src_points = np.float32([tl, tr, bl, br])

        # 透视变换
        matrix = cv2.getPerspectiveTransform(src_points, dst_points)
        corrected = cv2.warpPerspective(image, matrix, (max_width, max_height))
        return corrected

    def extract_pie_chart_data(self, image: np.ndarray) -> Dict[str, Any]:
        # 新增：图表主体检测
        chart_body, (x, y, w_box, h_box) = self._find_chart_body(image)
        # 新增：透视矫正
        chart_body = self._perspective_correct(chart_body)

        parts = self._split_card_regions(chart_body)
        plot = parts["plot"]
        center, radius = self._find_dominant_circle(plot)
        header_lines = self._ocr_lines(parts["title"], self.title_config)
        legend_lines = self._collect_pie_legend_lines(parts, center, radius)

        # 新增：图例 marker 与文本配对
        legend_pairs = self._find_pie_legend_pairs(plot, center, radius)

        segments = []
        total_value = 0.0
        seen_labels = set()

        # 优先使用配对结果
        for label, value in legend_pairs:
            if label in seen_labels:
                continue
            seen_labels.add(label)
            percentage = 0.0
            if 0 < value <= 100:
                percentage = value
            segments.append({
                "label": label,
                "value": value,
                "percentage": percentage,
                "color": None,
                "raw": label,
            })
            total_value += value

        # 兜底：如果配对结果太少，用传统 OCR 方式补充
        if len(segments) < 2:
            for line in legend_lines:
                clean = line.strip()
                numbers = self._extract_numbers(clean)
                if not numbers:
                    continue
                if self._is_probable_axis_tick(clean):
                    continue
                label = re.sub(self.num_pattern, " ", clean)
                label = self._sanitize_ocr_label(label)
                if not label or label in seen_labels:
                    continue
                seen_labels.add(label)
                value = numbers[0]
                percentage = 0.0
                if len(numbers) >= 2 and 0 <= numbers[1] <= 100:
                    percentage = numbers[1]
                elif "%" in clean and 0 <= value <= 100:
                    percentage = value
                segments.append({
                    "label": label,
                    "value": value,
                    "percentage": percentage,
                    "color": None,
                    "raw": clean,
                })
                total_value += value

        if not segments:
            # 兜底：至少保留图例原文，避免空结果
            for line in legend_lines[:6]:
                label = self._sanitize_ocr_label(line)
                if label and label not in seen_labels:
                    seen_labels.add(label)
                    segments.append({
                        "label": label,
                        "value": 0.0,
                        "percentage": 0.0,
                        "color": None,
                        "raw": line,
                    })

        return {
            "chart_type": "pie",
            "total_value": total_value,
            "segments": segments,
            "center": center,
            "radius": radius,
            "title": " ".join(header_lines[:2]).strip(),
            "legend_lines": legend_lines,
            "chart_body_box": (x, y, w_box, h_box),
        }


    def _find_bar_categories_and_values(self, image: np.ndarray) -> Tuple[List[str], List[float]]:
        """
        基于坐标轴位置分离类目与数值
        返回: (categories, values)
        """
        h, w = image.shape[:2]
        if h == 0 or w == 0:
            return [], []

        gray = self._gray(image)
        # 检测水平线（X轴）
        edges = cv2.Canny(gray, 50, 150)
        lines = cv2.HoughLinesP(
            edges,
            1,
            np.pi / 180,
            threshold=20,
            minLineLength=max(30, w // 4),
            maxLineGap=12,
        )

        x_axis_y = None
        if lines is not None:
            for line in lines[:, 0]:
                x1, y1, x2, y2 = line
                if abs(y2 - y1) < 8 and w * 0.3 < (x2 - x1) < w * 0.95:
                    x_axis_y = (y1 + y2) // 2
                    break

        # 如果没有检测到 X 轴，用底部 10% 位置
        if x_axis_y is None:
            x_axis_y = int(h * 0.9)

        # 分割区域
        title_region = image[0:int(h * 0.2), :]
        plot_region = image[int(h * 0.2):x_axis_y, :]
        axis_region = image[x_axis_y:h, :]

        # OCR 各区域（防越界）
        categories = []
        values = []

        if title_region.size > 0 and title_region.shape[0] > 8 and title_region.shape[1] > 8:
            title_lines = self._ocr_lines(title_region, self.line_config)
            for line in title_lines:
                clean = line.strip()
                numbers = self._extract_numbers(clean)
                if numbers and not self._is_probable_axis_tick(clean):
                    continue
                label = re.sub(self.num_pattern, " ", clean)
                label = self._sanitize_ocr_label(label)
                if label and len(label) < 18:
                    categories.append(label)

        if plot_region.size > 0 and plot_region.shape[0] > 8 and plot_region.shape[1] > 8:
            plot_lines = self._ocr_lines(plot_region, self.sparse_config)
            for line in plot_lines:
                numbers = self._extract_numbers(line)
                if not numbers:
                    continue
                if self._is_probable_axis_tick(line):
                    continue
                value = numbers[-1]
                values.append(value)

        if axis_region.size > 0 and axis_region.shape[0] > 8 and axis_region.shape[1] > 8:
            axis_lines = self._ocr_lines(axis_region, self.sparse_config)
            axis_cats = []
            for line in axis_lines:
                clean = line.strip()
                numbers = self._extract_numbers(clean)
                if numbers and not self._is_probable_axis_tick(clean):
                    continue
                label = re.sub(self.num_pattern, " ", clean)
                label = self._sanitize_ocr_label(label)
                if label and len(label) < 18:
                    axis_cats.append(label)
            if axis_cats:
                categories = axis_cats

    def _detect_lines_and_shapes(self, image: np.ndarray) -> Dict[str, Any]:
        """
        基于 Hough 变换检测线条，基于轮廓检测形状
        返回: {"lines": [...], "shapes": [...]}
        """
        h, w = image.shape[:2]
        if h == 0 or w == 0:
            return {"lines": [], "shapes": []}

        gray = self._gray(image)
        edges = cv2.Canny(gray, 50, 150)

        # 线条检测
        lines = cv2.HoughLinesP(
            edges,
            1,
            np.pi / 180,
            threshold=20,
            minLineLength=max(15, min(w, h) // 8),
            maxLineGap=12,
        )

        line_segments = []
        if lines is not None:
            for line in lines[:, 0]:
                x1, y1, x2, y2 = line
                length = np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
                angle = np.arctan2(y2 - y1, x2 - x1) * 180 / np.pi
                line_segments.append({
                    "x1": int(x1),
                    "y1": int(y1),
                    "x2": int(x2),
                    "y2": int(y2),
                    "length": float(length),
                    "angle": float(angle),
                })

        # 形状检测
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        shapes = []
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area < 30:
                continue
            perimeter = cv2.arcLength(cnt, True)
            if perimeter == 0:
                continue
            circularity = 4 * np.pi * area / (perimeter ** 2)
            x, y, w_box, h_box = cv2.boundingRect(cnt)
            aspect_ratio = w_box / max(1, h_box)
            shapes.append({
                "area": float(area),
                "perimeter": float(perimeter),
                "circularity": float(circularity),
                "x": int(x),
                "y": int(y),
                "w": int(w_box),
                "h": int(h_box),
                "aspect_ratio": float(aspect_ratio),
            })

        return {"lines": line_segments, "shapes": shapes}

    def extract_bar_chart_data(self, image: np.ndarray) -> Dict[str, Any]:
        parts = self._split_card_regions(image)
        title = self._ocr_text(parts["title"], self.title_config)
        x_label = self._ocr_text(parts["bottom"], self.axis_config)
        y_label = self._ocr_text(parts["left"], self.axis_config)
        plot_lines = self._ocr_lines(parts["plot"], self.sparse_config)

        # 新增：基于坐标轴位置分离类目与数值
        cat_val = self._find_bar_categories_and_values(parts["plot"])
        if cat_val is None:
            categories, values = [], []
        else:
            categories, values = cat_val

        # 新增：线条/形状检测
        plot_analysis = self._detect_lines_and_shapes(parts["plot"])

        # 如果分离失败，用传统方式兜底
        if not categories or not values:
            categories = []
            values = []
            raw_pairs = []
            for line in plot_lines:
                numbers = self._extract_numbers(line)
                if not numbers:
                    continue
                if self._is_probable_axis_tick(line):
                    continue
                label = re.sub(self.num_pattern, " ", line)
                label = self._sanitize_ocr_label(label)
                value = numbers[-1]
                if not label and len(numbers) == 1:
                    continue
                categories.append(label or f"类别{len(categories) + 1}")
                values.append(value)
                raw_pairs.append({"raw": line, "label": label or f"类别{len(categories)}", "value": value})
        else:
            raw_pairs = []
            for i, (cat, val) in enumerate(zip(categories, values)):
                raw_pairs.append({"raw": f"{cat} {val}", "label": cat, "value": val})

        return {
            "chart_type": "bar",
            "categories": categories,
            "values": values,
            "x_label": x_label,
            "y_label": y_label,
            "title": title,
            "raw_lines": plot_lines,
            "data_pairs": raw_pairs,
            "plot_analysis": plot_analysis,
        }



    def _find_line_chart_points(self, image: np.ndarray) -> List[Dict[str, float]]:
        """
        基于坐标轴检测与标尺映射提取数据点
        返回: [{"x": x_val, "y": y_val, "pixel_x": px, "pixel_y": py}, ...]
        """
        h, w = image.shape[:2]
        if h == 0 or w == 0:
            return []

        gray = self._gray(image)
        edges = cv2.Canny(gray, 50, 150)
        lines = cv2.HoughLinesP(
            edges,
            1,
            np.pi / 180,
            threshold=20,
            minLineLength=max(30, min(w, h) // 4),
            maxLineGap=12,
        )

        x_axis_y = None
        y_axis_x = None
        if lines is not None:
            for line in lines[:, 0]:
                x1, y1, x2, y2 = line
                # 水平线（X轴）
                if abs(y2 - y1) < 8 and w * 0.3 < (x2 - x1) < w * 0.95:
                    x_axis_y = (y1 + y2) // 2
                # 垂直线（Y轴）
                elif abs(x2 - x1) < 8 and h * 0.3 < (y2 - y1) < h * 0.95:
                    y_axis_x = (x1 + x2) // 2

        if x_axis_y is None:
            x_axis_y = int(h * 0.85)
        if y_axis_x is None:
            y_axis_x = int(w * 0.15)

        # 提取坐标轴附近文本
        margin = 32
        x_axis_region = image[max(0, x_axis_y - margin):min(h, x_axis_y + margin), :]
        y_axis_region = image[:, max(0, y_axis_x - margin):min(w, y_axis_x + margin)]

        x_ticks = []
        y_ticks = []

        if x_axis_region.size > 0 and x_axis_region.shape[0] > 8 and x_axis_region.shape[1] > 8:
            x_lines = self._ocr_lines(x_axis_region, self.sparse_config)
            for line in x_lines:
                numbers = self._extract_numbers(line)
                if numbers and self._is_probable_axis_tick(line):
                    for num in numbers:
                        x_ticks.append(num)

        if y_axis_region.size > 0 and y_axis_region.shape[0] > 8 and y_axis_region.shape[1] > 8:
            y_lines = self._ocr_lines(y_axis_region, self.sparse_config)
            for line in y_lines:
                numbers = self._extract_numbers(line)
                if numbers and self._is_probable_axis_tick(line):
                    for num in numbers:
                        y_ticks.append(num)

        # 去重排序
        x_ticks = sorted(set(x_ticks))
        y_ticks = sorted(set(y_ticks))

        # 估计数据点
        points = []

        # 基于线条几何估计
        line_points = self._estimate_line_points_from_plot(image)
        for pt in line_points:
            px = pt["pixel_x"]
            py = pt["pixel_y"]
            # 映射到坐标轴
            x_val = None
            y_val = None
            if x_ticks:
                x_val = float(len(x_ticks))
            if y_ticks:
                y_val = pt["y"]
            if x_val is not None and y_val is not None:
                points.append({
                    "x": x_val,
                    "y": y_val,
                    "pixel_x": px,
                    "pixel_y": py,
                })

        # 如果几何估计不够，用 OCR 补充
        if len(points) < 2:
            plot_lines = self._ocr_lines(image, self.sparse_config)
            for idx, line in enumerate(plot_lines, start=1):
                numbers = self._extract_numbers(line)
                if len(numbers) >= 2 and not self._is_probable_axis_tick(line):
                    x_val = numbers[0]
                    y_val = numbers[1]
                    points.append({
                        "x": float(x_val),
                        "y": float(y_val),
                        "pixel_x": 0.0,
                        "pixel_y": 0.0,
                    })
                elif len(numbers) == 1 and not self._is_probable_axis_tick(line):
                    y_val = numbers[0]
                    points.append({
                        "x": float(idx),
                        "y": float(y_val),
                        "pixel_x": 0.0,
                        "pixel_y": 0.0,
                    })

        return points

    def extract_line_chart_data(self, image: np.ndarray) -> Dict[str, Any]:
        parts = self._split_card_regions(image)
        title = self._ocr_text(parts["title"], self.title_config)
        x_label = self._ocr_text(parts["bottom"], self.axis_config)
        y_label = self._ocr_text(parts["left"], self.axis_config)
        plot_lines = self._ocr_lines(parts["plot"], self.sparse_config)

        # 新增：基于坐标轴检测与标尺映射提取数据点
        data_points = self._find_line_chart_points(parts["plot"])

        # 新增：线条/形状检测
        plot_analysis = self._detect_lines_and_shapes(parts["plot"])

        x_values = [pt["x"] for pt in data_points]
        y_values = [pt["y"] for pt in data_points]

        return {
            "chart_type": "line",
            "series": [],
            "x_values": x_values,
            "y_values": y_values,
            "x_label": x_label,
            "y_label": y_label,
            "title": title,
            "data_points": data_points,
            "raw_lines": plot_lines,
            "plot_analysis": plot_analysis,
        }



    def extract_table_data(self, image: np.ndarray) -> Dict[str, Any]:
        lines = self._ocr_lines(image, self.line_config)
        headers: List[str] = []
        rows: List[List[str]] = []
        if lines:
            headers = lines[0].split()
            col_count = len(headers)
            for line in lines[1:]:
                cells = line.split()
                if len(cells) == col_count and col_count > 0:
                    rows.append(cells)
        else:
            col_count = 0

        return {
            "chart_type": "table",
            "headers": headers,
            "rows": rows,
            "row_count": len(rows),
            "col_count": col_count,
            "raw_lines": lines,
        }

    def extract_chart_data(self, image_path: str, chart_types: List[str]) -> Dict[str, Any]:
        image = self.preprocess_image(image_path)
        regions = self._find_chart_regions(image)

        if "auto" in chart_types:
            target_region = regions[0]
            chart_type = target_region.chart_type
        else:
            chart_type = chart_types[0]
            target_region = next((r for r in regions if r.chart_type == chart_type), regions[0])

        roi = image[target_region.y:target_region.y + target_region.h, target_region.x:target_region.x + target_region.w]
        result = self._extract_by_type(chart_type, roi)
        result["selected_region"] = target_region.as_dict()
        result["candidate_regions"] = [r.as_dict() for r in regions[:5]]
        result["quality_notes"] = self._quality_notes(result)
        return result

    def _extract_by_type(self, chart_type: str, image: np.ndarray) -> Dict[str, Any]:
        if chart_type == "pie":
            return self.extract_pie_chart_data(image)
        if chart_type == "bar":
            return self.extract_bar_chart_data(image)
        if chart_type == "line":
            return self.extract_line_chart_data(image)
        if chart_type == "table":
            return self.extract_table_data(image)
        return {
            "chart_type": "unknown",
            "message": "未识别出可靠图表类型",
            "raw_lines": self._ocr_lines(image, self.sparse_config),
        }

    def extract_dashboard_data(self, image_path: str) -> Dict[str, Any]:
        image = self.preprocess_image(image_path)
        regions = self._find_chart_regions(image)
        charts = []
        seen_boxes = set()

        for region in regions[:4]:
            key = (region.x, region.y, region.w, region.h, region.chart_type)
            if key in seen_boxes or region.chart_type == "unknown":
                continue
            seen_boxes.add(key)
            roi = image[region.y:region.y + region.h, region.x:region.x + region.w]
            chart = self._extract_by_type(region.chart_type, roi)
            chart["region"] = region.as_dict()
            chart["quality_notes"] = self._quality_notes(chart)
            charts.append(chart)

        return {
            "chart_type": "dashboard",
            "chart_count": len(charts),
            "charts": charts,
            "candidate_regions": [r.as_dict() for r in regions],
        }

    def visualize_result(self, image_path: str, result: Dict[str, Any], output_path: str) -> str:
        """生成图表识别调试图：候选区域、选中区域、类型和分数。"""
        image = self.preprocess_image(image_path)
        canvas = image.copy()

        def draw_region(region: Dict[str, Any], color: Tuple[int, int, int], label: str, thickness: int = 2) -> None:
            x, y, w, h = int(region.get("x", 0)), int(region.get("y", 0)), int(region.get("w", 0)), int(region.get("h", 0))
            cv2.rectangle(canvas, (x, y), (x + w, y + h), color, thickness)
            text = f"{label} {region.get('chart_type', '?')} {region.get('score', '')}"
            text = text.strip()
            y_text = max(18, y - 6)
            cv2.rectangle(canvas, (x, y_text - 18), (min(canvas.shape[1] - 1, x + max(160, len(text) * 9)), y_text + 4), color, -1)
            cv2.putText(canvas, text, (x + 4, y_text), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)

        candidate_regions = result.get("candidate_regions", [])
        for idx, region in enumerate(candidate_regions[:12], start=1):
            draw_region(region, (180, 180, 180), f"cand{idx}", thickness=1)

        if result.get("chart_type") == "dashboard":
            for idx, chart in enumerate(result.get("charts", []), start=1):
                region = chart.get("region")
                if region:
                    draw_region(region, (0, 180, 255), f"chart{idx}", thickness=3)
        elif result.get("selected_region"):
            draw_region(result["selected_region"], (0, 80, 255), "selected", thickness=3)

        out = Path(output_path).expanduser().resolve()
        out.parent.mkdir(parents=True, exist_ok=True)
        if not cv2.imwrite(str(out), canvas):
            raise RuntimeError(f"无法写入可视化图片: {out}")
        return str(out)


class DashboardOCR:
    def __init__(self, lang: str = "chi_sim+eng", psm: int = 6):
        self.chart_ocr = ChartOCR(lang=lang, psm=psm)

    def analyze(self, image_path: str) -> Dict[str, Any]:
        return self.chart_ocr.extract_dashboard_data(image_path)


def main() -> None:
    parser = argparse.ArgumentParser(description="图表识别扩展工具")
    parser.add_argument("image_path", help="图片路径")
    parser.add_argument("--chart-type", choices=["auto", "pie", "bar", "line", "table", "dashboard"], default="auto", help="图表类型")
    parser.add_argument("--lang", default="chi_sim+eng", help="OCR语言")
    parser.add_argument("--psm", type=int, default=6, help="Tesseract PSM模式")
    parser.add_argument("--extract-numbers", action="store_true", help="提取数值")
    parser.add_argument("--extract-labels", action="store_true", help="提取标签")
    parser.add_argument("--visualize", action="store_true", help="生成图表识别可视化调试图")
    parser.add_argument("--visualize-output", help="可视化图片输出路径；默认根据输入文件生成 *_debug.png")
    parser.add_argument("--json", action="store_true", help="以JSON格式输出")
    parser.add_argument("--output", "-o", help="输出文件路径")
    args = parser.parse_args()

    chart_ocr = ChartOCR(lang=args.lang, psm=args.psm)

    if args.chart_type == "dashboard":
        result = chart_ocr.extract_dashboard_data(args.image_path)
    elif args.chart_type == "auto":
        result = chart_ocr.extract_chart_data(args.image_path, ["auto"])
    else:
        result = chart_ocr.extract_chart_data(args.image_path, [args.chart_type])

    if args.visualize:
        if args.visualize_output:
            visualize_output = args.visualize_output
        else:
            src = Path(args.image_path)
            visualize_output = str(src.with_name(f"{src.stem}_debug.png"))
        result["visualization"] = chart_ocr.visualize_result(args.image_path, result, visualize_output)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"结果已保存到: {args.output}")
    elif args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print("\n=== 图表识别结果 ===")
        print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
