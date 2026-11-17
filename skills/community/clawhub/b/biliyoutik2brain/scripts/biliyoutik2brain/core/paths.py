"""统一存储路径管理

替代散落在各模块中的 os.path.expanduser("~/openclaw/...") 调用。
可通过环境变量 BILI_STORAGE_HOME 覆盖存储根目录。
"""

import os

# ── 存储根目录 ──
_STORAGE_HOME = os.environ.get(
    "BILI_STORAGE_HOME",
    os.path.join(os.path.expanduser("~"), "openclaw", "workspace", "storage"),
)

# ── 子目录 ──
TRANSCRIPTS_DIR = os.path.join(_STORAGE_HOME, "transcripts")
NOTES_DIR = os.path.join(_STORAGE_HOME, "notes")
CARDS_DIR = os.path.join(_STORAGE_HOME, "cards")
ERRORS_DIR = os.path.join(_STORAGE_HOME, "errors")
KNOWLEDGE_DIR = os.path.join(_STORAGE_HOME, "knowledge")
COMMENTS_DIR = os.path.join(_STORAGE_HOME, "comments")

# ── 自动创建（允许 race condition，调用者失败时自行重试） ──
for _d in [TRANSCRIPTS_DIR, NOTES_DIR, CARDS_DIR, ERRORS_DIR, KNOWLEDGE_DIR, COMMENTS_DIR]:
    os.makedirs(_d, exist_ok=True)


def storage_path(sub: str, *parts: str) -> str:
    """返回存储子目录下的文件路径，自动确保父目录存在。

    用法:
        p = storage_path("transcripts", "UP主名_视频ID.md")
    """
    sub_dir = os.path.join(_STORAGE_HOME, sub)
    os.makedirs(sub_dir, exist_ok=True)
    return os.path.join(sub_dir, *parts)
