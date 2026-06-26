"""通用常量 + 小工具集（无业务逻辑）。

这个文件存放：
  - BizyAir HTTP API 端点常量（API_BASE / CREATE_URL / WEBAPP_DETAIL_URL ...）
  - 网络/超时常量（DEFAULT_TIMEOUT / POLL_INTERVAL / MAX_POLL_SECONDS）
  - 字段识别规则集合（PROMPT_EXCLUDE_* / KNOWN_PROMPT_* / TEXT_INPUT_FIELD_TYPES）
  - 通用文本归一化与匹配评分函数（normalized_text / classify_route_match / count_term_matches ...）

被 api / contract / remote / search 等几乎所有模块依赖。修改这里要谨慎，传染面大。
"""
from __future__ import annotations
import argparse, json, re
from pathlib import Path
from paths import config_display_path as preferred_config_display_path
from typing import Any

API_BASE = 'https://api.bizyair.cn'

CREATE_URL = f'{API_BASE}/w/v1/webapp/task/openapi/create'

DETAIL_URL = f'{API_BASE}/w/v1/webapp/task/openapi/detail'

OUTPUTS_URL = f'{API_BASE}/w/v1/webapp/task/openapi/outputs'

UPLOAD_TOKEN_URL = f'{API_BASE}/x/v1/upload/token'

INPUT_COMMIT_URL = f'{API_BASE}/x/v1/input_resource/commit'

COMMUNITY_URL = f'{API_BASE}/x/v1/bizy_models/community'

OFFICIAL_URL = f'{API_BASE}/x/v1/bizy_models/official'

BIZY_MODEL_DETAIL_URL = f'{API_BASE}/x/v1/bizy_models'

RESOLVE_VERSION_URL = f'{API_BASE}/x/v1/resolve/BizyModelVersion'

SCRIPT_DIR = Path(__file__).resolve().parent

DEFAULT_TIMEOUT = 60

POLL_INTERVAL = 5

MAX_POLL_SECONDS = 900

WEBAPP_RETRY_LIMIT = 1

SEARCH_MIN_ROUNDS = 3

SEARCH_MAX_ROUNDS = 5

BIZYAIR_INFO_HOSTS = {'bizyair.cn', 'www.bizyair.cn'}

PROMPT_EXCLUDE_EN = {'title', 'caption', 'subtitle', 'watermark', 'label', 'logo'}  # 仅用于 info/prefill 展示标注

PROMPT_EXCLUDE_ZH = {'标题', '副标题', '字幕', '水印', '标签', '标语', '角标', '徽标'}  # 仅用于 info/prefill 展示标注

EXPLICIT_PROMPT_LABELS = {'prompt', 'text', '提示词', '文本', '正向提示词', '文本提示词'}  # 仅用于 info/prefill 展示标注

TEXT_INPUT_FIELD_TYPES = {'customtext', 'textarea', 'text', 'string'}

KNOWN_PROMPT_NODE_MARKERS = {'cliptextencode', 'primitivestringmultiline', 'primitivestring'}  # 仅用于 info/prefill 展示标注

KNOWN_PROMPT_FIELD_NAMES = {'prompt', 'user_prompt', 'positive_prompt'}  # 仅用于 info/prefill 展示标注

REMOTE_EXPOSED_CONTRACT_SOURCES = {'execution_target.webapp_detail.input_nodes', 'webapp_detail.input_nodes'}

REMOTE_GENERIC_PROMPT_ALIASES = {'prompt', 'text', 'value', 'positiveprompt', 'positive_prompt', 'userprompt', 'user_prompt'}

REMOTE_CONTRACT_SOURCE_PRIORITY = ['execution_target.webapp_detail.input_nodes', 'webapp_detail.input_nodes', 'workflow_hints']

def normalized_text(text: Any) -> str:
    return (str(text) if text is not None else '').strip().lower()

def config_display_path() -> str:
    return preferred_config_display_path()

def local_script_command(script_name: str, *args: str) -> str:
    script_path = (SCRIPT_DIR / script_name).resolve()
    parts = ['python3', str(script_path)]
    parts.extend((str(arg) for arg in args))
    return ' '.join(parts)

def safe_int(value: Any) -> int:
    try:
        return int(value)
    except Exception:
        return 0

def add_unique_key(items: list[str], value: str | None) -> None:
    text = str(value or '').strip()
    if text and text not in items:
        items.append(text)


WORKFLOW_LINK_NOT_SUPPORTED_MESSAGE = '你发的是 ComfyUI 的 workflow 链接（comfy-ui?id=xxx），这种链接目前不支持直接运行～\n\n如果你想执行这个工作流，可以去 BizyAir 社区找一下它对应的 AI 应用版本，把 AI 应用的链接发给我就行。\n\nAI 应用链接长这样：https://bizyair.cn/community/app/xxxxx'


def build_prompt_bundle_for_args(args: argparse.Namespace, *, route_name: str | None=None, modality: str | None=None, task: str | None=None, input_profile: dict[str, Any] | None=None) -> dict[str, Any]:
    cached = getattr(args, '_compiled_prompt_bundle', None)
    signature = (str(getattr(args, 'prompt', None) or ''), route_name, modality, task, json.dumps(input_profile or {}, ensure_ascii=False, sort_keys=True), len(getattr(args, 'image', None) or []), len(getattr(args, 'audio', None) or []))
    if isinstance(cached, dict) and cached.get('_signature') == signature:
        return cached
    raw = re.sub(r'\s+', ' ', str(getattr(args, 'prompt', None) or '').strip())
    bundle = {'raw_prompt': raw, 'card_display_prompt': raw, 'execution_prompt': raw, 'polished_prompt': raw, 'structured_prompt': raw, 'enriched_prompt': raw, 'rewritten_prompt': '', 'negative_prompt': '', 'changed': False, 'polish_notes': [], 'mode': None, 'mode_source': 'passthrough', 'style_profile': {'name': None, 'source': 'none', 'en_hint': None}, 'rewrite_applied': False}
    bundle['_signature'] = signature
    setattr(args, '_compiled_prompt_bundle', bundle)
    return bundle
