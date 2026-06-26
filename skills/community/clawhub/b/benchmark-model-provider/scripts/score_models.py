#!/usr/bin/env python3
import argparse
import json
import re
from pathlib import Path


ERROR_PATTERNS = [
    r'^ERROR:',
    r'HTTP Error',
    r'Bad Gateway',
    r'Unauthorized',
    r'unknown provider',
]


def inverse_normalize(values):
    if not values:
        return []
    lo, hi = min(values), max(values)
    if hi == lo:
        return [50.0 for _ in values]
    return [round(100.0 * (hi - v) / (hi - lo), 2) for v in values]


def forward_normalize(values):
    if not values:
        return []
    lo, hi = min(values), max(values)
    if hi == lo:
        return [50.0 for _ in values]
    return [round(100.0 * (v - lo) / (hi - lo), 2) for v in values]


def is_error_answer(text: str) -> bool:
    text = (text or '').strip()
    if not text:
        return True
    return any(re.search(pattern, text, re.I | re.M) for pattern in ERROR_PATTERNS)


def answer_features(text: str):
    text = (text or '').strip()
    if is_error_answer(text):
        return {
            'error': True,
            'chars': len(text),
            'lines': 0,
            'sections': 0,
            'bullets': 0,
            'numbers': 0,
            'hedging': 0,
            'action_words': 0,
        }
    return {
        'error': False,
        'chars': len(text),
        'lines': len([ln for ln in text.splitlines() if ln.strip()]),
        'sections': len(re.findall(r'^(#+|\d+[\.)]|[-*]\s)', text, re.M)),
        'bullets': len(re.findall(r'^[-*]\s', text, re.M)),
        'numbers': len(re.findall(r'\d', text)),
        'hedging': len(re.findall(r'không có truy cập dữ liệu thời gian thực|không thể xác nhận|cần kiểm tra thêm|chưa đủ cơ sở', text, re.I)),
        'action_words': len(re.findall(r'tác động|rủi ro|theo dõi|kết luận|khuyến nghị|nguyên nhân|hệ quả|quy trình', text, re.I)),
    }


def clamp(value: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, value))


def derive_raw_scores_from_answers(markdown_path: Path):
    text = markdown_path.read_text(encoding='utf-8')
    answers = re.findall(r'### Answer\n(.*?)(?=\n## |\Z)', text, re.S)
    if not answers:
        return 0.0, 0.0, {'answered_questions': 0, 'error_questions': 0}

    quality_total = 0.0
    depth_total = 0.0
    answered_questions = 0
    error_questions = 0

    for answer in answers:
        feat = answer_features(answer)
        if feat['error']:
            error_questions += 1
            continue
        answered_questions += 1
        quality_q = (
            2.0
            + min(1.5, feat['sections'] * 0.25)
            + min(1.0, feat['bullets'] * 0.1)
            + min(1.0, feat['numbers'] * 0.03)
            + min(1.5, feat['action_words'] * 0.15)
            + min(2.0, feat['chars'] / 1200.0)
            - min(1.0, feat['hedging'] * 0.35)
        )
        depth_q = (
            1.5
            + min(2.0, feat['chars'] / 900.0)
            + min(1.5, feat['lines'] * 0.08)
            + min(1.5, feat['sections'] * 0.25)
            + min(1.5, feat['numbers'] * 0.035)
            + min(1.0, feat['action_words'] * 0.1)
            - min(0.8, feat['hedging'] * 0.25)
        )
        quality_total += clamp(quality_q, 0.0, 10.0)
        depth_total += clamp(depth_q, 0.0, 10.0)

    answered_ratio = answered_questions / max(1, len(answers))
    if answered_ratio < 1.0:
        quality_total *= answered_ratio
        depth_total *= answered_ratio

    return round(clamp(quality_total, 0.0, 100.0), 2), round(clamp(depth_total, 0.0, 100.0), 2), {
        'answered_questions': answered_questions,
        'error_questions': error_questions,
    }


def main():
    ap = argparse.ArgumentParser(description='Score models from raw metrics and optional manual scores')
    ap.add_argument('raw_metrics_file')
    ap.add_argument('--manual-scores', help='Optional JSON file with per-model quality_raw and depth_raw')
    ap.add_argument('--output', help='Output JSON path for score breakdown')
    args = ap.parse_args()

    raw = json.loads(Path(args.raw_metrics_file).read_text(encoding='utf-8'))
    manual = {}
    if args.manual_scores:
        manual = json.loads(Path(args.manual_scores).read_text(encoding='utf-8'))

    models = raw.get('models', [])
    quality_raws, depth_raws, costs, speeds = [], [], [], []
    rows = []
    for m in models:
        model_name = m['model']
        totals = m.get('totals', {})
        q_raw = manual.get(model_name, {}).get('quality_raw')
        d_raw = manual.get(model_name, {}).get('depth_raw')
        diagnostics = {}
        markdown_path = Path(m.get('file', '')) if m.get('file') else None
        if q_raw is None or d_raw is None:
            if markdown_path and markdown_path.exists():
                auto_q, auto_d, diagnostics = derive_raw_scores_from_answers(markdown_path)
                q_raw = auto_q if q_raw is None else q_raw
                d_raw = auto_d if d_raw is None else d_raw
            else:
                q_raw = q_raw if q_raw is not None else min(50.0, round((totals.get('output_tokens', 0) / 250.0), 2))
                d_raw = d_raw if d_raw is not None else min(50.0, round((totals.get('output_tokens', 0) / 300.0), 2))
        quality_raws.append(q_raw)
        depth_raws.append(d_raw)
        costs.append(float(totals.get('cost_usd', 0.0)))
        speeds.append(float(totals.get('latency_sec', 0.0)))
        rows.append({
            'model': model_name,
            'quality_raw': q_raw,
            'depth_raw': d_raw,
            'cost_usd': float(totals.get('cost_usd', 0.0)),
            'latency_sec': float(totals.get('latency_sec', 0.0)),
            'total_tokens': int(totals.get('total_tokens', 0)),
            **diagnostics,
        })

    q_scores = forward_normalize(quality_raws)
    d_scores = forward_normalize(depth_raws)
    c_scores = inverse_normalize(costs)
    s_scores = inverse_normalize(speeds)

    rankings = []
    for i, row in enumerate(rows):
        overall = round(0.45 * q_scores[i] + 0.35 * d_scores[i] + 0.20 * c_scores[i], 2)
        ranked = {
            **row,
            'quality_score': q_scores[i],
            'depth_score': d_scores[i],
            'cost_score': c_scores[i],
            'speed_score': s_scores[i],
            'overall_score': overall,
        }
        rankings.append(ranked)

    rankings.sort(key=lambda x: x['overall_score'], reverse=True)
    for idx, row in enumerate(rankings, start=1):
        row['rank'] = idx

    out = {
        'run_id': raw.get('run_id'),
        'weights': {'quality': 0.45, 'depth': 0.35, 'cost': 0.20, 'speed_included': False},
        'rankings': rankings,
    }
    out_path = Path(args.output) if args.output else Path(args.raw_metrics_file).with_name('score_breakdown.json')
    out_path.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f'Wrote score breakdown to {out_path}')


if __name__ == '__main__':
    main()
