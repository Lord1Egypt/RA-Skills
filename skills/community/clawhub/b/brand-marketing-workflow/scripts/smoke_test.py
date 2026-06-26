#!/usr/bin/env python3
"""End-to-end smoke test for brand-marketing-workflow skill."""
from __future__ import annotations

import json
import subprocess
from pathlib import Path

BASE = Path('/Users/macmini/.openclaw/workspace/skills/brand-marketing-workflow/scripts')
SCRIPTS = {
    'normalize': BASE / 'normalize_brand_input.py',
    'score': BASE / 'score_content_effect.py',
    'cluster': BASE / 'competitor_cluster.py',
    'orchestrator': BASE / 'workflow_orchestrator.py',
    'content_producer': BASE / 'content_producer_stub.py',
    'auth': BASE / 'authorization_manager.py',
    'browser': BASE / 'browser_execution.py',
}

INPUTS = {
    'normalize': json.dumps({'brand_name':'Aurora Lane','brand_tone':'calm sharp poetic'}, ensure_ascii=False),
    'score': json.dumps({'notes':'smoke'}, ensure_ascii=False),
    'cluster': json.dumps([{'theme':'minimal','tone':'calm'}], ensure_ascii=False),
    'orchestrator': json.dumps({'brand_name':'Aurora Lane','brand_tone':'calm sharp poetic','channels':['xiaohongshu','weibo'],'competitor_scope':['public competitor signals'],'execution_action':'publish','data_access':'authorized','browser_action':'collect_public_signals','need_login':False}, ensure_ascii=False),
    'content_producer': json.dumps({'brand_name':'Aurora Lane'}, ensure_ascii=False),
    'auth': json.dumps({'action':'payment','data_access':'authorized','requires_payment':True,'human_response':'','state':'running','fallback':'draft only'}, ensure_ascii=False),
    'browser': json.dumps({'action':'bypass captcha','data_access':'unknown','need_login':True,'platform':'xiaohongshu'}, ensure_ascii=False),
}


def run(script: Path, data: str) -> dict:
    proc = subprocess.run(
        ['python3', str(script)],
        input=data.encode(),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True,
    )
    return json.loads(proc.stdout.decode())


def main() -> int:
    results = {name: run(path, INPUTS[name]) for name, path in SCRIPTS.items()}
    print(json.dumps(results, ensure_ascii=False, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
