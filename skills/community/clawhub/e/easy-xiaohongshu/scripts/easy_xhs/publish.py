from __future__ import annotations

import base64
import json
from pathlib import Path
from typing import Any, Dict, List, Optional

import requests

from .common import AppConfig, PublishError

DEFAULT_HEADERS = {'Content-Type': 'application/json'}



def post_json(url: str, payload: Dict[str, Any], headers: Optional[Dict[str, str]] = None, timeout: int = 30):
    resp = requests.post(url, json=payload, headers=headers or DEFAULT_HEADERS, timeout=timeout)
    resp.raise_for_status()
    return resp


def post_json_with_retry(
    config: AppConfig,
    payload: Dict[str, Any],
    headers: Optional[Dict[str, str]] = None,
    timeout: Optional[int] = None,
):
    retries = config.max_retries
    request_timeout = timeout or config.mcp_timeout_seconds
    last_error = None
    for attempt in range(retries):
        try:
            return post_json(config.mcp_url, payload, headers=headers, timeout=request_timeout)
        except requests.HTTPError as exc:
            body = exc.response.text[:500] if exc.response is not None else str(exc)
            last_error = PublishError(f'发布请求失败: {body}')
        except requests.RequestException as exc:
            last_error = PublishError(f'发布网络异常: {exc}')
        if attempt == retries - 1 and last_error is not None:
            raise last_error
    raise PublishError('发布请求失败')



def mcp_init(config: AppConfig) -> str:
    payload = {
        'jsonrpc': '2.0',
        'method': 'initialize',
        'params': {
            'protocolVersion': '2024-11-05',
            'capabilities': {},
            'clientInfo': {'name': 'easy-xiaohongshu', 'version': '2.0'},
        },
        'id': 1,
    }
    resp = post_json_with_retry(config, payload)
    session_id = resp.headers.get('mcp-session-id') or resp.headers.get('Mcp-Session-Id')
    if not session_id:
        raise PublishError('无法获取 MCP Session ID，请检查 MCP 服务是否运行')
    post_json_with_retry(
        config,
        {'jsonrpc': '2.0', 'method': 'notifications/initialized', 'params': {}},
        headers={**DEFAULT_HEADERS, 'mcp-session-id': session_id},
    )
    return session_id



def mcp_call(config: AppConfig, session_id: str, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
    headers = {**DEFAULT_HEADERS, 'mcp-session-id': session_id}
    payload = {
        'jsonrpc': '2.0',
        'method': 'tools/call',
        'params': {'name': tool_name, 'arguments': arguments},
        'id': 2,
    }
    resp = post_json_with_retry(config, payload, headers=headers, timeout=max(120, config.mcp_timeout_seconds))
    data = resp.json()
    if 'error' in data:
        raise PublishError(f"MCP 调用失败: {json.dumps(data['error'], ensure_ascii=False)}")
    return data.get('result', {})



def image_to_data_uri(image_path: str) -> str:
    path = Path(image_path)
    if not path.exists():
        raise PublishError(f'图片不存在: {image_path}')
    encoded = base64.b64encode(path.read_bytes()).decode('utf-8')
    return f'data:image/png;base64,{encoded}'



def publish_note(config: AppConfig, title: str, content: str, images: List[str], tags: Optional[List[str]] = None) -> Dict[str, Any]:
    if not title.strip():
        raise PublishError('标题不能为空')
    if not content.strip():
        raise PublishError('正文不能为空')
    if not images:
        raise PublishError('至少需要一张图片')

    session_id = mcp_init(config)
    image_payload = [image_to_data_uri(path) for path in images]
    arguments = {
        'title': title.strip(),
        'content': content.strip(),
        'images': image_payload,
        'tags': tags or [],
    }
    return mcp_call(config, session_id, 'publish_content', arguments)
