"""卡片解析回流 + 参数状态判定。

合并路 A / 路 B 之后，card.py 不再渲染卡片（渲染由 remote.build_remote_prefilled_card
统一接管），只负责：
  - parse_card_text:           把用户填好的卡片字符串 → 字段 dict
  - compile_card_selection:    字段 dict → args.aspect_ratio / resolution 等
  - apply_compiled_selection:  把上面结果写回 argparse.Namespace
  - determine_parameter_state: 判断当前是 ready_to_run / awaiting_confirmation / missing_required
  - inherit_previous_run:      "跟刚才一样" 这种续跑场景，从 runtime_state 拷贝上轮参数
  - has_explicit_run_authorization / allows_explicit_defaults: 用户口令识别（"开跑" / "默认"）

被 dispatch.py 主流程和 batch.py 共用。
"""
from __future__ import annotations
import argparse, re

import dispatch_common
from dispatch_common import (
    COMPILER_RULES, INHERIT_MARKERS, RUN_AUTH_MARKERS, RUN_AUTH_NEGATION_MARKERS,
)


def build_prompt_bundle_for_model(model: str | None, args: argparse.Namespace) -> dict:
    cached = getattr(args, '_compiled_prompt_bundle', None)
    task_hint = 'text-to-video' if dispatch_common.is_video_model(model) else 'text-to-image'
    signature = (model, task_hint, str(getattr(args, 'prompt', None) or ''), len(getattr(args, 'image', None) or []), len(getattr(args, 'audio', None) or []))
    if isinstance(cached, dict) and cached.get('_signature') == signature:
        return cached
    raw = re.sub(r'\s+', ' ', str(getattr(args, 'prompt', None) or '').strip())
    bundle = {'raw_prompt': raw, 'card_display_prompt': raw, 'execution_prompt': raw, 'polished_prompt': raw, 'structured_prompt': raw, 'enriched_prompt': raw, 'rewritten_prompt': '', 'negative_prompt': '', 'changed': False, 'polish_notes': [], 'mode': None, 'mode_source': 'passthrough', 'style_profile': {'name': None, 'source': 'none', 'en_hint': None}, 'rewrite_applied': False}
    bundle['_signature'] = signature
    setattr(args, '_compiled_prompt_bundle', bundle)
    return bundle


def has_explicit_tuning(args: argparse.Namespace) -> bool:
    return any([bool(args.card_input), bool(args.aspect_ratio), bool(args.resolution), bool(args.steps), bool(args.duration), bool(args.seed), bool(args.random_seed), bool(args.model_name), bool(args.width), bool(args.height), bool(args.param)])

def collect_intent_text(args: argparse.Namespace) -> str:
    texts = [getattr(args, 'prompt', None), getattr(args, 'card_input', None)]
    return dispatch_common.normalized_text('\n'.join([str(x or '') for x in texts]))

def asks_to_inherit_previous(args: argparse.Namespace) -> bool:
    low = collect_intent_text(args)
    return any((x in low for x in INHERIT_MARKERS))

def allows_explicit_defaults(args: argparse.Namespace) -> bool:
    if args.run_with_defaults:
        return True
    low = collect_intent_text(args)
    markers = ['默认就行', '默认', '你定', '推荐就行', '都行', '随便', 'auto', 'default']
    return any((x in low for x in markers))

def has_explicit_run_authorization(args: argparse.Namespace) -> bool:
    if getattr(args, 'confirm_run', False) or args.run_with_defaults:
        return True
    low = collect_intent_text(args)
    if any((x in low for x in RUN_AUTH_NEGATION_MARKERS)):
        return False
    return any((x in low for x in RUN_AUTH_MARKERS))


def inherit_previous_run(args: argparse.Namespace, model: str | None) -> bool:
    if not model or not asks_to_inherit_previous(args):
        return False
    state = dispatch_common.load_runtime_state().get('last_run', {})
    previous = state.get(str(model))
    if not dispatch_common.runtime_state_entry_is_valid(previous):
        return False
    inherited_any = False
    prompt_low = dispatch_common.normalized_text(args.prompt or '')
    if previous.get('prompt') and (not args.prompt or any((marker in prompt_low for marker in INHERIT_MARKERS))):
        args.prompt = previous.get('prompt')
        inherited_any = True
    if not (args.image or []) and previous.get('image'):
        args.image = list(previous.get('image') or [])
        inherited_any = True
    if not (args.audio or []) and previous.get('audio'):
        args.audio = list(previous.get('audio') or [])
        inherited_any = True
    if not (args.video or []) and previous.get('video'):
        args.video = list(previous.get('video') or [])
        inherited_any = True
    if not args.aspect_ratio and previous.get('aspect_ratio'):
        args.aspect_ratio = previous.get('aspect_ratio')
        inherited_any = True
    if not args.resolution and previous.get('resolution'):
        args.resolution = previous.get('resolution')
        inherited_any = True
    if not args.duration and previous.get('duration') is not None:
        args.duration = previous.get('duration')
        inherited_any = True
    if not args.seed and previous.get('seed') is not None:
        args.seed = previous.get('seed')
        inherited_any = True
    if previous.get('random_seed') and (not args.seed) and (not args.random_seed):
        args.random_seed = True
        inherited_any = True
    if not args.model_name and previous.get('model_name'):
        args.model_name = previous.get('model_name')
        inherited_any = True
    if not args.width and previous.get('width') is not None:
        args.width = previous.get('width')
        inherited_any = True
    if not args.height and previous.get('height') is not None:
        args.height = previous.get('height')
        inherited_any = True
    if not (args.param or []) and previous.get('param'):
        args.param = list(previous.get('param') or [])
        inherited_any = True
    return inherited_any

def determine_parameter_state(args: argparse.Namespace, model: str | None) -> str:
    if not model:
        return 'user_supplied_enough'
    if model in {'remote-search-flow', 'remote-video-search-flow', 'modelzoo-search-flow', 'modelzoo-video-search-flow'}:
        return 'user_supplied_enough'
    run_authorized = has_explicit_run_authorization(args)
    if asks_to_inherit_previous(args):
        inherited = inherit_previous_run(args, model)
        if not inherited:
            return 'missing_required'
        return 'ready_to_run' if run_authorized else 'awaiting_confirmation'
    if allows_explicit_defaults(args):
        return 'ready_to_run' if run_authorized else 'awaiting_confirmation'
    if has_explicit_tuning(args):
        return 'ready_to_run' if run_authorized else 'awaiting_confirmation'
    if model in COMPILER_RULES:
        return 'missing_required'
    return 'ready_to_run' if run_authorized else 'awaiting_confirmation'

def normalize_field_name(name: str) -> str:
    cleaned = re.sub('[^\\w\\u4e00-\\u9fff]+', '', str(name or ''))
    return cleaned.strip()

def parse_card_text(card_text: str) -> dict[str, str]:
    parsed = {}
    current_key = None
    for raw_line in (card_text or '').splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if '：' in line:
            (key, value) = line.split('：', 1)
        elif ':' in line:
            (key, value) = line.split(':', 1)
        else:
            if current_key and line and (not line.startswith(('1.', '2.', '3.', '4.', '5.', '6.', '7.'))):
                parsed[current_key] = (parsed.get(current_key, '') + '\n' + line).strip()
            continue
        key = normalize_field_name(key)
        value = value.strip()
        parsed[key] = value
        current_key = key
    return parsed

def is_defaultish(value: str | None) -> bool:
    low = dispatch_common.normalized_text(value)
    return low in {'', '默认', '你定', '推荐就行', '都行', '随便', 'auto', 'default'}

def coerce_size_to_width_height(value: str) -> tuple[int, int] | None:
    if 'x' in value.lower():
        (left, right) = value.lower().split('x', 1)
        if left.strip().isdigit() and right.strip().isdigit():
            return (int(left.strip()), int(right.strip()))
    return None

def compile_card_selection(model: str, card_text: str) -> dict:
    """把用户填好的卡片文本解析成结构化参数。

    三段式逻辑（顺序很重要，别乱动）：
      1) 用户在卡片字段里明确填的值       —— 最高优先级
      2) "其他补充" 里的自然语言推断       —— 仅对用户没填的字段生效
      3) COMPILER_RULES.defaults 兜底     —— 仅在前两步都没设的字段上生效

    曾经 defaults 是在最前面灌的，导致用户在"其他补充"里写"横版高清"时
    aspect_ratio 已经被 default 填成了 1:1，notes 推断条件
    `not compiled.get('aspect_ratio')` 永远是 False，自然语言推断完全不工作。
    所以 reorder 之后这个顺序必须保持。

    seed 的特殊 guard：如果用户/notes 已经选了"随机"（random_seed=True），
    最后一步不要再用 defaults 里的固定 seed 把意图压回去。
    """
    rule = COMPILER_RULES.get(model, {})
    parsed = parse_card_text(card_text)
    compiled = {'prompt': parsed.get('提示词', ''), 'images': [], 'audios': [], 'aspect_ratio': None, 'resolution': None, 'duration': None, 'seed': None, 'random_seed': False, 'model_name': None, 'width': None, 'height': None, 'params': [], 'notes': parsed.get('其他补充', '')}

    # 卡片字段名的中英别名表。用户回 "图片比例：3:2" / "aspect_ratio: 3:2" / "画面比例：3:2" 都识别。
    keys_to_map = {
        'aspect_ratio': ['aspect_ratio', '比例', '视频比例', '画面比例', '图片比例'],
        'resolution': ['resolution', '规格', '清晰度', '图片质量', '图片规格', '画面规格', '视频尺寸', '图片尺寸'],
        'duration': ['duration', '时长', '视频时长'],
        'model_name': ['model_name', '模型档位'],
        'seed': ['seed', '随机性', '固定seed'],
        'width': ['width', '宽度'],
        'height': ['height', '高度'],
    }

    # 1) 先解析用户在卡片字段里填的值（最高优先级）
    for target, aliases in keys_to_map.items():
        for alias in aliases:
            val = parsed.get(normalize_field_name(alias))
            if val and not is_defaultish(val):
                if target == 'seed':
                    if '随机' in str(val) or str(val).lower() == 'random':
                        compiled['random_seed'] = True
                        compiled['seed'] = None
                    elif str(val).isdigit():
                        compiled['seed'] = int(val)
                elif target == 'resolution' and 'x' in str(val).lower():
                    wh = coerce_size_to_width_height(str(val))
                    if wh:
                        (compiled['width'], compiled['height']) = wh
                    else:
                        compiled[target] = val
                else:
                    compiled[target] = val
                break

    # 2) 再看"其他补充"里的自然语言推断（仅对用户没填的字段生效）
    notes = dispatch_common.normalized_text(compiled.get('notes') or '')
    if notes:
        if '横' in notes and (not compiled.get('aspect_ratio')) and (not compiled.get('width')):
            compiled['aspect_ratio'] = '16:9'
        if '竖' in notes and (not compiled.get('aspect_ratio')) and (not compiled.get('width')):
            compiled['aspect_ratio'] = '9:16'
        if ('方' in notes or '1:1' in notes) and (not compiled.get('aspect_ratio')) and (not compiled.get('width')):
            compiled['aspect_ratio'] = '1:1'
        if compiled.get('duration') is None:
            if '10秒' in notes or '10 秒' in notes:
                compiled['duration'] = 10
            elif '8秒' in notes or '8 秒' in notes:
                compiled['duration'] = 8
            elif '5秒' in notes or '5 秒' in notes:
                compiled['duration'] = 5
            elif '3秒' in notes or '3 秒' in notes:
                compiled['duration'] = 3
        if '随机' in notes and compiled.get('seed') is None and (not compiled.get('random_seed')):
            compiled['random_seed'] = True
        if '高清' in notes or 'high' in notes or 'large' in notes:
            for (idx, item) in enumerate(list(compiled['params'])):
                if item.startswith('60:BizyAir_Sora_V2_T2V_API.size='):
                    compiled['params'][idx] = '60:BizyAir_Sora_V2_T2V_API.size=large'
            if model == 'nano-banana-pro-text' and (not compiled.get('resolution')):
                compiled['resolution'] = '2K'

    # 3) 最后用 COMPILER_RULES.defaults 填空缺：仅在用户没填、notes 也没推断的字段上生效
    for (key, value) in (rule.get('defaults') or {}).items():
        if key == 'params':
            existing_param_keys = {p.split('=', 1)[0] for p in compiled['params'] if '=' in p}
            for (p_key, p_val) in value.items():
                if p_key not in existing_param_keys:
                    compiled['params'].append(f'{p_key}={p_val}')
        elif key == 'seed' and compiled.get('random_seed'):
            # 用户或推断已选随机 → 不要再灌固定 seed 默认值把意图压回去
            continue
        elif compiled.get(key) is None:
            compiled[key] = value

    return compiled

def apply_compiled_selection(args: argparse.Namespace, target: str) -> None:
    if not getattr(args, 'card_input', None):
        return
    compiled = compile_card_selection(target, args.card_input)
    if compiled.get('prompt') and (not args.prompt):
        args.prompt = compiled['prompt']
    if compiled.get('aspect_ratio') and (not args.aspect_ratio):
        args.aspect_ratio = str(compiled['aspect_ratio'])
    if compiled.get('resolution') and (not args.resolution):
        args.resolution = str(compiled['resolution'])
    if compiled.get('duration') and (not args.duration):
        args.duration = int(compiled['duration'])
    if compiled.get('seed') and (not args.seed):
        args.seed = int(compiled['seed'])
    if compiled.get('random_seed'):
        args.random_seed = True
    if compiled.get('model_name') and (not args.model_name):
        args.model_name = str(compiled['model_name'])
    if compiled.get('width') and (not args.width):
        args.width = int(compiled['width'])
    if compiled.get('height') and (not args.height):
        args.height = int(compiled['height'])
    if compiled.get('params'):
        args.param = (args.param or []) + list(compiled['params'])
