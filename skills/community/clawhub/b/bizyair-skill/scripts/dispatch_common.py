"""dispatch.py 的公共逻辑 + 10 个固定模型（图片 5 + 视频 5）+ 4 类搜索路由（图片/视频 × ModelZoo/AI 应用）的元数据。

承载 dispatch.py 跑起来需要的几样东西：
  - APP_SCRIPT / DISPATCH_SCRIPT: 子进程调度时拼命令的路径常量
  - MODEL_MAP: 用户输入的别名 → 内部 slug
  - ROUTE_TABLE: slug → ModelZoo endpoint + modality（**加新菜单模型从这里改**）
  - SCENE_NUMBER_MAP: 菜单数字 → slug（"5" → "b2-t2i" / "v2" → "happyhorse-t2v" / "6" → "modelzoo-search-flow" / "7" → "remote-search-flow"）
  - COMPILER_RULES: slug → defaults。**只有 defaults，没有 fields**——字段集合 / 中文标签 / 可选值全部从远端 contract 动态拿
  - IMAGE_SCENE_MENU / VIDEO_SCENE_MENU: 用户看到的菜单文案（从 config/menus.json 加载）
  - 各种 runtime_state（续跑缓存）、batch policy、subprocess 调度工具

【加一个新菜单模型怎么改】
  1) ROUTE_TABLE 加一行 {'slug': {'endpoint': '<modelzoo-endpoint>', 'modality': 'image/video'}}（注：表是从 config/routes.json 加载的，要加去那里的 image / video 段）
  2) MODEL_MAP 加几条别名 → slug
  3) config/routes.json 的 scene_number_map 占用一个空槽位
  4) config/menus.json 的对应菜单文案补一行
  5) display_model_name 的 names 表加一条
  6) （可选）COMPILER_RULES 加 defaults，让卡片有合理的默认值
  字段、可选值、中文标签、推荐文案——全都不用动，从远端 contract 自动拿。
"""
from __future__ import annotations
import argparse, hashlib, json, os, re, subprocess, sys, time
from collections.abc import Callable
from pathlib import Path
from paths import config_display_path as preferred_config_display_path, load_config_json, resolve_runtime_state_file
from common import normalized_text
from typing import Any

SCRIPT_DIR = Path(__file__).resolve().parent

# 子进程调度的目标脚本路径。dispatch.py 把活分给 app.py（远端 CLI），
# batch.py 把 batch worker 子进程分给 dispatch.py 自己。
# 注意：千万别用 Path(__file__) 当 worker 入口——之前 batch.py 这么写过，
# 因为 batch.py 没有 main()，导致整个 --batch-run 静默失败。
APP_SCRIPT = SCRIPT_DIR / 'app.py'

DISPATCH_SCRIPT = SCRIPT_DIR / 'dispatch.py'

# 用户输入的别名 → 内部 slug。键全部小写比较。
MODEL_MAP = {'bpro-t2i': 'bpro-t2i', '通用图片b.pro': 'bpro-t2i', 'fkmax-t2i': 'fkmax-t2i', 'flux-2-klein': 'fkmax-t2i', 'flux klein': 'fkmax-t2i', 'flux kontext max': 'fkmax-t2i', '通用图片f.k.max': 'fkmax-t2i', 'seedream5-t2i': 'seedream5-t2i', '即梦5.0': 'seedream5-t2i', '即梦': 'seedream5-t2i', 'seedream': 'seedream5-t2i', 'o2-t2i': 'o2-t2i', '通用图片o.2': 'o2-t2i', 'b2-t2i': 'b2-t2i', '通用图片b.2': 'b2-t2i', 'v31pro-t2v': 'v31pro-t2v', '通用视频v.3.1.pro': 'v31pro-t2v', 'happyhorse-t2v': 'happyhorse-t2v', 'happyhorse': 'happyhorse-t2v', '快乐马': 'happyhorse-t2v', 'kling30-t2v': 'kling30-t2v', 'kling3.0': 'kling30-t2v', 'kling': 'kling30-t2v', 'wan27-t2v': 'wan27-t2v', 'wan2.7': 'wan27-t2v', 'wan': 'wan27-t2v', 'seedance2-t2v': 'seedance2-t2v', 'seedance': 'seedance2-t2v', 'seedance 2.0': 'seedance2-t2v'}

# 用户没明确指模型时，按 task 类型回落到的默认 slug。
TASK_DEFAULTS = {'text-to-image': 'bpro-t2i', 'illustration-anime': 'bpro-t2i', 'commercial-visual': 'seedream5-t2i', 'text-layout-image': 'o2-t2i', 'text-to-video': 'wan27-t2v', 'cinematic-video': 'v31pro-t2v'}

# slug → ModelZoo endpoint + 模态。固定模型直接调 ModelZoo API 执行，非固定模型走 app.py webapp 路径。
# 路由表和菜单从 config/ 加载（**加新菜单模型只改 config/routes.json + config/menus.json**）
def _load_routes_config():
    config_dir = SCRIPT_DIR.parent / 'config'
    routes_file = config_dir / 'routes.json'
    if routes_file.exists():
        data = json.loads(routes_file.read_text(encoding='utf-8'))
        table = {}
        for slug, info in (data.get('image') or {}).items():
            table[slug] = {'endpoint': info['endpoint'], 'modality': 'image'}
        for slug, info in (data.get('video') or {}).items():
            table[slug] = {'endpoint': info['endpoint'], 'modality': 'video'}
        return table, data.get('scene_number_map') or {}
    return {}, {}

def _load_menus_config():
    config_dir = SCRIPT_DIR.parent / 'config'
    menus_file = config_dir / 'menus.json'
    if menus_file.exists():
        data = json.loads(menus_file.read_text(encoding='utf-8'))
        return data.get('image_menu', ''), data.get('video_menu', '')
    return '', ''

_rt, _snm = _load_routes_config()
_im, _vm = _load_menus_config()
ROUTE_TABLE = _rt
IMAGE_SCENE_MENU = _im
VIDEO_SCENE_MENU = _vm
SCENE_NUMBER_MAP = _snm

# slug → 默认参数。**只有 defaults，没有 fields**——字段集合 / 中文标签 / 可选值
# 全部从远端 contract 动态拿（见 remote.choose_remote_field_display_label
# / humanize_remote_prefill_label）。这里的 defaults 用来在两个地方兜底：
#   1) card.compile_card_selection 里"用户没填、notes 也没推断"的字段
#   2) batch.should_batch_use_defaults 用来判断这个 model 是否走"无参数直接跑"
# 加新模型可以不写 defaults，写了就当兜底。
COMPILER_RULES = {'bpro-t2i': {'defaults': {'aspect_ratio': '1:1', 'resolution': '4K'}}, 'fkmax-t2i': {'defaults': {'width': 1536, 'height': 1024}}, 'seedream5-t2i': {'defaults': {'aspect_ratio': '4:3', 'resolution': '2K'}}, 'o2-t2i': {'defaults': {'width': 1280, 'height': 1280}}, 'b2-t2i': {'defaults': {'aspect_ratio': '2:3', 'resolution': '2k'}}, 'v31pro-t2v': {'defaults': {'model_name': 'veo3.1-pro', 'aspect_ratio': '16:9'}}, 'happyhorse-t2v': {'defaults': {'aspect_ratio': '16:9', 'resolution': '1080P', 'duration': 7}}, 'kling30-t2v': {'defaults': {'model_name': 'kling-v3.0-std', 'aspect_ratio': '1:1', 'duration': 3}}, 'wan27-t2v': {'defaults': {'resolution': '720*1280', 'duration': 5}}, 'seedance2-t2v': {'defaults': {'duration': 10, 'resolution': '768P'}}}

CONFIGURED_MAX_BATCH_CONCURRENCY_FALLBACK = 3

SYSTEM_MAX_BATCH_CONCURRENCY = 5

CONFIGURED_MAX_BATCH_TASKS_FALLBACK = 5

SYSTEM_MAX_BATCH_TASKS = 10

RUNTIME_STATE_VERSION = 3

RUNTIME_STATE_TTL_SECONDS = 30 * 60

RUNTIME_STATE_DISABLED_ENV = 'BIZYAIR_DISABLE_RUNTIME_STATE'

RUNTIME_SESSION_ID_ENV = 'BIZYAIR_SESSION_ID'

HOST_SESSION_TOKEN_KEYS = ['CODEX_THREAD_ID', 'TERM_SESSION_ID', 'TMUX', 'STY', 'KITTY_WINDOW_ID', 'KITTY_PID', 'WEZTERM_PANE']

INHERIT_MARKERS = ['跟刚才一样', '和刚才一样', '按刚才', '同上', '上一轮', '沿用刚才', '继续刚才', '保持刚才', '和上次一样', '跟上次一样', '按上次', '沿用上次', '继续上次', '保持上次', '照上次', 'same as before', 'same as last time']

RUN_AUTH_MARKERS = ['开跑', '直接跑', '确认执行', '确认生成', '开始生成', '生成吧', '开始吧', '提交吧', '跑吧', 'go ahead', 'run it', 'confirm run', 'confirm execution']

RUN_AUTH_NEGATION_MARKERS = ['不要直接跑', '先别直接跑', '先不要直接跑', '别直接跑', '不要跑', '先别跑', '先不跑', '先不要跑', '不要执行', '先别执行', '先不执行', '不要生成', '先别生成', '先不生成', '不直接执行', '暂不执行']

def resolve_model(task: str | None, model: str | None) -> str:
    if model:
        normalized = model.strip()
        mapped = MODEL_MAP.get(normalized, MODEL_MAP.get(normalized.lower(), normalized))
        return mapped
    if task and task in TASK_DEFAULTS:
        return TASK_DEFAULTS[task]
    return 'bpro-t2i'

def has_any(text: str, terms: list[str]) -> bool:
    return any((term in text for term in terms))

def looks_like_image_edit_prompt(prompt: str | None) -> bool:
    q = normalized_text(prompt)
    if not q:
        return False
    if has_any(q, ['改图', '重绘', '换背景', '局部重绘', '图生图', '参考图', '扩图', '修图', '抠图']):
        return True
    background_edit_patterns = ['换.{0,3}背景', '改.{0,3}背景', '背景.{0,3}换', '背景.{0,3}改']
    return any((re.search(pattern, q) for pattern in background_edit_patterns))

def recommend_image_option(prompt: str | None, images: list[str] | None) -> tuple[str, str]:
    q = normalized_text(prompt)
    image_count = len(images or [])
    if image_count >= 1 or looks_like_image_edit_prompt(q):
        return ('7', '你这次更像图生图 / 图片编辑路线，5 个精选模型都是文生图，我更建议直接走 7 号 AI 应用检索，那边有现成的编辑工作流。')
    if has_any(q, ['endpoint', '调用api', '调用 api', '按次扣费', '底层模型', 'modelzoo', 'model zoo', '模型api', '模型 api']):
        return ('6', '你这是想直接调底层模型 API，那走 6 号 ModelZoo 搜索更对路——参数明确、按次扣费稳定。')
    if has_any(q, ['海报', '广告', 'kv', '主视觉', '封面']):
        return ('3', '你这类目标很像主视觉成稿，3 号 Seedream 5.0 往往会更会给你那股“能直接拿去用”的味道。')
    if has_any(q, ['中文', '汉字', '排版', '标题字', '字效', 'logo字']):
        return ('4', '你这里明显很在意中文文字和排版别翻车，那我会更偏向先推 4 号通用图片O.2。')
    if has_any(q, ['写实', '质感', '摄影', '人像', '大片', '写真']):
        return ('2', '你这类要求更像“别太AI、最好有点真拍质感”，那我会更想让你先看 2 号通用图片F.K.Max。')
    if has_any(q, ['细节', '高级感', '电商', '商品图', '详情页', '审美']):
        return ('5', '你这类更看重细节、质感和审美，我会更愿意把 5 号通用图片B.2 往前推。')
    if has_any(q, ['快一点', '快速', '先来一版', '先出一张', '赶时间']):
        return ('5', '你现在更像是先抢速度、先拿版本感受方向，那 5 号通用图片B.2 会更顺手——它本来就是“节奏更快”那一档。')
    return ('1', '你这类还没特别卡死风格，那就先从 1 号通用图片B.Pro 试，容错会更高。')

def recommend_video_option(prompt: str | None, images: list[str] | None, audios: list[str] | None) -> tuple[str, str]:
    q = normalized_text(prompt)
    image_count = len(images or [])
    audio_count = len(audios or [])
    if image_count >= 1 or audio_count >= 1 or has_any(q, ['图生视频', '首尾帧', '首帧', '尾帧', '过渡', '转场', '对口型', '口播', '说话', '嘴型', '音频', '配音', '唱歌']):
        return ('7', '你这次不是纯文生视频，5 个精选模型都不太贴，我更建议直接走 7 号 AI 应用检索，那边的工作流模板对路得多。')
    if has_any(q, ['endpoint', '调用api', '调用 api', '按次扣费', '底层模型', 'modelzoo', 'model zoo', '模型api', '模型 api']):
        return ('6', '你这是想直接调底层视频模型 API，那走 6 号 ModelZoo 搜索更对路——参数明确、按次扣费稳定。')
    if has_any(q, ['电影感', '镜头', '光影', '质感', '大片']):
        return ('1', '你这类明显冲着电影感和镜头语言去的，那我会更想先推 1 号通用视频V.3.1.Pro。')
    if has_any(q, ['剧情', '叙事', '分镜', '讲故事', '连续场景']):
        return ('2', '你这次更想先快速出一版看方向，那 2 号 HappyHorse 会比较顺手——出片快、性价比舒服。')
    if has_any(q, ['动作', '打斗', '运动', '快节奏', '冲击力']):
        return ('3', '你这个就是要动起来、要有劲，那我会更偏向先让你看 3 号可灵3.0.Pro。')
    if has_any(q, ['中文', '稳定', '量产', '广告脚本', '省钱']):
        return ('4', '你这类更像要稳定量产、中文别跑偏，那 4 号万相2.7 会更省心。')
    if has_any(q, ['表现力', '演绎', '人物动作', '表情', '风格化']):
        return ('5', '你这类更看重人物演绎和动态味道，那 5 号 Seedance 2.0 会更讨喜。')
    return ('4', '你这类还没把风格卡太死，那先看 4 号万相2.7，一般会更稳。')

def build_image_menu_message(prompt: str | None, images: list[str] | None) -> str:
    (option, reason) = recommend_image_option(prompt, images)
    return f'{IMAGE_SCENE_MENU}\n我建议你优先看看 {option} 号～ {reason}\n回 1-7 就行；你明确说模型名、编号，也可以直接按那个走。'

def build_video_menu_message(prompt: str | None, images: list[str] | None, audios: list[str] | None) -> str:
    (option, reason) = recommend_video_option(prompt, images, audios)
    return f'{VIDEO_SCENE_MENU}\n我建议你优先看看 {option} 号～ {reason}\n回 1-7 就行；你明确说模型名、编号，也可以直接按那个走。'

def is_video_model(model: str | None) -> bool:
    if model in ROUTE_TABLE:
        return ROUTE_TABLE[model]['modality'] == 'video'
    return False

def display_model_name(model: str | None) -> str:
    names = {'bpro-t2i': '📷 通用图片B.Pro', 'fkmax-t2i': '🖼️ 通用图片F.K.Max', 'seedream5-t2i': '🌈 Seedream 5.0', 'o2-t2i': '🎨 通用图片O.2', 'b2-t2i': '⚡ 通用图片B.2', 'v31pro-t2v': '🎬 通用视频V.3.1.Pro', 'happyhorse-t2v': '🐎 HappyHorse', 'kling30-t2v': '🐉 可灵3.0.Pro', 'wan27-t2v': '🌊 万相2.7', 'seedance2-t2v': '💃 Seedance 2.0'}
    return names.get(model or '', model or '这个模型')

def build_run_dispatch_message(model: str | None) -> str:
    name = display_model_name(model)
    if is_video_model(model):
        return f'好嘞，已经让 {name} 开始跑啦。视频任务要稍微多等一会儿，我帮你守着进度！'
    return f'好嘞，已经提交给 {name} 啦。我在这帮你盯着进度，图一出来立马发给你！'

def runtime_state_enabled() -> bool:
    return os.environ.get(RUNTIME_STATE_DISABLED_ENV, '').strip().lower() not in {'1', 'true', 'yes', 'on'}

def resolve_runtime_terminal_token() -> str | None:
    for fd in [0, 1, 2]:
        try:
            if os.isatty(fd):
                value = os.ttyname(fd)
                if value:
                    return str(value)
        except Exception:
            continue
    return None

def resolve_runtime_session_signal() -> tuple[str | None, str | None]:
    explicit = os.environ.get(RUNTIME_SESSION_ID_ENV, '').strip()
    if explicit:
        return ('explicit_env', explicit)
    for key in HOST_SESSION_TOKEN_KEYS:
        value = os.environ.get(key)
        if value:
            return ('host_env', f'{key}:{value}')
    terminal_token = resolve_runtime_terminal_token()
    if terminal_token:
        return ('terminal', terminal_token)
    try:
        parent_pid = int(os.getppid())
    except Exception:
        parent_pid = 0
    if parent_pid > 1:
        return ('parent_pid', str(parent_pid))
    return (None, None)

def build_runtime_scope_hash(scope: dict[str, Any]) -> str:
    payload = {'workspace_root': str(scope.get('workspace_root') or ''), 'invocation_cwd': str(scope.get('invocation_cwd') or ''), 'session_source': str(scope.get('session_source') or ''), 'session_token': str(scope.get('session_token') or '')}
    encoded = json.dumps(payload, ensure_ascii=False, sort_keys=True).encode('utf-8')
    return hashlib.sha256(encoded).hexdigest()[:16]

def resolve_runtime_scope() -> dict[str, Any]:
    (session_source, session_token) = resolve_runtime_session_signal()
    scope = {'workspace_root': str(SCRIPT_DIR.parent.resolve()), 'invocation_cwd': str(Path.cwd().resolve()), 'session_source': session_source, 'session_token': session_token}
    scope['scope_hash'] = build_runtime_scope_hash(scope)
    return scope

def normalize_runtime_state_payload(payload: Any) -> dict[str, Any]:
    if not isinstance(payload, dict):
        return {'version': RUNTIME_STATE_VERSION, 'last_run': {}}
    last_run = payload.get('last_run')
    if not isinstance(last_run, dict):
        last_run = {}
    return {'version': payload.get('version') if isinstance(payload.get('version'), int) else RUNTIME_STATE_VERSION, 'last_run': last_run}

def build_runtime_state_entry(app_id: str, args: argparse.Namespace, execution_prompt: str | None) -> dict[str, Any]:
    now = int(time.time())
    scope = resolve_runtime_scope()
    return {'version': RUNTIME_STATE_VERSION, 'app_id': str(app_id), 'saved_at': now, 'expires_at': now + RUNTIME_STATE_TTL_SECONDS, 'scope': scope, 'prompt': execution_prompt or args.prompt, 'raw_prompt': args.prompt, 'image': list(args.image or []), 'audio': list(args.audio or []), 'video': list(args.video or []), 'aspect_ratio': args.aspect_ratio, 'resolution': args.resolution, 'duration': args.duration, 'seed': args.seed, 'random_seed': bool(args.random_seed), 'model_name': args.model_name, 'width': args.width, 'height': args.height, 'param': list(args.param or [])}

def runtime_state_entry_is_valid(entry: Any, *, now: int | None=None) -> bool:
    if not isinstance(entry, dict):
        return False
    if entry.get('version') != RUNTIME_STATE_VERSION:
        return False
    expires_at = entry.get('expires_at')
    saved_at = entry.get('saved_at')
    try:
        expires_at = int(expires_at)
        saved_at = int(saved_at)
    except Exception:
        return False
    current_ts = int(now if now is not None else time.time())
    if expires_at < current_ts or saved_at > current_ts:
        return False
    scope = entry.get('scope') if isinstance(entry.get('scope'), dict) else {}
    expected_scope = resolve_runtime_scope()
    workspace_root = scope.get('workspace_root')
    if workspace_root and workspace_root != expected_scope['workspace_root']:
        return False
    invocation_cwd = scope.get('invocation_cwd')
    if invocation_cwd and invocation_cwd != expected_scope['invocation_cwd']:
        return False
    stored_hash = str(scope.get('scope_hash') or '').strip()
    expected_hash = str(expected_scope.get('scope_hash') or '').strip()
    if stored_hash and expected_hash:
        return stored_hash == expected_hash
    session_token = scope.get('session_token')
    expected_token = expected_scope.get('session_token')
    if session_token and expected_token and (session_token != expected_token):
        return False
    session_source = scope.get('session_source')
    expected_source = expected_scope.get('session_source')
    if session_source and expected_source and (session_source != expected_source):
        return False
    return True

def load_runtime_state() -> dict:
    state_file = resolve_runtime_state_file()
    if not runtime_state_enabled():
        return {'version': RUNTIME_STATE_VERSION, 'last_run': {}}
    try:
        if state_file.exists():
            return normalize_runtime_state_payload(json.loads(state_file.read_text(encoding='utf-8')))
    except Exception:
        pass
    return {'version': RUNTIME_STATE_VERSION, 'last_run': {}}

def save_runtime_state(state: dict) -> None:
    state_file = resolve_runtime_state_file()
    if not runtime_state_enabled():
        return
    try:
        state_file.parent.mkdir(parents=True, exist_ok=True)
        normalized = normalize_runtime_state_payload(state)
        state_file.write_text(json.dumps(normalized, ensure_ascii=False, indent=2), encoding='utf-8')
    except Exception:
        pass

def clear_runtime_state() -> bool:
    state_file = resolve_runtime_state_file()
    try:
        if state_file.exists():
            state_file.unlink()
            return True
    except Exception:
        pass
    return False

def load_skill_config() -> dict:
    return load_config_json()

def classify_error_bucket(payload: dict) -> str:
    error = str(payload.get('error') or '')
    message = json.dumps(payload, ensure_ascii=False).lower()
    if error == 'NO_API_KEY':
        return 'missing_api_key'
    if error == 'LOCAL_APP_CATALOG_REMOVED':
        return 'local_app_catalog_removed'
    if error == 'REMOTE_APP_RUN_NOT_SUPPORTED':
        return 'remote_app_run_not_supported'
    if error == 'REMOTE_APP_RUN_ATTEMPT_FAILED' and any((m in message for m in ['webappid', 'web_app_id', 'invalid parameter: webappid', 'invalid parameter: webappid'])):
        return 'remote_app_run_not_supported'
    if error == 'FILE_NOT_FOUND':
        return 'missing_file'
    if error == 'REMOTE_APP_RUN_REQUIRES_USER_MEDIA':
        return 'missing_user_media'
    if error == 'UPLOAD_FAILED':
        if any((m in message for m in ['too large', 'size', 'format', 'invalid', 'image', 'audio'])):
            return 'bad_upload_input'
        return 'upload_or_station'
    if error == 'TIMEOUT':
        return 'station_timeout'
    if error == 'APP_NOT_FOUND':
        return 'app_not_found'
    if error == 'TASK_FAILED':
        if any((m in message for m in ['quota', 'rate', 'busy', 'overload', 'internal', 'upstream', 'service unavailable', 'temporarily', 'network', 'timeout'])):
            return 'station_runtime'
        if any((m in message for m in ['prompt', 'param', 'invalid', 'missing', 'unsupported', 'format', 'size', 'empty', 'not found', 'image', 'audio', 'upload'])):
            return 'bad_input_runtime'
        return 'station_runtime'
    return 'raw'

def friendly_error_message(payload: dict) -> str | None:
    bucket = classify_error_bucket(payload)
    if bucket == 'missing_api_key':
        return '还没连上 BizyAir API Key，任务跑不起来。先把 Key 配好，配完接着跑～'
    if bucket == 'local_app_catalog_removed':
        return '本地 catalog 的老通道已经关了。固定的图片和视频入口还能直接用，其他的走在线搜索或直接看详情～'
    if bucket == 'remote_app_run_not_supported':
        reason = str(payload.get('reason') or '')
        feedback_channel = str(payload.get('feedback_channel') or '')
        if reason == 'workflow_without_ref_app':
            return '这是一个纯 ComfyUI 工作流，没有对应的 AI 应用版本，目前不支持直接运行～你可以在 BizyAir 网页端打开它，手动加载到 ComfyUI 编辑器里跑。'
        return '信息和参数都整理出来了。不过后台还没完全打通这条线，这轮先不直接跑～'
    if bucket == 'missing_user_media':
        missing_inputs = payload.get('missing_inputs') or {}
        parts = []
        if missing_inputs.get('image'):
            parts.append('图片')
        if missing_inputs.get('audio'):
            parts.append('音频')
        if missing_inputs.get('video'):
            parts.append('视频')
        joined = '、'.join(parts) if parts else '素材'
        return f'这次缺了你自己的素材。这个任务必须用你自己的素材来跑，站内示例不能直接套用。这轮缺的是：{joined}。'
    if bucket == 'missing_file':
        return '还没收到你要用的文件。可能是路径没填对，或者还没传完。重新发一下，接着跑～'
    if bucket == 'bad_upload_input':
        return '卡在上传素材这步了，可能是文件格式或大小不符合要求。换个常见格式，或者把文件弄小一点再试～'
    if bucket == 'upload_or_station':
        return '上传环节卡住了，BizyAir 那边通道暂时有点波动。素材应该没问题，稍后再试一下～'
    if bucket == 'station_timeout':
        return '这次是 BizyAir 那边处理太慢导致超时了。不是你的操作问题，等会儿再重试一次～'
    if bucket == 'station_runtime':
        return '这次是 BizyAir 那边没跑通，可能是服务器太忙或有点波动。不是你参数填错了～'
    if bucket == 'bad_input_runtime':
        return '这次是素材或参数有点不匹配。可能是提示词、格式或尺寸哪里没对上，帮你找一下问题在哪～'
    if bucket == 'app_not_found':
        return '没找到对应的模型或应用。可能是编号、名字或 ID 没对齐。把你选的对象再发一次，帮你核对～'
    return None

def format_success_payload(payload: dict) -> str | None:
    if payload.get('status') == 'ok' and payload.get('summary') and payload.get('verdict'):
        return f"{payload['summary']}\n{payload['verdict']}"
    return None

def ensure_api_key_ready(api_key_arg: str | None) -> None:
    cmd = [sys.executable, str(APP_SCRIPT), '--check']
    if api_key_arg:
        cmd += ['--api-key', api_key_arg]
    result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='replace')
    payload = None
    raw_stdout = (result.stdout or '').strip()
    if raw_stdout:
        try:
            payload = json.loads(raw_stdout)
        except Exception:
            payload = None
    if isinstance(payload, dict) and payload.get('status') == 'no_key':
        print(friendly_error_message({'error': 'NO_API_KEY'}))
        sys.exit(1)

def run_subprocess(args: list[str], *, success_callback: Callable[[], None] | None=None):
    result = subprocess.run(args, capture_output=True, text=True, encoding='utf-8', errors='replace')
    if result.returncode == 0:
        if success_callback:
            try:
                success_callback()
            except Exception:
                pass
        payload = None
        if result.stdout:
            raw_stdout = result.stdout.strip()
            if raw_stdout:
                try:
                    payload = json.loads(raw_stdout)
                except Exception:
                    for line in reversed(result.stdout.splitlines()):
                        line = line.strip()
                        if not line:
                            continue
                        try:
                            payload = json.loads(line)
                            break
                        except Exception:
                            continue
        friendly_success = format_success_payload(payload) if isinstance(payload, dict) else None
        if friendly_success:
            print(friendly_success)
            if result.stderr:
                print(result.stderr, end='', file=sys.stderr)
            sys.exit(result.returncode)
        if result.stdout:
            print(result.stdout, end='')
        if result.stderr:
            print(result.stderr, end='', file=sys.stderr)
        sys.exit(result.returncode)
    payload = None
    candidate_streams = [(result.stderr or '').strip(), (result.stdout or '').strip()]
    for text in candidate_streams:
        if not text:
            continue
        try:
            payload = json.loads(text)
            break
        except Exception:
            pass
        for line in reversed(text.splitlines()):
            line = line.strip()
            if not line:
                continue
            try:
                payload = json.loads(line)
                break
            except Exception:
                continue
        if payload is not None:
            break
    friendly = friendly_error_message(payload) if isinstance(payload, dict) else None
    if friendly:
        print(friendly)
        sys.exit(result.returncode)
    if result.stdout:
        print(result.stdout, end='')
    if result.stderr:
        print(result.stderr, end='', file=sys.stderr)
    sys.exit(result.returncode)
