#!/usr/bin/env python3
import argparse
import json
import shutil
import subprocess
import tempfile
from pathlib import Path

from kb_env import KB_VENV_PYTHON

SCRIPT_DIR = Path(__file__).resolve().parent
KB_INIT = SCRIPT_DIR / 'kb_init.py'
KB_INGEST = SCRIPT_DIR / 'kb_ingest.py'
KB_BUILD = SCRIPT_DIR / 'kb_build.py'
KB_SUMMARIZE = SCRIPT_DIR / 'kb_summarize_concepts.py'
KB_SEARCH = SCRIPT_DIR / 'kb_search.py'
KB_ASK = SCRIPT_DIR / 'kb_ask.py'
KB_LINT = SCRIPT_DIR / 'kb_lint.py'
KB_CHART = SCRIPT_DIR / 'kb_chart.py'
VENV_PY = KB_VENV_PYTHON


def run(cmd, use_venv=False):
    if use_venv and VENV_PY.exists() and cmd[0] == 'python3':
        cmd = [str(VENV_PY)] + cmd[1:]
    p = subprocess.run(cmd, capture_output=True, text=True, check=False)
    return p.returncode, p.stdout, p.stderr


def main():
    parser = argparse.ArgumentParser(description='Smoke test duru-obsidian-kb scripts')
    parser.add_argument('--keep', action='store_true', help='Keep temp test dir')
    args = parser.parse_args()

    temp_dir = Path(tempfile.mkdtemp(prefix='kb-smoke-'))
    kb_root = temp_dir / 'kb'
    sample_txt = temp_dir / 'sample.txt'
    sample_csv = temp_dir / 'sample.csv'

    sample_txt.write_text('LLM agents and security tradeoffs with MCP integration.', encoding='utf-8')
    sample_csv.write_text('day,latency_ms\n2026-04-01,220\n2026-04-02,210\n', encoding='utf-8')

    steps = []

    def step(name, cmd, use_venv=False):
        rc, out, err = run(cmd, use_venv=use_venv)
        steps.append({
            'step': name,
            'ok': rc == 0,
            'cmd': cmd,
            'stdout': out[:800],
            'stderr': err[:800],
        })
        return rc == 0

    ok = True
    ok &= step('init', ['python3', str(KB_INIT), '--root', str(kb_root), '--name', 'smoke-kb'])
    ok &= step('ingest-local-file', ['python3', str(KB_INGEST), '--root', str(kb_root), '--source', str(sample_txt), '--type', 'file', '--tags', 'ai,llm,agent'])
    ok &= step('build', ['python3', str(KB_BUILD), '--root', str(kb_root)])
    ok &= step('summarize', ['python3', str(KB_SUMMARIZE), '--root', str(kb_root)])
    ok &= step('search', ['python3', str(KB_SEARCH), '--root', str(kb_root), '--query', 'agent security', '--top-k', '3', '--include-wiki'])
    ok &= step('ask', ['python3', str(KB_ASK), '--root', str(kb_root), '--question', 'What is the security tradeoff of MCP agents?', '--format', 'md', '--top-k', '3'])
    ok &= step('lint', ['python3', str(KB_LINT), '--root', str(kb_root)])
    # chart uses pandas/matplotlib in venv
    ok &= step('chart', ['python3', str(KB_CHART), '--root', str(kb_root), '--data', str(sample_csv), '--x-col', 'day', '--y-col', 'latency_ms', '--kind', 'line', '--title', 'Smoke Latency'], use_venv=True)

    summary = {
        'ok': ok,
        'kb_root': str(kb_root),
        'temp_dir': str(temp_dir),
        'steps': steps,
    }

    if not args.keep:
        shutil.rmtree(temp_dir, ignore_errors=True)
        summary['temp_dir_removed'] = True
    else:
        summary['temp_dir_removed'] = False

    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
