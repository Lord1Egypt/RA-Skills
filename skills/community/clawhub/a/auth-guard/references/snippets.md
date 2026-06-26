# Drop-in Snippets

## HEARTBEAT.md Snippet

```md
### <Service> Check
1. Run authenticated helper first:
   - `/home/ada/.openclaw/workspace/.pi/<service>-check.sh`
2. If helper reports unauthorized/missing auth, use documented fallback endpoint.
3. Do not run raw unauthenticated curl to protected endpoints when helper exists.
```

## AGENTS.md Snippet

```md
### Auth Guard
- For services with protected endpoints, always use the workspace helper script.
- Credential order: ENV var first, then `~/.config/<service>/credentials.json`.
- Before periodic loops, run a startup auth probe.
- Never log secret values.
```

## Helper Template (copy to `.pi/<service>-check.sh`)

```bash
#!/usr/bin/env bash
set -euo pipefail

URL='https://example.com/api/protected'
FALLBACK_URL='https://example.com/api/public'
ENV_VAR='SERVICE_API_KEY'
CRED_FILE="$HOME/.config/service/credentials.json"

KEY="${!ENV_VAR:-}"
if [[ -z "$KEY" && -f "$CRED_FILE" ]]; then
  KEY="$(python3 - <<'PY'
import json, os
p=os.path.expanduser('~/.config/service/credentials.json')
d=json.load(open(p))
print((d.get('apiKey') or d.get('api_key') or '').strip(), end='')
PY
)"
fi

if [[ -n "$KEY" ]]; then
  if curl -fsS -H "Authorization: Bearer $KEY" "$URL"; then
    exit 0
  fi
fi

curl -fsS "$FALLBACK_URL"
```
