# ENV Key Naming & Comment Standard (v1)

Use this standard for all `.env` key creation and maintenance.

## 1) Naming rule (mandatory)

- Regex: `^[A-Z][A-Z0-9_]*$`
- Allowed: uppercase letters, digits, underscore
- Forbidden: lowercase, hyphen `-`, spaces, non-ASCII symbols, leading digit

## 2) Naming structure (recommended)

`<SYSTEM>_<DOMAIN>_<TYPE>`

- `SYSTEM`: provider/platform/module (e.g., `OPENAI`, `GITHUB`, `MOLTBOOK`, `FEISHU`)
- `DOMAIN`: function area (e.g., `API`, `AUTH`, `GATEWAY`, `PROXY`)
- `TYPE`: semantic suffix (e.g., `KEY`, `TOKEN`, `SECRET`, `BASE_URL`, `ID`)

Examples:

- `OPENAI_API_KEY`
- `OPENAI_BASE_URL`
- `GATEWAY_AUTH_TOKEN`
- `FEISHU_APP_SECRET`

## 3) Comment rule (mandatory for new keys)

Every new key must have a one-line comment immediately above it.

Template:

```env
# [SYSTEM] <purpose description> (<TYPE>) | used-by: <module/workflow> | owner: <team/role> | updated: YYYY-MM-DD
KEY_NAME=value
```

## 4) Good examples

```env
# [OPENAI] OpenAI-compatible key for model/ACP calls (KEY) | used-by: acp-router,acpx-codex,model-routing | owner: platform | updated: 2026-03-24
OPENAI_API_KEY=...

# [GATEWAY] OpenClaw Gateway auth token (TOKEN) | used-by: gateway-auth | owner: platform | updated: 2026-03-24
GATEWAY_AUTH_TOKEN=...
```

## 5) Bad examples

```env
openai_key=...         # lowercase
OPENAI-API-KEY=...     # hyphen
TEMP=...               # ambiguous name
```

## 6) Maintenance workflow

1. Run key discovery first (`keys`)
2. Check existence (`exists`)
3. Add/update/delete via `set`/`unset`
4. Run `lint`
5. Run `doctor --strict` for release/automation gates

## 7) Security notes

- Never echo secret values in chat/logs.
- Prefer stdin for set operations.
- Keep policy file permissions strict (not group/world writable).
- Use protected key list for high-risk keys.
