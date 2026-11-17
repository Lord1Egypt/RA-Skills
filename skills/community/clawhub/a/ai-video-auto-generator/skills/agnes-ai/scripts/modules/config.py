"""agnes-ai 配置/工具函数。"""
import os, sys

# 加载主 skill 共享工具函数（零跨 skill import）
_SHARED_SCRIPTS = os.path.normpath(os.path.join(
    os.path.dirname(__file__), *(4 * [os.pardir]), "scripts"
))
if _SHARED_SCRIPTS not in sys.path:
    sys.path.insert(0, _SHARED_SCRIPTS)
from _shared_tools import (
    _aspect_to_size, _auto_size, _parse_shot_range,
    _safe_write_json, _progress_str, _resolve_generation_refs,
    _log, set_log_file, LOG_LEVEL,
    get, _legacy,
)


def get_agnes_key() -> str | None:
    """从 config.toml 的 [agnes] api_key 读取 Agnes AI Key。"""
    return get("agnes", "api_key") or _legacy("~/.agnes-api-key", "AGNES_API_KEY")


def get_agnes_api_base() -> str:
    """从 config.toml 读取 Agnes API base URL，失败时回退到硬编码默认值。"""
    return get("agnes", "api_base") or "https://apihub.agnes-ai.com/v1"


def get_agnes_default_model() -> str:
    """从 config.toml 读取默认图片模型，失败时回退到硬编码默认值。"""
    return get("agnes", "default_image_model") or "agnes-image-2.1-flash"


def get_github_repo() -> str:
    """从 config.toml [github] 读取图床仓库，失败时回退。"""
    return get("github", "repo") or "JinXuchen2020/video-images"


def get_github_branch() -> str:
    """从 config.toml [github] 读取图床分支，失败时回退。"""
    return get("github", "branch") or "master"


# ══════════════════════════════════
# 通用工具函数（与 project-generate 共享自 _shared_tools.py）
# ══════════════════════════════════

# 以下函数定义在 scripts/_shared_tools.py 中，通过 sys.path 导入：
#   _aspect_to_size, _auto_size, _parse_shot_range,
#   _safe_write_json, _progress_str, _resolve_generation_refs
