"""远端对象信息整理 + 卡片渲染。

主要职责：
  - resolve_info_target / resolve_remote_prefill_target: 把链接 / draft id / app id
    归一化成可用的 bizy_model_id
  - build_remote_info_output: 把远端 detail / webapp_detail / version_detail / workflow
    捏成 summary（给 LLM）+ raw（给开发）的双层 JSON
  - build_remote_info_summary: summary 内部结构（identity / capability / workflow_summary
    / human_summary / resolved_contract / execution_support / executable_draft）
  - build_remote_prefilled_card: **唯一的预填卡渲染器**。菜单 10 个固定模型（图片 5 + 视频 5）和远端任意 app
    都走这个。卡片字段、中文标签、可选值全部从 contract 拿
  - choose_remote_field_display_label / humanize_remote_prefill_label: 通用中文标签翻译
    （logical_name 优先，fallback 用 field_name 启发式）。覆盖 prompt / aspect_ratio /
    resolution / quality / cfg / strength / temperature / top_p / sampler 等 20+ 字段

【统一执行路径后】
菜单 10 个固定模型（图片 5 + 视频 5）已经不再有专属渲染器。dispatch.py 单任务和 batch.py 批量都直接调
build_remote_prefilled_card，参数表 / 中文标签 / 可选值都从 BizyAir 远端 contract 动态拿。
新加菜单模型只需 dispatch_common.ROUTE_TABLE 加一行 ID，零字段配置。
"""
from __future__ import annotations
import argparse, json, re, sys, urllib.parse
from typing import Any

import api
import contract
import app
import common
from common import (
    BIZYAIR_INFO_HOSTS, BIZY_MODEL_DETAIL_URL, COMMUNITY_URL, OFFICIAL_URL,
)

def normalize_remote_type(modality: str | None) -> str | None:
    if modality is None:
        return None
    value = common.normalized_text(modality)
    mapping = {'image': 'Application', 'application': 'Application', 'app': 'Application', 'video': 'Workflow', 'workflow': 'Workflow', 'mcp': 'MCP', 'model': 'Checkpoint', 'lora': 'LoRA', 'checkpoint': 'Checkpoint'}
    return mapping.get(value, modality)

def remote_list_endpoint(remote_source: str) -> str:
    return OFFICIAL_URL if common.normalized_text(remote_source) == 'official' else COMMUNITY_URL

def is_workflow_identity(detail_result: dict[str, Any] | None, fallback_model: dict[str, Any] | None=None) -> bool:
    detail_data = api.extract_result_data(detail_result)
    fallback = fallback_model or {}
    kind = str(detail_data.get('type') or fallback.get('type') or '').strip().lower()
    return kind == 'workflow'

def collect_workflow_ref_ids(detail_result: dict[str, Any] | None, webapp_detail: dict[str, Any] | None, version_detail: dict[str, Any] | None) -> dict[str, Any]:
    detail_data = api.extract_result_data(detail_result)
    webapp_data = api.extract_result_data(webapp_detail)
    version_data = api.extract_result_data(version_detail)
    first_version = {}
    versions = detail_data.get('versions') or []
    if versions and isinstance(versions[0], dict):
        first_version = versions[0]
    return {'ref_bizy_model_id': version_data.get('ref_bizy_model_id') or webapp_data.get('ref_bizy_model_id') or first_version.get('ref_bizy_model_id') or detail_data.get('ref_bizy_model_id'), 'ref_web_app_id': version_data.get('ref_web_app_id') or webapp_data.get('ref_web_app_id') or first_version.get('ref_web_app_id') or detail_data.get('ref_web_app_id')}

def build_workflow_info_only_message() -> str:
    return '这是一个纯 ComfyUI 工作流，没有对应的 AI 应用版本，目前不支持直接运行～你可以在 BizyAir 网页端打开它，手动加载到 ComfyUI 编辑器里跑。'

def build_missing_execution_mapping_message() -> str:
    return '这边的信息和参数都已经帮你整理好啦~ 只是目前后台还没拿到它稳定的执行路线图，为了安全起见，这轮咱们就先不直接跑了。你要不要拿着参数去网页端试一下？'

def build_workflow_ref_app_ready_message() -> str:
    return '好嘞～这条工作流的通道已经完全打通，随时可以帮你跑起来～'

def resolve_remote_execution_target(api_key: str, detail_result: dict[str, Any] | None, webapp_detail: dict[str, Any] | None, version_detail: dict[str, Any] | None, *, fallback_model: dict[str, Any] | None=None) -> dict[str, Any]:
    webapp_data = api.extract_result_data(webapp_detail)
    if not is_workflow_identity(detail_result, fallback_model=fallback_model):
        supported = bool(webapp_data.get('id'))
        return {'supported': supported, 'mode': 'direct_webapp' if supported else 'missing_webapp_mapping', 'reason': None if supported else 'missing_webapp_mapping', 'webapp_detail': webapp_detail or {}, 'web_app_id': webapp_data.get('id'), 'support_scope': {'info': True, 'parameter_card': True, 'execute': supported}, 'message': None if supported else build_missing_execution_mapping_message(), 'feedback_channel': None}
    ref_ids = collect_workflow_ref_ids(detail_result, webapp_detail, version_detail)
    candidate_ids: list[str] = []
    for candidate in [ref_ids.get('ref_bizy_model_id'), ref_ids.get('ref_web_app_id')]:
        if candidate in (None, '', [], {}):
            continue
        candidate_text = str(candidate)
        if candidate_text not in candidate_ids:
            candidate_ids.append(candidate_text)
    for candidate in candidate_ids:
        resolved = api.fetch_remote_webapp_detail(api_key, candidate)
        resolved_data = api.extract_result_data(resolved)
        if resolved_data.get('id'):
            return {'supported': True, 'mode': 'workflow_ref_app', 'reason': None, 'webapp_detail': resolved, 'web_app_id': resolved_data.get('id'), 'ref_bizy_model_id': ref_ids.get('ref_bizy_model_id'), 'ref_web_app_id': ref_ids.get('ref_web_app_id') or resolved_data.get('id'), 'resolved_from': candidate, 'support_scope': {'info': True, 'parameter_card': True, 'execute': True}, 'message': build_workflow_ref_app_ready_message(), 'feedback_channel': None}
    return {'supported': False, 'mode': 'workflow_info_only', 'reason': 'workflow_without_ref_app', 'webapp_detail': {}, 'web_app_id': None, 'ref_bizy_model_id': ref_ids.get('ref_bizy_model_id'), 'ref_web_app_id': ref_ids.get('ref_web_app_id'), 'support_scope': {'info': True, 'parameter_card': True, 'execute': False}, 'message': build_workflow_info_only_message(), 'feedback_channel': None}

def preflight_remote_app_run(api_key: str, bizy_model_id: str | int) -> dict[str, Any]:
    detail = api.fetch_remote_detail(api_key, bizy_model_id)
    detail_data = api.extract_result_data(detail)
    webapp_detail = api.fetch_remote_webapp_detail(api_key, bizy_model_id)
    webapp_detail_data = api.extract_result_data(webapp_detail)
    versions = detail_data.get('versions') or []
    version_id = None
    if versions and isinstance(versions[0], dict):
        version_id = versions[0].get('id')
    if version_id is None:
        version_id = detail_data.get('bizy_model_version_id') or detail_data.get('version_id')
    version_detail = api.fetch_remote_version_detail(api_key, version_id) if version_id is not None else {}
    workflow = api.fetch_remote_workflow(api_key, version_id) if version_id is not None else {}
    if not api.extract_result_data(workflow):
        workflow = api.fetch_remote_workflow_from_url(webapp_detail_data.get('web_app_workflow_url'))
    execution_target = resolve_remote_execution_target(api_key, detail, webapp_detail, version_detail)
    resolved_contract = contract.resolve_remote_input_contract(execution_target=execution_target, webapp_detail=webapp_detail, workflow=workflow)
    summary = build_remote_info_summary(bizy_model_id=str(bizy_model_id), detail_result=detail, webapp_detail=webapp_detail, fallback_model=None, version_detail=version_detail, workflow=workflow, execution_target=execution_target, resolved_contract=resolved_contract)
    return {'bizy_model_id': str(bizy_model_id), 'version_id': version_id, 'detail': detail, 'webapp_detail': webapp_detail, 'version_detail': version_detail, 'workflow': workflow, 'execution_target': execution_target, 'resolved_contract': resolved_contract, 'summary': summary}

def collect_workflow_summary(workflow: dict[str, Any]) -> dict[str, Any]:
    nodes = workflow.get('nodes', []) if isinstance(workflow, dict) else []
    node_types: dict[str, int] = {}
    image_inputs = 0
    audio_inputs = 0
    video_inputs = 0
    prompt_like_nodes: list[str] = []
    save_like_nodes: list[str] = []
    widget_candidates: list[dict[str, Any]] = []
    preferred_param_names = {'prompt', 'text', 'seed', 'steps', 'cfg', 'strength', 'width', 'height', 'aspect_ratio', 'size', 'duration', 'model', 'images', 'image', 'audio', 'video'}
    noise_node_keywords = ['save', 'preview']
    noise_value_markers = ['comfyui']
    for node in nodes:
        node_type = str(node.get('type') or 'Unknown')
        node_types[node_type] = node_types.get(node_type, 0) + 1
        lowered = node_type.lower()
        if 'loadimage' in lowered:
            image_inputs += 1
        if 'audio' in lowered and ('load' in lowered or 'input' in lowered):
            audio_inputs += 1
        if 'video' in lowered and ('load' in lowered or 'input' in lowered):
            video_inputs += 1
        if any((x in lowered for x in ['prompt', 'text', 'banana', 'qwen', 'gemini', 'flux', 'wan'])):
            if node_type not in prompt_like_nodes:
                prompt_like_nodes.append(node_type)
        if any((x in lowered for x in noise_node_keywords)):
            if node_type not in save_like_nodes:
                save_like_nodes.append(node_type)
        widget_values = node.get('widgets_values')
        inputs = node.get('inputs') or []
        outputs = node.get('outputs') or []
        output_names = [str(o.get('name') or '') for o in outputs]
        if isinstance(widget_values, list):
            for (idx, value) in enumerate(widget_values):
                widget_name = None
                if idx < len(inputs):
                    widget_name = inputs[idx].get('name') or inputs[idx].get('label')
                if not widget_name and idx < len(output_names):
                    widget_name = output_names[idx]
                widget_name = str(widget_name or f'widget_{idx}')
                if not isinstance(value, (str, int, float, bool)) or str(value) == '':
                    continue
                widget_candidates.append({'node_id': node.get('id'), 'node_type': node_type, 'name': widget_name, 'value': value, 'confidence': 'confirmed_from_resolved_workflow'})
    top_node_types = sorted(node_types.items(), key=lambda kv: (-kv[1], kv[0]))[:12]
    key_parameters = []
    seen_param_keys: set[tuple[str, str]] = set()
    for item in widget_candidates:
        name_low = str(item['name']).lower()
        node_low = str(item['node_type']).lower()
        value_low = str(item['value']).lower()
        if any((k in node_low for k in noise_node_keywords)):
            continue
        if any((marker == value_low for marker in noise_value_markers)):
            continue
        looks_key = name_low in preferred_param_names or any((k in name_low for k in ['prompt', 'seed', 'ratio', 'size', 'width', 'height', 'steps', 'cfg', 'strength', 'duration', 'model'])) or ('image' in name_low and 'load' not in node_low) or ('audio' in name_low and 'load' not in node_low) or ('video' in name_low and 'load' not in node_low)
        if not looks_key:
            continue
        dedupe = (str(item['node_type']), str(item['name']))
        if dedupe in seen_param_keys:
            continue
        seen_param_keys.add(dedupe)
        key_parameters.append(item)
        if len(key_parameters) >= 12:
            break
    return {'node_count': len(nodes), 'top_node_types': [{'type': k, 'count': v} for (k, v) in top_node_types], 'detected_inputs': {'image_like_loaders': image_inputs, 'audio_like_loaders': audio_inputs, 'video_like_loaders': video_inputs}, 'prompt_like_nodes': prompt_like_nodes[:8], 'save_like_nodes': save_like_nodes[:8], 'key_parameters': key_parameters, 'confidence': {'node_shape': 'confirmed_from_resolved_workflow', 'key_parameters': 'heuristic_from_resolved_workflow'}}


def build_brief_summary(identity: dict[str, Any], capability: dict[str, Any], human_summary: dict[str, Any]) -> str:
    name = identity.get('name') or identity.get('bizy_model_id') or 'unknown app'
    task = capability.get('task_type') or 'unknown_task'
    base_model = capability.get('base_model_hint') or identity.get('base_model')
    input_hint = human_summary.get('input_hint', {})
    image_count = input_hint.get('images')
    brief_parts = [str(name)]
    task_map = {'multi_image_edit_or_fusion': '多图编辑/融合', 'image_to_image': '图生图', 'text_to_image_or_general_workflow': '文生图/通用工作流', 'audio_conditioned_generation': '音频条件生成', 'video_or_animation': '视频/动画'}
    brief_parts.append(task_map.get(str(task), str(task)))
    if isinstance(image_count, int) and image_count > 0:
        brief_parts.append(f'显式图片输入 {image_count} 张')
    elif image_count == 0 and task == 'text_to_image_or_general_workflow':
        brief_parts.append('无显式图片输入')
    if base_model:
        brief_parts.append(f'base model: {base_model}')
    param_map = {str(item.get('name')): item.get('value') for item in human_summary.get('important_params', [])}
    if param_map.get('aspect_ratio'):
        brief_parts.append(f"比例 {param_map['aspect_ratio']}")
    if param_map.get('image_size'):
        brief_parts.append(f"尺寸 {param_map['image_size']}")
    return '，'.join(brief_parts)

def get_remote_contract_binding_keys(contract_data: dict[str, Any], logical_name: str) -> list[str]:
    return contract.get_remote_contract_binding_keys(contract_data, logical_name)

def build_remote_executable_draft(*, bizy_model_id: str, detail_result: dict[str, Any] | None, webapp_detail: dict[str, Any] | None, fallback_model: dict[str, Any] | None, version_detail: dict[str, Any] | None, workflow: dict[str, Any] | None, execution_target: dict[str, Any] | None=None, resolved_contract: dict[str, Any] | None=None) -> dict[str, Any]:
    detail_data = api.extract_result_data(detail_result)
    execution = execution_target or {}
    runtime_webapp_detail = execution.get('webapp_detail') or webapp_detail or {}
    webapp_detail_data = api.extract_result_data(runtime_webapp_detail)
    version_data = api.extract_result_data(version_detail)
    workflow_data = api.extract_result_data(workflow)
    input_hints = contract.collect_required_input_hints(workflow_data)
    resolved = resolved_contract or contract.resolve_remote_input_contract(execution_target=execution, webapp_detail=webapp_detail, workflow=workflow)
    required_inputs = list(resolved.get('required_inputs') or [])
    hidden_media_slots = collect_hidden_remote_media_slots(webapp_detail_data) if webapp_detail_data else {}
    existing_required_types = {str(item.get('type')) for item in required_inputs}
    for media_type in ['image', 'audio', 'video']:
        if media_type in existing_required_types:
            continue
        hidden_count = len(hidden_media_slots.get(media_type, []))
        if hidden_count > 0:
            required_inputs.append({'type': media_type, 'count': hidden_count, 'required': True})
    if execution and (not execution.get('supported')):
        return {'required_inputs': required_inputs, 'candidate_fields': resolved.get('candidate_fields') or input_hints.get('candidate_fields', []), 'resolved_contract': resolved, 'status': 'info_only', 'support_scope': execution.get('support_scope'), 'message': execution.get('message')}
    payload = api.build_remote_run_payload(str(bizy_model_id), {'bizy_model_id': str(bizy_model_id), 'version_id': version_data.get('id') or detail_data.get('bizy_model_version_id') or detail_data.get('version_id'), 'detail': detail_result or {}, 'webapp_detail': webapp_detail or {}, 'version_detail': version_detail or {}, 'workflow': workflow or {}, 'execution_target': execution}, argparse.Namespace(prompt=None, image=None, audio=None, video=None, aspect_ratio=None, resolution=None, steps=None, duration=None, seed=None, random_seed=False, model_name=None, width=None, height=None, param=None, output=None, sync=False))
    return {'required_inputs': required_inputs, 'candidate_fields': resolved.get('candidate_fields') or input_hints.get('candidate_fields', []), 'resolved_contract': resolved, 'status': 'draft_from_detail_version_workflow', 'execution_mode': execution.get('mode') or 'direct_webapp', 'execution_web_app_id': webapp_detail_data.get('id')}

def build_remote_info_summary(*, bizy_model_id: str, detail_result: dict[str, Any] | None, webapp_detail: dict[str, Any] | None, fallback_model: dict[str, Any] | None, version_detail: dict[str, Any] | None, workflow: dict[str, Any] | None, execution_target: dict[str, Any] | None=None, resolved_contract: dict[str, Any] | None=None) -> dict[str, Any]:
    version_data = api.extract_result_data(version_detail)
    workflow_summary = collect_workflow_summary(workflow or {}) if workflow else {}
    capability = {}
    detail_data = api.extract_result_data(detail_result)
    webapp_detail_data = api.extract_result_data(webapp_detail)
    fallback = fallback_model or {}
    execution = execution_target or {}
    resolved = resolved_contract or contract.resolve_remote_input_contract(execution_target=execution, webapp_detail=webapp_detail, workflow=workflow)
    identity = {'bizy_model_id': bizy_model_id, 'web_app_id': webapp_detail_data.get('id'), 'execution_web_app_id': execution.get('web_app_id'), 'version_id': version_data.get('id') or (fallback.get('versions', [{}])[0].get('id') if fallback.get('versions') else None), 'name': detail_data.get('name') or webapp_detail_data.get('name') or fallback.get('name') or version_data.get('name'), 'type': detail_data.get('type') or fallback.get('type'), 'base_model': version_data.get('base_model') or webapp_detail_data.get('base_model') or (fallback.get('versions', [{}])[0].get('base_model') if fallback.get('versions') else None), 'intro': version_data.get('intro') or webapp_detail_data.get('intro'), 'sign': version_data.get('sign') or (fallback.get('versions', [{}])[0].get('sign') if fallback.get('versions') else None), 'path': version_data.get('path') or (fallback.get('versions', [{}])[0].get('file_name') if fallback.get('versions') else None), 'draft_id': version_data.get('draft_id') or (fallback.get('versions', [{}])[0].get('draft_id') if fallback.get('versions') else None), 'public': version_data.get('public'), 'available': version_data.get('available')}
    specialized_parameters = []
    important_params = specialized_parameters or [{'name': item.get('name'), 'value': item.get('value'), 'node_type': item.get('node_type'), 'confidence': item.get('confidence')} for item in workflow_summary.get('key_parameters', [])[:8] if str(item.get('name') or '').lower() not in {'prompt', 'text', 'example_prompt'}]
    important_params = [item for item in important_params if str(item.get('name') or '').lower() not in {'prompt', 'text', 'example_prompt'}]
    human_summary = {'task_guess': capability.get('task_type'), 'input_profile': capability.get('input_profile') or {}, 'input_hint': {'images': workflow_summary.get('detected_inputs', {}).get('image_like_loaders'), 'audios': workflow_summary.get('detected_inputs', {}).get('audio_like_loaders'), 'videos': workflow_summary.get('detected_inputs', {}).get('video_like_loaders')}, 'likely_nodes': [item.get('type') for item in workflow_summary.get('top_node_types', [])[:5]], 'important_params': important_params}
    brief = build_brief_summary(identity, capability, human_summary)
    executable_draft = build_remote_executable_draft(bizy_model_id=bizy_model_id, detail_result=detail_result, webapp_detail=webapp_detail, fallback_model=fallback_model, version_detail=version_detail, workflow=workflow, execution_target=execution, resolved_contract=resolved)
    execution_support = {'supported': bool(execution.get('support_scope', {}).get('execute', execution.get('supported'))), 'mode': execution.get('mode') or 'direct_webapp', 'support_scope': execution.get('support_scope') or {'info': True, 'parameter_card': True, 'execute': True}, 'ref_bizy_model_id': execution.get('ref_bizy_model_id'), 'ref_web_app_id': execution.get('ref_web_app_id'), 'message': execution.get('message')}
    return {'identity': identity, 'capability': capability, 'brief': brief, 'workflow_summary': workflow_summary, 'human_summary': human_summary, 'resolved_contract': resolved, 'execution_support': execution_support, 'executable_draft': executable_draft}

def remote_identity_label(identity: dict[str, Any]) -> str:
    kind = common.normalized_text(identity.get('type'))
    if kind == 'workflow':
        return 'Workflow'
    if kind == 'application':
        return 'App'
    return '对象'

def infer_remote_prompt_modality(human_summary: dict[str, Any]) -> str:
    input_profile = human_summary.get('input_profile') or {}
    if common.safe_int(input_profile.get('video_inputs')) > 0:
        return 'video'
    if str(human_summary.get('task_guess') or '').startswith('video'):
        return 'video'
    return 'image'

def summarize_remote_confirmation_fields(summary: dict[str, Any]) -> list[str]:
    draft = summary.get('executable_draft') or {}
    human_summary = summary.get('human_summary') or {}
    important_params = human_summary.get('important_params') or []
    candidate_fields = draft.get('candidate_fields') or []
    resolved_contract = summary.get('resolved_contract') or draft.get('resolved_contract') or {}
    labels: list[str] = []
    seen: set[str] = set()

    def add(label: str) -> None:
        if label not in seen:
            seen.add(label)
            labels.append(label)
    raw_fields = []
    for item in important_params:
        raw_fields.append(str(item.get('name') or ''))
    for item in candidate_fields:
        raw_fields.append(str(item))
    for logical_name in ['aspect_ratio', 'resolution', 'duration', 'model_name', 'seed']:
        if contract.remote_contract_supports(resolved_contract, logical_name):
            raw_fields.append(logical_name)
    joined = '\n'.join(raw_fields).lower()
    if any((x in joined for x in ['ratio', 'aspect', '比例', '画幅'])):
        add('比例 / 画幅')
    if any((x in joined for x in ['size', 'resolution', 'width', 'height', '尺寸', '分辨率', '规格'])):
        add('尺寸 / 规格')
    if any((x in joined for x in ['duration', '时长', '秒'])):
        add('时长')
    if any((x in joined for x in ['seed', '随机'])):
        add('随机性 / Seed')
    if any((x in joined for x in ['model', 'checkpoint', '档位'])):
        add('模型档位')
    return labels

def choose_remote_field_display_label(field: dict[str, Any]) -> str:
    display_name = str(field.get('display_name') or '').strip()
    if display_name and (not display_name.startswith('其他可控参数')):
        return display_name
    logical_name = str(field.get('logical_name') or '').strip()
    logical_labels = {'prompt': '文本指令（告诉模型这轮要做什么）', 'negative_prompt': '反向提示词（不想出现什么）', 'aspect_ratio': '比例 / 画幅（横竖和构图比例）', 'resolution': '尺寸 / 规格（清晰度或出图档位）', 'width': '宽度（像素）', 'height': '高度（像素）', 'duration': '时长（秒）', 'seed': '随机性 / Seed（想复现时再固定）', 'steps': '采样步数（细化强度）', 'model_name': '模型档位', 'batch_size': '生成数量（一次出几张）', 'sound': '声音开关', 'cfg_scale': '运动强度', 'image': '图片素材', 'audio': '音频素材', 'video': '视频素材'}
    return logical_labels.get(logical_name, display_name or '其他可控参数（需确认）')

def format_remote_option_values(field: dict[str, Any]) -> str | None:
    options = field.get('field_options') or []
    labels: list[str] = []
    ignored_markers = {'max', 'min', 'precision', 'step', 'step2', 'hideonzoom', 'minnodesize'}
    for option in options[:8]:
        label = str(option.get('label') or option.get('value') or '').strip()
        if not label:
            continue
        if label.lower() in ignored_markers:
            continue
        if label and label not in labels:
            labels.append(label)
    if not labels:
        return None
    return ' / '.join(labels)

def prefilled_remote_contract_value(field: dict[str, Any], args: argparse.Namespace, prompt_bundle: dict[str, Any] | None=None) -> str | None:
    logical_name = str(field.get('logical_name') or '').strip()
    bundle = prompt_bundle or {}
    prompt = str(bundle.get('card_display_prompt') or getattr(args, 'prompt', None) or '').strip()
    negative_prompt = str(bundle.get('negative_prompt') or '').strip()
    field_value = field.get('field_value')
    if logical_name == 'prompt':
        if prompt:
            return prompt
    elif logical_name == 'negative_prompt':
        if negative_prompt:
            return negative_prompt
        if field_value not in (None, ''):
            return str(field_value)
        if field.get('system_inject'):
            return '`系统默认负向词`'
    elif logical_name == 'seed':
        if getattr(args, 'seed', None) is not None:
            return f'`{args.seed}`'
        if getattr(args, 'random_seed', False):
            return '`随机`'
    elif logical_name == 'aspect_ratio' and getattr(args, 'aspect_ratio', None):
        return f'`{args.aspect_ratio}`'
    elif logical_name == 'resolution' and getattr(args, 'resolution', None):
        return f'`{args.resolution}`'
    elif logical_name == 'duration' and getattr(args, 'duration', None) is not None:
        return f'`{args.duration} 秒`'
    elif logical_name == 'model_name' and getattr(args, 'model_name', None):
        return f'`{args.model_name}`'
    elif logical_name == 'width' and getattr(args, 'width', None) is not None:
        return f'`{args.width}`'
    elif logical_name == 'height' and getattr(args, 'height', None) is not None:
        return f'`{args.height}`'
    elif logical_name == 'steps' and getattr(args, 'steps', None) is not None:
        return f'`{args.steps}`'
    override_value = match_remote_field_override(logical_name, args)
    if override_value is not None and logical_name not in {'image', 'audio', 'video'}:
        if logical_name == 'duration':
            return f'`{override_value} 秒`'
        return f'`{override_value}`'
    if field_value not in (None, '') and (not field.get('media_type')):
        return f'`{field_value}`' if not isinstance(field_value, str) or not str(field_value).startswith('`') else str(field_value)
    return None

def should_show_remote_contract_field(field: dict[str, Any]) -> bool:
    if str(field.get('support_level') or 'supported') != 'supported':
        return False
    if field.get('media_type'):
        return False
    logical_name = str(field.get('logical_name') or '').strip()
    if logical_name in {'image', 'audio', 'video'}:
        return False
    if logical_name == 'negative_prompt':
        return True
    return bool(field.get('user_input')) or bool(field.get('system_inject'))

def build_remote_prefilled_card(summary: dict[str, Any], args: argparse.Namespace, *, input_kind: str | None=None, original_object_id: str | None=None, resolved_object_id: str | None=None, draft_resolution: dict[str, Any] | None=None, webapp_detail_data: dict[str, Any] | None=None) -> str:
    """**路 A 路 B 合并后唯一的预填卡渲染器。**
    菜单 10 个固定模型（图片 5 + 视频 5） + 远端任意 app/workflow 都走这。
    输入 summary 来自 build_remote_info_output，args 是 argparse.Namespace（用户已填的覆盖值）。
    输出 markdown 字符串，包含：identity → 状态 → prompt → 必需输入 → args 已填字段 → contract 可选字段。
    """
    identity = summary.get('identity') or {}
    execution_support = summary.get('execution_support') or {}
    draft = summary.get('executable_draft') or {}
    supported = bool(execution_support.get('supported'))
    resolved_contract = summary.get('resolved_contract') or draft.get('resolved_contract') or {}
    name = identity.get('name') or f"BizyAir {remote_identity_label(identity)} {resolved_object_id or original_object_id or ''}".strip()
    lines = [f'🧾 **{name} 预填确认卡**']
    if supported:
        lines.append('我先按这轮需求把能确认的部分预填了一版，你看下有没有问题。')
    else:
        lines.append('我先把这轮能确认的部分整理成一张卡；这类对象当前先停在参数整理层，不直接提交执行。')
    lines.append('')
    lines.append(f'- **对象**：{name}')
    lines.append(f'- **类型**：{remote_identity_label(identity)}')
    if resolved_object_id:
        lines.append(f'- **ID**：`{resolved_object_id}`')
    if input_kind == 'workflow_link' and draft_resolution and draft_resolution.get('matched') and original_object_id and resolved_object_id and (original_object_id != resolved_object_id):
        lines.append(f'- **页面还原**：workflow 页面 ID `{original_object_id}` 已还原成公开对象 `{resolved_object_id}`')
    status_text = '✅ 支持继续执行' if supported else '⚠️ 当前先停在信息和参数层，不直接执行'
    lines.append(f'- **当前状态**：{status_text}')
    human_summary = summary.get('human_summary') or {}
    prompt_bundle = app.build_prompt_bundle_for_args(args, route_name=name, modality=infer_remote_prompt_modality(human_summary), task=str(human_summary.get('task_guess') or ''), input_profile=human_summary.get('input_profile') or {})
    prompt = str(prompt_bundle.get('raw_prompt') or getattr(args, 'prompt', None) or '').strip()
    card_display_prompt = str(prompt_bundle.get('card_display_prompt') or prompt).strip()
    prompt_supported = bool(contract.get_supported_remote_prompt_binding_keys(resolved_contract))
    if prompt:
        lines.append(f'- **原始需求**：{prompt}')
        if prompt_bundle.get('changed') and prompt_supported:
            lines.append(f'- **系统整理后的执行提示词**：{card_display_prompt}')
    required_inputs = draft.get('required_inputs') or []
    prompt_required = any((str(item.get('type')) == 'prompt' for item in required_inputs))
    image_required = next((item for item in required_inputs if str(item.get('type')) == 'image'), None)
    audio_required = next((item for item in required_inputs if str(item.get('type')) == 'audio'), None)
    video_required = next((item for item in required_inputs if str(item.get('type')) == 'video'), None)
    if prompt_required and (not prompt):
        lines.append('- **提示词**：[待你补充]')
    image_count = len(getattr(args, 'image', None) or [])
    if image_required:
        required = int(image_required.get('count') or 0)
        if image_count >= required and required > 0:
            lines.append(f'- **图片素材**：已收到 `{image_count} 张`')
        elif image_count > 0:
            lines.append(f'- **图片素材**：已收到 `{image_count} 张`，还差 `{max(required - image_count, 0)} 张`')
        else:
            lines.append(f'- **图片素材**：[待提供 `{required} 张`]')
    elif image_count > 0:
        lines.append(f'- **图片素材**：已收到 `{image_count} 张`')
    audio_count = len(getattr(args, 'audio', None) or [])
    if audio_required:
        required = int(audio_required.get('count') or 0)
        if audio_count >= required and required > 0:
            lines.append(f'- **音频素材**：已收到 `{audio_count} 段`')
        elif audio_count > 0:
            lines.append(f'- **音频素材**：已收到 `{audio_count} 段`，还差 `{max(required - audio_count, 0)} 段`')
        else:
            lines.append(f'- **音频素材**：[待提供 `{required} 段`]')
    elif audio_count > 0:
        lines.append(f'- **音频素材**：已收到 `{audio_count} 段`')
    if video_required:
        required = int(video_required.get('count') or 0)
        video_count = len(getattr(args, 'video', None) or [])
        if video_count >= required and required > 0:
            lines.append(f'- **视频素材**：已收到 `{video_count} 段`')
        elif video_count > 0:
            lines.append(f'- **视频素材**：已收到 `{video_count} 段`，还差 `{max(required - video_count, 0)} 段`')
        else:
            lines.append(f'- **视频素材**：[待提供 `{required} 段`]')
    if getattr(args, 'aspect_ratio', None) and contract.remote_contract_supports(resolved_contract, 'aspect_ratio'):
        lines.append(f'- **比例 / 画幅**：`{args.aspect_ratio}`')
    if getattr(args, 'resolution', None) and contract.remote_contract_supports(resolved_contract, 'resolution'):
        lines.append(f'- **尺寸 / 规格**：`{args.resolution}`')
    if getattr(args, 'duration', None) is not None and contract.remote_contract_supports(resolved_contract, 'duration'):
        lines.append(f'- **时长**：`{args.duration} 秒`')
    if getattr(args, 'model_name', None) and contract.remote_contract_supports(resolved_contract, 'model_name'):
        lines.append(f'- **模型档位**：`{args.model_name}`')
    if getattr(args, 'seed', None) is not None and contract.remote_contract_supports(resolved_contract, 'seed'):
        lines.append(f'- **固定 Seed**：`{args.seed}`')
    elif getattr(args, 'random_seed', False) and contract.remote_contract_supports(resolved_contract, 'seed'):
        lines.append('- **随机性 / Seed**：`随机`')
    confirm_fields = summarize_remote_confirmation_fields(summary)
    if confirm_fields:
        lines.append('')
        lines.append('### 这轮还适合继续确认的项')
        for item in confirm_fields:
            lines.append(f'- **{item}**：[待你确认]')
    visible_fields = [field for field in resolved_contract.get('fields') or [] if should_show_remote_contract_field(field)]
    if visible_fields:
        lines.append('')
        lines.append('### 这轮对象的可确认字段')
        for field in visible_fields[:8]:
            label = choose_remote_field_display_label(field)
            value = prefilled_remote_contract_value(field, args, prompt_bundle=prompt_bundle)
            if value is None:
                value = '[待你确认]'
            option_values = format_remote_option_values(field)
            if option_values:
                lines.append(f'- **{label}**：{value}  可选 `{option_values}`')
            else:
                lines.append(f'- **{label}**：{value}')
    lines.append('')
    if supported:
        lines.append('没问题的话直接回我“开跑” / “直接跑” / “确认执行”就行；如果你还想改参数，也可以继续说。')
    else:
        lines.append('这类对象当前我先帮你停在参数整理层；如果你想继续推进，我可以接着帮你把这张卡补完整。')
    return '\n'.join(lines)

def resolve_info_target(target: str) -> dict[str, Any]:
    raw = str(target or '').strip()
    if not raw:
        return {'ok': False, 'error': 'EMPTY_INFO_TARGET', 'message': 'Please provide a BizyAir app/workflow link or numeric id'}
    if raw.isdigit():
        return {'ok': True, 'input_kind': 'raw_id', 'input_value': raw, 'resolved_object_id': raw}
    normalized = raw
    if '://' not in normalized and normalized.startswith('bizyair.cn/'):
        normalized = f'https://{normalized}'
    parsed = urllib.parse.urlparse(normalized)
    if not parsed.scheme or not parsed.netloc:
        trailing_digits = re.search('(\\d+)(?:/)?$', raw)
        if trailing_digits:
            resolved = trailing_digits.group(1)
            return {'ok': True, 'input_kind': 'path_like_id', 'input_value': raw, 'resolved_object_id': resolved}
        return {'ok': False, 'error': 'UNSUPPORTED_INFO_TARGET', 'message': 'Unsupported info target format', 'input_value': raw}
    host = parsed.netloc.lower().split(':', 1)[0]
    if host not in BIZYAIR_INFO_HOSTS:
        return {'ok': False, 'error': 'UNSUPPORTED_INFO_HOST', 'message': 'Only bizyair.cn links are supported for --info-from-link', 'input_value': raw, 'host': host}
    segments = [seg for seg in (parsed.path or '').split('/') if seg]
    query = urllib.parse.parse_qs(parsed.query or '')
    query_id = (query.get('id') or [None])[0]
    if len(segments) >= 3 and segments[0] == 'community' and (segments[1] == 'app') and segments[2].isdigit():
        return {'ok': True, 'input_kind': 'app_link', 'input_value': raw, 'normalized_url': normalized, 'resolved_object_id': segments[2]}
    if segments and segments[0] == 'comfy-ui' and query_id and str(query_id).isdigit():
        return {'ok': True, 'input_kind': 'workflow_link', 'input_value': raw, 'normalized_url': normalized, 'resolved_object_id': str(query_id)}
    if query_id and str(query_id).isdigit():
        return {'ok': True, 'input_kind': 'bizyair_link_with_query_id', 'input_value': raw, 'normalized_url': normalized, 'resolved_object_id': str(query_id)}
    for segment in reversed(segments):
        if segment.isdigit():
            return {'ok': True, 'input_kind': 'bizyair_link_with_path_id', 'input_value': raw, 'normalized_url': normalized, 'resolved_object_id': segment}
    return {'ok': False, 'error': 'INFO_TARGET_ID_NOT_FOUND', 'message': 'Could not extract a BizyAir object id from the provided link', 'input_value': raw}

def build_remote_info_output(app_id: str, *, api_key_arg: str | None=None, include_workflow: bool=False) -> dict[str, Any]:
    api_key = api.require_api_key(api_key_arg)
    if not api_key:
        print(json.dumps({'error': 'NO_REMOTE_CREDENTIAL', 'message': 'Remote detail/info requires api key', 'supported_inputs': {'api_key': f'--api-key / BIZYAIR_API_KEY / {common.config_display_path()} -> credentials.api_key'}}, ensure_ascii=False), file=sys.stderr)
        sys.exit(1)
    detail_attempt = api.safe_request_json('GET', f'{BIZY_MODEL_DETAIL_URL}/{app_id}/detail', api_key)
    detail = api.unwrap_result_payload(detail_attempt) if detail_attempt.get('ok') else None
    fallback_model = None
    id_diagnosis = None
    webapp_detail_attempt = api.fetch_remote_webapp_detail(api_key, app_id)
    if not detail_attempt.get('ok'):
        fallback_model = api.find_remote_model_by_id(api_key, app_id, remote_source='community')
        if fallback_model is None:
            fallback_model = api.find_remote_model_by_id(api_key, app_id, remote_source='official')
        id_diagnosis = api.diagnose_remote_numeric_id(api_key, app_id)
    versions: list[dict[str, Any]] = []
    if isinstance(detail, dict):
        versions = api.extract_result_data(detail).get('versions', []) or []
    elif fallback_model:
        versions = fallback_model.get('versions', []) or []
    version_id = versions[0].get('id') if versions else None
    version_detail = api.fetch_remote_version_detail(api_key, version_id) if version_id is not None else None
    workflow = api.fetch_remote_workflow(api_key, version_id) if include_workflow and version_id is not None else None
    if include_workflow and (not api.extract_result_data(workflow)):
        workflow = api.fetch_remote_workflow_from_url(api.extract_result_data(webapp_detail_attempt).get('web_app_workflow_url'))
    execution_target = resolve_remote_execution_target(api_key, detail, webapp_detail_attempt, version_detail, fallback_model=fallback_model)
    resolved_contract = contract.resolve_remote_input_contract(execution_target=execution_target, webapp_detail=webapp_detail_attempt, workflow=workflow)
    summary = build_remote_info_summary(bizy_model_id=str(app_id), detail_result=detail, webapp_detail=webapp_detail_attempt, fallback_model=fallback_model, version_detail=version_detail, workflow=workflow, execution_target=execution_target, resolved_contract=resolved_contract)
    out: dict[str, Any] = {'source': 'remote', 'auth_mode': 'api_key_only', 'summary': summary, 'raw': {'detail': detail if detail_attempt.get('ok') else None, 'detail_error': None if detail_attempt.get('ok') else {'status': detail_attempt.get('status'), 'error': detail_attempt.get('error')}, 'id_diagnosis': id_diagnosis, 'webapp_detail': api.unwrap_result_payload(webapp_detail_attempt) if api.result_is_ok(webapp_detail_attempt) else None, 'webapp_detail_error': None if not isinstance(webapp_detail_attempt, dict) or webapp_detail_attempt.get('ok') else {'status': webapp_detail_attempt.get('status'), 'error': webapp_detail_attempt.get('error')}, 'fallback_model': fallback_model, 'version_detail': version_detail, 'execution_target': execution_target, 'resolved_contract': resolved_contract}}
    if include_workflow:
        out['raw']['resolved_workflow'] = workflow
    return out

def resolve_remote_prefill_target(target: str, *, api_key_arg: str | None=None) -> dict[str, Any]:
    resolved = resolve_info_target(target)
    if not resolved.get('ok'):
        return resolved
    if resolved.get('input_kind') == 'workflow_link':
        return {'ok': False, 'error': 'WORKFLOW_LINK_NOT_SUPPORTED', 'input_kind': 'workflow_link', 'input_value': resolved.get('input_value'), 'draft_id': resolved.get('resolved_object_id'), 'message': common.WORKFLOW_LINK_NOT_SUPPORTED_MESSAGE}
    api_key = api.resolve_api_key(api_key_arg)
    original_object_id = str(resolved['resolved_object_id'])
    final_object_id = original_object_id
    return {'ok': True, 'input_kind': resolved.get('input_kind'), 'input_value': resolved.get('input_value'), 'normalized_url': resolved.get('normalized_url'), 'original_object_id': original_object_id, 'resolved_object_id': final_object_id, 'draft_resolution': None}

def match_remote_field_override(field_name: str, args: argparse.Namespace) -> Any:
    low = str(field_name or '').strip().lower()
    if not low:
        return None
    seed = getattr(args, 'seed', None)
    random_seed = bool(getattr(args, 'random_seed', False))
    steps = getattr(args, 'steps', None)
    duration = getattr(args, 'duration', None)
    width = getattr(args, 'width', None)
    height = getattr(args, 'height', None)
    aspect_ratio = getattr(args, 'aspect_ratio', None)
    resolution = getattr(args, 'resolution', None)
    model_name = getattr(args, 'model_name', None)
    if seed is not None and contract.is_remote_logical_field('seed', low):
        return int(seed)
    if random_seed and contract.is_remote_logical_field('seed', low):
        return api.generate_seed()
    if steps is not None and contract.is_remote_logical_field('steps', low):
        return int(steps)
    if duration is not None and contract.is_remote_logical_field('duration', low):
        return int(duration)
    if width is not None and contract.is_remote_logical_field('width', low):
        return int(width)
    if height is not None and contract.is_remote_logical_field('height', low):
        return int(height)
    if aspect_ratio is not None and contract.is_remote_logical_field('aspect_ratio', low):
        return aspect_ratio
    if resolution is not None and contract.is_remote_logical_field('resolution', low):
        return resolution
    if model_name is not None and contract.is_remote_logical_field('model_name', low):
        return model_name
    return None

def collect_hidden_remote_media_slots(webapp_detail_data: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    result: dict[str, list[dict[str, Any]]] = {'image': [], 'audio': [], 'video': []}
    for node in webapp_detail_data.get('input_nodes', []) or []:
        media_type = contract.classify_remote_media_slot(node)
        if not media_type:
            continue
        if str(node.get('field_type') or '').lower() != 'hidden':
            continue
        if node.get('field_value') in (None, '', [], {}):
            continue
        result[media_type].append(node)
    return result

def collect_raw_param_override_keys(args: argparse.Namespace) -> set[str]:
    keys: set[str] = set()
    for item in getattr(args, 'param', None) or []:
        if '=' not in item:
            continue
        (key, _) = item.split('=', 1)
        normalized = str(key).strip().lower()
        if normalized:
            keys.add(normalized)
    return keys

def summarize_missing_remote_media(preflight: dict[str, Any], args: argparse.Namespace, uploaded_urls: list[str] | None=None, uploaded_audios: list[str] | None=None, uploaded_videos: list[str] | None=None) -> dict[str, Any]:
    execution_target = preflight.get('execution_target') or {}
    runtime_webapp_detail = execution_target.get('webapp_detail') or preflight.get('webapp_detail')
    webapp_detail_data = api.extract_result_data(runtime_webapp_detail)
    resolved_contract = preflight.get('resolved_contract') or {}
    hidden_slots = collect_hidden_remote_media_slots(webapp_detail_data) if webapp_detail_data else {'image': [], 'audio': [], 'video': []}
    contract_media_slots = (resolved_contract.get('bindings') or {}).get('media_slots') or {}
    override_keys = collect_raw_param_override_keys(args)
    generic_override_counts = {'image': int(any((k in override_keys for k in {'image', 'images'}))), 'audio': int(any((k in override_keys for k in {'audio', 'audios'}))), 'video': int(any((k in override_keys for k in {'video', 'videos'})))}
    provided_counts = {'image': len(uploaded_urls or []), 'audio': len(uploaded_audios or []), 'video': len(uploaded_videos or [])}
    missing: dict[str, Any] = {}
    for media_type in ['image', 'audio', 'video']:
        slots = list(hidden_slots.get(media_type, []) or [])
        contract_slots = list(contract_media_slots.get(media_type, []) or [])
        exact_override_count = 0
        for node in slots:
            variable_name = str(node.get('variable_name') or '').strip().lower()
            if variable_name and variable_name in override_keys:
                exact_override_count += 1
        total_provided = provided_counts.get(media_type, 0) + exact_override_count + generic_override_counts.get(media_type, 0)
        required_count = max(len(slots), len(contract_slots))
        if required_count > total_provided:
            missing[media_type] = {'required': required_count, 'provided': total_provided, 'missing': required_count - total_provided, 'variables': [str(node.get('variable_name') or '') for node in slots] or contract_slots}
    return missing
