"""api.py — BizyAir HTTP 客户端 + 任务执行管线。

职责：
  - API key 解析与读取（CLI / env / config.json 三层 fallback，见 resolve_api_key）
  - 远端 HTTP 调用：bizy_models 列表 / 单个模型 detail / webapp_detail / version_detail / workflow
  - 任务执行管线：upload_input_file → build_remote_run_payload → create_remote_task_attempt
                → poll_until_done → download_outputs
  - NO_API_KEY 错误时给用户的引导提示（require_api_key 里那段 quick test 命令）

build_remote_run_payload 构建远端 AI 应用的执行 payload：
  遍历 webapp input_nodes，媒体槽绑定上传文件，标准参数（duration/resolution 等）
  走 override，seed 自动随机，--prompt 写入所有 customtext 类型的非负向文本字段，
  --param key=value 精确覆盖任意字段（最高优先级）。
"""
from __future__ import annotations
import argparse, base64, hashlib, hmac, json, mimetypes, os, random, sys, time, urllib.parse, urllib.request
from email.utils import formatdate
from pathlib import Path
from paths import load_config_json, resolve_output_root
from typing import Any

import contract
import remote
import search
import common
from common import (
    BIZY_MODEL_DETAIL_URL, CREATE_URL, DEFAULT_TIMEOUT, DETAIL_URL,
    INPUT_COMMIT_URL, MAX_POLL_SECONDS, OUTPUTS_URL, POLL_INTERVAL,
    RESOLVE_VERSION_URL, UPLOAD_TOKEN_URL,
)

def fetch_remote_models(api_key: str, *, remote_source: str='community', page: int=1, page_size: int=10, keyword: str | None=None, sort: str | None=None, model_types: str | None=None, base_models: str | None=None) -> dict[str, Any]:
    params: dict[str, Any] = {'current': page, 'page_size': page_size}
    if keyword is not None:
        params['keyword'] = keyword
    if sort:
        params['sort'] = sort
    if model_types:
        params['model_types'] = model_types
    if base_models:
        params['base_models'] = base_models
    if common.normalized_text(remote_source) == 'official':
        params['mode'] = 'official'
    return request_json('GET', remote.remote_list_endpoint(remote_source), api_key, params=params)

def find_remote_model_by_id(api_key: str, bizy_model_id: str | int, *, remote_source: str='community') -> dict[str, Any] | None:
    """在社区/官方列表中按 ID 查找对象。先不限类型搜一页（100 条），找不到再按类型各搜一页。"""
    target = str(bizy_model_id)
    sort = 'Auto' if common.normalized_text(remote_source) == 'official' else 'Most Used'
    # 第一轮：不限类型，覆盖面最广
    resp = fetch_remote_models(api_key, remote_source=remote_source, page=1, page_size=100, keyword='', sort=sort, model_types=None)
    items = extract_result_data(resp).get('list', [])
    for item in items:
        if str(item.get('id')) == target:
            return item
    # 第二轮：按类型各搜一页（某些类型可能不在默认排序前 100）
    for model_type in ['Application', 'Workflow']:
        resp = fetch_remote_models(api_key, remote_source=remote_source, page=1, page_size=100, keyword='', sort=sort, model_types=model_type)
        items = extract_result_data(resp).get('list', [])
        for item in items:
            if str(item.get('id')) == target:
                return item
    return None

def resolve_public_remote_target_from_draft_id(api_key: str | None, draft_id: str | int) -> dict[str, Any]:
    """comfy-ui 链接的 draft_id 无公开 API 可还原为 bizy_model_id，直接返回不支持。"""
    return {'draft_id': str(draft_id), 'matched': False, 'resolved_bizy_model_id': None, 'reason': 'comfy_ui_workflow_not_supported'}

def fetch_remote_detail(api_key: str, bizy_model_id: str | int) -> dict[str, Any]:
    return safe_request_json('GET', f'{BIZY_MODEL_DETAIL_URL}/{bizy_model_id}/detail', api_key)

def safe_request_json_public(method: str, url: str, *, params: dict[str, Any] | None=None, payload: dict[str, Any] | None=None, headers: dict[str, str] | None=None, timeout: int=DEFAULT_TIMEOUT) -> dict[str, Any]:
    if params:
        url = url + '?' + urllib.parse.urlencode(params)
    body = None
    req_headers = {'Content-Type': 'application/json', 'Accept': 'application/json', 'User-Agent': 'BizyAir-Skill/1.0', 'lang': 'zh'}
    if headers:
        req_headers.update(headers)
    if payload is not None:
        body = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(url, data=body, method=method, headers=req_headers)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read().decode('utf-8')
            if not raw.strip():
                return {}
            return {'ok': True, 'status': resp.status, 'data': json.loads(raw)}
    except urllib.error.HTTPError as e:
        detail = e.read().decode('utf-8', errors='replace')
        try:
            parsed = json.loads(detail)
        except Exception:
            parsed = {'message': detail}
        return {'ok': False, 'status': e.code, 'error': parsed}
    except Exception as e:
        return {'ok': False, 'status': None, 'error': {'message': str(e)}}

def unwrap_result_payload(result: dict[str, Any] | None) -> dict[str, Any]:
    if not isinstance(result, dict):
        return {}
    if 'ok' in result:
        payload = result.get('data')
        if isinstance(payload, dict):
            result = payload
        else:
            return {}
    return result if isinstance(result, dict) else {}

def extract_result_data(result: dict[str, Any] | None) -> dict[str, Any]:
    payload = unwrap_result_payload(result)
    if isinstance(payload.get('data'), dict):
        return payload.get('data', {})
    return payload

def result_is_ok(result: dict[str, Any] | None) -> bool:
    if not isinstance(result, dict):
        return False
    if 'ok' in result:
        return bool(result.get('ok'))
    status = result.get('status')
    if isinstance(status, bool):
        return status
    return True

def fetch_remote_webapp_detail(api_key: str, webapp_id: str | int) -> dict[str, Any]:
    headers = {'Accept': 'application/json', 'User-Agent': 'BizyAir-Skill/1.0'}
    return safe_request_json_public('GET', f'https://bizyair.cn/api/x/v1/webapp/{webapp_id}', headers=headers)

def fetch_remote_version_detail(api_key: str, version_id: str | int) -> dict[str, Any]:
    return request_json('GET', f'{BIZY_MODEL_DETAIL_URL}/versions/{version_id}', api_key)

def fetch_remote_workflow(api_key: str, version_id: str | int) -> dict[str, Any]:
    return request_json('GET', f'{RESOLVE_VERSION_URL}/{version_id}', api_key)

_WORKFLOW_URL_ALLOWED_HOSTS = {'bizyair-prod.oss-cn-shanghai.aliyuncs.com', 'bizyair.cn', 'api.bizyair.cn'}

def fetch_remote_workflow_from_url(url: str | None) -> dict[str, Any]:
    target = str(url or '').strip()
    if not target:
        return {}
    parsed = urllib.parse.urlparse(target)
    host = (parsed.hostname or '').lower()
    if not any(host == allowed or host.endswith('.' + allowed) for allowed in _WORKFLOW_URL_ALLOWED_HOSTS):
        return {'ok': False, 'error': f'blocked_host: {host}'}
    req = urllib.request.Request(target, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req, timeout=DEFAULT_TIMEOUT) as resp:
            raw = resp.read().decode('utf-8')
            if not raw.strip():
                return {}
            return {'ok': True, 'status': resp.status, 'data': json.loads(raw)}
    except Exception as exc:
        return {'ok': False, 'error': str(exc)}

def safe_request_json(method: str, url: str, api_key: str, *, params: dict[str, Any] | None=None, payload: dict[str, Any] | None=None, headers: dict[str, str] | None=None, timeout: int=DEFAULT_TIMEOUT) -> dict[str, Any]:
    if params:
        url = url + '?' + urllib.parse.urlencode(params)
    body = None
    req_headers = {'Authorization': f'Bearer {api_key}', 'Content-Type': 'application/json', 'lang': 'zh'}
    if headers:
        req_headers.update(headers)
    if payload is not None:
        body = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(url, data=body, method=method, headers=req_headers)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read().decode('utf-8')
            if not raw.strip():
                return {}
            return {'ok': True, 'status': resp.status, 'data': json.loads(raw)}
    except urllib.error.HTTPError as e:
        detail = e.read().decode('utf-8', errors='replace')
        try:
            parsed = json.loads(detail)
        except Exception:
            parsed = {'message': detail}
        return {'ok': False, 'status': e.code, 'error': parsed}
    except Exception as e:
        return {'ok': False, 'status': None, 'error': {'message': str(e)}}

def diagnose_remote_numeric_id(api_key: str | None, raw_id: str) -> dict[str, Any]:
    result: dict[str, Any] = {'input_id': str(raw_id), 'is_numeric': str(raw_id).isdigit(), 'matched_remote_bizy_model': None, 'matched_local_web_app': None, 'suspected_id_kind': None, 'guidance': []}
    if not str(raw_id).isdigit():
        result['suspected_id_kind'] = 'non_numeric'
        result['guidance'] = ['我看了一下，你给的这个 ID 不是纯数字，系统没法直接精准定位哦。', '最稳妥的办法是你直接把完整的网页链接发给我，或者多告诉我一点它是干嘛的，我再去帮你找～']
        return result
    if api_key:
        community = find_remote_model_by_id(api_key, str(raw_id), remote_source='community')
        official = None if community else find_remote_model_by_id(api_key, str(raw_id), remote_source='official')
        matched = community or official
        if matched:
            result['matched_remote_bizy_model'] = search.summarize_remote_candidate(matched)
            result['suspected_id_kind'] = 'remote_bizy_model_id'
            result['guidance'] = ['对上号啦～这个数字 ID 在库里是有的，我接着顺藤摸瓜去帮你查它的详细信息。稍等哈～']
            return result
    result['suspected_id_kind'] = 'unknown_numeric_id_or_web_app_id'
    result['guidance'] = ['哎呀，这个数字 ID 在公开库里没找到对应的东西。', '为了稳妥起见，我先不闭着眼睛瞎跑了。', '你看看手头有没有完整的链接，直接发给我，咱们再试一次！']
    return result

def read_bizyair_entry_from_skill_config() -> dict[str, Any]:
    cfg = load_config_json()
    entry = cfg.get('credentials', {})
    return entry if isinstance(entry, dict) else {}

def read_key_from_skill_config() -> str | None:
    entry = read_bizyair_entry_from_skill_config()
    api_key = entry.get('api_key')
    if isinstance(api_key, str) and api_key.strip():
        return api_key.strip()
    # 多 key 模式：取第一个
    api_keys = entry.get('api_keys')
    if isinstance(api_keys, list) and api_keys:
        first = api_keys[0]
        if isinstance(first, str) and first.strip():
            return first.strip()
    return None

def read_all_keys_from_skill_config() -> list[str]:
    """读取所有配置的 API Key（支持单 key 和多 key 模式）。"""
    entry = read_bizyair_entry_from_skill_config()
    keys: list[str] = []
    # 多 key 模式
    api_keys = entry.get('api_keys')
    if isinstance(api_keys, list):
        for k in api_keys:
            if isinstance(k, str) and k.strip():
                keys.append(k.strip())
    # 单 key 模式（兼容）
    api_key = entry.get('api_key')
    if isinstance(api_key, str) and api_key.strip():
        if api_key.strip() not in keys:
            keys.insert(0, api_key.strip())
    return keys

def resolve_all_api_keys(provided: str | None) -> list[str]:
    """解析所有可用 key（CLI > env > config），返回列表。"""
    keys: list[str] = []
    placeholders = {'your_api_key_here', '<your_api_key>', 'YOUR_API_KEY', 'BIZYAIR_API_KEY'}
    if provided:
        normalized = provided.strip()
        if normalized and normalized not in placeholders:
            keys.append(normalized)
    env = os.environ.get('BIZYAIR_API_KEY', '').strip()
    if env and env not in keys:
        keys.append(env)
    for k in read_all_keys_from_skill_config():
        if k not in keys:
            keys.append(k)
    return keys

def _load_retryable_codes() -> tuple[set[int], set[int]]:
    """从 config/error_codes.json 加载可重试错误码。"""
    config_dir = Path(__file__).resolve().parent.parent / 'config'
    ec_file = config_dir / 'error_codes.json'
    if ec_file.exists():
        data = json.loads(ec_file.read_text(encoding='utf-8'))
        biz = {int(k) for k in (data.get('retryable_biz_codes') or {}).keys()}
        http = set(data.get('retryable_http_codes') or [])
        return biz, http
    # fallback
    return {20049, 20050, 20051, 30039, 30040, 30015, 30016, 30018, 50600, 50601, 50602, 50603, 50604}, {429, 402}

_RETRYABLE_BIZ_CODES, _RETRYABLE_HTTP_CODES = _load_retryable_codes()

def is_retryable_error(result: dict[str, Any]) -> bool:
    """判断一个 safe_request_json 的返回是否是可重试错误（换 key 可能恢复）。"""
    if result.get('ok'):
        return False
    http_status = result.get('status')
    if http_status in _RETRYABLE_HTTP_CODES:
        return True
    error = result.get('error') or {}
    biz_code = error.get('code') if isinstance(error, dict) else None
    if isinstance(biz_code, int) and biz_code in _RETRYABLE_BIZ_CODES:
        return True
    return False

def resolve_api_key(provided: str | None) -> str | None:
    if provided:
        normalized = provided.strip()
        placeholders = {'your_api_key_here', '<your_api_key>', 'YOUR_API_KEY', 'BIZYAIR_API_KEY'}
        if normalized and normalized not in placeholders:
            return normalized
    env = os.environ.get('BIZYAIR_API_KEY', '').strip()
    if env:
        return env
    return read_key_from_skill_config()

def get_key_source(provided: str | None) -> str:
    if provided:
        normalized = provided.strip()
        placeholders = {'your_api_key_here', '<your_api_key>', 'YOUR_API_KEY', 'BIZYAIR_API_KEY'}
        if normalized and normalized not in placeholders:
            return 'cli'
    if os.environ.get('BIZYAIR_API_KEY', '').strip():
        return 'env'
    if read_key_from_skill_config():
        return 'skill_config'
    return 'none'

def require_api_key(provided: str | None) -> str:
    key = resolve_api_key(provided)
    if key:
        return key
    print(json.dumps({'error': 'NO_API_KEY', 'message': 'No BizyAir API key configured', 'supported_inputs': {'cli': '--api-key YOUR_BIZYAIR_KEY', 'env': 'BIZYAIR_API_KEY', 'skill_config': f'{common.config_display_path()} -> credentials.api_key'}, 'recommended': f'Save the key to {common.config_display_path()} at credentials.api_key for reusable local skill runs', 'steps': ['1. Get BizyAir API key', f"2. Quick test: {common.local_script_command('dispatch.py', '--check', '--api-key', 'YOUR_BIZYAIR_KEY')}", f'3. Recommended: save it to {common.config_display_path()} under credentials.api_key', '4. Or set env BIZYAIR_API_KEY for the current shell/session']}, ensure_ascii=False))
    sys.exit(1)

def request_json(method: str, url: str, api_key: str, *, params: dict[str, Any] | None=None, payload: dict[str, Any] | None=None, headers: dict[str, str] | None=None, timeout: int=DEFAULT_TIMEOUT) -> dict[str, Any]:
    """向 BizyAir 发起认证请求，返回与 safe_request_json 相同的信封格式。

    成功时返回 {ok: True, status: 200, data: {...}}；
    失败时返回 {ok: False, status: ..., error: ...}。
    所有调用方统一使用 extract_result_data() 解包业务数据。
    """
    return safe_request_json(method, url, api_key, params=params, payload=payload, headers=headers, timeout=timeout)

def generate_seed() -> int:
    return random.randint(1, 2 ** 50)

def get_upload_token(api_key: str, file_name: str) -> dict[str, Any]:
    return request_json('GET', UPLOAD_TOKEN_URL, api_key, params={'file_name': file_name, 'file_type': 'inputs'})

def upload_to_oss(file_path: str, token_inner: dict[str, Any]) -> None:
    """上传文件到 OSS。token_inner 是 extract_result_data(token_resp) 解包后的内层数据。"""
    file_info = token_inner['file']
    storage = token_inner['storage']
    object_key = file_info['object_key']
    bucket = storage['bucket']
    endpoint = storage['endpoint']
    access_key_id = file_info['access_key_id']
    access_key_secret = file_info['access_key_secret']
    security_token = file_info['security_token']
    file_bytes = Path(file_path).read_bytes()
    content_type = mimetypes.guess_type(file_path)[0] or 'application/octet-stream'
    date_str = formatdate(usegmt=True)
    canonical_headers = f'x-oss-security-token:{security_token}\n'
    canonical_resource = f'/{bucket}/{object_key}'
    string_to_sign = f'PUT\n\n{content_type}\n{date_str}\n{canonical_headers}{canonical_resource}'
    signature = base64.b64encode(hmac.new(access_key_secret.encode('utf-8'), string_to_sign.encode('utf-8'), hashlib.sha1).digest()).decode('utf-8')
    upload_url = f'https://{bucket}.{endpoint}/{object_key}'
    req = urllib.request.Request(upload_url, data=file_bytes, method='PUT')
    req.add_header('Date', date_str)
    req.add_header('Content-Type', content_type)
    req.add_header('Content-Length', str(len(file_bytes)))
    req.add_header('x-oss-security-token', security_token)
    req.add_header('Authorization', f'OSS {access_key_id}:{signature}')
    try:
        with urllib.request.urlopen(req, timeout=300) as resp:
            if resp.status not in {200, 201}:
                raise RuntimeError(f'Unexpected upload status: {resp.status}')
    except urllib.error.HTTPError as e:
        detail = e.read().decode('utf-8', errors='replace')
        print(json.dumps({'error': 'UPLOAD_FAILED', 'status': e.code, 'message': detail}, ensure_ascii=False), file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(json.dumps({'error': 'UPLOAD_FAILED', 'message': str(e)}, ensure_ascii=False), file=sys.stderr)
        sys.exit(1)

def commit_input(api_key: str, file_name: str, object_key: str) -> str:
    resp = request_json('POST', INPUT_COMMIT_URL, api_key, payload={'name': file_name, 'object_key': object_key})
    data = extract_result_data(resp)
    url = data.get('url')
    if not url:
        print(json.dumps({'error': 'UPLOAD_FAILED', 'message': 'No input url returned after commit'}, ensure_ascii=False), file=sys.stderr)
        sys.exit(1)
    return url

def upload_input_file(api_key: str, file_path: str) -> str:
    """上传文件到 OSS，返回真实 HTTP URL。所有文件统一走 OSS 直传 + commit。"""
    p = Path(file_path)
    if not p.exists():
        print(json.dumps({'error': 'FILE_NOT_FOUND', 'message': str(file_path)}, ensure_ascii=False), file=sys.stderr)
        sys.exit(1)
    token_resp = get_upload_token(api_key, p.name)
    if not result_is_ok(token_resp):
        print(json.dumps({'error': 'UPLOAD_FAILED', 'message': 'Failed to get upload token', 'detail': token_resp.get('error') if isinstance(token_resp, dict) else str(token_resp)}, ensure_ascii=False), file=sys.stderr)
        sys.exit(1)
    token_inner = extract_result_data(token_resp)
    upload_to_oss(str(p), token_inner)
    return commit_input(api_key, p.name, token_inner['file']['object_key'])

def coerce_value(value: str) -> Any:
    low = value.lower()
    if low == 'true':
        return True
    if low == 'false':
        return False
    try:
        if '.' in value:
            return float(value)
        return int(value)
    except ValueError:
        return value

def build_remote_run_payload(bizy_model_id: str, preflight: dict[str, Any], args: argparse.Namespace, uploaded_urls: list[str] | None=None, uploaded_audios: list[str] | None=None, uploaded_videos: list[str] | None=None) -> dict[str, Any]:
    detail_data = extract_result_data(preflight.get('detail'))
    execution_target = preflight.get('execution_target') or {}
    runtime_webapp_detail = execution_target.get('webapp_detail') or preflight.get('webapp_detail')
    webapp_detail_data = extract_result_data(runtime_webapp_detail)
    version_data = extract_result_data(preflight.get('version_detail'))
    resolved_contract = preflight.get('resolved_contract') or (preflight.get('summary') or {}).get('resolved_contract') or contract.resolve_remote_input_contract(execution_target=execution_target, webapp_detail=preflight.get('webapp_detail'), workflow=preflight.get('workflow'))
    input_values: dict[str, Any] = {}
    uploaded_urls = list(uploaded_urls or [])
    uploaded_audios = list(uploaded_audios or [])
    uploaded_videos = list(uploaded_videos or [])
    contract_bindings = resolved_contract.get('bindings') or {}
    logical_bindings = contract_bindings.get('logical') or {}
    media_slot_bindings = contract_bindings.get('media_slots') or {}
    binding_field_map = contract.contract_field_by_binding_key(resolved_contract)
    if webapp_detail_data:
        image_index = 0
        audio_index = 0
        video_index = 0
        field_alias_map: dict[str, str] = {}
        bound_media_keys = {'image': set(), 'audio': set(), 'video': set()}
        for node in webapp_detail_data.get('input_nodes', []) or []:
            variable_name = node.get('variable_name')
            if not variable_name:
                continue
            variable_key = str(variable_name)
            field_name = str(node.get('field_name') or '').lower()
            field_label = str(node.get('field_label') or '').lower()
            field_type = str(node.get('field_type') or '').lower()
            field_value = node.get('field_value')
            media_slot_type = contract.classify_remote_media_slot(node)
            contract_field = binding_field_map.get(variable_key) or {}
            logical_name = str(contract_field.get('logical_name') or '')
            if field_name:
                field_alias_map[field_name] = variable_key
            if field_label:
                field_alias_map[field_label] = variable_key
            # 媒体槽绑定
            if uploaded_urls and image_index < len(uploaded_urls) and (media_slot_type == 'image' or variable_key in (media_slot_bindings.get('image') or [])):
                input_values[variable_key] = uploaded_urls[image_index]
                image_index += 1
                bound_media_keys['image'].add(variable_key)
                continue
            if uploaded_audios and audio_index < len(uploaded_audios) and (media_slot_type == 'audio' or variable_key in (media_slot_bindings.get('audio') or [])):
                input_values[variable_key] = uploaded_audios[audio_index]
                audio_index += 1
                bound_media_keys['audio'].add(variable_key)
                continue
            if uploaded_videos and video_index < len(uploaded_videos) and (media_slot_type == 'video' or variable_key in (media_slot_bindings.get('video') or [])):
                input_values[variable_key] = uploaded_videos[video_index]
                video_index += 1
                bound_media_keys['video'].add(variable_key)
                continue
            # 标准参数 override（duration/aspect_ratio 等）
            override_value = None
            if logical_name and logical_name in logical_bindings and (variable_key in (logical_bindings.get(logical_name) or [])):
                override_value = remote.match_remote_field_override(logical_name, args)
            if override_value is None:
                override_value = remote.match_remote_field_override(field_name or field_label, args)
            if override_value is not None:
                input_values[variable_key] = override_value
                continue
            # 隐藏的媒体槽跳过
            if media_slot_type is not None and field_type == 'hidden':
                continue
            # seed 字段兜底
            is_seed_field = logical_name == 'seed' or contract.is_remote_seed_field(field_name, field_label)
            empty_seed_value = field_value is None or field_value == '' or (not isinstance(field_value, bool) and field_value == 0) or field_value == '0'
            if is_seed_field and empty_seed_value:
                input_values[variable_key] = generate_seed()
                continue
            # 默认值保留
            input_values[variable_key] = field_value
        # 补充未绑定的媒体槽
        for key in list(media_slot_bindings.get('image') or []):
            if key in bound_media_keys['image'] or image_index >= len(uploaded_urls):
                continue
            input_values[str(key)] = uploaded_urls[image_index]
            image_index += 1
        for key in list(media_slot_bindings.get('audio') or []):
            if key in bound_media_keys['audio'] or audio_index >= len(uploaded_audios):
                continue
            input_values[str(key)] = uploaded_audios[audio_index]
            audio_index += 1
        for key in list(media_slot_bindings.get('video') or []):
            if key in bound_media_keys['video'] or video_index >= len(uploaded_videos):
                continue
            input_values[str(key)] = uploaded_videos[video_index]
            video_index += 1
        # --prompt 兼容：写入所有 customtext 类型的非负向文本字段（会被后面的 --param 覆盖）
        user_prompt = getattr(args, 'prompt', None)
        if user_prompt:
            text_field_types = {'customtext', 'textarea', 'text', 'string'}
            for node in webapp_detail_data.get('input_nodes', []) or []:
                vn = node.get('variable_name')
                if not vn:
                    continue
                ft = str(node.get('field_type') or '').lower()
                fn = str(node.get('field_name') or '').lower()
                fl = str(node.get('field_label') or '').lower()
                if ft not in text_field_types:
                    continue
                if contract.is_negative_prompt_key(fn, fl):
                    continue
                input_values[str(vn)] = user_prompt
        # --param 精确覆盖（最高优先级）
        for item in getattr(args, 'param', None) or []:
            if '=' not in item:
                continue
            (key, value) = item.split('=', 1)
            resolved_key = field_alias_map.get(str(key).strip().lower(), key)
            input_values[resolved_key] = coerce_value(value)
        return {'web_app_id': webapp_detail_data.get('id'), 'backend_id': 0, 'client_id': ''.join((random.choice('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789') for _ in range(25))), 'suppress_preview_output': False, 'input_values': input_values}
    # 无 webapp_detail 的 fallback 路径
    for (key, url) in zip(list(media_slot_bindings.get('image') or []), uploaded_urls):
        input_values[str(key)] = url
    for (key, url) in zip(list(media_slot_bindings.get('audio') or []), uploaded_audios):
        input_values[str(key)] = url
    for (key, url) in zip(list(media_slot_bindings.get('video') or []), uploaded_videos):
        input_values[str(key)] = url
    for item in getattr(args, 'param', None) or []:
        if '=' not in item:
            continue
        (key, value) = item.split('=', 1)
        input_values[str(key)] = coerce_value(value)
    payload: dict[str, Any] = {'bizy_model_id': int(bizy_model_id) if str(bizy_model_id).isdigit() else bizy_model_id, 'input_values': input_values}
    identity_candidates = {'version_id': preflight.get('version_id') or version_data.get('id') or detail_data.get('bizy_model_version_id') or detail_data.get('version_id'), 'sign': version_data.get('sign') or detail_data.get('sign'), 'draft_id': version_data.get('draft_id') or detail_data.get('draft_id'), 'web_app_id': detail_data.get('web_app_id') or version_data.get('web_app_id'), 'bizy_model_version_id': version_data.get('bizy_model_version_id') or detail_data.get('bizy_model_version_id'), 'path': version_data.get('path') or detail_data.get('path'), 'file_name': version_data.get('file_name') or detail_data.get('file_name')}
    for (key, value) in identity_candidates.items():
        if value not in (None, '', [], {}):
            payload[key] = value
    media_slot_bindings = contract_bindings.get('media_slots') or {}
    if media_slot_bindings.get('image'):
        payload['expected_image_slots'] = len(media_slot_bindings['image'])
    if media_slot_bindings.get('audio'):
        payload['expected_audio_slots'] = len(media_slot_bindings['audio'])
    if media_slot_bindings.get('video'):
        payload['expected_video_slots'] = len(media_slot_bindings['video'])
    return payload

def create_remote_task_attempt(api_key: str, bizy_model_id: str, preflight: dict[str, Any], args: argparse.Namespace, uploaded_urls: list[str] | None=None, uploaded_audios: list[str] | None=None, uploaded_videos: list[str] | None=None, *, use_async: bool=True) -> dict[str, Any]:
    headers = {}
    if use_async:
        headers['X-Bizyair-Task-Async'] = 'enable'
    payload = build_remote_run_payload(bizy_model_id, preflight, args, uploaded_urls=uploaded_urls, uploaded_audios=uploaded_audios, uploaded_videos=uploaded_videos)
    result = safe_request_json('POST', CREATE_URL, api_key, payload=payload, headers=headers, timeout=120)
    return {'payload': payload, 'result': result, 'auth_mode': 'api_key', 'submit_route': 'openapi_create_api_key'}

def query_detail(api_key: str, request_id: str) -> dict[str, Any]:
    return request_json('GET', DETAIL_URL, api_key, params={'requestId': request_id})

def query_outputs(api_key: str, request_id: str) -> dict[str, Any]:
    return request_json('GET', OUTPUTS_URL, api_key, params={'requestId': request_id})

def normalize_output_extension(ext: str | None) -> str | None:
    if not ext:
        return None
    cleaned = str(ext).strip()
    if not cleaned:
        return None
    return cleaned if cleaned.startswith('.') else f'.{cleaned}'

def infer_extension_from_url(url: str) -> str | None:
    path = urllib.parse.urlparse(url or '').path
    suffix = Path(path).suffix
    return normalize_output_extension(suffix)

UNTRUSTED_CONTENT_TYPE_MIMES = {'application/octet-stream', 'binary/octet-stream'}

def infer_extension_from_content_type(content_type: str | None) -> str | None:
    if not content_type:
        return None
    mime = str(content_type).split(';', 1)[0].strip().lower()
    if mime in UNTRUSTED_CONTENT_TYPE_MIMES:
        return None
    if not mime:
        return None
    guessed = mimetypes.guess_extension(mime)
    if guessed:
        return normalize_output_extension(guessed)
    manual_map = {'video/mp4': '.mp4', 'video/quicktime': '.mov', 'video/webm': '.webm', 'image/jpeg': '.jpg', 'image/png': '.png', 'image/webp': '.webp', 'image/gif': '.gif'}
    return manual_map.get(mime)

def resolve_download_output_path(output_path: str, *, content_type: str | None=None, source_url: str | None=None, preferred_ext: str | None=None) -> Path:
    out = Path(output_path)
    if out.suffix:
        return out
    inferred_ext = infer_extension_from_content_type(content_type) or infer_extension_from_url(source_url or '') or normalize_output_extension(preferred_ext)
    if not inferred_ext:
        return out
    return out.with_name(f'{out.name}{inferred_ext}')

def download_file(url: str, output_path: str, *, preferred_ext: str | None=None) -> str:
    import shutil as _shutil
    with urllib.request.urlopen(url, timeout=300) as resp:
        final_url = resp.geturl() or url
        content_type = resp.headers.get('Content-Type')
        out = resolve_download_output_path(output_path, content_type=content_type, source_url=final_url, preferred_ext=preferred_ext)
        out.parent.mkdir(parents=True, exist_ok=True)
        with open(out, 'wb') as f:
            _shutil.copyfileobj(resp, f, length=8 * 1024 * 1024)
    return str(out.resolve())

def resolve_indexed_output_path(output_path: str | None, *, index: int, total: int, preferred_ext: str | None=None) -> str:
    default_output_root = resolve_output_root()
    if total <= 1:
        if output_path:
            return output_path
        inferred_ext = normalize_output_extension(preferred_ext) or '.bin'
        return str((default_output_root / f'result{inferred_ext}').resolve())
    if output_path:
        base_path = Path(output_path)
        if base_path.exists() and base_path.is_dir():
            base_path = base_path / 'result'
    else:
        base_path = default_output_root / 'result'
    preferred = normalize_output_extension(preferred_ext)
    suffix = preferred or base_path.suffix
    if base_path.suffix:
        base_name = base_path.stem
        return str(base_path.with_name(f'{base_name}-{index:02d}{suffix or base_path.suffix}').resolve())
    return str(base_path.with_name(f"{base_path.name}-{index:02d}{suffix or ''}").resolve())

def download_outputs(outputs: list[dict[str, Any]], output_path: str | None) -> list[str]:
    saved_paths: list[str] = []
    total = len(outputs)
    for (index, item) in enumerate(outputs, start=1):
        object_url = item.get('object_url')
        if not object_url:
            raise ValueError(f'output #{index} missing object_url')
        target_path = resolve_indexed_output_path(output_path, index=index, total=total, preferred_ext=item.get('output_ext'))
        saved_paths.append(download_file(object_url, target_path, preferred_ext=item.get('output_ext')))
    return saved_paths

def _is_auxiliary_output(object_url: str, saved_path: str) -> bool:
    """识别过程图 / 占位缩略图（如 rgthree.compare 的 _temp_ 节点输出）。"""
    url_lower = (object_url or '').lower()
    if '_temp_' in url_lower or 'rgthree.compare' in url_lower:
        return True
    # 文件 < 10KB 且是图片格式，大概率是占位缩略图
    try:
        size = Path(saved_path).stat().st_size
        if size < 10240 and any(saved_path.lower().endswith(ext) for ext in ('.png', '.jpg', '.jpeg', '.webp')):
            return True
    except Exception:
        pass
    return False


def emit_downloaded_outputs(outputs: list[dict[str, Any]], saved_paths: list[str]) -> None:
    video_exts = ('.mp4', '.mov', '.webm', '.mkv', '.m4v')
    main_outputs = []
    aux_outputs = []
    for (index, saved) in enumerate(saved_paths, start=1):
        output_meta = outputs[index - 1] if index - 1 < len(outputs) else {}
        object_url = output_meta.get('object_url') or ''
        if _is_auxiliary_output(object_url, saved):
            aux_outputs.append((index, saved, output_meta))
        else:
            main_outputs.append((index, saved, output_meta))

    print(f'OUTPUT_COUNT:{len(main_outputs)}')
    for (index, saved, output_meta) in main_outputs:
        object_url = output_meta.get('object_url') or ''
        print(f'OUTPUT_FILE:{saved}')
        if object_url:
            print(f'OUTPUT_URL:{object_url}')
        url_lower = object_url.lower().split('?', 1)[0]
        saved_lower = saved.lower()
        is_video = url_lower.endswith(video_exts) or saved_lower.endswith(video_exts)
        if is_video and object_url:
            print(object_url)
        else:
            display_src = object_url or saved
            print(f'![生成结果]({display_src})')
        if output_meta.get('cost_time') is not None:
            print(f"OUTPUT_{index:02d}_DURATION_MS:{output_meta['cost_time']}")

    if aux_outputs:
        print(f'AUX_OUTPUT_COUNT:{len(aux_outputs)}')
        for (index, saved, output_meta) in aux_outputs:
            print(f'AUX_OUTPUT_FILE:{saved}')

def poll_until_done(api_key: str, request_id: str) -> dict[str, Any]:
    start = time.time()
    last_status = None
    consecutive_errors = 0
    while time.time() - start < MAX_POLL_SECONDS:
        resp = query_detail(api_key, request_id)
        # query_detail 返回错误（网络抖动等）→ 容忍几次后放弃
        if isinstance(resp, dict) and resp.get('ok') is False:
            consecutive_errors += 1
            if consecutive_errors >= 3:
                return {'ok': False, 'error': 'POLL_QUERY_FAILED', 'detail': resp.get('error'), 'request_id': request_id}
            time.sleep(POLL_INTERVAL)
            continue
        consecutive_errors = 0
        data = extract_result_data(resp)
        status = data.get('status')
        if status != last_status:
            print(f'STATUS:{status}', file=sys.stderr)
            last_status = status
        if status == 'Success':
            outputs_resp = query_outputs(api_key, request_id)
            if isinstance(outputs_resp, dict) and outputs_resp.get('ok') is False:
                return {'ok': False, 'error': 'OUTPUTS_QUERY_FAILED', 'detail': outputs_resp.get('error'), 'request_id': request_id}
            return outputs_resp
        if status in {'Failed', 'Canceled'}:
            return {'ok': False, 'error': 'TASK_FAILED', 'status': status, 'detail': data, 'request_id': request_id}
        time.sleep(POLL_INTERVAL)
    return {'ok': False, 'error': 'TIMEOUT', 'message': 'Polling timed out', 'request_id': request_id}
