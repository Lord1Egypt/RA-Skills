# agnes-ai modules — 统一导出（仅含生成层模块，项目级命令在 project-generate）

import sys, os
_THIS_DIR = os.path.dirname(os.path.abspath(__file__))
if _THIS_DIR not in sys.path:
    sys.path.insert(0, _THIS_DIR)

from config import (
    _aspect_to_size, _auto_size, _parse_shot_range, _safe_write_json,
    _progress_str, _resolve_generation_refs,
    LOG_LEVEL, _log,
)
from image_api import API_BASE, DEFAULT_MODEL, VERSION, load_api_key, upload_to_url, generate_image
from prompt import _generate_prompt_template, _clean_prompt, _resolve_single_shot_params, _build_first_frame

__all__ = [
    # config
    "_aspect_to_size", "_auto_size", "_parse_shot_range", "_safe_write_json",
    "_progress_str", "_resolve_generation_refs",
    "LOG_LEVEL", "_log",
    # api
    "API_BASE", "DEFAULT_MODEL", "VERSION", "load_api_key", "upload_to_url", "generate_image",
    # prompt
    "_generate_prompt_template", "_clean_prompt", "_resolve_single_shot_params", "_build_first_frame",
]
