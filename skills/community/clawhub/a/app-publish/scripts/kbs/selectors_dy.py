"""抖音创作者中心 — 内容上传页选择器与文案。

上传页: https://creator.douyin.com/creator-micro/content/upload
"""

from __future__ import annotations

UPLOAD_URL = "https://creator.douyin.com/creator-micro/content/upload"

VIDEO_FILE_INPUT = 'input[type="file"]'
COVER_FILE_INPUT = 'input[type="file"]'

TITLE_INPUT_CANDIDATES: tuple[str, ...] = (
    'input[placeholder*="标题"]',
    'textarea[placeholder*="标题"]',
    'div[contenteditable="true"]',
)

TAG_INPUT_CANDIDATES: tuple[str, ...] = (
    'input[placeholder*="话题"]',
    'input[placeholder*="推荐"]',
)

PUBLISH_BUTTON_CANDIDATES: tuple[str, ...] = ()

TEXT_VIDEO_READY_HINTS: tuple[str, ...] = (
    "上传成功",
    "上传完成",
    "封面编辑",
    "作品描述",
)
TEXT_UPLOAD_FAIL_HINTS: tuple[str, ...] = ("上传失败", "不支持", "超限")
