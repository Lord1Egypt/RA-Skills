import argparse
import json
import secrets
import shlex
import shutil
import sys
from pathlib import Path
from string import Template

DIMS = ['typography', 'whitespace', 'hierarchy', 'color', 'motion', 'micro-interactions', 'responsive', 'originality', 'usability', 'retention']
STATIC = ['typography', 'whitespace', 'hierarchy', 'color', 'responsive', 'originality']
LISTS = ['pages', 'references', 'signature_moments', 'deliberate_flaws', 'rejected_looks', 'how_to_operate']
STRINGS = ['product', 'url', 'scenario', 'machine_limits']


def main():
    parser = argparse.ArgumentParser(description='Build blind screenshot sets, reviewer prompts and the blind mapping.')
    parser.add_argument('--config', required=True)
    parser.add_argument('--anchor-shots', required=True)
    parser.add_argument('--current', required=True)
    parser.add_argument('--round', required=True)
    parser.add_argument('--best')
    parser.add_argument('--live-best')
    parser.add_argument('--reviewers', type=int, default=2)
    args = parser.parse_args()
    target = Path(args.round).resolve()
    if target.exists():
        sys.exit(f'Round directory already exists, refusing to overwrite: {target}')
    if args.live_best and not args.best:
        sys.exit('--live-best needs --best')
    if args.reviewers < 2:
        sys.exit('At least 2 reviewers')
    with open(args.config, encoding='utf-8') as f:
        config = json.load(f)
    if not isinstance(config, dict):
        sys.exit(f'{args.config} must be a JSON object')
    for key in LISTS + STRINGS + ['rubric']:
        if key not in config:
            sys.exit(f'{args.config} is missing "{key}"')
    for key in LISTS:
        if not isinstance(config[key], list) or any(not isinstance(x, str) for x in config[key]):
            sys.exit(f'{args.config} "{key}" must be a list of strings')
    for key in STRINGS:
        if not isinstance(config[key], str):
            sys.exit(f'{args.config} "{key}" must be a string')
    if not isinstance(config.get('sounds', []), list) or any(not isinstance(x, str) for x in config.get('sounds', [])):
        sys.exit(f'{args.config} "sounds" must be a list of strings')
    rubric = config['rubric']
    if not isinstance(rubric, dict) or set(rubric) != set(DIMS):
        sys.exit(f'{args.config} "rubric" must contain exactly the ten dimensions: ' + ', '.join(DIMS))
    if any(not isinstance(rubric[d], str) for d in DIMS):
        sys.exit(f'{args.config} rubric entries must all be strings')
    sources = {'anchor': Path(args.anchor_shots).resolve(), 'current': Path(args.current).resolve()}
    if args.best:
        sources['best'] = Path(args.best).resolve()
    shots = {}
    for name, source in sources.items():
        if not source.is_dir():
            sys.exit(f'{name} screenshot directory not found: {source}')
        shots[name] = sorted(p for p in source.iterdir() if p.is_file() and p.suffix.lower() == '.png')
        if not shots[name]:
            sys.exit(f'{name} screenshot directory has no PNG files: {source}')
    template = Template((Path(__file__).resolve().parent.parent / 'templates' / 'REVIEW_PROMPT.md').read_text(encoding='utf-8'))
    target.mkdir(parents=True)
    sets = target / 'sets'
    sets.mkdir()
    directories = {}

    def copy_set(name):
        code = secrets.token_hex(3)
        while code in directories:
            code = secrets.token_hex(3)
        path = sets / code
        path.mkdir()
        for shot in shots[name]:
            shutil.copy2(shot, path / shot.name)
        directories[code] = name
        return str(path)

    anchor_dir, current_dir = copy_set('anchor'), copy_set('current')
    if args.best:
        compare_current, compare_best = copy_set('current'), copy_set('best')
    first, compare_first = secrets.randbelow(2), secrets.randbelow(2)
    mappings = {}
    example = {'A': {d: 7 for d in DIMS}, 'B': {d: 7 for d in DIMS}, 'awwwards': {'design': 6.8, 'usability': 7.0, 'creativity': 6.5, 'content': 6.9}}
    if args.best:
        example['compare'] = {d: ['C', 'tie', 'D'][i % 3] for i, d in enumerate(DIMS if args.live_best else STATIC)}
    example_text = json.dumps(example, ensure_ascii=False, indent=2)
    if args.best:
        example_text += '\nEach "compare" item is "C", "D" or "tie" (which set is better; "tie" when you cannot tell).'
    for i in range(args.reviewers):
        reviewer = f'r{i + 1}'
        out = target / reviewer
        out.mkdir()
        order = (first + i) % 2
        labels = [('anchor', anchor_dir), ('current', current_dir)]
        labels = labels[order:] + labels[:order]
        mapping = {'A': labels[0][0], 'B': labels[1][0]}
        compare_materials = 'There is no previous best version this round, so no side-by-side comparison.'
        if args.best:
            compare_order = (compare_first + i) % 2
            pairs = [('current', compare_current), ('best', compare_best)]
            pairs = pairs[compare_order:] + pairs[:compare_order]
            mapping.update({'C': pairs[0][0], 'D': pairs[1][0]})
            compare_materials = f'Screenshots C: {pairs[0][1]}; screenshots D: {pairs[1][1]} (one is the version at the address above, the other is the previous best version, same pages and widths. Compare them item by item and fill "compare" in the JSON.)'
            if args.live_best:
                compare_materials += f' The previous best version can also be opened at {args.live_best}; click through both for motion, micro-interactions, usability and retention before comparing.'
            else:
                compare_materials += ' The previous best version only exists as screenshots, which cannot show motion, micro-interactions, usability or retention, so "compare" only covers typography, whitespace, hierarchy, color, responsive and originality.'
        mappings[reviewer] = mapping
        values = dict(product=config['product'], url=config['url'], pages='\n'.join('- ' + x for x in config['pages']), set_a=labels[0][1], set_b=labels[1][1], compare_materials=compare_materials, refs='\n'.join('- ' + x for x in config['references']), moments='\n'.join(config['signature_moments']) or 'none', sounds=('This site has sound, which you cannot hear in a headless browser. Whether each action makes a sound and how loud is in the level files below (peak level measured on the audio output in the test browser, 0 is silent, 1 is full scale); check them before saying "no audio feedback":\n' + '\n'.join(config['sounds']) + '\n') if config.get('sounds') else '', deliberate='\n'.join(config['deliberate_flaws']) or 'none', operate='\n'.join(['- ' + x for x in config['how_to_operate']] + (['- ' + config['machine_limits']] if config['machine_limits'] else [])), out_dir=str(out) + '/', scenario=config['scenario'], rubric='\n'.join(f'- {d}: {rubric[d]}' for d in DIMS), rejected=', '.join(config['rejected_looks']) or 'none', compare_output='- Compare sets C and D item by item: which is better for each item and why.' if args.best else '', json_example=example_text, review_path=str(out / 'review.md'), json_path=str(out / 'scores.json'))
        prompt_path = target / f'prompt-{reviewer}.md'
        prompt_path.write_text(template.substitute(values), encoding='utf-8')
        print(f'Prompt: {prompt_path}')
    blind = {'reviewers': mappings, 'has_best': bool(args.best), 'best_live': bool(args.live_best), 'directories': directories, 'sources': {k: str(v) for k, v in sources.items()}}
    blind_path = target / 'blind.json'
    blind_path.write_text(json.dumps(blind, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'Blind mapping: {blind_path}')
    script = shlex.quote(str(Path(__file__).with_name('calibrate.py').resolve()))
    print(f'Next: python3 {script} --round {shlex.quote(str(target))} --anchor <anchor scores.json> --model "reviewer model and effort"' + (' --best <best.json>' if args.best else ''))


if __name__ == '__main__':
    main()
