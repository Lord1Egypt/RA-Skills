#!/usr/bin/env python3
import argparse
import json
import os
import subprocess
import sys
import time
import urllib.request
from pathlib import Path
from collections import deque

try:
    import yaml
except Exception:
    yaml = None

EST_CHARS_PER_TOKEN = 3.6


def estimate_tokens(text: str) -> int:
    return max(1, round(len(text) / EST_CHARS_PER_TOKEN))


def slugify(model: str) -> str:
    return model.replace('/', '-').replace(':', '-').replace(' ', '-').lower()


def normalize_model_name(model: str, base_url: str) -> str:
    model = str(model).strip()
    if '/v1' in (base_url or '') and '/' in model:
        return model.split('/', 1)[1]
    return model


def load_structured(path: Path):
    text = path.read_text(encoding='utf-8')
    if path.suffix.lower() == '.json':
        return json.loads(text)
    if yaml is None:
        raise SystemExit('PyYAML is required for YAML files')
    return yaml.safe_load(text)


def save_structured(path: Path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.suffix.lower() == '.json':
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
        return
    if yaml is None:
        raise SystemExit('PyYAML is required for YAML files')
    path.write_text(yaml.safe_dump(data, sort_keys=False, allow_unicode=True), encoding='utf-8')


def call_model(base_url, api_key, model, prompt):
    url = base_url.rstrip('/') + '/chat/completions'
    normalized_model = normalize_model_name(model, base_url)
    payload = {'model': normalized_model, 'messages': [{'role': 'user', 'content': prompt}]}
    raw_payload = json.dumps(payload).encode('utf-8')
    headers = {'Content-Type': 'application/json'}
    if api_key:
        headers['Authorization'] = f'Bearer {api_key}'
    start = time.time()
    try:
        req = urllib.request.Request(url, data=raw_payload, headers=headers, method='POST')
        with urllib.request.urlopen(req, timeout=180) as resp:
            data = json.loads(resp.read().decode('utf-8'))
        latency = round(time.time() - start, 3)
        choice = (data.get('choices') or [{}])[0]
        message = choice.get('message') or {}
        text = message.get('content', '')
        usage = data.get('usage') or {}
        return {'ok': True, 'text': text, 'latency_sec': latency, 'usage': usage, 'raw': data, 'normalized_model': normalized_model}
    except Exception as e:
        latency = round(time.time() - start, 3)
        hint = ''
        err_text = str(e)
        if 'unknown provider for model' in err_text and normalized_model != model:
            hint = f' | Hint: endpoint may expect raw model id `{normalized_model}` instead of `{model}`'
        return {'ok': False, 'text': f'ERROR: {e}{hint}', 'latency_sec': latency, 'usage': {}, 'raw': {'error': str(e), 'normalized_model': normalized_model}}


def resolve_pricing(model: str):
    from resolve_pricing import resolve
    return resolve(model)


def compute_cost(model: str, input_tokens: int, output_tokens: int):
    pricing = resolve_pricing(model)
    cost = (input_tokens / 1_000_000.0) * pricing['input_per_million'] + (output_tokens / 1_000_000.0) * pricing['output_per_million']
    return round(cost, 8), pricing


def write_model_markdown(path: Path, model: str, run_id: str, questions_out: list):
    lines = [f'# {model}', '', f'- run_id: {run_id}', '']
    for item in questions_out:
        lines.extend([
            f"## {item['id']} — {item['title']}",
            '',
            '### Prompt',
            item['prompt'],
            '',
            '### Answer',
            item['answer'],
            '',
        ])
    path.write_text('\n'.join(lines), encoding='utf-8')


def _is_safe_base_url(base_url: str) -> bool:
    """Basic safety checks.

    - Require https
    - Block raw IPs
    - Block localhost

    This is not a complete security solution, but it prevents the most common
    foot-guns that trigger security scanners and protects against accidental
    exfiltration to an IP/short endpoint.
    """
    if not base_url:
        return False
    base_url = base_url.strip()
    if not base_url.startswith('https://'):
        return False
    lowered = base_url.lower()
    if 'localhost' in lowered or '127.0.0.1' in lowered or '0.0.0.0' in lowered:
        return False
    # crude IP check (blocks http(s)://<digits>.<digits>.<digits>.<digits>)
    import re
    if re.search(r'https://\d{1,3}(?:\.\d{1,3}){3}(?::\d+)?(?:/|$)', lowered):
        return False
    return True


def run_single_model(spec: dict, model: str, run_dir: Path, run_id: str):
    base_url = spec.get('base_url') or os.environ.get('BENCHMARK_BASE_URL') or ''
    if not _is_safe_base_url(base_url):
        raise SystemExit(
            'Unsafe or missing base_url. For safety, base_url must be https and not localhost/raw IP. '
            'Set it in the benchmark spec (base_url) or BENCHMARK_BASE_URL.'
        )
    api_key = os.environ.get(spec.get('auth_env', 'BENCHMARK_API_KEY'), '')
    questions_out = []
    total_in = total_out = 0
    total_latency = 0.0
    total_cost = 0.0

    effective_model = normalize_model_name(model, base_url)
    if effective_model != model:
        print(f'[subagent:{model}] Normalized model name -> {effective_model}')

    for idx, q in enumerate(spec.get('questions', []), start=1):
        print(f'[subagent:{model}] Running question {idx}/{len(spec.get("questions", []))}: {q.get("id")}')
        result = call_model(base_url, api_key, model, q['prompt'])
        answer = result['text'] if isinstance(result['text'], str) else json.dumps(result['text'], ensure_ascii=False)
        usage = result.get('usage') or {}
        input_tokens = usage.get('prompt_tokens') or estimate_tokens(q['prompt'])
        output_tokens = usage.get('completion_tokens') or estimate_tokens(answer)
        total_tokens = usage.get('total_tokens') or (input_tokens + output_tokens)
        cost, pricing = compute_cost(model, input_tokens, output_tokens)
        total_in += input_tokens
        total_out += output_tokens
        total_latency += result['latency_sec']
        total_cost += cost
        questions_out.append({
            'id': q['id'],
            'title': q.get('title', q['id']),
            'prompt': q['prompt'],
            'answer': answer,
            'input_tokens': input_tokens,
            'output_tokens': output_tokens,
            'total_tokens': total_tokens,
            'latency_sec': result['latency_sec'],
            'cost_usd': cost,
            'cost_source': pricing['confidence'],
            'usage_is_estimated': not bool(usage),
        })

    model_path = run_dir / f'{slugify(model)}.md'
    write_model_markdown(model_path, model, run_id, questions_out)
    result_payload = {
        'model': model,
        'file': str(model_path),
        'questions': [{k: v for k, v in item.items() if k not in ('prompt', 'answer', 'title')} for item in questions_out],
        'totals': {
            'input_tokens': total_in,
            'output_tokens': total_out,
            'total_tokens': total_in + total_out,
            'latency_sec': round(total_latency, 3),
            'cost_usd': round(total_cost, 8),
        },
    }
    result_json = run_dir / f'{slugify(model)}.json'
    result_json.write_text(json.dumps(result_payload, ensure_ascii=False, indent=2), encoding='utf-8')
    return result_payload


def orchestrate_subagents(spec: dict, run_dir: Path, run_id: str, max_parallel: int = 1):
    script_path = Path(__file__).resolve()
    results = []
    models = spec.get('models', [])
    total_models = len(models)
    max_parallel = max(1, min(max_parallel, total_models or 1))
    print(f'[orchestrator] Starting subagent_orchestrated run for {total_models} models (max_parallel={max_parallel})')

    pending = deque((idx, model) for idx, model in enumerate(models, start=1))
    running = []
    completed = 0

    while pending or running:
        while pending and len(running) < max_parallel:
            idx, model = pending.popleft()
            print(f'[orchestrator] Dispatching model {idx}/{total_models}: {model}')
            sub_spec = dict(spec)
            sub_spec['models'] = [model]
            sub_spec_path = run_dir / 'sub_specs' / f'{slugify(model)}.yaml'
            save_structured(sub_spec_path, sub_spec)
            cmd = [
                sys.executable,
                str(script_path),
                str(sub_spec_path),
                '--run-id', run_id,
                '--out-dir', str(run_dir.parent),
                '--strategy', 'sequential',
                '--single-model', model,
            ]
            proc = subprocess.Popen(cmd, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            running.append({'idx': idx, 'model': model, 'proc': proc})

        still_running = []
        for item in running:
            proc = item['proc']
            if proc.poll() is None:
                still_running.append(item)
                continue

            stdout, stderr = proc.communicate()
            if stdout:
                print(stdout, end='')
            if proc.returncode != 0:
                if stderr:
                    print(stderr, end='', file=sys.stderr)
                raise SystemExit(proc.returncode)

            result_json = run_dir / f'{slugify(item["model"])}.json'
            if not result_json.exists():
                raise SystemExit(f'Missing subagent result for {item["model"]}: {result_json}')
            results.append(json.loads(result_json.read_text(encoding='utf-8')))
            completed += 1
            print(f'[orchestrator] Completed {completed}/{total_models}: {item["model"]}')
            print(f'[progress] Agent finished: {item["model"]} ({completed}/{total_models})')

        running = still_running
        if running:
            time.sleep(0.2)

    results.sort(key=lambda x: models.index(x['model']) if x['model'] in models else 10**9)
    return results


def build_metrics(spec: dict, run_id: str, execution_strategy: str, model_results: list):
    return {
        'run_id': run_id,
        'benchmark_name': spec.get('name'),
        'benchmark_version': spec.get('version'),
        'mode': spec.get('mode', 'prompt_only'),
        'execution_strategy': execution_strategy,
        'models': model_results,
    }


def main():
    ap = argparse.ArgumentParser(description='Run benchmark and save raw outputs/metrics')
    ap.add_argument('spec_file')
    ap.add_argument('--run-id', default=time.strftime('%Y-%m-%dT%H-%M-%SZ', time.gmtime()))
    ap.add_argument('--out-dir', default='test_results')
    ap.add_argument('--strategy', default='sequential', choices=['sequential', 'subagent_orchestrated'])
    ap.add_argument('--max-parallel', type=int, default=1, help='Maximum concurrent subagents for subagent_orchestrated mode')
    ap.add_argument('--single-model', help='Internal subagent mode: run only one model')
    args = ap.parse_args()

    spec = load_structured(Path(args.spec_file))
    run_dir = Path(args.out_dir) / args.run_id
    run_dir.mkdir(parents=True, exist_ok=True)

    if args.single_model:
        print(f'Current step: run benchmark for single model {args.single_model}')
        model_result = run_single_model(spec, args.single_model, run_dir, args.run_id)
        metrics = build_metrics(spec, args.run_id, 'sequential', [model_result])
        raw_metrics_path = run_dir / f'{slugify(args.single_model)}-raw_metrics.json'
        raw_metrics_path.write_text(json.dumps(metrics, ensure_ascii=False, indent=2), encoding='utf-8')
        print(f'Completed single-model benchmark for {args.single_model}')
        print(f'Next step: return result to orchestrator')
        return

    print('Current step: load benchmark spec and prepare run directory')
    print(f'Completed preparation for benchmark {spec.get("name")}')
    if spec.get('providers_available'):
        print('[info] Providers/models available from OpenClaw context:')
        for item in spec.get('providers_available', []):
            print(f'[info] - {item}')
    print(f'Next step: run benchmark using strategy={args.strategy}')

    if args.strategy == 'subagent_orchestrated':
        model_results = orchestrate_subagents(spec, run_dir, args.run_id, max_parallel=args.max_parallel)
    else:
        model_results = []
        total_models = len(spec.get('models', []))
        for idx, model in enumerate(spec.get('models', []), start=1):
            print(f'Current step: benchmark model {idx}/{total_models} -> {model}')
            model_results.append(run_single_model(spec, model, run_dir, args.run_id))
            print(f'Completed model {idx}/{total_models} -> {model}')
            if idx < total_models:
                print(f'Next step: benchmark model {idx + 1}/{total_models}')

    print('Current step: aggregate benchmark outputs into raw metrics')
    metrics = build_metrics(spec, args.run_id, args.strategy, model_results)
    raw_metrics_path = run_dir / 'raw_metrics.json'
    raw_metrics_path.write_text(json.dumps(metrics, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f'Completed metrics aggregation: {raw_metrics_path}')
    print('Next step: scoring and report generation')
    print(f'Run directory: {run_dir}')


if __name__ == '__main__':
    sys_path = Path(__file__).resolve().parent
    if str(sys_path) not in os.sys.path:
        os.sys.path.insert(0, str(sys_path))
    main()
