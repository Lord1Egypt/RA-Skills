# Gemini Smart Search Config Notes

## Environment variables

Preferred API key resolution order:

1. `SMART_SEARCH_GEMINI_API_KEY`
2. `GEMINI_API_KEY`

## Intended model chains

Human-facing display chains:

### cheap
- `gemini-2.5-flash-lite`
- `gemini-3.1-flash-lite`
- `gemini-2.5-flash`

### balanced
- `gemini-2.5-flash`
- `gemini-3-flash`
- `gemini-2.5-flash-lite`

### deep
- `gemini-3-flash`
- `gemini-2.5-flash`
- `gemini-3.1-flash-lite`

API candidate ids:
- `gemini-2.5-flash-lite` → `gemini-2.5-flash-lite`
- `gemini-2.5-flash` → `gemini-2.5-flash`
- `gemini-3-flash` → probe `gemini-3-flash-preview`, then `gemini-3-flash`
- `gemini-3.1-flash-lite` → probe `gemini-3.1-flash-lite-preview`, then `gemini-3.1-flash-lite`

## Notes

- The first implementation should stay Gemini-only.
- Keep the script output JSON-first for orchestration.
- Avoid coupling the script to gateway config.
- If later promoted to a plugin, preserve the same mode names and result schema.
- For quota-free smoke tests, Python supports `GEMINI_SMART_SEARCH_SKIP_LOCAL_ENV=1` to disable the Python script's repo-local `.env.local` loading temporarily.
- That skip flag does **not** stop the shell wrapper from sourcing `.env.local` first; use direct Python invocation for missing-key smoke checks or temporarily hide the env file when testing wrapper parity.
- Request auth should be sent via the `x-goog-api-key` header rather than a URL query parameter so the key is less likely to leak into logs or telemetry.
- Registry/skill metadata should declare `SMART_SEARCH_GEMINI_API_KEY` as the primary required env, even though runtime still falls back to `GEMINI_API_KEY` for compatibility.
