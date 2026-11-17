"""
统一配置加载器 + 通用工具函数。不依赖任何 AI 工具。
配置通过 init_config(skill_root, project) 显式初始化，配置只来自项目/config/ 和 skill/config/。
"""

from __future__ import annotations
import os, sys
from typing import Optional

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
    init_config, get, _legacy,
)


def init_skill_config(skill_root: str, project: str | None = None) -> dict:
    """初始化配置并返回（对 init_config 的简单封装）。"""
    return init_config(skill_root, project)


def get_agnes_key() -> Optional[str]:
    return get("agnes", "api_key") or _legacy("~/.agnes-api-key", "AGNES_API_KEY")


def get_github_pat() -> Optional[str]:
    return get("github", "pat") or _legacy("~/.github-pat", "GITHUB_PAT")


def get_feishu_base_token() -> Optional[str]:
    # base_token 已从 config.toml 迁出；缺失时回退 ~/.feishu-base-token 文件或 FEISHU_BASE_TOKEN 环境变量
    return get("feishu", "base_token") or _legacy("~/.feishu-base-token", "FEISHU_BASE_TOKEN")


def get_feishu_table_id() -> Optional[str]:
    return get("feishu", "table_id")


def get_feishu_workflow_table_id() -> Optional[str]:
    return get("feishu", "workflow_table_id")


def get_freesound_key() -> Optional[str]:
    return get("freesound", "api_key") or _legacy("~/.freesound-api-key", "FREESOUND_API_KEY")


def get_xiaoyunqiao_access_key() -> Optional[str]:
    """小云雀 AccessKey（与 get_xyq_ak 同义，推荐使用全称）。"""
    return (get("xiaoyunqiao", "access_key")
            or _legacy("~/.xyq-access-key", "VOLCENGINE_ACCESS_KEY")
            or os.environ.get("XYQ_ACCESS_KEY"))


def get_xiaoyunqiao_secret_key() -> Optional[str]:
    """小云雀 SecretKey（与 get_xyq_sk 同义，推荐使用全称）。"""
    return (get("xiaoyunqiao", "secret_key")
            or _legacy("~/.xyq-secret-key", "VOLCENGINE_SECRET_KEY")
            or os.environ.get("XYQ_SECRET_KEY"))


def get_xyq_ak() -> Optional[str]:
    """小云雀 AccessKey（简写，为新别名的 alias）。"""
    return get_xiaoyunqiao_access_key()


def get_xyq_sk() -> Optional[str]:
    """小云雀 SecretKey（简写，为新别名的 alias）。"""
    return get_xiaoyunqiao_secret_key()


# ── 图床配置 ───────────────────────────────

def get_img_host() -> str:
    """图床提供者名称，默认 'github'。"""
    return get("img_host", "provider", "github")


def get_github_repo() -> str:
    """GitHub 图床仓库，如 'JinXuchen2020/video-images'。"""
    return get("github", "repo") or "JinXuchen2020/video-images"


def get_github_branch() -> str:
    """GitHub 图床分支，默认 'master'。"""
    return get("github", "branch") or "master"


# ══════════════════════════════════
# 通用工具函数（来自 _shared_tools.py）
# ══════════════════════════════════

# 以下函数定义在 scripts/_shared_tools.py 中，通过 sys.path 导入：
#   _aspect_to_size, _auto_size, _parse_shot_range,
#   _safe_write_json, _progress_str, _resolve_generation_refs


# ── 路径工具函数（统一入口，消除 4 处重复定义）──

def _script_path(project: str) -> str:
    """返回 script.json 绝对路径。"""
    return os.path.join(project, "script.json")


def _videos_dir(project: str) -> str:
    """返回 videos/ 目录绝对路径。"""
    return os.path.join(project, "videos")


def _output_dir(project: str) -> str:
    """返回 output/ 目录绝对路径。"""
    return os.path.join(project, "output")


def _sounds_dir(project: str) -> str:
    """返回 sounds/ 目录绝对路径。"""
    return os.path.join(project, "sounds")
