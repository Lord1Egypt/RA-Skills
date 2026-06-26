#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
NORMALIZER = ROOT / 'scripts' / 'normalize-request.py'
RENDERER = ROOT / 'scripts' / 'render-cp2k-input.py'
REPORT_TEMPLATE = ROOT / 'assets' / 'report.md'


def load_json(path: Path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def write_text(path: Path, text: str) -> None:
    path.write_text(text.rstrip() + '\n', encoding='utf-8')


def render_report(template: str, job: dict) -> str:
    text = template
    for key in ['task_type','run_type','system_type','structure_file','periodicity','charge','multiplicity','priority','xc_functional','basis_family','potential_family','scf_mode','kpoints_scheme','cell_handling']:
        text = text.replace('{{ ' + key + ' }}', str(job.get(key)))
    hw = job.get('hardware', {})
    text = text.replace('{{ hardware.type }}', str(hw.get('type')))
    text = text.replace('{{ hardware.cores }}', str(hw.get('cores')))
    text = text.replace('{{ hardware.memory_gb }}', str(hw.get('memory_gb')))
    defaults = job.get('defaults_applied') or []
    notes = job.get('notes') or []
    review = job.get('review_required') or []
    text = text.replace('{{ defaults_applied_block }}', '\n'.join(f'- {x}' for x in defaults) if defaults else '- None recorded')
    text = text.replace('{{ notes_block }}', '\n'.join(f'- {x}' for x in notes) if notes else '- None')
    text = text.replace('{{ review_required_block }}', '\n'.join(f'- {x}' for x in review) if review else '- None')
    return text


def parse_args():
    p = argparse.ArgumentParser(description='Generate normalized.json, job.inp, and report.md in one shot')
    p.add_argument('raw_request_json')
    p.add_argument('structure_file')
    p.add_argument('-d', '--outdir', default='out')
    return p.parse_args()


def main() -> None:
    args = parse_args()
    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    normalized = outdir / 'normalized.json'
    job_inp = outdir / 'job.inp'
    report_md = outdir / 'report.md'

    subprocess.run([sys.executable, str(NORMALIZER), args.raw_request_json, '-o', str(normalized)], check=True)
    subprocess.run([sys.executable, str(RENDERER), str(normalized), args.structure_file, '-o', str(job_inp)], check=True)

    job = load_json(normalized)
    template = REPORT_TEMPLATE.read_text(encoding='utf-8')
    write_text(report_md, render_report(template, job))
    print(f'Wrote {normalized}')
    print(f'Wrote {job_inp}')
    print(f'Wrote {report_md}')


if __name__ == '__main__':
    main()
