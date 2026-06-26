"""批量参数卡 / 批量执行的处理。

两个主入口：
  - handle_batch_prefill: --batch-prefill。串联多个任务的预填卡，**走路 B 渲染**
                          （remote.build_remote_info_output → build_remote_prefilled_card）。
                          per-batch 缓存：同一 model id 在一批里只 fetch 一次 contract。
  - handle_batch_run:     --batch-run。把每个任务写成独立子进程
                          （`python3 dispatch.py --model X --confirm-run ...`），
                          异步起一个 worker 调度它们，主进程立刻返回 status JSON。
                          worker 本身也是一个 dispatch.py 子进程
                          （`python3 dispatch.py --batch-worker-file <file>`）。

【⚠️ subprocess 入口都是 dispatch.py，不是 batch.py 自身】
build_batch_child_command 和 handle_batch_run 里启动 worker 的地方，都用
dispatch_common.DISPATCH_SCRIPT 而不是 Path(__file__)。原因：batch.py 没有 main()，
之前曾误用 __file__ 导致整个 --batch-run 静默退出（进程起来 0 秒就死）。

并发 / 任务数都受 config.json 的 batch.max_concurrency / max_tasks + 系统硬上限双重限制
（见 resolve_batch_policy 和 enforce_batch_task_limits）。
"""
from __future__ import annotations
import argparse, json, os, subprocess, sys, time, traceback
from pathlib import Path
from paths import resolve_batch_runs_dir
from typing import Any

import card
import dispatch_common
import remote
from dispatch_common import (
    COMPILER_RULES, CONFIGURED_MAX_BATCH_CONCURRENCY_FALLBACK,
    CONFIGURED_MAX_BATCH_TASKS_FALLBACK, ROUTE_TABLE,
    RUNTIME_STATE_DISABLED_ENV, SCENE_NUMBER_MAP,
    SYSTEM_MAX_BATCH_CONCURRENCY, SYSTEM_MAX_BATCH_TASKS,
)

# 搜索路由（菜单 6 / 7 / v6 / v7）是交互式 picker，不是可执行模型。batch 不允许跑这类 slug。
SEARCH_FLOW_SLUGS = {
    'remote-search-flow', 'remote-video-search-flow',
    'modelzoo-search-flow', 'modelzoo-video-search-flow',
}


def reject_search_flow_target(target: str, *, task_index: int, phase: str) -> None:
    """批量任务里如果出现搜索路由 slug（用户写 scene: 6 / 7 会触发），直接返回友好错误。"""
    if target not in SEARCH_FLOW_SLUGS:
        return
    print(json.dumps({
        'error': 'BATCH_SEARCH_FLOW_NOT_SUPPORTED',
        'message': (
            f'批量任务里第 {task_index} 个解析出来的是搜索入口（菜单 6 / 7），不是可执行模型。'
            '搜索入口属于交互式查找，无法直接 batch。'
            '请先单独跑搜索拿到具体的模型 slug 或 ModelZoo endpoint，再放进 batch。'
        ),
        'slug': target,
        'task_index': task_index,
        'phase': phase,
    }, ensure_ascii=False, indent=2), file=sys.stderr)
    sys.exit(2)

def resolve_batch_policy() -> dict:
    config = dispatch_common.load_skill_config()
    batch_cfg = config.get('batch') if isinstance(config.get('batch'), dict) else {}
    configured_max_concurrency = batch_cfg.get('max_concurrency', CONFIGURED_MAX_BATCH_CONCURRENCY_FALLBACK)
    configured_max_tasks = batch_cfg.get('max_tasks', CONFIGURED_MAX_BATCH_TASKS_FALLBACK)
    try:
        configured_max_concurrency = int(configured_max_concurrency)
    except Exception:
        configured_max_concurrency = CONFIGURED_MAX_BATCH_CONCURRENCY_FALLBACK
    try:
        configured_max_tasks = int(configured_max_tasks)
    except Exception:
        configured_max_tasks = CONFIGURED_MAX_BATCH_TASKS_FALLBACK
    if configured_max_concurrency < 1:
        configured_max_concurrency = CONFIGURED_MAX_BATCH_CONCURRENCY_FALLBACK
    if configured_max_tasks < 1:
        configured_max_tasks = CONFIGURED_MAX_BATCH_TASKS_FALLBACK
    configured_max_concurrency = min(configured_max_concurrency, SYSTEM_MAX_BATCH_CONCURRENCY)
    configured_max_tasks = min(configured_max_tasks, SYSTEM_MAX_BATCH_TASKS)
    return {'max_concurrency': configured_max_concurrency, 'system_max_concurrency': SYSTEM_MAX_BATCH_CONCURRENCY, 'max_tasks': configured_max_tasks, 'system_max_tasks': SYSTEM_MAX_BATCH_TASKS}

def build_cli_arg_list(flag: str, values: list[str] | None) -> list[str]:
    output: list[str] = []
    for value in values or []:
        output += [flag, str(value)]
    return output

def listify_task_value(value) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(item) for item in value if str(item or '').strip()]
    text = str(value).strip()
    return [text] if text else []

def task_label(task: dict, index: int) -> str:
    label = str(task.get('label') or task.get('title') or '').strip()
    return label if label else f'任务 {index}'

def parse_batch_payload(raw: str) -> tuple[list[dict], int | None]:
    parsed = json.loads(raw)
    concurrency = None
    tasks = parsed
    if isinstance(parsed, dict):
        tasks = parsed.get('tasks')
        concurrency = parsed.get('concurrency')
    if not isinstance(tasks, list) or not tasks:
        raise ValueError('batch_json must be a non-empty JSON array or an object with a tasks array')
    normalized: list[dict] = []
    for (index, item) in enumerate(tasks, start=1):
        if isinstance(item, str):
            normalized.append({'prompt': item})
            continue
        if isinstance(item, dict):
            normalized.append(dict(item))
            continue
        raise ValueError(f'batch task #{index} must be an object or string')
    return (normalized, concurrency)

def build_task_args(base_args: argparse.Namespace, task: dict) -> argparse.Namespace:
    prompt = task.get('prompt')
    card_input = task.get('card_input')
    task_args = argparse.Namespace(api_key=base_args.api_key, check=False, wallet=False, browse=False, search=None, modality=None, stability=None, info=None, task=task.get('task') or getattr(base_args, 'task', None), model=task.get('model') or base_args.model, scene=task.get('scene') or getattr(base_args, 'scene', None), image_menu=False, video_menu=False, prompt='' if prompt is None else str(prompt), param_help=bool(task.get('param_help', False)), prefill_card=False, card_input='' if card_input is None else str(card_input), run_with_defaults=bool(task.get('run_with_defaults', getattr(base_args, 'run_with_defaults', False))), confirm_run=bool(task.get('confirm_run', False)), image=listify_task_value(task.get('image')), audio=listify_task_value(task.get('audio')), video=listify_task_value(task.get('video')), aspect_ratio=task.get('aspect_ratio'), resolution=task.get('resolution'), steps=task.get('steps'), duration=task.get('duration'), seed=task.get('seed'), random_seed=bool(task.get('random_seed', False)), model_name=task.get('model_name'), width=task.get('width'), height=task.get('height'), param=listify_task_value(task.get('param')), output=task.get('output'), sync=bool(task.get('sync', getattr(base_args, 'sync', False))), batch_json=None, batch_prefill=False, batch_run=False, batch_concurrency=None, batch_concurrency_approved=False, batch_task_count_approved=False, batch_worker_file=None)
    return task_args

def should_batch_use_defaults(task_args: argparse.Namespace, model: str | None) -> bool:
    if task_args.run_with_defaults or card.allows_explicit_defaults(task_args):
        return True
    if model in COMPILER_RULES and (not card.has_explicit_tuning(task_args)):
        return True
    return False

def build_batch_prefill_reply(tasks: list[dict]) -> str:
    lines = ['我先把这批任务的参数确认卡分开整理好了：', '']
    for item in tasks:
        lines.append(f"### {item['label']}")
        lines.append(item['card_markdown'].strip())
        lines.append('')
    lines.append('你可以逐条改，也可以直接说“全部开跑”，我再一起提交。')
    return '\n'.join(lines).strip()

def build_batch_run_reply(tasks: list[dict]) -> str:
    lines = ['这批任务我已经按独立任务分别提交了：', '']
    for item in tasks:
        lines.append(f"- **{item['label']}**：已进入批量队列，日志在 `{item['log_path']}`")
    lines.append('')
    lines.append('我会按每个任务各自的结果继续往下接，不会把它们揉成一条。')
    return '\n'.join(lines).strip()

def redact_command_args(args: list[str]) -> list[str]:
    redacted = list(args)
    sensitive_flags = {'--api-key'}
    for (idx, value) in enumerate(redacted[:-1]):
        if value in sensitive_flags:
            redacted[idx + 1] = '***'
    return redacted

def resolve_batch_concurrency(base_args: argparse.Namespace, requested: int | None, task_count: int) -> tuple[int, int, dict]:
    policy = resolve_batch_policy()
    cli_value = getattr(base_args, 'batch_concurrency', None)
    raw_value = cli_value if cli_value is not None else requested
    if raw_value is None:
        raw_value = policy['max_concurrency']
    try:
        normalized = int(raw_value)
    except Exception as exc:
        raise ValueError('batch concurrency must be an integer') from exc
    if normalized < 1:
        raise ValueError('batch concurrency must be at least 1')
    effective = min(normalized, policy['system_max_concurrency'], max(task_count, 1))
    return (normalized, effective, policy)

def write_batch_status_file(status_path: Path, payload: dict) -> None:
    status_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

def build_public_batch_payload(payload: dict[str, Any]) -> dict[str, Any]:
    public_payload = dict(payload)
    public_payload.pop('system_max_concurrency', None)
    public_payload.pop('system_max_tasks', None)
    return public_payload

def enforce_batch_task_limits(base_args: argparse.Namespace, *, task_count: int, policy: dict, phase: str) -> None:
    if task_count > policy['system_max_tasks']:
        print(json.dumps({'error': 'BATCH_TASK_LIMIT_EXCEEDED', 'message': f"Batch task count {task_count} exceeds hard system max {policy['system_max_tasks']} during {phase}. Split into smaller batches.", 'phase': phase, 'task_count': task_count, 'configured_max_tasks': policy['max_tasks'], 'system_max_tasks': policy['system_max_tasks']}, ensure_ascii=False, indent=2), file=sys.stderr)
        sys.exit(2)
    if task_count > policy['max_tasks'] and (not getattr(base_args, 'batch_task_count_approved', False)):
        print(json.dumps({'error': 'BATCH_TASK_COUNT_REQUIRES_APPROVAL', 'message': f"Batch task count {task_count} exceeds configured max_tasks {policy['max_tasks']} during {phase}. Ask for explicit user approval, then rerun with --batch-task-count-approved.", 'phase': phase, 'task_count': task_count, 'configured_max_tasks': policy['max_tasks'], 'system_max_tasks': policy['system_max_tasks']}, ensure_ascii=False, indent=2), file=sys.stderr)
        sys.exit(2)

def build_batch_child_command(task: dict) -> list[str]:
    """拼一个 batch 子任务的 dispatch.py 子进程命令。
    必须用 DISPATCH_SCRIPT，不要用 Path(__file__)（batch.py 没有 main，会静默退出）。
    """
    command = [sys.executable, str(dispatch_common.DISPATCH_SCRIPT), '--model', str(task['model'])]
    if task.get('prompt'):
        command += ['--prompt', str(task['prompt'])]
    command += build_cli_arg_list('--image', task.get('image'))
    command += build_cli_arg_list('--audio', task.get('audio'))
    command += build_cli_arg_list('--video', task.get('video'))
    if task.get('aspect_ratio'):
        command += ['--aspect-ratio', str(task['aspect_ratio'])]
    if task.get('resolution'):
        command += ['--resolution', str(task['resolution'])]
    if task.get('steps') is not None:
        command += ['--steps', str(task['steps'])]
    if task.get('duration') is not None:
        command += ['--duration', str(task['duration'])]
    if task.get('seed') is not None:
        command += ['--seed', str(task['seed'])]
    if task.get('random_seed'):
        command += ['--random-seed']
    if task.get('model_name'):
        command += ['--model-name', str(task['model_name'])]
    if task.get('width') is not None:
        command += ['--width', str(task['width'])]
    if task.get('height') is not None:
        command += ['--height', str(task['height'])]
    command += build_cli_arg_list('--param', task.get('param'))
    command += ['--output', str(task['output_path'])]
    if task.get('sync'):
        command += ['--sync']
    if task.get('run_mode') == 'run_with_defaults':
        command += ['--run-with-defaults']
    else:
        command += ['--confirm-run']
    return command

def launch_logged_process(command: list[str], log_path: Path, *, env: dict[str, str] | None=None) -> tuple[subprocess.Popen, object]:
    log_handle = open(log_path, 'w', encoding='utf-8')
    proc = subprocess.Popen(command, stdout=log_handle, stderr=subprocess.STDOUT, text=True, encoding='utf-8', errors='replace', stdin=subprocess.DEVNULL, env=env)
    return (proc, log_handle)

def append_supervisor_log(log_path: Path, message: str) -> None:
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with open(log_path, 'a', encoding='utf-8') as handle:
        handle.write(f'[{timestamp}] {message}\n')

def mark_batch_tasks_failed(payload: dict, *, reason: str, running_only: bool=False) -> None:
    for task in payload.get('tasks') or []:
        if not isinstance(task, dict):
            continue
        if running_only and task.get('status') != 'running':
            continue
        if not running_only and task.get('status') not in {'queued', 'running'}:
            continue
        task['status'] = 'failed'
        task.setdefault('failure_reason', reason)

def handle_batch_worker(worker_file: str) -> None:
    worker_path = Path(worker_file)
    payload = json.loads(worker_path.read_text(encoding='utf-8'))
    tasks = payload.get('tasks') or []
    concurrency = int(payload.get('effective_concurrency') or CONFIGURED_MAX_BATCH_CONCURRENCY_FALLBACK)
    status_path = Path(payload['status_path'])
    supervisor_log = Path(payload.get('supervisor_log') or status_path.with_name('batch-supervisor.log'))
    payload['scheduler_status'] = 'running'
    payload['started_at'] = int(time.time())
    write_batch_status_file(status_path, payload)
    append_supervisor_log(supervisor_log, f'worker started with {len(tasks)} task(s), concurrency={concurrency}')
    active: list[dict] = []
    next_index = 0
    try:
        while next_index < len(tasks) or active:
            while next_index < len(tasks) and len(active) < concurrency:
                task = tasks[next_index]
                child_env = dict(os.environ)
                child_env[RUNTIME_STATE_DISABLED_ENV] = '1'
                (proc, log_handle) = launch_logged_process(build_batch_child_command(task), Path(task['log_path']), env=child_env)
                task['pid'] = proc.pid
                task['status'] = 'running'
                append_supervisor_log(supervisor_log, f"launched task#{task.get('index')} pid={proc.pid} label={task.get('label')}")
                active.append({'proc': proc, 'log_handle': log_handle, 'task': task})
                next_index += 1
                write_batch_status_file(status_path, payload)
            if not active:
                break
            time.sleep(1)
            still_active: list[dict] = []
            for entry in active:
                proc = entry['proc']
                task = entry['task']
                ret = proc.poll()
                if ret is None:
                    still_active.append(entry)
                    continue
                entry['log_handle'].close()
                task['exit_code'] = ret
                task['status'] = 'completed' if ret == 0 else 'failed'
                append_supervisor_log(supervisor_log, f"task#{task.get('index')} pid={task.get('pid')} finished status={task['status']} exit_code={ret}")
                write_batch_status_file(status_path, payload)
            active = still_active
    except Exception:
        mark_batch_tasks_failed(payload, reason='worker_crashed')
        payload['scheduler_status'] = 'failed'
        payload['worker_error'] = traceback.format_exc()
        write_batch_status_file(status_path, payload)
        append_supervisor_log(supervisor_log, payload['worker_error'].rstrip())
        raise
    finally:
        for entry in active:
            try:
                entry['log_handle'].close()
            except Exception:
                pass
    payload['scheduler_status'] = 'completed'
    payload['finished_at'] = int(time.time())
    write_batch_status_file(status_path, payload)
    append_supervisor_log(supervisor_log, 'worker finished')

def handle_batch_prefill(base_args: argparse.Namespace) -> None:
    """批量预填卡。每个任务都通过路 B 渲染（远端 contract 驱动）。

    per-batch contract 缓存（_info_cache）：同一 model id 在一批里只 fetch 一次。
    比如 5 个任务都用 ChatGPT Image2，只打一次 BizyAir API 拿 contract。
    """
    (tasks, _) = parse_batch_payload(base_args.batch_json)
    policy = resolve_batch_policy()
    enforce_batch_task_limits(base_args, task_count=len(tasks), policy=policy, phase='batch_prefill')
    dispatch_common.ensure_api_key_ready(base_args.api_key)
    _info_cache: dict[str, dict] = {}
    payload_tasks = []
    for (index, task) in enumerate(tasks, start=1):
        task_args = build_task_args(base_args, task)
        model = task_args.model
        if task_args.scene:
            model = SCENE_NUMBER_MAP.get(task_args.scene, task_args.scene)
        target = dispatch_common.resolve_model(task_args.task, model)
        reject_search_flow_target(target, task_index=index, phase='batch_prefill')
        card.apply_compiled_selection(task_args, target)
        if target in ROUTE_TABLE:
            # 固定模型：用 ModelZoo detail 渲染 prefill card
            import modelzoo
            import api as _api
            endpoint = ROUTE_TABLE[target]['endpoint']
            cache_key = endpoint
            if cache_key not in _info_cache:
                key = _api.require_api_key(base_args.api_key)
                detail_result = modelzoo.get_detail(key, endpoint)
                detail_data = (detail_result.get('data') or {}).get('data') or detail_result.get('data') or {}
                _info_cache[cache_key] = detail_data
            detail_data = _info_cache[cache_key]
            input_params = detail_data.get('input_params') or []
            param_summary = ', '.join(f"{p.get('field_label', p.get('field_name'))}" for p in input_params if p.get('field_name'))
            card_markdown = f"**{dispatch_common.display_model_name(target)}** (ModelZoo: {endpoint})\n参数：{param_summary}"
        else:
            # 非固定模型：旧 webapp 路径
            app_id = target
            if app_id not in _info_cache:
                _info_cache[app_id] = remote.build_remote_info_output(app_id, api_key_arg=base_args.api_key, include_workflow=True)
            info_out = _info_cache[app_id]
            summary = info_out.get('summary') or {}
            card_markdown = remote.build_remote_prefilled_card(summary, task_args, resolved_object_id=app_id)
        payload_tasks.append({'index': index, 'label': task_label(task, index), 'model': target, 'display_name': dispatch_common.display_model_name(target), 'card_markdown': card_markdown})
    print(json.dumps({'mode': 'batch_prefill', 'task_count': len(payload_tasks), 'tasks': payload_tasks, 'reply_markdown': build_batch_prefill_reply(payload_tasks)}, ensure_ascii=False, indent=2))

def handle_batch_run(base_args: argparse.Namespace) -> None:
    (tasks, requested_concurrency) = parse_batch_payload(base_args.batch_json)
    (requested_concurrency, effective_concurrency, policy) = resolve_batch_concurrency(base_args, requested_concurrency, len(tasks))
    enforce_batch_task_limits(base_args, task_count=len(tasks), policy=policy, phase='batch_run')
    if requested_concurrency > policy['system_max_concurrency']:
        print(json.dumps({'error': 'BATCH_CONCURRENCY_LIMIT_EXCEEDED', 'message': f"Requested concurrency {requested_concurrency} exceeds hard system max {policy['system_max_concurrency']}. Lower the concurrency and try again.", 'requested_concurrency': requested_concurrency, 'configured_max_concurrency': policy['max_concurrency'], 'system_max_concurrency': policy['system_max_concurrency']}, ensure_ascii=False, indent=2), file=sys.stderr)
        sys.exit(2)
    if requested_concurrency > policy['max_concurrency'] and (not getattr(base_args, 'batch_concurrency_approved', False)):
        print(json.dumps({'error': 'BATCH_CONCURRENCY_REQUIRES_APPROVAL', 'message': f"Requested concurrency {requested_concurrency} exceeds configured max_concurrency {policy['max_concurrency']}. Ask for explicit user approval, then rerun with --batch-concurrency-approved.", 'requested_concurrency': requested_concurrency, 'configured_max_concurrency': policy['max_concurrency'], 'system_max_concurrency': policy['system_max_concurrency']}, ensure_ascii=False, indent=2), file=sys.stderr)
        sys.exit(2)
    batch_dir = resolve_batch_runs_dir() / time.strftime('%Y%m%d-%H%M%S')
    batch_dir.mkdir(parents=True, exist_ok=True)
    status_path = batch_dir / 'batch-status.json'
    worker_file = batch_dir / 'batch-payload.json'
    supervisor_log = batch_dir / 'batch-supervisor.log'
    payload_tasks = []
    for (index, task) in enumerate(tasks, start=1):
        task_args = build_task_args(base_args, task)
        model = task_args.model
        if task_args.scene:
            model = SCENE_NUMBER_MAP.get(task_args.scene, task_args.scene)
        target = dispatch_common.resolve_model(task_args.task, model)
        reject_search_flow_target(target, task_index=index, phase='batch_run')
        card.apply_compiled_selection(task_args, target)
        output_path = str((batch_dir / f'task-{index:02d}-output').resolve())
        log_path = batch_dir / f'task-{index:02d}.log'
        if task_args.sync:
            child_sync = True
        else:
            child_sync = False
        if should_batch_use_defaults(task_args, target):
            run_mode = 'run_with_defaults'
        else:
            run_mode = 'confirm_run'
        payload_tasks.append({'index': index, 'label': task_label(task, index), 'model': target, 'display_name': dispatch_common.display_model_name(target), 'status': 'queued', 'log_path': str(log_path.resolve()), 'output_path': str(Path(task.get('output') or output_path).resolve()), 'prompt': task_args.prompt, 'image': list(task_args.image or []), 'audio': list(task_args.audio or []), 'video': list(task_args.video or []), 'aspect_ratio': task_args.aspect_ratio, 'resolution': task_args.resolution, 'steps': task_args.steps, 'duration': task_args.duration, 'seed': task_args.seed, 'random_seed': bool(task_args.random_seed), 'model_name': task_args.model_name, 'width': task_args.width, 'height': task_args.height, 'param': list(task_args.param or []), 'sync': child_sync, 'run_mode': run_mode, 'command_preview': redact_command_args(build_batch_child_command({'model': target, 'prompt': task_args.prompt, 'image': list(task_args.image or []), 'audio': list(task_args.audio or []), 'video': list(task_args.video or []), 'aspect_ratio': task_args.aspect_ratio, 'resolution': task_args.resolution, 'steps': task_args.steps, 'duration': task_args.duration, 'seed': task_args.seed, 'random_seed': bool(task_args.random_seed), 'model_name': task_args.model_name, 'width': task_args.width, 'height': task_args.height, 'param': list(task_args.param or []), 'output_path': str(Path(task.get('output') or output_path).resolve()), 'sync': child_sync, 'run_mode': run_mode}))})
    payload = {'mode': 'batch_run', 'version': 2, 'task_count': len(payload_tasks), 'requested_concurrency': requested_concurrency, 'effective_concurrency': effective_concurrency, 'configured_max_concurrency': policy['max_concurrency'], 'system_max_concurrency': policy['system_max_concurrency'], 'configured_max_tasks': policy['max_tasks'], 'system_max_tasks': policy['system_max_tasks'], 'batch_dir': str(batch_dir.resolve()), 'status_path': str(status_path.resolve()), 'supervisor_log': str(supervisor_log.resolve()), 'scheduler_status': 'queued', 'tasks': payload_tasks}
    write_batch_status_file(status_path, payload)
    worker_file.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    worker_env = dict(os.environ)
    if base_args.api_key:
        worker_env['BIZYAIR_API_KEY'] = base_args.api_key
    worker_env[RUNTIME_STATE_DISABLED_ENV] = '1'
    log_handle = open(supervisor_log, 'a', encoding='utf-8')
    try:
        worker_proc = subprocess.Popen([sys.executable, str(dispatch_common.DISPATCH_SCRIPT), '--batch-worker-file', str(worker_file.resolve())], stdout=log_handle, stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL, text=True, encoding='utf-8', errors='replace', env=worker_env, start_new_session=True, close_fds=True)
    except Exception as exc:
        log_handle.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] failed to launch batch worker: {exc}\n")
        log_handle.flush()
        payload['scheduler_status'] = 'failed'
        mark_batch_tasks_failed(payload, reason='worker_launch_failed')
        write_batch_status_file(status_path, payload)
        raise
    finally:
        log_handle.close()
    payload['scheduler_pid'] = worker_proc.pid
    payload['scheduler_status'] = 'running'
    payload['reply_markdown'] = f"这批任务我已经按独立任务排进批量执行队列了。\n\n- 当前配置任务上限：{policy['max_tasks']}\n- 这次任务数：{len(payload_tasks)}\n- 当前配置并发上限：{policy['max_concurrency']}\n- 你这次请求并发：{requested_concurrency}\n- 实际并发上限：{effective_concurrency}\n\n" + build_batch_run_reply(payload_tasks)
    write_batch_status_file(status_path, payload)
    print(json.dumps(build_public_batch_payload(payload), ensure_ascii=False, indent=2))
