#!/usr/bin/env python3
import argparse
import json
import re
import subprocess
from pathlib import Path
from typing import Optional
from urllib.parse import urlparse

from kb_env import KB_CONFIG_PATH

CONFIG_PATH = KB_CONFIG_PATH

def load_json(path: Path):
    return json.loads(path.read_text(encoding='utf-8'))


def infer_type(source: str, explicit: Optional[str]):
    if explicit:
        return explicit
    lower = source.lower()
    if source.startswith(('http://', 'https://')):
        host = urlparse(source).netloc.lower()
        if 'github.com' in host:
            return 'repo'
        if lower.endswith('.pdf') or 'arxiv' in host:
            return 'paper'
        return 'article'
    if lower.endswith('.pdf'):
        return 'paper'
    if lower.endswith(('.xlsx', '.xlsm', '.csv', '.tsv')):
        return 'spreadsheet'
    return 'file'


def normalize_text(*parts):
    return ' '.join([p for p in parts if p]).lower()


def score_repo(repo: dict, source: str, source_type: str, title: str, preview: str, tags: list[str]):
    routing = repo.get('routing', {})
    score = repo.get('priority', 0)
    reasons = []
    domain = urlparse(source).netloc.lower() if source.startswith(('http://', 'https://')) else ''
    text = normalize_text(title, preview, source, ' '.join(tags))

    for d in routing.get('domains', []):
        if d and d.lower() in domain:
            score += 5
            reasons.append(f'domain:{d}')
    for kw in routing.get('keywords', []):
        if kw.lower() in text:
            score += 2
            reasons.append(f'keyword:{kw}')
    for kw in routing.get('exclude_keywords', []):
        if kw.lower() in text:
            score -= 4
            reasons.append(f'exclude:{kw}')
    for tag in repo.get('tags', []):
        if tag.lower() in text:
            score += 3
            reasons.append(f'tag:{tag}')
    if source_type == 'paper' and any(t in repo.get('tags', []) for t in ['arxiv', 'paper', 'ai']):
        score += 2
        reasons.append('source_type:paper')
    if source_type == 'repo' and any(t in repo.get('tags', []) for t in ['repo', 'training', 'llm']):
        score += 2
        reasons.append('source_type:repo')
    if source_type == 'spreadsheet' and any(t in repo.get('tags', []) for t in ['benchmark', 'dataset']):
        score += 2
        reasons.append('source_type:spreadsheet')

    return score, reasons


def strip_ansi(text: str) -> str:
    return re.sub(r'\x1b\[[0-?]*[ -/]*[@-~]', '', text)


def extract_json_object(text: str):
    if not text:
        return None
    cleaned = strip_ansi(text.strip())
    cleaned = re.sub(r'^```(?:json)?\s*', '', cleaned)
    cleaned = re.sub(r'\s*```$', '', cleaned)
    try:
        data = json.loads(cleaned)
        if isinstance(data, dict):
            return data
    except Exception:
        pass
    matches = re.findall(r'\{(?:[^{}]|(?:\{[^{}]*\}))*\}', cleaned, re.DOTALL)
    for candidate in matches[::-1]:
        try:
            data = json.loads(candidate)
            if isinstance(data, dict):
                return data
        except Exception:
            continue
    repo_match = re.search(r'"repo"\s*:\s*"([^"]+)"', cleaned)
    conf_match = re.search(r'"confidence"\s*:\s*"([^"]+)"', cleaned)
    reason_match = re.search(r'"reason"\s*:\s*"(.*?)"\s*\}', cleaned, re.DOTALL)
    if repo_match and conf_match and reason_match:
        reason = reason_match.group(1)
        reason = reason.replace('\n', ' ').strip()
        reason = re.sub(r'\b(\w+)\s+\1\b', r'\1', reason)
        reason = re.sub(r'\s+', ' ', reason).strip()
        return {
            'repo': repo_match.group(1).strip(),
            'confidence': conf_match.group(1).strip(),
            'reason': reason,
        }
    return None


def maybe_local_model(config: dict, source: str, source_type: str, title: str, preview: str, tags: list[str], candidates: list[dict]):
    lm = config.get('routing', {}).get('local_model', {})
    if not lm.get('enabled'):
        return None
    if lm.get('provider') != 'ollama':
        return None

    candidate_lines = []
    for r in candidates:
        candidate_lines.append(json.dumps({
            'name': r['name'],
            'description': r.get('description', ''),
            'tags': r.get('tags', [])
        }, ensure_ascii=False))

    prompt = (
        "You are a routing classifier. Choose the best repository for the content.\n"
        "Return EXACTLY one JSON object and nothing else.\n"
        "Allowed schema: {\"repo\": string, \"confidence\": \"low\"|\"medium\"|\"high\", \"reason\": string}.\n"
        "Do not use markdown fences. Do not add commentary.\n\n"
        f"SOURCE_TYPE: {source_type}\n"
        f"TITLE: {title}\n"
        f"SOURCE: {source}\n"
        f"TAGS: {json.dumps(tags, ensure_ascii=False)}\n"
        f"PREVIEW: {preview[:1200]}\n\n"
        "CANDIDATES:\n" + "\n".join(candidate_lines)
    )

    try:
        proc = subprocess.run(
            ['ollama', 'run', lm.get('model', 'gemma4:e4b')],
            input=prompt,
            capture_output=True,
            text=True,
            timeout=lm.get('timeout_sec', 8),
            check=False,
        )
        raw = strip_ansi((proc.stdout or proc.stderr or '').strip())
        data = extract_json_object(raw)
        if not data:
            return {'raw_output': raw[:1000], 'parse_error': 'no_json'}
        data['raw_output'] = raw[:1000]
        return data
    except Exception as exc:
        return {'raw_output': str(exc), 'parse_error': 'exception'}


def main():
    parser = argparse.ArgumentParser(description='Route content to the best configured KB repo')
    parser.add_argument('--source', required=True)
    parser.add_argument('--type', default=None)
    parser.add_argument('--title', default='')
    parser.add_argument('--preview', default='')
    parser.add_argument('--tags', default='')
    parser.add_argument('--repo', default=None, help='Explicit repo override')
    parser.add_argument('--config', default=str(CONFIG_PATH))
    args = parser.parse_args()

    config = load_json(Path(args.config).expanduser().resolve())
    repos = config.get('repos', [])
    source_type = infer_type(args.source, args.type)
    tags = [t.strip() for t in args.tags.split(',') if t.strip()]

    if args.repo:
        chosen = next((r for r in repos if r.get('name') == args.repo), None)
        if not chosen:
            raise SystemExit(f'Explicit repo not found: {args.repo}')
        print(json.dumps({
            'ok': True,
            'repo': chosen['name'],
            'root': chosen['root'],
            'confidence': 'explicit',
            'reasons': ['explicit_override'],
            'used_local_model': False,
            'local_model_debug': None,
        }, ensure_ascii=False, indent=2))
        return

    scored = []
    for repo in repos:
        score, reasons = score_repo(repo, args.source, source_type, args.title, args.preview, tags)
        scored.append({'repo': repo, 'score': score, 'reasons': reasons})
    scored.sort(key=lambda x: (-x['score'], x['repo']['name']))

    default_name = config.get('routing', {}).get('default_repo')
    default_repo = next((r for r in repos if r.get('name') == default_name), None)
    top = scored[0] if scored else None
    second = scored[1] if len(scored) > 1 else None
    threshold = config.get('routing', {}).get('min_confidence_score', 6)
    margin = config.get('routing', {}).get('min_margin', 2)
    low_conf = (not top) or top['score'] < threshold or (second and (top['score'] - second['score'] < margin))

    local_choice = None
    local_model_debug = None
    if low_conf:
        local_choice = maybe_local_model(config, args.source, source_type, args.title, args.preview, tags, repos)
        local_model_debug = local_choice

    used_local_model = bool(local_choice and local_choice.get('repo'))
    if used_local_model:
        chosen = next((r for r in repos if r.get('name') == local_choice['repo']), None)
        if chosen:
            print(json.dumps({
                'ok': True,
                'repo': chosen['name'],
                'root': chosen['root'],
                'confidence': local_choice.get('confidence', 'medium'),
                'reasons': [f"local_model:{local_choice.get('reason', 'no_reason')}"] + (top['reasons'] if top else []),
                'used_local_model': True,
                'local_model_debug': {
                    'confidence': local_choice.get('confidence'),
                    'reason': local_choice.get('reason'),
                    'raw_output': local_choice.get('raw_output', '')[:500],
                },
                'scores': [{'repo': item['repo']['name'], 'score': item['score'], 'reasons': item['reasons']} for item in scored]
            }, ensure_ascii=False, indent=2))
            return

    chosen = top['repo'] if top and top['score'] >= threshold else default_repo
    confidence = 'high' if top and top['score'] >= threshold and (not second or top['score'] - second['score'] >= margin) else 'low'
    reasons = top['reasons'] if top and chosen == top['repo'] else ['default_fallback']
    if chosen is None:
        raise SystemExit('No repos configured and no default repo available')

    print(json.dumps({
        'ok': True,
        'repo': chosen['name'],
        'root': chosen['root'],
        'confidence': confidence,
        'reasons': reasons,
        'used_local_model': False,
        'local_model_debug': local_model_debug,
        'scores': [{'repo': item['repo']['name'], 'score': item['score'], 'reasons': item['reasons']} for item in scored]
    }, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
