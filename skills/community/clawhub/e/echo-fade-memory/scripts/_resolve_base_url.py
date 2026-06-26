#!/usr/bin/env python3
import json
import os
from pathlib import Path

# precedence:
# 1. EFM_BASE_URL
# 2. /Users/system/.openclaw/openclaw.json -> skills.entries.echo-fade-memory.baseUrl
# 3. /home/node/.openclaw/openclaw.json -> same path
# 4. default localhost

env = os.environ.get('EFM_BASE_URL')
if env:
    print(env)
    raise SystemExit(0)

candidates = [
    Path('/Users/system/.openclaw/openclaw.json'),
    Path('/home/node/.openclaw/openclaw.json'),
]

for path in candidates:
    if not path.exists():
        continue
    try:
        data = json.loads(path.read_text())
        value = (
            data.get('skills', {})
                .get('entries', {})
                .get('echo-fade-memory', {})
                .get('baseUrl')
        )
        if value:
            print(value)
            raise SystemExit(0)
    except Exception:
        pass

print('http://127.0.0.1:8080')
