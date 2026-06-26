from __future__ import annotations

import base64
import json
from pathlib import Path
from typing import Any, Dict, List

import requests

from .common import ApiError, AppConfig, GENERATED_DIR, save_json

PROGRESS_FILE = GENERATED_DIR / '.progress.json'



def load_progress() -> Dict[str, Any]:
    if PROGRESS_FILE.exists():
        try:
            return json.loads(PROGRESS_FILE.read_text(encoding='utf-8'))
        except json.JSONDecodeError:
            return {'completed': [], 'failed': [], 'total': 0}
    return {'completed': [], 'failed': [], 'total': 0}



def save_progress(progress_data: Dict[str, Any]) -> None:
    save_json(PROGRESS_FILE, progress_data)



def clear_progress() -> None:
    if PROGRESS_FILE.exists():
        PROGRESS_FILE.unlink()



def _extract_image_bytes(data: Dict[str, Any]) -> bytes:
    try:
        part = data['candidates'][0]['content']['parts'][0]
        inline = part['inlineData']
        return base64.b64decode(inline['data'])
    except (KeyError, IndexError, TypeError, ValueError) as exc:
        raise ApiError(f'图片生成返回结构异常: {json.dumps(data, ensure_ascii=False)[:500]}') from exc



def generate_image(config: AppConfig, prompt: str, style_preset: Dict[str, Any], image_index: int = 0, negative_prompt: str = '') -> Path:
    GENERATED_DIR.mkdir(parents=True, exist_ok=True)
    full_prompt = prompt
    if style_preset:
        suffix = []
        for key in ['style', 'colors', 'tone']:
            value = style_preset.get(key)
            if value:
                suffix.append(f'{key}: {value}')
        if suffix:
            full_prompt += '\n\n风格补充：' + '；'.join(suffix)
    if negative_prompt:
        full_prompt += f'\n\n负向要求：{negative_prompt}'

    url = f"{config.base_url}/models/{config.model}:generateContent"
    payload = {
        'contents': [{'parts': [{'text': full_prompt}]}],
    }
    headers = {'x-goog-api-key': config.api_key}
    retries = config.max_retries
    timeout = config.timeout_seconds
    last_error = None
    for attempt in range(retries):
        try:
            resp = requests.post(url, json=payload, headers=headers, timeout=timeout)
            resp.raise_for_status()
            image_bytes = _extract_image_bytes(resp.json())
            break
        except requests.HTTPError as exc:
            body = exc.response.text[:500] if exc.response is not None else str(exc)
            last_error = ApiError(f'图片生成请求失败: {body}')
        except requests.RequestException as exc:
            last_error = ApiError(f'图片生成网络异常: {exc}')
        if attempt == retries - 1 and last_error is not None:
            raise last_error
    else:
        raise ApiError('图片生成请求失败')
    output_path = GENERATED_DIR / f'image_{image_index + 1}.png'
    output_path.write_bytes(image_bytes)
    return output_path



def generate_images(config: AppConfig, prompts: List[str], style_preset: Dict[str, Any], negative_prompt: str = '') -> List[str]:
    progress = load_progress()
    progress['total'] = len(prompts)
    save_progress(progress)

    output_files: List[str] = []
    for index, prompt in enumerate(prompts):
        marker = index + 1
        if marker in progress.get('completed', []):
            path = GENERATED_DIR / f'image_{marker}.png'
            if path.exists():
                output_files.append(str(path))
                continue
            progress['completed'] = [m for m in progress.get('completed', []) if m != marker]
            save_progress(progress)
        try:
            path = generate_image(config, prompt, style_preset, index, negative_prompt)
            output_files.append(str(path))
            progress.setdefault('completed', []).append(marker)
            progress['failed'] = [m for m in progress.get('failed', []) if m != marker]
        except ApiError:
            if marker not in progress.setdefault('failed', []):
                progress['failed'].append(marker)
            save_progress(progress)
            raise
        save_progress(progress)
    return output_files
