from __future__ import annotations

import json
import re
from typing import Any, Dict, List

import requests

from .common import ApiError, AppConfig, load_reference_text
from .style import load_style_presets, match_style_preset, recommend_hashtags


SYSTEM_INSTRUCTION = "你是一个擅长小红书内容策划与视觉生成的助手。严格按要求输出，不要附加解释。"



def build_prompt_variables(account_type: str, content_direction: str, target_audience: str, topic: str) -> Dict[str, str]:
    preset = match_style_preset(account_type, {})
    return {
        'account_type': account_type,
        'content_direction': content_direction,
        'target_audience': target_audience,
        'topic': topic,
        'style': str(preset.get('style', '通用')),
        'colors': str(preset.get('colors', '干净、统一、适合图文阅读')),
        'tone': str(preset.get('tone', '自然、真诚、口语化')),
        'emoji': str(preset.get('emoji', '✨')),
        'content_min': str(preset.get('content_min', 35)),
        'content_max': str(preset.get('content_max', 70)),
    }



def apply_template(template: str, values: Dict[str, Any]) -> str:
    try:
        return template.format(**values)
    except KeyError as exc:
        raise ApiError(f'模板变量缺失: {exc}') from exc



def call_gemini_text_api(config: AppConfig, prompt: str) -> str:
    url = f"{config.base_url}/models/{config.model}:generateContent"
    payload = {
        'system_instruction': {'parts': [{'text': SYSTEM_INSTRUCTION}]},
        'contents': [{'parts': [{'text': prompt}]}],
    }
    headers = {'x-goog-api-key': config.api_key}
    retries = config.max_retries
    timeout = config.timeout_seconds
    last_error = None
    for attempt in range(retries):
        try:
            resp = requests.post(url, json=payload, headers=headers, timeout=timeout)
            resp.raise_for_status()
            data = resp.json()
            break
        except requests.HTTPError as exc:
            body = exc.response.text[:500] if exc.response is not None else str(exc)
            last_error = ApiError(f'内容生成请求失败: {body}')
        except requests.RequestException as exc:
            last_error = ApiError(f'内容生成网络异常: {exc}')
        if attempt == retries - 1 and last_error is not None:
            raise last_error
    else:
        raise ApiError('内容生成请求失败')
    try:
        return data['candidates'][0]['content']['parts'][0]['text']
    except (KeyError, IndexError, TypeError) as exc:
        raise ApiError(f'内容生成返回结构异常: {json.dumps(data, ensure_ascii=False)[:500]}') from exc



def extract_json_block(text: str) -> Dict[str, Any]:
    match = re.search(r'```json\s*(\{.*?\})\s*```', text, re.S)
    raw = match.group(1) if match else text.strip()
    try:
        return json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ApiError(f'模型未返回合法 JSON: {raw[:500]}') from exc



def extract_page_prompts(content_text: str) -> List[str]:
    matches = re.findall(r'成品图生成提示词[：:]\s*(.+?)(?=\n\s*【第|\n\s*# 第二部分|\Z)', content_text, re.S)
    return [m.strip() for m in matches if isinstance(m, str) and m.strip()]



def parse_combined_output(raw_text: str) -> Dict[str, Any]:
    split_match = re.search(r'(^|\n)\s*# 第二部分：发布文案 JSON\s*', raw_text)
    if split_match:
        content_text = raw_text[:split_match.start()].strip()
        caption_text = raw_text[split_match.end():].strip()
    else:
        content_text = raw_text.strip()
        caption_text = raw_text.strip()

    caption_json = extract_json_block(caption_text)
    page_prompts = extract_page_prompts(content_text)

    return {
        'generated_content': {
            'raw_text': content_text,
            'page_prompts': page_prompts,
        },
        'generated_caption': caption_json,
        'raw_text': raw_text,
    }



def parse_generated_content_prompts(content_data: Any) -> List[str]:
    if isinstance(content_data, dict):
        prompts = content_data.get('page_prompts')
        if isinstance(prompts, list):
            normalized = [str(item).strip() for item in prompts if str(item).strip()]
            if normalized:
                return normalized
        pages = content_data.get('pages')
        if isinstance(pages, list):
            normalized = []
            for page in pages:
                if not isinstance(page, dict):
                    continue
                prompt = str(page.get('prompt', '')).strip()
                if prompt:
                    normalized.append(prompt)
            if normalized:
                return normalized
        raw_text = content_data.get('raw_text')
        if isinstance(raw_text, str):
            return extract_page_prompts(raw_text)
        return []
    if isinstance(content_data, str):
        return extract_page_prompts(content_data)
    return []



def generate_prompts(account_type: str, content_direction: str, target_audience: str, topic: str) -> Dict[str, Any]:
    presets = load_style_presets()
    preset = match_style_preset(account_type, presets)
    values = {
        'account_type': account_type,
        'content_direction': content_direction,
        'target_audience': target_audience,
        'topic': topic,
        'style': str(preset.get('style', '通用')),
        'colors': str(preset.get('colors', '干净、统一、适合图文阅读')),
        'tone': str(preset.get('tone', '自然、真诚、口语化')),
        'emoji': str(preset.get('emoji', '✨')),
        'content_min': str(preset.get('content_min', 35)),
        'content_max': str(preset.get('content_max', 70)),
    }
    prompt_template = load_reference_text('prompt-template.md')
    caption_template = load_reference_text('caption-template.md')
    hashtags = recommend_hashtags(topic, content_direction, target_audience)
    return {
        'style_preset': preset,
        'image_prompt': apply_template(prompt_template, values),
        'caption_prompt': apply_template(caption_template, values),
        'recommended_tags': hashtags,
    }



def generate_content(config: AppConfig, caption_prompt: str, image_prompt: str) -> Dict[str, Any]:
    combined_raw = call_gemini_text_api(config, image_prompt)
    parsed = parse_combined_output(combined_raw)

    if not parsed['generated_caption']:
        caption_raw = call_gemini_text_api(config, caption_prompt)
        parsed['generated_caption'] = extract_json_block(caption_raw)

    return {
        'generated_content': parsed['generated_content'],
        'generated_caption': parsed['generated_caption'],
    }
