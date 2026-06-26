#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import time
import venv
from datetime import date, timedelta
from pathlib import Path


BOOTSTRAP_WAIT_SECONDS = 180.0
LOCK_STALE_SECONDS = 300.0


def _python_has_module(python_executable: Path, module_name: str) -> bool:
    if not python_executable.exists():
        return False
    result = subprocess.run(
        [str(python_executable), "-c", f"import {module_name}"],
        check=False,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    return result.returncode == 0


def _create_or_refresh_pdf_venv(venv_dir: Path, venv_python: Path) -> None:
    if venv_dir.exists() and not venv_python.exists():
        shutil.rmtree(venv_dir)

    if not venv_python.exists():
        tmp_dir = venv_dir.with_name(f"{venv_dir.name}.tmp-{os.getpid()}")
        if tmp_dir.exists():
            shutil.rmtree(tmp_dir)

        venv.EnvBuilder(with_pip=True, clear=True).create(str(tmp_dir))

        tmp_python = tmp_dir / "bin" / "python"
        if not tmp_python.exists():
            raise RuntimeError(f"Failed to create Python runtime at {tmp_dir}")

        if venv_dir.exists():
            shutil.rmtree(venv_dir)
        tmp_dir.rename(venv_dir)

    if not _python_has_module(venv_python, "reportlab"):
        subprocess.run(
            [str(venv_python), "-m", "ensurepip", "--upgrade"],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        subprocess.run(
            [str(venv_python), "-m", "pip", "install", "--disable-pip-version-check", "reportlab"],
            check=True,
        )


def _acquire_bootstrap_lock(lock_path: Path) -> int:
    started_at = time.time()
    while True:
        try:
            fd = os.open(lock_path, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            os.write(fd, f"{os.getpid()} {int(time.time())}\n".encode("utf-8"))
            return fd
        except FileExistsError:
            try:
                lock_age = time.time() - lock_path.stat().st_mtime
            except FileNotFoundError:
                continue

            if lock_age > LOCK_STALE_SECONDS:
                try:
                    lock_path.unlink()
                except FileNotFoundError:
                    pass
                continue

            if time.time() - started_at > BOOTSTRAP_WAIT_SECONDS:
                raise TimeoutError(f"Timed out waiting for bootstrap lock: {lock_path}")

            time.sleep(0.25)


def _release_bootstrap_lock(lock_fd: int | None, lock_path: Path) -> None:
    if lock_fd is None:
        return
    try:
        os.close(lock_fd)
    finally:
        try:
            lock_path.unlink()
        except FileNotFoundError:
            pass


def ensure_reportlab() -> None:
    try:
        __import__("reportlab")
        return
    except ModuleNotFoundError:
        pass

    repo_root = Path(__file__).resolve().parents[1]
    venv_dir = repo_root / ".pdfgen-venv"
    venv_python = venv_dir / "bin" / "python"
    lock_path = repo_root / ".pdfgen-venv.lock"
    entry_script = str(Path(sys.argv[0]).resolve())
    current_python = Path(sys.executable).resolve()
    running_inside_bootstrap_venv = venv_python.exists() and current_python == venv_python.resolve()

    if venv_python.exists() and not running_inside_bootstrap_venv and _python_has_module(venv_python, "reportlab"):
        os.execv(str(venv_python), [str(venv_python), entry_script, *sys.argv[1:]])

    lock_fd: int | None = None
    try:
        lock_fd = _acquire_bootstrap_lock(lock_path)
        _create_or_refresh_pdf_venv(venv_dir, venv_python)
    except Exception as exc:
        raise SystemExit(
            "Missing Python PDF dependency 'reportlab' and automatic bootstrap failed. "
            "Create a local runtime manually with: python3 -m venv .pdfgen-venv && "
            ".pdfgen-venv/bin/python -m pip install reportlab"
        ) from exc
    finally:
        _release_bootstrap_lock(lock_fd, lock_path)

    if current_python != venv_python.resolve():
        os.execv(str(venv_python), [str(venv_python), entry_script, *sys.argv[1:]])

    try:
        __import__("reportlab")
    except ModuleNotFoundError as exc:
        raise SystemExit(
            "The local PDF runtime was created, but 'reportlab' is still unavailable. "
            "Re-run: .pdfgen-venv/bin/python -m pip install reportlab"
        ) from exc


ensure_reportlab()

from reportlab.lib.colors import HexColor, white
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas


PAGE_WIDTH, PAGE_HEIGHT = A4

COLOR_BG = HexColor("#F4F7FB")
COLOR_NAVY = HexColor("#12213F")
COLOR_TEXT = HexColor("#162033")
COLOR_MUTED = HexColor("#66758A")
COLOR_BORDER = HexColor("#DCE4EF")
COLOR_BLUE = HexColor("#3793F6")
COLOR_BLUE_SOFT = HexColor("#EAF3FF")
COLOR_GREEN = HexColor("#2FB072")
COLOR_GREEN_SOFT = HexColor("#EAF8F1")
COLOR_ORANGE = HexColor("#F29B38")
COLOR_ORANGE_SOFT = HexColor("#FFF4E9")
COLOR_RED = HexColor("#E35B5B")
COLOR_TEAL = HexColor("#34B7B4")


def monday_of_week(day: date | None = None) -> date:
    today = day or date.today()
    return today - timedelta(days=today.weekday())


def default_output_path(base_dir: Path, week_start: date | None = None) -> Path:
    resolved_week_start = week_start or monday_of_week()
    return base_dir / "data" / "weekly_reports" / f"week_{resolved_week_start.isoformat()}.pdf"


def format_week_range(week_start: date) -> str:
    week_end = week_start + timedelta(days=6)
    return f"{week_start:%Y.%m.%d} - {week_end:%Y.%m.%d}"


def parse_week_start(raw_value: str | None) -> date:
    if not raw_value:
        return monday_of_week()

    parsed_date = date.fromisoformat(raw_value)
    if parsed_date.weekday() != 0:
        raise SystemExit("--week-start must be a Monday in YYYY-MM-DD format.")
    return parsed_date


def default_report_data() -> dict:
    week_start = monday_of_week()
    return {
        "client": "颜同学",
        "date_range": format_week_range(week_start),
        "goal": "减脂期 | 每周5练 | 高蛋白饮食",
        "weight_points": [79.8, 79.7, 79.6, 79.4, 79.4, 79.3, 79.2],
        "training_completed": 4,
        "training_planned": 5,
        "training_minutes": 248,
        "weekly_delta": -0.6,
        "nutrition_value": "5 / 7 天",
        "nutrition_label": "蛋白目标命中",
        "nutrition_note": "最近一周蛋白目标命中表现稳定，训练日饮食执行较整齐。",
        "hydration_value": "5 / 7 天",
        "hydration_label": "饮水目标命中",
        "hydration_note": "平均 2900 ml，补水节奏比上周更稳定，晚间补水拖延减少。",
        "sleep_value": "7.2 小时",
        "sleep_label": "平均睡眠",
        "sleep_note": "最低 6.2 小时，整体恢复尚可，但腿部日前一晚仍有提升空间。",
        "recovery_status": "恢复中等偏好",
        "rhr_note": "静息心率较上周下降 2 bpm",
        "hrv_note": "HRV 较上周回升 4 ms",
        "highlights": [
            "卧推动作品质稳定，训练容量继续上行，主项输出比上周更扎实。",
            "周末外卖依然控制在热量范围内，没有拖累本周整体执行率。",
        ],
        "verdict": [
            "这一周最大的优点是执行稳定，体重下降速度理想，没有出现明显透支。",
            "训练质量没有因为热量缺口而明显下滑，说明当前饮食结构仍然可持续；下周把腿部日前后的睡眠和补水再抬一档，恢复会更整齐。",
        ],
        "next_week": [
            "训练重点：保住 Day 3 强度，但辅助动作不过量堆疲劳。",
            "营养重点：训练日上午前半段提前吃够蛋白，晚餐控制油脂密度。",
            "执行挑战：至少 4 天在晚饭前完成全天饮水目标。",
        ],
    }


def load_report_data(input_path: Path | None) -> dict:
    data = default_report_data()
    if input_path is None:
        return data
    incoming = json.loads(input_path.read_text(encoding="utf-8"))
    data.update(incoming)
    return data


def register_fonts() -> dict[str, str]:
    font_candidates = {
        "CNHeading": [
            "/System/Library/Fonts/PingFang.ttc",
            "/System/Library/Fonts/Hiragino Sans GB.ttc",
            "/System/Library/Fonts/STHeiti Medium.ttc",
            "/System/Library/Fonts/Supplemental/Songti.ttc",
            "C:/Windows/Fonts/msyhbd.ttc",
            "C:/Windows/Fonts/simhei.ttf",
            "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc",
            "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
            "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",
        ],
        "CNBody": [
            "/System/Library/Fonts/PingFang.ttc",
            "/System/Library/Fonts/Supplemental/Songti.ttc",
            "/System/Library/Fonts/Hiragino Sans GB.ttc",
            "C:/Windows/Fonts/msyh.ttc",
            "C:/Windows/Fonts/simsun.ttc",
            "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
            "/usr/share/fonts/opentype/noto/NotoSerifCJK-Regular.ttc",
            "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc",
            "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",
        ],
    }
    registered: dict[str, str] = {}
    for name, paths in font_candidates.items():
        for path in paths:
            if not Path(path).exists():
                continue
            try:
                pdfmetrics.registerFont(TTFont(name, path))
                registered[name] = name
                break
            except Exception:
                continue
    if "CNHeading" not in registered:
        registered["CNHeading"] = "Helvetica-Bold"
    if "CNBody" not in registered:
        registered["CNBody"] = registered["CNHeading"]
    registered["ENBold"] = "Helvetica-Bold"
    registered["ENBody"] = "Helvetica"
    return registered


def wrap_text(text: str, font_name: str, font_size: float, max_width: float) -> list[str]:
    lines: list[str] = []
    current = ""
    for char in text:
        if char == "\n":
            lines.append(current)
            current = ""
            continue
        candidate = current + char
        if current and pdfmetrics.stringWidth(candidate, font_name, font_size) > max_width:
            lines.append(current)
            current = char
        else:
            current = candidate
    if current:
        lines.append(current)
    return lines or [""]


def measure_text_height(text: str, width: float, font_name: str, font_size: float, leading: float) -> float:
    return len(wrap_text(text, font_name, font_size, width)) * leading


def measure_bullet_list_height(
    items: list[str],
    width: float,
    font_name: str,
    font_size: float,
    leading: float,
    gap: float = 10.0,
) -> float:
    total = 0.0
    for item in items:
        total += measure_text_height(item, width - 18, font_name, font_size, leading) + gap
    return max(0.0, total - gap)


def draw_text_block(
    c: canvas.Canvas,
    text: str,
    x: float,
    top_y: float,
    width: float,
    *,
    font_name: str,
    font_size: float,
    leading: float,
    color,
) -> float:
    c.setFillColor(color)
    y = top_y
    c.setFont(font_name, font_size)
    for line in wrap_text(text, font_name, font_size, width):
        c.drawString(x, y, line)
        y -= leading
    return y


def draw_round_card(c: canvas.Canvas, x: float, y: float, w: float, h: float, accent, fill=white) -> None:
    c.setFillColor(HexColor("#E7EDF5"))
    c.roundRect(x, y - 3, w, h, 18, stroke=0, fill=1)
    c.setFillColor(fill)
    c.roundRect(x, y, w, h, 18, stroke=0, fill=1)
    c.setFillColor(accent)
    c.roundRect(x, y + h - 6, w, 6, 18, stroke=0, fill=1)


def draw_chip_icon(c: canvas.Canvas, x: float, y: float, label: str, fill_color, fonts: dict[str, str]) -> None:
    c.setFillColor(fill_color)
    c.circle(x, y, 12, stroke=0, fill=1)
    c.setFillColor(white)
    c.setFont(fonts["CNHeading"], 9.5)
    c.drawCentredString(x, y - 3.5, label)


def draw_section_header(
    c: canvas.Canvas,
    x: float,
    y: float,
    title_cn: str,
    title_en: str,
    accent,
    icon_text: str,
    fonts: dict[str, str],
) -> None:
    draw_chip_icon(c, x + 12, y + 8, icon_text, accent, fonts)
    c.setFillColor(COLOR_TEXT)
    c.setFont(fonts["CNHeading"], 13.5)
    c.drawString(x + 32, y + 4, title_cn)
    c.setFillColor(COLOR_MUTED)
    c.setFont(fonts["ENBody"], 8.5)
    c.drawString(x + 32, y - 10, title_en.upper())


def draw_donut(
    c: canvas.Canvas,
    center_x: float,
    center_y: float,
    radius: float,
    ratio: float,
    *,
    accent,
    track,
    text_top: str,
    text_bottom: str,
    fonts: dict[str, str],
) -> None:
    ratio = max(0.0, min(1.0, ratio))
    c.setLineWidth(11)
    c.setStrokeColor(track)
    c.circle(center_x, center_y, radius, stroke=1, fill=0)
    c.setStrokeColor(accent)
    c.arc(
        center_x - radius,
        center_y - radius,
        center_x + radius,
        center_y + radius,
        startAng=90,
        extent=-360 * ratio,
    )
    c.setFillColor(COLOR_TEXT)
    c.setFont(fonts["ENBold"], 18)
    c.drawCentredString(center_x, center_y + 2, text_top)
    c.setFillColor(COLOR_MUTED)
    c.setFont(fonts["CNBody"], 9.5)
    c.drawCentredString(center_x, center_y - 13, text_bottom)


def draw_line_chart(
    c: canvas.Canvas,
    x: float,
    y: float,
    w: float,
    h: float,
    values: list[float],
    fonts: dict[str, str],
) -> None:
    chart_left = x + 10
    chart_bottom = y + 16
    chart_w = w - 20
    chart_h = h - 32

    c.setStrokeColor(COLOR_BORDER)
    c.setLineWidth(0.8)
    for step in range(4):
        yy = chart_bottom + chart_h * step / 3
        c.line(chart_left, yy, chart_left + chart_w, yy)

    v_min = min(values)
    v_max = max(values)
    span = max(v_max - v_min, 0.4)

    def point(index: int, value: float) -> tuple[float, float]:
        px = chart_left + chart_w * index / max(len(values) - 1, 1)
        py = chart_bottom + ((value - v_min) / span) * chart_h
        return px, py

    pts = [point(i, v) for i, v in enumerate(values)]

    area = c.beginPath()
    area.moveTo(pts[0][0], chart_bottom)
    for px, py in pts:
        area.lineTo(px, py)
    area.lineTo(pts[-1][0], chart_bottom)
    area.close()
    c.setFillColor(COLOR_BLUE_SOFT)
    c.drawPath(area, fill=1, stroke=0)

    path = c.beginPath()
    path.moveTo(pts[0][0], pts[0][1])
    for px, py in pts[1:]:
        path.lineTo(px, py)
    c.setStrokeColor(COLOR_BLUE)
    c.setLineWidth(2.2)
    c.drawPath(path, fill=0, stroke=1)

    for px, py in pts:
        c.setFillColor(white)
        c.setStrokeColor(COLOR_BLUE)
        c.setLineWidth(1.5)
        c.circle(px, py, 3.6, stroke=1, fill=1)

    c.setFillColor(COLOR_MUTED)
    c.setFont(fonts["ENBody"], 8)
    c.drawString(chart_left, chart_bottom + chart_h + 8, f"{values[0]:.1f} kg")
    c.drawRightString(chart_left + chart_w, chart_bottom + chart_h + 8, f"{values[-1]:.1f} kg")


def draw_metric_card(
    c: canvas.Canvas,
    x: float,
    y: float,
    w: float,
    h: float,
    *,
    title_cn: str,
    title_en: str,
    icon_text: str,
    accent,
    label: str,
    value: str,
    note: str,
    fonts: dict[str, str],
) -> None:
    draw_round_card(c, x, y, w, h, accent)
    draw_section_header(c, x + 18, y + h - 36, title_cn, title_en, accent, icon_text, fonts)
    c.setFillColor(COLOR_MUTED)
    c.setFont(fonts["CNBody"], 8.8)
    c.drawString(x + 18, y + h - 82, label)
    c.setFillColor(COLOR_TEXT)
    c.setFont(fonts["CNHeading"], 16.5)
    c.drawString(x + 18, y + h - 106, value)
    note_top = y + h - 126
    draw_text_block(
        c,
        note,
        x + 18,
        note_top,
        w - 36,
        font_name=fonts["CNBody"],
        font_size=8.5,
        leading=10.8,
        color=COLOR_MUTED,
    )


def draw_bullet_list(
    c: canvas.Canvas,
    items: list[str],
    x: float,
    top_y: float,
    width: float,
    *,
    bullet_color,
    font_name: str,
    font_size: float,
    leading: float,
) -> float:
    y = top_y
    for item in items:
        c.setFillColor(bullet_color)
        c.circle(x + 4, y - 1, 2.2, stroke=0, fill=1)
        y = draw_text_block(
            c,
            item,
            x + 14,
            y + 4,
            width - 18,
            font_name=font_name,
            font_size=font_size,
            leading=leading,
            color=COLOR_TEXT,
        )
        y -= 10
    return y


def compute_layout(data: dict, fonts: dict[str, str]) -> dict[str, float]:
    top_margin = 28.0
    header_h = 88.0
    gap = 18.0
    top_row_h = 220.0
    metric_note_h = max(
        measure_text_height(data["nutrition_note"], 129, fonts["CNBody"], 8.5, 10.8),
        measure_text_height(data["hydration_note"], 129, fonts["CNBody"], 8.5, 10.8),
        measure_text_height(data["sleep_note"], 129, fonts["CNBody"], 8.5, 10.8),
    )
    metrics_h = max(148.0, 138.0 + metric_note_h)
    bottom_margin = 26.0

    highlights_text_h = measure_bullet_list_height(
        data["highlights"],
        214,
        fonts["CNBody"],
        10.3,
        14.2,
    )
    highlights_h = max(180.0, 54.0 + highlights_text_h + 24.0)

    verdict_text_h = 0.0
    for line in data["verdict"]:
        verdict_text_h += measure_text_height(line, 214, fonts["CNBody"], 10.2, 13.6) + 8.0
    verdict_h = max(190.0, 106.0 + verdict_text_h + 18.0)

    next_text_h = measure_bullet_list_height(
        data["next_week"],
        492,
        fonts["CNBody"],
        10.0,
        13.4,
    )
    next_h = max(118.0, 52.0 + next_text_h + 18.0)

    content_h = (
        top_margin
        + header_h
        + gap
        + top_row_h
        + gap
        + metrics_h
        + gap
        + max(highlights_h, verdict_h)
        + gap
        + next_h
        + bottom_margin
    )
    page_h = max(PAGE_HEIGHT, content_h)

    header_y = page_h - top_margin - header_h
    top_cards_y = header_y - gap - top_row_h
    metrics_y = top_cards_y - gap - metrics_h
    lower_top = metrics_y - gap
    highlights_y = lower_top - highlights_h
    verdict_y = lower_top - verdict_h
    next_y = min(highlights_y, verdict_y) - gap - next_h

    return {
        "page_h": page_h,
        "header_y": header_y,
        "top_cards_y": top_cards_y,
        "metrics_y": metrics_y,
        "metrics_h": metrics_h,
        "highlights_y": highlights_y,
        "highlights_h": highlights_h,
        "verdict_y": verdict_y,
        "verdict_h": verdict_h,
        "next_y": next_y,
        "next_h": next_h,
    }


def render_report(data: dict, output_path: Path) -> None:
    fonts = register_fonts()
    layout = compute_layout(data, fonts)
    c = canvas.Canvas(str(output_path), pagesize=(PAGE_WIDTH, layout["page_h"]))
    c.setTitle("每周体能复盘")

    c.setFillColor(COLOR_BG)
    c.rect(0, 0, PAGE_WIDTH, layout["page_h"], stroke=0, fill=1)

    margin_x = 34.0
    header_y = layout["header_y"]
    c.setFillColor(COLOR_NAVY)
    c.roundRect(margin_x, header_y, PAGE_WIDTH - margin_x * 2, 88, 24, stroke=0, fill=1)
    c.setFillColor(HexColor("#25477F"))
    c.roundRect(margin_x, header_y, PAGE_WIDTH - margin_x * 2, 12, 24, stroke=0, fill=1)
    c.setFillColor(white)
    c.setFont(fonts["CNHeading"], 24)
    c.drawString(margin_x + 20, header_y + 53, "每周体能复盘")
    c.setFont(fonts["ENBody"], 11)
    c.drawString(margin_x + 22, header_y + 32, "WEEKLY FITNESS PERFORMANCE REPORT")
    c.setFillColor(HexColor("#D6E2F2"))
    c.setFont(fonts["CNBody"], 10.5)
    c.drawString(margin_x + 20, header_y + 16, f"{data['date_range']}    {data['goal']}")
    c.setFillColor(white)
    c.setFont(fonts["CNHeading"], 13)
    c.drawRightString(PAGE_WIDTH - margin_x - 20, header_y + 54, data["client"])
    c.setFillColor(HexColor("#BFD0E6"))
    c.setFont(fonts["ENBody"], 8.8)
    c.drawRightString(PAGE_WIDTH - margin_x - 20, header_y + 34, "CLIENT PROFILE")

    left_x = margin_x
    top_cards_y = layout["top_cards_y"]

    draw_round_card(c, left_x, top_cards_y, 332, 220, COLOR_BLUE)
    draw_section_header(c, left_x + 18, top_cards_y + 184, "体重趋势", "Body Progress", COLOR_BLUE, "重", fonts)
    c.setFillColor(COLOR_BLUE)
    c.setFont(fonts["ENBold"], 27)
    c.drawString(left_x + 20, top_cards_y + 146, f"{data['weekly_delta']:+.1f} kg")
    c.setFillColor(COLOR_MUTED)
    c.setFont(fonts["CNBody"], 10)
    c.drawString(left_x + 112, top_cards_y + 152, "本周体重变化")
    c.setFillColor(COLOR_TEXT)
    c.setFont(fonts["CNHeading"], 11.5)
    c.drawString(left_x + 20, top_cards_y + 126, f"周初 {data['weight_points'][0]:.1f} kg")
    c.drawString(left_x + 122, top_cards_y + 126, f"周末 {data['weight_points'][-1]:.1f} kg")
    draw_line_chart(c, left_x + 16, top_cards_y + 38, 300, 76, fonts=fonts, values=data["weight_points"])
    draw_text_block(
        c,
        "体重曲线呈现平滑下行，说明当前热量缺口足够有效，但没有把恢复压得过头。",
        left_x + 20,
        top_cards_y + 28,
        288,
        font_name=fonts["CNBody"],
        font_size=10.2,
        leading=13.5,
        color=COLOR_MUTED,
    )

    right_x = left_x + 350
    draw_round_card(c, right_x, top_cards_y, 177, 220, COLOR_GREEN)
    draw_section_header(c, right_x + 18, top_cards_y + 184, "训练执行", "Training Score", COLOR_GREEN, "练", fonts)
    ratio = data["training_completed"] / max(data["training_planned"], 1)
    draw_donut(
        c,
        right_x + 88,
        top_cards_y + 124,
        36,
        ratio,
        accent=COLOR_GREEN,
        track=COLOR_GREEN_SOFT,
        text_top=f"{int(ratio * 100)}%",
        text_bottom="执行率",
        fonts=fonts,
    )
    c.setFillColor(COLOR_TEXT)
    c.setFont(fonts["CNHeading"], 11)
    c.drawCentredString(
        right_x + 88,
        top_cards_y + 66,
        f"{data['training_completed']} / {data['training_planned']} 次训练完成",
    )
    c.setFillColor(COLOR_MUTED)
    c.setFont(fonts["CNBody"], 9.5)
    c.drawCentredString(right_x + 88, top_cards_y + 48, f"总训练时长 {data['training_minutes']} 分钟")

    metrics_y = layout["metrics_y"]
    metric_w = 165
    gap = 16
    draw_metric_card(
        c,
        left_x,
        metrics_y,
        metric_w,
        layout["metrics_h"],
        title_cn="饮食",
        title_en="Nutrition",
        icon_text="食",
        accent=COLOR_RED,
        label=data["nutrition_label"],
        value=data["nutrition_value"],
        note=data["nutrition_note"],
        fonts=fonts,
    )
    draw_metric_card(
        c,
        left_x + metric_w + gap,
        metrics_y,
        metric_w,
        layout["metrics_h"],
        title_cn="补水",
        title_en="Hydration",
        icon_text="水",
        accent=COLOR_BLUE,
        label=data["hydration_label"],
        value=data["hydration_value"],
        note=data["hydration_note"],
        fonts=fonts,
    )
    draw_metric_card(
        c,
        left_x + (metric_w + gap) * 2,
        metrics_y,
        metric_w,
        layout["metrics_h"],
        title_cn="睡眠",
        title_en="Sleep",
        icon_text="眠",
        accent=COLOR_TEAL,
        label=data["sleep_label"],
        value=data["sleep_value"],
        note=data["sleep_note"],
        fonts=fonts,
    )

    draw_round_card(c, left_x, layout["highlights_y"], 252, layout["highlights_h"], COLOR_GREEN)
    draw_section_header(
        c,
        left_x + 18,
        layout["highlights_y"] + layout["highlights_h"] - 36,
        "本周亮点",
        "Highlights",
        COLOR_GREEN,
        "亮",
        fonts,
    )
    draw_bullet_list(
        c,
        data["highlights"],
        left_x + 18,
        layout["highlights_y"] + layout["highlights_h"] - 72,
        214,
        bullet_color=COLOR_GREEN,
        font_name=fonts["CNBody"],
        font_size=10.3,
        leading=14.2,
    )

    verdict_x = left_x + 270
    draw_round_card(c, verdict_x, layout["verdict_y"], 257, layout["verdict_h"], COLOR_NAVY)
    draw_section_header(
        c,
        verdict_x + 18,
        layout["verdict_y"] + layout["verdict_h"] - 36,
        "教练结论",
        "Coach Verdict",
        COLOR_NAVY,
        "评",
        fonts,
    )
    c.setFillColor(COLOR_MUTED)
    c.setFont(fonts["CNBody"], 9.5)
    c.drawString(verdict_x + 18, layout["verdict_y"] + layout["verdict_h"] - 78, "恢复状态")
    c.setFillColor(COLOR_ORANGE_SOFT)
    c.roundRect(verdict_x + 82, layout["verdict_y"] + layout["verdict_h"] - 92, 88, 24, 12, stroke=0, fill=1)
    c.setFillColor(COLOR_ORANGE)
    c.setFont(fonts["CNHeading"], 10.5)
    c.drawCentredString(verdict_x + 126, layout["verdict_y"] + layout["verdict_h"] - 84, data["recovery_status"])
    c.setFillColor(COLOR_MUTED)
    c.setFont(fonts["CNBody"], 9.4)
    c.drawString(verdict_x + 18, layout["verdict_y"] + layout["verdict_h"] - 110, data["rhr_note"])
    c.drawString(verdict_x + 18, layout["verdict_y"] + layout["verdict_h"] - 126, data["hrv_note"])

    verdict_y = layout["verdict_y"] + layout["verdict_h"] - 146
    for line in data["verdict"]:
        verdict_y = draw_text_block(
            c,
            line,
            verdict_x + 18,
            verdict_y,
            221,
            font_name=fonts["CNBody"],
            font_size=10.2,
            leading=13.6,
            color=COLOR_TEXT,
        )
        verdict_y -= 8

    draw_round_card(c, left_x, layout["next_y"], 527, layout["next_h"], COLOR_TEAL)
    draw_section_header(c, left_x + 18, layout["next_y"] + layout["next_h"] - 36, "下周动作", "Next Week Focus", COLOR_TEAL, "下", fonts)
    draw_bullet_list(
        c,
        data["next_week"],
        left_x + 18,
        layout["next_y"] + layout["next_h"] - 72,
        492,
        bullet_color=COLOR_TEAL,
        font_name=fonts["CNBody"],
        font_size=10.0,
        leading=13.4,
    )

    c.setFillColor(COLOR_MUTED)
    c.setFont(fonts["ENBody"], 8.5)
    c.drawString(left_x, 12, "Premium weekly fitness PDF styling")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    c.save()


def main() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description="Generate a polished weekly fitness PDF report.")
    parser.add_argument("--output", type=Path, help="Output PDF path. Defaults to the current week's Monday-based filename.")
    parser.add_argument("--input", type=Path, help="Optional JSON summary payload for the report.")
    parser.add_argument("--week-start", type=str, help="Optional Monday date in YYYY-MM-DD format for the default output filename.")
    args = parser.parse_args()

    week_start = parse_week_start(args.week_start)
    output_path = args.output.resolve() if args.output else default_output_path(repo_root, week_start).resolve()
    data = load_report_data(args.input)
    render_report(data, output_path)
    print(output_path)


if __name__ == "__main__":
    main()
