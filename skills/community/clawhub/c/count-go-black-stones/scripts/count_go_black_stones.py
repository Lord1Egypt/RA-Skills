#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import math
import sys
from collections import deque
from dataclasses import dataclass
from pathlib import Path

try:
    import cv2
    import numpy as np
    from PIL import Image, ImageDraw, ImageFont
except ImportError as exc:
    raise SystemExit(
        "Missing dependency. Install with: "
        "python3 -m pip install -r scripts/requirements.txt"
    ) from exc


CHINESE_RULE_BLACK_KOMI_STONES = 3.75


@dataclass
class GridFit:
    offset: float
    spacing: float
    score: float
    coverage: int
    candidates: int


def read_image(path: Path) -> np.ndarray:
    data = np.fromfile(str(path), dtype=np.uint8)
    image = cv2.imdecode(data, cv2.IMREAD_COLOR)
    if image is None:
        raise SystemExit(f"Could not read image: {path}")
    return image


def write_image(path: Path, image: np.ndarray) -> None:
    ext = path.suffix or ".jpg"
    ok, encoded = cv2.imencode(ext, image)
    if not ok:
        raise SystemExit(f"Could not encode overlay as {ext}")
    encoded.tofile(str(path))


def parse_corners(raw: str) -> np.ndarray:
    parts = raw.replace(";", " ").split()
    if len(parts) != 4:
        raise SystemExit("--corners expects four points, e.g. '74,76 1100,53 1118,1031 72,1034'")
    pts = []
    for part in parts:
        xy = part.split(",")
        if len(xy) != 2:
            raise SystemExit(f"Bad corner point: {part}")
        pts.append([float(xy[0]), float(xy[1])])
    return np.array(pts, dtype=np.float32)


def order_points(points: np.ndarray) -> np.ndarray:
    pts = np.array(points, dtype=np.float32).reshape(4, 2)
    s = pts.sum(axis=1)
    d = np.diff(pts, axis=1).reshape(-1)
    ordered = np.zeros((4, 2), dtype=np.float32)
    ordered[0] = pts[np.argmin(s)]
    ordered[2] = pts[np.argmax(s)]
    ordered[1] = pts[np.argmin(d)]
    ordered[3] = pts[np.argmax(d)]
    return ordered


def side_lengths(points: np.ndarray) -> tuple[float, float, float, float]:
    pts = order_points(points)
    return tuple(float(np.linalg.norm(pts[(i + 1) % 4] - pts[i])) for i in range(4))


def candidate_score(points: np.ndarray, area: float, image_area: float) -> float:
    lengths = side_lengths(points)
    width = (lengths[0] + lengths[2]) / 2.0
    height = (lengths[1] + lengths[3]) / 2.0
    if width <= 1 or height <= 1:
        return -1.0
    aspect = width / height
    square_score = math.exp(-abs(math.log(aspect)) * 2.2)
    area_score = min(area / image_area, 1.0)
    return area_score * square_score


def detect_board_candidates(image: np.ndarray) -> list[np.ndarray]:
    height, width = image.shape[:2]
    image_area = float(height * width)
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    ranges = [
        ((8, 35, 55), (38, 240, 250)),
        ((10, 45, 65), (35, 230, 245)),
        ((5, 25, 45), (45, 255, 255)),
        ((0, 20, 45), (55, 255, 255)),
    ]
    ksize = max(9, int(max(height, width) / 45))
    if ksize % 2 == 0:
        ksize += 1
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (ksize, ksize))
    candidates: list[tuple[float, np.ndarray]] = []

    for low, high in ranges:
        mask = cv2.inRange(hsv, np.array(low, dtype=np.uint8), np.array(high, dtype=np.uint8))
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=2)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=1)
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for contour in sorted(contours, key=cv2.contourArea, reverse=True)[:8]:
            area = float(cv2.contourArea(contour))
            if area < image_area * 0.12:
                continue
            perimeter = cv2.arcLength(contour, True)
            point_sets = []
            for eps in (0.02, 0.04, 0.06):
                approx = cv2.approxPolyDP(contour, eps * perimeter, True)
                if len(approx) == 4:
                    point_sets.append(approx.reshape(4, 2).astype(np.float32))
            rect = cv2.minAreaRect(contour)
            point_sets.append(cv2.boxPoints(rect).astype(np.float32))

            for points in point_sets:
                score = candidate_score(points, area, image_area)
                if score > 0:
                    candidates.append((score, order_points(points)))

    if not candidates:
        return []

    candidates.sort(key=lambda item: item[0], reverse=True)
    unique: list[np.ndarray] = []
    for _, points in candidates:
        if all(np.max(np.abs(points - existing)) > 12 for existing in unique):
            unique.append(points)
        if len(unique) >= 8:
            break
    return unique


def warp_board(image: np.ndarray, corners: np.ndarray, size: int) -> np.ndarray:
    dst = np.array(
        [[0, 0], [size - 1, 0], [size - 1, size - 1], [0, size - 1]],
        dtype=np.float32,
    )
    transform = cv2.getPerspectiveTransform(order_points(corners), dst)
    return cv2.warpPerspective(image, transform, (size, size))


def cluster_positions(items: list[tuple[float, float]], tolerance: float) -> list[tuple[float, float]]:
    if not items:
        return []
    items = sorted(items)
    clusters: list[list[tuple[float, float]]] = []
    for value, weight in items:
        if not clusters or value - clusters[-1][-1][0] > tolerance:
            clusters.append([(value, weight)])
        else:
            clusters[-1].append((value, weight))

    merged = []
    for cluster in clusters:
        total_weight = sum(weight for _, weight in cluster)
        if total_weight <= 0:
            continue
        value = sum(value * weight for value, weight in cluster) / total_weight
        merged.append((value, total_weight))
    return merged


def projection_peaks(mask: np.ndarray, axis: int, percentile: float = 93.0) -> list[tuple[float, float]]:
    projection = mask.mean(axis=axis)
    if projection.size < 16:
        return []
    smooth = np.convolve(projection, np.ones(7) / 7.0, mode="same")
    threshold = float(np.percentile(smooth, percentile))
    if threshold <= 0:
        return []
    peaks = []
    for idx in range(4, len(smooth) - 4):
        window = smooth[idx - 4 : idx + 5]
        if smooth[idx] >= threshold and smooth[idx] >= window.max():
            peaks.append((float(idx), float(max(smooth[idx], 1.0)) / 255.0))
    return cluster_positions(peaks, 12.0)


def collect_line_candidates(warped: np.ndarray, axis: str) -> list[tuple[float, float]]:
    size = warped.shape[0]
    gray = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)
    candidates: list[tuple[float, float]] = []

    edges = cv2.Canny(cv2.GaussianBlur(gray, (3, 3), 0), 50, 120, apertureSize=3)
    lines = cv2.HoughLinesP(
        edges,
        1,
        np.pi / 180,
        threshold=max(55, int(size * 0.055)),
        minLineLength=max(140, int(size * 0.18)),
        maxLineGap=max(16, int(size * 0.035)),
    )
    if lines is not None:
        for x1, y1, x2, y2 in lines[:, 0, :]:
            dx = float(x2 - x1)
            dy = float(y2 - y1)
            length = math.hypot(dx, dy)
            if length < size * 0.18:
                continue
            angle = abs(math.degrees(math.atan2(dy, dx)))
            if axis == "x" and 84 <= angle <= 96:
                candidates.append(((x1 + x2) / 2.0, 1.0 + length / size))
            elif axis == "y" and (angle <= 6 or angle >= 174):
                candidates.append(((y1 + y2) / 2.0, 1.0 + length / size))

    block_size = max(31, int(size / 20))
    if block_size % 2 == 0:
        block_size += 1
    dark = cv2.adaptiveThreshold(
        gray,
        255,
        cv2.ADAPTIVE_THRESH_MEAN_C,
        cv2.THRESH_BINARY_INV,
        block_size,
        7,
    )
    kernel_len = max(35, int(size / 18))
    if axis == "x":
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, kernel_len))
        line_mask = cv2.morphologyEx(dark, cv2.MORPH_OPEN, kernel)
        candidates.extend(projection_peaks(line_mask, axis=0))
    else:
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_len, 2))
        line_mask = cv2.morphologyEx(dark, cv2.MORPH_OPEN, kernel)
        candidates.extend(projection_peaks(line_mask, axis=1))

    return cluster_positions(candidates, tolerance=max(8.0, size / 120.0))


def fit_regular_grid(
    candidates: list[tuple[float, float]],
    board_size: int,
    image_size: int,
) -> GridFit:
    nominal = image_size / float(board_size - 1)
    if not candidates:
        margin = image_size * 0.045
        spacing = (image_size - 2 * margin) / float(board_size - 1)
        return GridFit(margin, spacing, 0.0, 0, 0)

    values = np.array([value for value, _ in candidates], dtype=np.float64)
    weights = np.array([weight for _, weight in candidates], dtype=np.float64)
    weights = np.clip(weights, 0.25, 6.0)

    best: tuple[float, float, float, int] | None = None
    min_spacing = nominal * 0.78
    max_spacing = nominal * 1.02

    for spacing in np.linspace(min_spacing, max_spacing, 300):
        max_offset = image_size - 1 - (board_size - 1) * spacing
        if max_offset < 0:
            continue
        offsets = np.linspace(0, min(max_offset, image_size * 0.16), 220)
        tolerance = max(4.5, spacing * 0.095)
        for offset in offsets:
            grid = offset + np.arange(board_size) * spacing
            distances = np.min(np.abs(values[:, None] - grid[None, :]), axis=1)
            nearest = np.argmin(np.abs(values[:, None] - grid[None, :]), axis=1)
            weighted = float(np.sum(weights * np.exp(-((distances / tolerance) ** 2))))
            coverage = len(set(int(v) for v in nearest[distances < tolerance * 1.2]))
            score = weighted + coverage * 1.8
            if best is None or score > best[0]:
                best = (score, float(offset), float(spacing), coverage)

    if best is None:
        margin = image_size * 0.045
        spacing = (image_size - 2 * margin) / float(board_size - 1)
        return GridFit(margin, spacing, 0.0, 0, len(candidates))

    score, offset, spacing, coverage = best
    return GridFit(offset, spacing, score, coverage, len(candidates))


def detect_grid(warped: np.ndarray, board_size: int) -> tuple[GridFit, GridFit]:
    size = warped.shape[0]
    x_candidates = collect_line_candidates(warped, "x")
    y_candidates = collect_line_candidates(warped, "y")
    return (
        fit_regular_grid(x_candidates, board_size, size),
        fit_regular_grid(y_candidates, board_size, size),
    )


def choose_board(image: np.ndarray, corners: np.ndarray | None, board_size: int, warp_size: int) -> tuple[np.ndarray, np.ndarray, GridFit, GridFit]:
    if corners is not None:
        ordered = order_points(corners)
        warped = warp_board(image, ordered, warp_size)
        xfit, yfit = detect_grid(warped, board_size)
        return ordered, warped, xfit, yfit

    candidates = detect_board_candidates(image)
    if not candidates:
        h, w = image.shape[:2]
        side = min(h, w)
        x0 = (w - side) / 2.0
        y0 = (h - side) / 2.0
        candidates = [
            np.array(
                [[x0, y0], [x0 + side - 1, y0], [x0 + side - 1, y0 + side - 1], [x0, y0 + side - 1]],
                dtype=np.float32,
            )
        ]

    best = None
    for candidate in candidates:
        warped = warp_board(image, candidate, warp_size)
        xfit, yfit = detect_grid(warped, board_size)
        score = xfit.score + yfit.score + (xfit.coverage + yfit.coverage) * 2.0
        if best is None or score > best[0]:
            best = (score, candidate, warped, xfit, yfit)

    assert best is not None
    _, chosen, warped, xfit, yfit = best
    return order_points(chosen), warped, xfit, yfit


def fixed_grid_fit(warp_size: int, board_size: int) -> GridFit:
    spacing = (warp_size - 1) / float(board_size - 1)
    return GridFit(0.0, spacing, float(board_size), board_size, board_size)


def classify_intersections(
    warped: np.ndarray,
    xfit: GridFit,
    yfit: GridFit,
    board_size: int,
) -> list[list[str]]:
    hsv = cv2.cvtColor(warped, cv2.COLOR_BGR2HSV)
    gray = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)
    size = warped.shape[0]
    cell = (xfit.spacing + yfit.spacing) / 2.0
    radius = max(8, int(cell * 0.36))
    board: list[list[str]] = []

    for row in range(board_size):
        y = yfit.offset + row * yfit.spacing
        cells = []
        for col in range(board_size):
            x = xfit.offset + col * xfit.spacing
            x0 = max(0, int(round(x - radius)))
            x1 = min(size, int(round(x + radius + 1)))
            y0 = max(0, int(round(y - radius)))
            y1 = min(size, int(round(y + radius + 1)))
            yy, xx = np.ogrid[y0:y1, x0:x1]
            circle = (xx - x) ** 2 + (yy - y) ** 2 <= radius**2

            patch_gray = gray[y0:y1, x0:x1][circle]
            patch_hsv = hsv[y0:y1, x0:x1][circle]
            if patch_gray.size == 0:
                cells.append(".")
                continue

            mean_v = float(patch_hsv[:, 2].mean())
            mean_s = float(patch_hsv[:, 1].mean())
            dark_fraction = float((patch_gray < 82).mean())
            very_dark_fraction = float((patch_gray < 55).mean())
            bright_fraction = float((patch_gray > 165).mean())
            bright_low_sat = float(((patch_hsv[:, 2] > 170) & (patch_hsv[:, 1] < 70)).mean())
            white_core = float(((patch_hsv[:, 2] > 185) & (patch_hsv[:, 1] < 65)).mean())

            if dark_fraction > 0.30 or (mean_v < 108 and very_dark_fraction > 0.10):
                cells.append("B")
            elif (bright_low_sat > 0.48 and mean_s < 74) or (white_core > 0.36 and mean_s < 78 and bright_fraction > 0.60):
                cells.append("W")
            else:
                cells.append(".")
        board.append(cells)

    return board


def score_territory(board: list[list[str]]) -> tuple[dict[str, int], list[list[str]]]:
    size = len(board)
    marks = [["." for _ in range(size)] for _ in range(size)]
    visited: set[tuple[int, int]] = set()
    counts = {
        "black_stones": sum(row.count("B") for row in board),
        "white_stones": sum(row.count("W") for row in board),
        "empty": sum(row.count(".") for row in board),
        "black_territory": 0,
        "white_territory": 0,
        "neutral_empty": 0,
    }

    for y in range(size):
        for x in range(size):
            if board[y][x] != "." or (x, y) in visited:
                continue
            queue = deque([(x, y)])
            visited.add((x, y))
            cells = []
            adjacent = set()
            while queue:
                cx, cy = queue.popleft()
                cells.append((cx, cy))
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    nx, ny = cx + dx, cy + dy
                    if 0 <= nx < size and 0 <= ny < size:
                        value = board[ny][nx]
                        if value == "." and (nx, ny) not in visited:
                            visited.add((nx, ny))
                            queue.append((nx, ny))
                        elif value in {"B", "W"}:
                            adjacent.add(value)

            if adjacent == {"B"}:
                counts["black_territory"] += len(cells)
                mark = "b"
            elif adjacent == {"W"}:
                counts["white_territory"] += len(cells)
                mark = "w"
            else:
                counts["neutral_empty"] += len(cells)
                mark = "n"
            for cx, cy in cells:
                marks[cy][cx] = mark

    counts["black_area_chinese"] = counts["black_stones"] + counts["black_territory"]
    counts["white_area_chinese"] = counts["white_stones"] + counts["white_territory"]
    return counts, marks


def render_overlay(
    warped: np.ndarray,
    board: list[list[str]],
    territory: list[list[str]],
    xfit: GridFit,
    yfit: GridFit,
) -> np.ndarray:
    overlay = warped.copy()
    size = len(board)
    cell = (xfit.spacing + yfit.spacing) / 2.0
    stone_radius = max(8, int(cell * 0.24))
    marker_radius = max(4, int(cell * 0.09))

    for row in range(size):
        y = int(round(yfit.offset + row * yfit.spacing))
        for col in range(size):
            x = int(round(xfit.offset + col * xfit.spacing))
            value = board[row][col]
            terr = territory[row][col]
            if value == "B":
                cv2.circle(overlay, (x, y), stone_radius, (0, 0, 255), 2)
                cv2.putText(overlay, "B", (x - 8, y + 7), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 0, 255), 2)
            elif value == "W":
                cv2.circle(overlay, (x, y), stone_radius, (255, 0, 0), 2)
                cv2.putText(overlay, "W", (x - 11, y + 7), cv2.FONT_HERSHEY_SIMPLEX, 0.50, (255, 0, 0), 2)
            elif terr == "b":
                cv2.rectangle(
                    overlay,
                    (x - marker_radius, y - marker_radius),
                    (x + marker_radius, y + marker_radius),
                    (0, 0, 0),
                    -1,
                )
            elif terr == "w":
                cv2.rectangle(
                    overlay,
                    (x - marker_radius, y - marker_radius),
                    (x + marker_radius, y + marker_radius),
                    (255, 255, 255),
                    -1,
                )

    return overlay


def blend_circle(image: np.ndarray, center: tuple[int, int], radius: int, color: tuple[int, int, int], alpha: float) -> None:
    layer = image.copy()
    cv2.circle(layer, center, radius, color, -1, lineType=cv2.LINE_AA)
    cv2.addWeighted(layer, alpha, image, 1.0 - alpha, 0, image)


def draw_stone(image: np.ndarray, center: tuple[int, int], radius: int, color: str) -> None:
    x, y = center
    blend_circle(image, (x + max(1, radius // 12), y + max(1, radius // 12)), radius, (76, 110, 150), 0.28)
    if color == "B":
        cv2.circle(image, center, radius, (18, 18, 20), -1, lineType=cv2.LINE_AA)
        cv2.circle(image, (x - radius // 4, y - radius // 4), max(2, radius // 4), (54, 54, 58), -1, lineType=cv2.LINE_AA)
        cv2.circle(image, center, radius, (4, 4, 6), 2, lineType=cv2.LINE_AA)
    else:
        cv2.circle(image, center, radius, (236, 232, 218), -1, lineType=cv2.LINE_AA)
        cv2.circle(image, (x - radius // 4, y - radius // 4), max(3, radius // 3), (255, 252, 242), -1, lineType=cv2.LINE_AA)
        cv2.circle(image, center, radius, (176, 170, 155), 1, lineType=cv2.LINE_AA)


def load_display_font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    font_paths = [
        "/System/Library/Fonts/PingFang.ttc",
        "/System/Library/Fonts/STHeiti Light.ttc",
        "/System/Library/Fonts/STHeiti Medium.ttc",
        "/Library/Fonts/Arial Unicode.ttf",
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc",
        "C:/Windows/Fonts/msyh.ttc",
        "C:/Windows/Fonts/simhei.ttf",
    ]
    for font_path in font_paths:
        if Path(font_path).exists():
            try:
                return ImageFont.truetype(font_path, size=size)
            except OSError:
                continue
    return ImageFont.load_default()


def black_chinese_area_judgement(black_area: int, board_size: int) -> dict[str, object]:
    win_threshold = math.floor((board_size * board_size) / 2.0 + CHINESE_RULE_BLACK_KOMI_STONES) + 1
    black_wins = black_area >= win_threshold
    return {
        "black_result_chinese": "胜" if black_wins else "负",
        "black_wins_chinese": black_wins,
        "black_win_threshold_chinese": win_threshold,
        "black_komi_stones_chinese": CHINESE_RULE_BLACK_KOMI_STONES,
    }


def text_size(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.FreeTypeFont | ImageFont.ImageFont) -> tuple[int, int]:
    bbox = draw.textbbox((0, 0), text, font=font)
    return bbox[2] - bbox[0], bbox[3] - bbox[1]


def add_score_footer(board_image: np.ndarray, counts: dict[str, int], judgement: dict[str, object]) -> np.ndarray:
    board_size = board_image.shape[1]
    footer_height = max(126, int(round(board_size * 0.135)))
    footer = np.full((footer_height, board_size, 3), (244, 246, 242), dtype=np.uint8)
    cv2.line(footer, (0, 0), (board_size, 0), (198, 212, 202), max(2, board_size // 500), lineType=cv2.LINE_AA)
    cv2.line(footer, (0, footer_height - 1), (board_size, footer_height - 1), (218, 226, 220), 1, lineType=cv2.LINE_AA)

    rgb = cv2.cvtColor(footer, cv2.COLOR_BGR2RGB)
    pil_image = Image.fromarray(rgb)
    draw = ImageDraw.Draw(pil_image)
    font = load_display_font(max(34, int(round(board_size * 0.055))))

    labels = [
        ("黑", (60, 128, 92)),
        (f"{counts['black_area_chinese']}", (190, 92, 54)),
        ("子", (60, 128, 92)),
        (str(judgement["black_result_chinese"]), (36, 132, 78) if judgement["black_wins_chinese"] else (174, 68, 64)),
    ]
    gap = max(16, int(round(board_size * 0.018)))
    stone_radius = max(13, int(round(board_size * 0.016)))

    label_sizes = [text_size(draw, text, font) for text, _ in labels]
    text_h = max(height for _, height in label_sizes)
    total_w = stone_radius * 2 + gap + sum(width for width, _ in label_sizes) + gap * (len(labels) - 1)
    start_x = int(round((board_size - total_w) / 2))
    center_y = footer_height // 2
    text_y = int(round(center_y - text_h / 2 - board_size * 0.004))

    stone_center = (start_x + stone_radius, center_y)
    draw.ellipse(
        [
            stone_center[0] - stone_radius,
            stone_center[1] - stone_radius,
            stone_center[0] + stone_radius,
            stone_center[1] + stone_radius,
        ],
        fill=(24, 30, 32),
        outline=(2, 3, 4),
        width=max(1, stone_radius // 7),
    )
    highlight = max(3, stone_radius // 4)
    draw.ellipse(
        [
            stone_center[0] - stone_radius // 3 - highlight,
            stone_center[1] - stone_radius // 3 - highlight,
            stone_center[0] - stone_radius // 3 + highlight,
            stone_center[1] - stone_radius // 3 + highlight,
        ],
        fill=(58, 62, 64),
    )

    x = start_x + stone_radius * 2 + gap
    for (text, color), (width, _) in zip(labels, label_sizes):
        draw.text((x, text_y), text, fill=color, font=font)
        x += width + gap

    footer = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
    return np.vstack([board_image, footer])


def render_result_board(
    board: list[list[str]],
    territory: list[list[str]],
    counts: dict[str, int],
    judgement: dict[str, object],
    output_size: int,
) -> np.ndarray:
    size = len(board)
    if size < 2:
        raise SystemExit("Cannot render a board with fewer than two lines")

    image = np.full((output_size, output_size, 3), (92, 166, 215), dtype=np.uint8)
    y = np.arange(output_size, dtype=np.float32)[:, None]
    x = np.arange(output_size, dtype=np.float32)[None, :]
    grain = (
        7.0 * np.sin(x / 5.5)
        + 4.0 * np.sin(x / 17.0)
        + 2.0 * np.sin((x + y) / 29.0)
    )
    image = np.clip(image.astype(np.float32) + grain[..., None], 0, 255).astype(np.uint8)

    pad = int(round(output_size * 0.055))
    cell = (output_size - 2 * pad) / float(size - 1)
    line_color = (38, 42, 52)
    border_color = (55, 72, 104)

    cv2.rectangle(image, (8, 8), (output_size - 9, output_size - 9), border_color, max(5, output_size // 190), lineType=cv2.LINE_AA)
    for idx in range(size):
        pos = int(round(pad + idx * cell))
        thickness = 2 if idx in {0, size - 1} else 1
        cv2.line(image, (pad, pos), (output_size - pad, pos), line_color, thickness, lineType=cv2.LINE_AA)
        cv2.line(image, (pos, pad), (pos, output_size - pad), line_color, thickness, lineType=cv2.LINE_AA)

    star_indices = [3, 9, 15] if size == 19 else []
    star_radius = max(3, int(round(cell * 0.055)))
    for row in star_indices:
        for col in star_indices:
            center = (int(round(pad + col * cell)), int(round(pad + row * cell)))
            cv2.circle(image, center, star_radius, (12, 18, 26), -1, lineType=cv2.LINE_AA)

    marker_half = max(4, int(round(cell * 0.12)))
    stone_radius = max(8, int(round(cell * 0.43)))

    for row in range(size):
        for col in range(size):
            value = board[row][col]
            mark = territory[row][col]
            cx = int(round(pad + col * cell))
            cy = int(round(pad + row * cell))
            if value == "." and mark == "b":
                cv2.rectangle(
                    image,
                    (cx - marker_half, cy - marker_half),
                    (cx + marker_half, cy + marker_half),
                    (0, 0, 0),
                    -1,
                    lineType=cv2.LINE_AA,
                )
            elif value == "." and mark == "w":
                cv2.rectangle(
                    image,
                    (cx - marker_half, cy - marker_half),
                    (cx + marker_half, cy + marker_half),
                    (252, 252, 245),
                    -1,
                    lineType=cv2.LINE_AA,
                )
                cv2.rectangle(
                    image,
                    (cx - marker_half, cy - marker_half),
                    (cx + marker_half, cy + marker_half),
                    (180, 172, 152),
                    1,
                    lineType=cv2.LINE_AA,
                )

    for row in range(size):
        for col in range(size):
            value = board[row][col]
            if value not in {"B", "W"}:
                continue
            center = (int(round(pad + col * cell)), int(round(pad + row * cell)))
            draw_stone(image, center, stone_radius, value)

    return add_score_footer(image, counts, judgement)


def board_to_strings(board: list[list[str]]) -> list[str]:
    return ["".join(row).replace("B", "X").replace("W", "O") for row in board]


def result_to_strings(board: list[list[str]], territory: list[list[str]]) -> list[str]:
    rows = []
    for row_idx, row in enumerate(board):
        chars = []
        for col_idx, value in enumerate(row):
            mark = territory[row_idx][col_idx]
            if value == "B":
                chars.append("X")
            elif value == "W":
                chars.append("O")
            elif mark == "b":
                chars.append("x")
            elif mark == "w":
                chars.append("o")
            else:
                chars.append(".")
        rows.append("".join(chars))
    return rows


def build_result(
    image_path: Path,
    corners: np.ndarray,
    xfit: GridFit,
    yfit: GridFit,
    board: list[list[str]],
    territory: list[list[str]],
    counts: dict[str, int],
    board_size: int,
) -> dict[str, object]:
    warnings = []
    likely_scoring_overlay = (
        counts["black_stones"] + counts["white_stones"] > int(board_size * board_size * 0.72)
    )
    if xfit.coverage < 6 or yfit.coverage < 6:
        warnings.append("Low grid-line confidence; verify the overlay or pass --corners manually.")
    if likely_scoring_overlay:
        warnings.append("The board looks like a scoring overlay; black_stones may include territory markers.")
    if counts["neutral_empty"] > 0:
        warnings.append("Neutral or dame intersections were found; scoring may need manual review.")
    area_total = counts["black_area_chinese"] + counts["white_area_chinese"]
    area_expected = board_size * board_size
    if area_total != area_expected:
        warnings.append(f"Area check failed: black_area_chinese + white_area_chinese = {area_total}, expected {area_expected}.")
    judgement = black_chinese_area_judgement(counts["black_area_chinese"], board_size)

    return {
        "image": str(image_path),
        "board_size": board_size,
        "black_stones": counts["black_stones"],
        "white_stones": counts["white_stones"],
        "black_territory": counts["black_territory"],
        "white_territory": counts["white_territory"],
        "neutral_empty": counts["neutral_empty"],
        "black_area_chinese": counts["black_area_chinese"],
        "white_area_chinese": counts["white_area_chinese"],
        "area_total": area_total,
        "area_expected": area_expected,
        "area_total_ok": area_total == area_expected,
        **judgement,
        "likely_scoring_overlay": likely_scoring_overlay,
        "board_corners": [[round(float(x), 2), round(float(y), 2)] for x, y in corners],
        "grid": {
            "x_offset": round(xfit.offset, 3),
            "x_spacing": round(xfit.spacing, 3),
            "x_coverage": xfit.coverage,
            "y_offset": round(yfit.offset, 3),
            "y_spacing": round(yfit.spacing, 3),
            "y_coverage": yfit.coverage,
        },
        "board_ascii": board_to_strings(board),
        "result_ascii": result_to_strings(board, territory),
        "result_ascii_legend": "X black stone, O white stone, x black territory, o white territory, . neutral empty",
        "warnings": warnings,
    }


def print_human(result: dict[str, object], overlay: Path | None) -> None:
    print(f"Black stones: {result['black_stones']}")
    print(f"White stones: {result['white_stones']}")
    print(f"Black territory: {result['black_territory']}")
    print(f"White territory: {result['white_territory']}")
    print(f"Estimated Chinese-area score: black {result['black_area_chinese']}, white {result['white_area_chinese']}")
    print(
        f"Chinese-area result: black {result['black_result_chinese']} "
        f"(wins at >= {result['black_win_threshold_chinese']})"
    )
    if result["neutral_empty"]:
        print(f"Neutral empty intersections: {result['neutral_empty']}")
    if overlay:
        print(f"Overlay: {overlay}")
    if result.get("result_image"):
        print(f"Result image: {result['result_image']}")
    warnings = result.get("warnings", [])
    if warnings:
        print("Warnings:")
        for warning in warnings:
            print(f"- {warning}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Count black Go stones and estimate Chinese-area score from a board image.")
    parser.add_argument("image", type=Path, help="Path to a Go board photo or screenshot")
    parser.add_argument("--board-size", type=int, default=19, help="Number of grid lines, default: 19")
    parser.add_argument("--warp-size", type=int, default=1200, help="Internal square board size in pixels")
    parser.add_argument("--corners", help="Four board corners as 'x,y x,y x,y x,y', clockwise from top-left")
    parser.add_argument("--grid-corners", action="store_true", help="Treat --corners as the four outer grid intersections instead of the wooden board corners")
    parser.add_argument("--overlay", type=Path, help="Write a warped-board overlay image for verification")
    parser.add_argument("--result-image", type=Path, help="Write a clean static result board image")
    parser.add_argument("--result-size", type=int, default=1200, help="Pixel size for --result-image, default: 1200")
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON")
    args = parser.parse_args()

    if args.board_size < 2:
        raise SystemExit("--board-size must be at least 2")
    if args.result_size < 320:
        raise SystemExit("--result-size must be at least 320")

    image = read_image(args.image)
    manual_corners = parse_corners(args.corners) if args.corners else None
    if args.grid_corners and manual_corners is None:
        raise SystemExit("--grid-corners requires --corners")
    if args.grid_corners:
        corners = order_points(manual_corners)
        warped = warp_board(image, corners, args.warp_size)
        xfit = fixed_grid_fit(args.warp_size, args.board_size)
        yfit = fixed_grid_fit(args.warp_size, args.board_size)
    else:
        corners, warped, xfit, yfit = choose_board(image, manual_corners, args.board_size, args.warp_size)
    board = classify_intersections(warped, xfit, yfit, args.board_size)
    counts, territory = score_territory(board)
    result = build_result(args.image, corners, xfit, yfit, board, territory, counts, args.board_size)

    if args.overlay:
        overlay = render_overlay(warped, board, territory, xfit, yfit)
        write_image(args.overlay, overlay)
    if args.result_image:
        result_board = render_result_board(
            board,
            territory,
            counts,
            black_chinese_area_judgement(counts["black_area_chinese"], args.board_size),
            args.result_size,
        )
        write_image(args.result_image, result_board)
        result["result_image"] = str(args.result_image)

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print_human(result, args.overlay)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
