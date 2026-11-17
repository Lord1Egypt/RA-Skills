import argparse
import json
import math
import sys
from pathlib import Path

DIMS = ['typography', 'whitespace', 'hierarchy', 'color', 'motion', 'micro-interactions', 'responsive', 'originality', 'usability', 'retention']
STATIC = ['typography', 'whitespace', 'hierarchy', 'color', 'responsive', 'originality']
DYNAMIC = [d for d in DIMS if d not in STATIC]
WEIGHTS = {'design': 0.4, 'usability': 0.3, 'creativity': 0.2, 'content': 0.1}


def load(path):
    with open(path, encoding='utf-8') as f:
        return json.load(f)


def number(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)


def scores(value, keys, location):
    if not isinstance(value, dict):
        sys.exit(f'{location} must be a dict of scores')
    missing = [k for k in keys if k not in value]
    extra = [k for k in value if k not in keys]
    if missing or extra:
        sys.exit(f'{location} has the wrong dimensions. Missing: {missing or "none"}; extra: {extra or "none"}')
    for key in keys:
        if not number(value[key]) or not 1 <= value[key] <= 10:
            sys.exit(f'{location} "{key}" must be a number from 1 to 10')


def main():
    parser = argparse.ArgumentParser(description='Calibrate blind review scores and decide the best version from the side-by-side comparison.')
    parser.add_argument('--round', required=True)
    parser.add_argument('--anchor', required=True)
    parser.add_argument('--model', required=True)
    parser.add_argument('--best')
    parser.add_argument('--save')
    parser.add_argument('--live-anchor', action='store_true')
    parser.add_argument('--max-shift', type=float, default=1.0)
    args = parser.parse_args()
    if not math.isfinite(args.max_shift) or args.max_shift < 0:
        sys.exit('--max-shift must be a non-negative number')
    std = load(args.anchor)
    scores(std, DIMS, args.anchor)
    round_path = Path(args.round).resolve()
    blind_path = round_path / 'blind.json'
    blind = load(blind_path)
    if not isinstance(blind, dict) or not isinstance(blind.get('reviewers'), dict) or len(blind['reviewers']) < 2 or type(blind.get('has_best')) is not bool or type(blind.get('best_live')) is not bool:
        sys.exit(f'{blind_path} has invalid reviewer or best-version info')
    has_best = blind['has_best']
    live_best = blind['best_live']
    if live_best and not has_best:
        sys.exit(f'{blind_path} has no best version, so it cannot be marked live')
    if args.best and not has_best:
        sys.exit(f'{blind_path} has no best version; regenerate the prompts with --best')
    if has_best and not args.best:
        sys.exit(f'{blind_path} includes best-version screenshots; pass the best version\'s score file with --best')
    best = None
    if args.best:
        best = load(args.best)
        message = f'{args.best} must look like: {{"scores": {{ten dimensions}}, "total": 74.0, "model": "model", "round": "r3", "awwwards": {{four items}} or null}}'
        if not isinstance(best, dict) or set(best) != {'scores', 'total', 'model', 'round', 'awwwards'} or not number(best['total']) or not isinstance(best['model'], str) or not isinstance(best['round'], str):
            sys.exit(message)
        scores(best['scores'], DIMS, args.best + ' scores')
        if best['awwwards'] is not None:
            scores(best['awwwards'], list(WEIGHTS), args.best + ' awwwards')
    corrected, raws, awards, reviews = [], [], [], []
    for name, mapping in blind['reviewers'].items():
        if not isinstance(name, str) or not name.startswith('r') or not name[1:].isdigit() or not isinstance(mapping, dict):
            sys.exit(f'{blind_path} has an invalid reviewer name or mapping: {name}')
        if {mapping.get('A'), mapping.get('B')} != {'anchor', 'current'}:
            sys.exit(f'{blind_path} {name}: A/B mapping is invalid')
        if has_best and {mapping.get('C'), mapping.get('D')} != {'current', 'best'}:
            sys.exit(f'{blind_path} {name}: C/D mapping is invalid')
        path = round_path / name / 'scores.json'
        review = load(path)
        if not isinstance(review, dict):
            sys.exit(f'{path} must be a JSON object')
        for label in ('A', 'B'):
            scores(review.get(label), DIMS, f'{path} "{label}"')
        if 'awwwards' in review:
            scores(review['awwwards'], list(WEIGHTS), f'{path} awwwards')
            awards.append(review['awwwards'])
        if has_best:
            compare = review.get('compare')
            required = DIMS if live_best else STATIC
            if not isinstance(compare, dict) or set(compare) != set(required):
                sys.exit(f'{path} "compare" must contain exactly: ' + ', '.join(required))
            for d in required:
                if compare[d] not in ('C', 'D', 'tie'):
                    sys.exit(f'{path} "compare" "{d}" must be C, D or tie')
        anchor_key = next(k for k in ('A', 'B') if mapping[k] == 'anchor')
        current_key = next(k for k in ('A', 'B') if mapping[k] == 'current')
        raw = review[current_key]
        adjusted = {}
        for d in DIMS:
            shift = 0 if not args.live_anchor and d in DYNAMIC else max(-args.max_shift, min(args.max_shift, std[d] - review[anchor_key][d]))
            adjusted[d] = raw[d] + shift
        raws.append(raw)
        corrected.append(adjusted)
        reviews.append((name, mapping, review))
    count = len(reviews)
    avg = {d: round(sum(c[d] for c in corrected) / count, 1) for d in DIMS}
    raw_avg = {d: sum(c[d] for c in raws) / count for d in DIMS}
    total = round(sum(avg.values()), 1)
    print('Calibrated averages:')
    for d in DIMS:
        spread = max(c[d] for c in corrected) - min(c[d] for c in corrected)
        print(f'  {d} {avg[d]:.1f}' + ('  reviewers differ by 3+ points, read their reasons' if spread >= 3 else ''))
    print(f'Total {total:.1f} / 100')
    print('Below 9: ' + (', '.join(d for d in DIMS if avg[d] < 9) or 'none'))
    print(f'Uncalibrated average total {sum(raw_avg.values()):.1f}')
    moved = [f'{d} {raw_avg[d]:.1f}->{avg[d]:.1f}' for d in DIMS if round(abs(sum(c[d] for c in corrected) / count - raw_avg[d]), 10) >= 1]
    print('Moved 1+ point by calibration: ' + (', '.join(moved) + '. Check the anchor set is shown under the same conditions as before.' if moved else 'none'))
    aw = None
    weighted = None
    if awards:
        aw = {k: round(sum(x[k] for x in awards) / len(awards), 2) for k in WEIGHTS}
        weighted = round(sum(aw[k] * WEIGHTS[k] for k in WEIGHTS), 2)
        print('Awwwards: ' + ' · '.join(f'{k} {aw[k]:.2f}' for k in WEIGHTS) + f'; weighted {weighted:.2f} (Honorable Mention 6.5+, SOTD usually 7.2-7.7)')
    else:
        print('Awwwards: not scored')
    conclusion = 'first round'
    results = {}
    if best:
        print('Side-by-side:')
        for d in DIMS:
            if live_best or d in STATIC:
                votes = []
                for name, mapping, review in reviews:
                    choice = review['compare'][d]
                    vote = 0 if choice == 'tie' else (1 if mapping[choice] == 'current' else -1)
                    votes.append(vote)
                if all(v == -1 for v in votes):
                    result = 'worse (all reviewers)'
                elif 1 in votes and -1 in votes and sum(votes) == 0:
                    result = 'split'
                elif sum(votes) >= 1:
                    result = 'better'
                elif sum(votes) <= -1:
                    result = 'worse'
                else:
                    result = 'tie'
                vote_text = ', '.join(f'{reviews[i][0]} {v:+d}' for i, v in enumerate(votes))
            else:
                vote_text = 'not comparable from screenshots'
                if args.model != best['model']:
                    result = 'tie (reviewer model changed, not comparable)'
                elif round(avg[d] - best['scores'][d], 10) >= 1:
                    result = 'better'
                elif round(best['scores'][d] - avg[d], 10) >= 1:
                    result = 'worse'
                else:
                    result = 'tie'
            results[d] = result
            print(f'  {d}: {vote_text}, {result}')
        good = [d for d in DIMS if results[d] == 'better']
        bad = [d for d in DIMS if results[d] in ('worse', 'worse (all reviewers)')]
        unanimous = [d for d in DIMS if results[d] == 'worse (all reviewers)']
        disagreements = [d for d in DIMS if results[d] == 'split']
        if unanimous:
            conclusion = 'revert'
            print('Revert: every reviewer judged the best version better on ' + ', '.join(unanimous) + '. Edit the changes in this batch that touched these back to the best version\'s look, as a new commit on top; keep the rest. The best version stays.')
        elif len(good) > len(bad):
            conclusion = 'new best version'
            print('New best version.')
            if bad or disagreements:
                print('Look at these first next batch: ' + ', '.join(d for d in DIMS if d in bad or d in disagreements) + '.')
        elif len(good) == len(bad):
            conclusion = 'tie'
            print('Tie: keep this version as the base for the next batch; the best version stays.')
            print('Worse or split: ' + (', '.join(d for d in DIMS if d in bad or d in disagreements) or 'none'))
        else:
            conclusion = 'worse than best'
            print('Worse than the best version: edit the items judged worse (' + ', '.join(bad) + ') back to the best version\'s look; the best version stays.')
        delta = round(total - best['total'], 10)
        print(f'Absolute: best version {best["total"]:.1f} ({best["model"]}) -> this round {total:.1f} ({args.model})')
        if args.model != best['model']:
            print('Reviewer models differ: do not compare absolute scores, go by the side-by-side.')
        elif abs(delta) < 3:
            print('Within 3 points: reviewer noise.')
        elif (delta < 0 and conclusion == 'new best version') or (delta > 0 and conclusion in ('revert', 'worse than best')):
            print(f'Absolute score and side-by-side point opposite ways ({abs(delta):.1f} points); read both reviewers\' reasons before deciding and note it in the log.')
    if args.save and (not best or conclusion == 'new best version'):
        saved = {'scores': avg, 'total': total, 'model': args.model, 'round': round_path.name, 'awwwards': aw}
        Path(args.save).write_text(json.dumps(saved, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        print(f'Saved: {args.save}')
    elif args.save:
        print(f'Not a new best version, {args.save} left unchanged')
    log = f'For the log: independent review ({args.model}, {count} reviewers) calibrated ' + ' · '.join(f'{d} {avg[d]:.1f}' for d in DIMS) + f' (total {total:.1f}); Awwwards weighted ' + (f'{weighted:.2f}' if weighted is not None else 'n/a')
    if best:
        good_count = sum(v == 'better' for v in results.values())
        bad_count = sum(v in ('worse', 'worse (all reviewers)') for v in results.values())
        log += f'; side-by-side better {good_count} · tie {len(DIMS) - good_count - bad_count} · worse {bad_count} -> {conclusion}'
    print(log)


if __name__ == '__main__':
    main()
