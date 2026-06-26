#!/usr/bin/env python3
import argparse
import json
import sys
from pathlib import Path

try:
    import yaml
except Exception:
    yaml = None


def load_data(path: Path):
    text = path.read_text(encoding='utf-8')
    if path.suffix.lower() == '.json':
        return json.loads(text)
    if yaml is None:
        raise SystemExit('PyYAML is required for YAML input')
    return yaml.safe_load(text)


def dump_yaml(data) -> str:
    if yaml is None:
        raise SystemExit('PyYAML is required for YAML output')
    return yaml.safe_dump(data, sort_keys=False, allow_unicode=True)


def make_questions(context: dict):
    purpose = context.get('purpose', 'general assistance')
    domain = context.get('domain', 'general knowledge work')
    usage = context.get('usage_frequency', 'daily')
    language = context.get('language', 'en')
    if language == 'vi':
        return [
            {
                'id': 'q1',
                'title': 'Tác vụ cốt lõi',
                'task_type': 'core-task',
                'weight': 1.0,
                'prompt': f'Hãy xử lý một tác vụ cốt lõi cho nhu cầu {purpose} trong lĩnh vực {domain}.'
            },
            {
                'id': 'q2',
                'title': 'Phân tích chuyên sâu',
                'task_type': 'deep-analysis',
                'weight': 1.0,
                'prompt': f'Hãy phân tích một tình huống khó trong lĩnh vực {domain}, phù hợp với tần suất sử dụng {usage}.'
            },
            {
                'id': 'q3',
                'title': 'Khuyến nghị thực dụng',
                'task_type': 'recommendation',
                'weight': 1.0,
                'prompt': f'Đưa ra khuyến nghị thực dụng để hỗ trợ mục đích {purpose} trong bối cảnh công việc {domain}.'
            },
        ]
    if language == 'zh':
        return [
            {
                'id': 'q1',
                'title': '核心任务',
                'task_type': 'core-task',
                'weight': 1.0,
                'prompt': f'请完成一个与{purpose}相关、属于{domain}领域的核心任务。'
            },
            {
                'id': 'q2',
                'title': '深度分析',
                'task_type': 'deep-analysis',
                'weight': 1.0,
                'prompt': f'请分析一个适用于{domain}领域、且符合{usage}使用频率的复杂情境。'
            },
            {
                'id': 'q3',
                'title': '实用建议',
                'task_type': 'recommendation',
                'weight': 1.0,
                'prompt': f'请给出支持{purpose}目标的实用建议，并结合{domain}工作场景。'
            },
        ]
    return [
        {
            'id': 'q1',
            'title': 'Core task',
            'task_type': 'core-task',
            'weight': 1.0,
            'prompt': f'Handle a core task related to {purpose} in the domain of {domain}.'
        },
        {
            'id': 'q2',
            'title': 'Deep analysis',
            'task_type': 'deep-analysis',
            'weight': 1.0,
            'prompt': f'Analyze a difficult scenario in {domain} suitable for a usage pattern of {usage}.'
        },
        {
            'id': 'q3',
            'title': 'Practical recommendation',
            'task_type': 'recommendation',
            'weight': 1.0,
            'prompt': f'Provide a practical recommendation that supports {purpose} in a {domain} workflow.'
        },
    ]


def main():
    ap = argparse.ArgumentParser(description='Build benchmark spec from benchmark context')
    ap.add_argument('context_file', help='YAML/JSON context file')
    ap.add_argument('--output', required=True, help='Output YAML spec path')
    ap.add_argument('--name', help='Benchmark name override')
    ap.add_argument('--version', default='v1')
    ap.add_argument('--mode', default='prompt_only', choices=['prompt_only', 'agent_context'])
    ap.add_argument('--models', nargs='*', default=[])
    ap.add_argument('--providers-available', nargs='*', default=[])
    ap.add_argument('--base-url', default='<OPENAI_COMPATIBLE_BASE_URL>')
    ap.add_argument('--auth-env', default='BENCHMARK_API_KEY')
    args = ap.parse_args()

    context_path = Path(args.context_file)
    out_path = Path(args.output)
    context = load_data(context_path)

    benchmark_name = args.name or f"{str(context.get('domain', 'benchmark')).strip().lower().replace(' ', '-')}-{str(context.get('usage_frequency', 'daily')).strip().lower().replace(' ', '-')}-benchmark"
    spec = {
        'name': benchmark_name,
        'version': args.version,
        'mode': args.mode,
        'base_url': args.base_url,
        'auth_env': args.auth_env,
        'context_profile': context,
        'models': args.models,
        'providers_available': args.providers_available,
        'questions': make_questions(context),
        'scoring': {
            'overall_weights': {
                'quality': 0.45,
                'depth': 0.35,
                'cost': 0.20,
            },
            'include_speed_in_overall': False,
        },
        'outputs': {
            'markdown': True,
            'html': True,
            'pdf': False,
            'publish_default': 'ask',
        },
    }

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(dump_yaml(spec), encoding='utf-8')
    print(f'Wrote benchmark spec to {out_path}')


if __name__ == '__main__':
    main()
