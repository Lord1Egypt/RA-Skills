from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Tuple

DEFAULT_STATE_DIR = Path('/tmp/macos_desktop_control')
DEFAULT_CALIBRATION_PATH = DEFAULT_STATE_DIR / 'calibration.json'


def ensure_state_dir() -> None:
    DEFAULT_STATE_DIR.mkdir(parents=True, exist_ok=True)


def save_calibration(data: Dict[str, Any], path: Path = DEFAULT_CALIBRATION_PATH) -> None:
    ensure_state_dir()
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')


def load_calibration(path: Path = DEFAULT_CALIBRATION_PATH) -> Dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(
            f'Calibration file not found: {path}. Run scripts/init_coordinate_mapping.py first.'
        )
    return json.loads(path.read_text(encoding='utf-8'))


def ensure_calibration(path: Path = DEFAULT_CALIBRATION_PATH) -> Dict[str, Any]:
    if path.exists():
        return load_calibration(path)

    import pyautogui

    screenshot = pyautogui.screenshot()
    screen_w, screen_h = pyautogui.size()
    shot_w, shot_h = screenshot.size

    scale_x = shot_w / screen_w
    scale_y = shot_h / screen_h
    mode = 'retina' if round(scale_x, 2) == 2.0 and round(scale_y, 2) == 2.0 else 'unknown'

    data = {
        'screen_width_points': screen_w,
        'screen_height_points': screen_h,
        'screenshot_width_pixels': shot_w,
        'screenshot_height_pixels': shot_h,
        'scale_x': scale_x,
        'scale_y': scale_y,
        'mode': mode,
        'note': 'auto-initialized on first use when calibration.json is missing.',
    }
    save_calibration(data, path)
    return data


def pixel_to_point(x: float, y: float, calibration: Dict[str, Any]) -> Tuple[float, float]:
    return x / float(calibration['scale_x']), y / float(calibration['scale_y'])


def point_to_pixel(x: float, y: float, calibration: Dict[str, Any]) -> Tuple[float, float]:
    return x * float(calibration['scale_x']), y * float(calibration['scale_y'])
