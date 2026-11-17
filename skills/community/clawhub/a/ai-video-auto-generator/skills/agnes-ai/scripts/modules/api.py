"""向后兼容 — 原 api.py 拆分为 image_api.py + video_api.py。"""
from image_api import API_BASE, DEFAULT_MODEL, VERSION, load_api_key, upload_to_url, generate_image
from video_api import (
    API_BASE_VIDEO, DEFAULT_VIDEO_MODEL, DURATION_PRESETS, ASPECT_MAP,
    submit_video, quick_query, poll_task, download_video,
    get_closest_valid_frames, parse_size, _select_mode,
    get_last_submit_result, _log,
)
