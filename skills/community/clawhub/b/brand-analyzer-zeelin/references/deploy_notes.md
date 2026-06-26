# Deploy Notes (Zero-config Package)

This package is SKILL.md-first and HTTP-only.

## Publish checklist

1. Replace API host in SKILL.md with your stable HTTPS domain.
2. Ensure backend endpoint is online:
   - POST /v1/brand-analyzer/generate
3. Keep billing flow on backend only:
   - detail -> generate -> cost(50)
4. Do not include .env files, keys, or backend code in publish package.

## User experience target

- User provides App-Key only.
- Agent handles API calls directly.
- No local python script execution required.
