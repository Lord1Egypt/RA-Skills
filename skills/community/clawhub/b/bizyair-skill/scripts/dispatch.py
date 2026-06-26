"""dispatch.py — 10 个固定模型（图片 5 + 视频 5）+ 4 类搜索路由（图片/视频 × ModelZoo/AI 应用）的入口 + 批量入口。

主流程按顺序判断（main() 自上而下）：
  --image-menu / --video-menu        本地直接打印菜单文案
  --clear-runtime-state              清续跑缓存
  --batch-worker-file <file>         作为 batch worker 子进程启动（被 batch.py 调起）
  --batch-json + --batch-prefill/run 批量入口，转 batch.handle_batch_*
  --check / --wallet / --browse / --search / --info  各自 shell 出去 app.py
  --param-help / --prefill-card      渲染预填卡（ROUTE_TABLE 模型走 ModelZoo）
  --model X (默认)                   resolve → 固定模型走 ModelZoo 直接执行

固定模型（ROUTE_TABLE 中的 10 个）全部走 ModelZoo 标准 API 执行，不再 shell 到 app.py。
非固定模型（AI 应用搜索结果等）仍走 app.py 的 webapp 路径。
搜索路由（modelzoo-search-flow / -video / remote-search-flow / -video）走 cli.py 的 pick-* 命令。

【⚠️ args.scene 的处理顺序】
args.scene 在 L155-156 被解析（scene -> model）。这一步必须在 batch path 之前
还是之后？现在的设计是：
  - 单任务路径在 L155 解析
  - 批量路径走 batch.build_task_args，里面 fall-back 到 base_args.scene（已修过一次）
之前 batch path 不读 base_args.scene 导致 `--scene 5 --batch-prefill` 静默落到默认。
"""
from __future__ import annotations
import argparse, json, sys
from paths import resolve_runtime_state_file

import card
import batch
import dispatch_common
from dispatch_common import (
    APP_SCRIPT, COMPILER_RULES, MODEL_MAP, ROUTE_TABLE, SCENE_NUMBER_MAP,
)

def _append_user_args(cmd: list[str], args, *, skip_prompt: bool = False) -> None:
    """把 args 里的所有用户参数 (image/audio/video/aspect_ratio/...) 转成 ['--flag', value] 片段。
    在 prefill / run 两条 shell 路径上都会用，避免每次手写一遍。
    """
    if not skip_prompt and getattr(args, 'prompt', None):
        cmd += ['--prompt', args.prompt]
    for image in args.image or []:
        cmd += ['--image', image]
    for audio in args.audio or []:
        cmd += ['--audio', audio]
    for video in args.video or []:
        cmd += ['--video', video]
    if args.aspect_ratio:
        cmd += ['--aspect-ratio', args.aspect_ratio]
    if args.resolution:
        cmd += ['--resolution', args.resolution]
    if args.steps:
        cmd += ['--steps', str(args.steps)]
    if args.duration:
        cmd += ['--duration', str(args.duration)]
    if args.seed:
        cmd += ['--seed', str(args.seed)]
    if args.random_seed:
        cmd += ['--random-seed']
    if args.model_name:
        cmd += ['--model-name', args.model_name]
    if args.width:
        cmd += ['--width', str(args.width)]
    if args.height:
        cmd += ['--height', str(args.height)]
    for param in args.param or []:
        cmd += ['--param', param]
    if args.output:
        cmd += ['--output', args.output]
    if args.sync:
        cmd += ['--sync']

def _collect_modelzoo_params(slug: str, args) -> dict[str, str]:
    """把 dispatch.py 的 args 参数收集成 ModelZoo 的 user_params dict。

    收集顺序（低优先级先写入，高优先级覆盖）：
    1. COMPILER_RULES defaults 兜底
    2. args 标准参数名（prompt/aspect_ratio/resolution/...）
    3. args.param 的 key=value 原样传（最高优先级）
    """
    params: dict[str, str] = {}
    # 1) defaults 兜底
    defaults = COMPILER_RULES.get(slug, {}).get('defaults', {})
    for k, v in defaults.items():
        params[k] = str(v) if not isinstance(v, str) else v
    # 2) args 标准参数
    prompt_bundle = card.build_prompt_bundle_for_model(slug, args)
    execution_prompt = prompt_bundle.get('execution_prompt', '') or (args.prompt or '')
    if execution_prompt:
        params['prompt'] = execution_prompt
    if args.aspect_ratio:
        params['aspect_ratio'] = args.aspect_ratio
    if args.resolution:
        params['resolution'] = args.resolution
    if args.duration:
        params['duration'] = str(args.duration)
    if args.seed:
        params['seed'] = str(args.seed)
    elif args.random_seed:
        params['seed'] = '-1'
    if args.model_name:
        params['model_name'] = args.model_name
    if args.width:
        params['width'] = str(args.width)
    if args.height:
        params['height'] = str(args.height)
    # 3) --param key=value 最高优先
    for kv in (args.param or []):
        if '=' in kv:
            k, v = kv.split('=', 1)
            params[k] = v
    return params


def _modelzoo_execute(slug: str, args) -> None:
    """通过 ModelZoo 执行固定模型任务（替代 app.py --run）。"""
    import modelzoo
    import api as _api

    endpoint = ROUTE_TABLE[slug]['endpoint']
    key = _api.require_api_key(args.api_key)

    # 上传媒体文件
    media_overrides: dict[str, list[str]] = {}
    if args.image:
        media_overrides['images'] = [_api.upload_input_file(key, p) for p in args.image]
    if args.audio:
        media_overrides['audios'] = [_api.upload_input_file(key, p) for p in args.audio]
    if args.video:
        media_overrides['videos'] = [_api.upload_input_file(key, p) for p in args.video]

    # 收集用户参数
    user_params = _collect_modelzoo_params(slug, args)

    # 拿 detail 构建 payload
    detail_result = modelzoo.get_detail(key, endpoint)
    detail_data = (detail_result.get('data') or {}).get('data') or detail_result.get('data') or {}
    payload = modelzoo.build_task_payload(detail_data, user_params, media_overrides=media_overrides)

    print(json.dumps({'action': 'modelzoo_submit', 'endpoint': endpoint, 'payload_preview': {k: (v if len(str(v)) < 100 else str(v)[:100] + '...') for k, v in payload.items()}}, ensure_ascii=False), file=sys.stderr)

    # 创建任务
    create_result = modelzoo.create_task(key, endpoint, payload)
    create_data = (create_result.get('data') or {}).get('data') or create_result.get('data') or {}
    request_id = create_data.get('request_id')
    if not request_id:
        print(json.dumps({'error': 'MODELZOO_CREATE_FAILED', 'message': f'Failed to create ModelZoo task for {endpoint}', 'detail': create_result}, ensure_ascii=False), file=sys.stderr)
        sys.exit(1)

    print(f'REQUEST_ID:{request_id}', file=sys.stderr)

    # 轮询
    final = modelzoo.poll_until_done(key, request_id)
    outputs = final.get('outputs') or {}
    status = final.get('status')

    if status == 'Success':
        # 汇总输出
        result_items: list[dict[str, str]] = []
        for media_type in ('texts', 'images', 'videos', 'audios'):
            for url in (outputs.get(media_type) or []):
                result_items.append({'type': media_type, 'url': url})
        model_name = dispatch_common.display_model_name(slug)
        summary = f'{model_name} 已完成！'
        if result_items:
            summary += f' 共 {len(result_items)} 个输出。'
        print(json.dumps({
            'status': 'ok',
            'summary': summary,
            'verdict': '\n'.join(f"[{item['type']}] {item['url']}" for item in result_items),
            'outputs': result_items,
            'request_id': request_id,
        }, ensure_ascii=False, indent=2))
    else:
        message = final.get('message') or 'Unknown error'
        print(json.dumps({
            'error': 'TASK_FAILED',
            'message': message,
            'status': status,
            'request_id': request_id,
        }, ensure_ascii=False), file=sys.stderr)
        sys.exit(1)


def _modelzoo_prefill(slug: str, args) -> None:
    """用 ModelZoo detail 的 input_params 渲染预填确认卡。"""
    import modelzoo
    import api as _api

    endpoint = ROUTE_TABLE[slug]['endpoint']
    key = _api.require_api_key(args.api_key)
    detail_result = modelzoo.get_detail(key, endpoint)
    detail_data = (detail_result.get('data') or {}).get('data') or detail_result.get('data') or {}
    input_params = detail_data.get('input_params') or []

    # 收集用户已提供的参数 + defaults
    user_params = _collect_modelzoo_params(slug, args)

    # 渲染卡片
    model_name = dispatch_common.display_model_name(slug)
    lines = [f'## {model_name} 参数确认', '']

    for param in input_params:
        field_name = param.get('field_name')
        field_label = param.get('field_label') or field_name
        field_type = (param.get('field_type') or '').lower()
        default_value = param.get('field_value')
        options = param.get('field_options') or {}

        if not field_name:
            continue

        # 用户值 > default
        current = user_params.get(field_name, default_value)

        if field_type == 'customtext':
            display = str(current or '') if current else '（请输入）'
            if len(display) > 80:
                display = display[:80] + '...'
            lines.append(f'**{field_label}**：{display}')
        elif field_type == 'combo':
            values = options.get('values') or []
            values_str = ' / '.join(str(v) for v in values[:8])
            if len(values) > 8:
                values_str += ' / ...'
            lines.append(f'**{field_label}**：{current or "默认"} （可选：{values_str}）')
        elif field_type in ('number', 'slider', 'slides'):
            lines.append(f'**{field_label}**：{current or default_value or "默认"}')
        elif field_type == 'seed':
            lines.append(f'**{field_label}**：{current or "-1（随机）"}')
        elif field_type == 'boolean':
            lines.append(f'**{field_label}**：{current if current is not None else default_value}')
        else:
            lines.append(f'**{field_label}**：{current or default_value or ""}')

    lines.append('')
    lines.append('确认参数后，加上 `--confirm-run` 即可开始执行。')

    print('\n'.join(lines))


def main():
    p = argparse.ArgumentParser(description='BizyAir task wrapper for common entries and remote discovery')
    p.add_argument('--api-key')
    p.add_argument('--check', action='store_true')
    p.add_argument('--wallet', action='store_true')
    p.add_argument('--browse', action='store_true')
    p.add_argument('--search')
    p.add_argument('--modality')
    p.add_argument('--stability')
    p.add_argument('--info')
    p.add_argument('--task')
    p.add_argument('--model')
    p.add_argument('--scene')
    p.add_argument('--image-menu', action='store_true')
    p.add_argument('--video-menu', action='store_true')
    p.add_argument('--clear-runtime-state', action='store_true', help='Clear the local follow-up runtime_state cache')
    p.add_argument('--prompt')
    p.add_argument('--param-help', action='store_true')
    p.add_argument('--prefill-card', action='store_true')
    p.add_argument('--batch-json')
    p.add_argument('--batch-prefill', action='store_true')
    p.add_argument('--batch-run', action='store_true')
    p.add_argument('--batch-concurrency', type=int)
    p.add_argument('--batch-concurrency-approved', action='store_true')
    p.add_argument('--batch-task-count-approved', action='store_true')
    p.add_argument('--batch-worker-file', help=argparse.SUPPRESS)
    p.add_argument('--card-input')
    p.add_argument('--run-with-defaults', action='store_true')
    p.add_argument('--confirm-run', action='store_true')
    p.add_argument('--image', action='append')
    p.add_argument('--audio', action='append')
    p.add_argument('--video', action='append')
    p.add_argument('--aspect-ratio')
    p.add_argument('--resolution')
    p.add_argument('--steps')
    p.add_argument('--duration')
    p.add_argument('--seed')
    p.add_argument('--random-seed', action='store_true')
    p.add_argument('--model-name')
    p.add_argument('--width')
    p.add_argument('--height')
    p.add_argument('--param', action='append')
    p.add_argument('-o', '--output')
    p.add_argument('--sync', action='store_true')
    args = p.parse_args()
    if args.image_menu:
        print(dispatch_common.build_image_menu_message(args.prompt, args.image or []), end='')
        return
    if args.video_menu:
        print(dispatch_common.build_video_menu_message(args.prompt, args.image or [], args.audio or []), end='')
        return
    if args.clear_runtime_state:
        cleared = dispatch_common.clear_runtime_state()
        print(json.dumps({'status': 'cleared' if cleared else 'already_empty', 'path': str(resolve_runtime_state_file().resolve())}, ensure_ascii=False, indent=2))
        return
    if args.batch_worker_file:
        batch.handle_batch_worker(args.batch_worker_file)
        return
    if args.batch_json:
        if args.batch_prefill == args.batch_run:
            print(json.dumps({'error': 'INVALID_BATCH_MODE', 'message': 'Use exactly one of --batch-prefill or --batch-run with --batch-json'}, ensure_ascii=False, indent=2), file=sys.stderr)
            sys.exit(2)
        if args.prefill_card or args.param_help or args.confirm_run or args.card_input:
            print(json.dumps({'error': 'INVALID_BATCH_FLAG_COMBINATION', 'message': 'Batch mode cannot be mixed with single-task flags like --prefill-card / --param-help / --confirm-run / --card-input'}, ensure_ascii=False, indent=2), file=sys.stderr)
            sys.exit(2)
        if args.batch_prefill:
            batch.handle_batch_prefill(args)
            return
        batch.handle_batch_run(args)
        return
    if args.batch_prefill or args.batch_run:
        print(json.dumps({'error': 'MISSING_BATCH_JSON', 'message': 'Use --batch-json together with --batch-prefill or --batch-run'}, ensure_ascii=False, indent=2), file=sys.stderr)
        sys.exit(2)
    if args.prefill_card and args.confirm_run:
        print(json.dumps({'error': 'INVALID_FLAG_COMBINATION', 'message': 'Single-task mode cannot combine --prefill-card and --confirm-run. Show the card first, then run in a separate command after confirmation.'}, ensure_ascii=False, indent=2), file=sys.stderr)
        sys.exit(2)
    base_cmd = [sys.executable, str(APP_SCRIPT)]
    if args.api_key:
        base_cmd += ['--api-key', args.api_key]
    if args.check:
        dispatch_common.run_subprocess(base_cmd + ['--check'])
        return
    if args.wallet:
        dispatch_common.run_subprocess(base_cmd + ['--wallet'])
        return
    if args.browse:
        cmd = list(base_cmd) + ['--browse', '--remote']
        if args.modality:
            cmd += ['--modality', args.modality]
        if args.stability:
            cmd += ['--stability', args.stability]
        dispatch_common.run_subprocess(cmd)
        return
    if args.search:
        dispatch_common.run_subprocess(base_cmd + ['--search', args.search, '--remote'])
        return
    if args.info:
        target = SCENE_NUMBER_MAP.get(args.info, args.info)
        target = MODEL_MAP.get(target, MODEL_MAP.get(str(target).lower(), target))
        if target in ROUTE_TABLE:
            # 固定模型：用 modelzoo detail 直接输出，不走 app.py --info
            import modelzoo
            import api as _api
            endpoint = ROUTE_TABLE[target]['endpoint']
            detail = modelzoo.get_detail(_api.require_api_key(args.api_key), endpoint)
            print(json.dumps(detail, ensure_ascii=False, indent=2))
            return
        # 非固定模型：shell 到 app.py --info
        dispatch_common.run_subprocess(base_cmd + ['--info', target, '--remote'])
        return
    model = args.model
    if args.scene:
        model = SCENE_NUMBER_MAP.get(args.scene, args.scene)
    if args.param_help or args.prefill_card:
        target = dispatch_common.resolve_model(args.task, model)
        if target in ROUTE_TABLE:
            # 固定模型：用 ModelZoo 渲染预填卡
            _modelzoo_prefill(target, args)
        else:
            prefill_cmd = list(base_cmd) + ['--prefill-card', target]
            _append_user_args(prefill_cmd, args)
            dispatch_common.run_subprocess(prefill_cmd)
        return
    target_for_card = dispatch_common.resolve_model(args.task, model) if args.card_input or model else None
    if args.card_input and target_for_card:
        card.apply_compiled_selection(args, target_for_card)
    if model == 'remote-search-flow':
        dispatch_common.ensure_api_key_ready(args.api_key)
        query = args.prompt or args.search or args.task or '通用出图'
        dispatch_common.run_subprocess(base_cmd + ['--pick-image-candidates', query, '--remote', '--remote-source', 'community', '--reply-format', 'json'])
        return
    if model == 'remote-video-search-flow':
        dispatch_common.ensure_api_key_ready(args.api_key)
        query = args.prompt or args.search or args.task or '文生视频'
        dispatch_common.run_subprocess(base_cmd + ['--pick-video-candidates', query, '--remote', '--remote-source', 'community', '--reply-format', 'json'])
        return
    if model == 'modelzoo-search-flow':
        dispatch_common.ensure_api_key_ready(args.api_key)
        query = args.prompt or args.search or args.task or '通用图片'
        cli_script = dispatch_common.SCRIPT_DIR / 'cli.py'
        cmd = [sys.executable, str(cli_script), 'pick-modelzoo-image', query, '--reply-format', 'json']
        if args.api_key:
            cmd += ['--api-key', args.api_key]
        dispatch_common.run_subprocess(cmd)
        return
    if model == 'modelzoo-video-search-flow':
        dispatch_common.ensure_api_key_ready(args.api_key)
        query = args.prompt or args.search or args.task or '文生视频'
        cli_script = dispatch_common.SCRIPT_DIR / 'cli.py'
        cmd = [sys.executable, str(cli_script), 'pick-modelzoo-video', query, '--reply-format', 'json']
        if args.api_key:
            cmd += ['--api-key', args.api_key]
        dispatch_common.run_subprocess(cmd)
        return
    app_id = dispatch_common.resolve_model(args.task, model)
    parameter_state = card.determine_parameter_state(args, app_id)
    if parameter_state in ('missing_required', 'awaiting_confirmation'):
        if app_id in ROUTE_TABLE:
            _modelzoo_prefill(app_id, args)
        else:
            prefill_cmd = list(base_cmd) + ['--prefill-card', app_id]
            _append_user_args(prefill_cmd, args)
            dispatch_common.run_subprocess(prefill_cmd)
        return
    dispatch_common.ensure_api_key_ready(args.api_key)
    print(dispatch_common.build_run_dispatch_message(app_id))

    if app_id in ROUTE_TABLE:
        # 固定模型：走 ModelZoo 直接执行
        prompt_bundle = card.build_prompt_bundle_for_model(app_id, args)
        execution_prompt = prompt_bundle.get('execution_prompt', '') or (args.prompt or '')
        state_entry = dispatch_common.build_runtime_state_entry(str(app_id), args, execution_prompt)
        _modelzoo_execute(app_id, args)
        # 成功后持久化 runtime state
        state = dispatch_common.load_runtime_state()
        state.setdefault('last_run', {})[str(app_id)] = state_entry
        dispatch_common.save_runtime_state(state)
        return

    # 非固定模型：旧 webapp 路径（AI 应用搜索结果等）
    cmd = list(base_cmd) + ['--run', app_id]
    prompt_bundle = card.build_prompt_bundle_for_model(app_id, args)
    execution_prompt = prompt_bundle.get('execution_prompt', '') or (args.prompt or '')
    if execution_prompt:
        cmd += ['--prompt', execution_prompt]
    _append_user_args(cmd, args, skip_prompt=True)
    state_entry = dispatch_common.build_runtime_state_entry(str(app_id), args, execution_prompt)

    def persist_runtime_state() -> None:
        state = dispatch_common.load_runtime_state()
        state.setdefault('last_run', {})[str(app_id)] = state_entry
        dispatch_common.save_runtime_state(state)
    dispatch_common.run_subprocess(cmd, success_callback=persist_runtime_state)


if __name__ == '__main__':
    main()
