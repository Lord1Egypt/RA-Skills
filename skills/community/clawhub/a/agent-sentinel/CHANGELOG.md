# Changelog

## 0.1.2

- switched the OpenClaw skill to local-first behavior by default
- removed API key persistence to `.env`
- made cloud mode opt-in via `AGENT_SENTINEL_API_KEY`
- made local mode self-contained with `python3` only
- replaced SDK-managed cloud sync with explicit stdlib HTTP ingest
- added an explicit `sync` command so local checks do not upload automatically
- added persistent local state for status and budget tracking across invocations
- added `reset --scope run|all`
- aligned skill metadata, path, and copy with OpenClaw expectations
- added OpenClaw-specific README and basic wrapper tests
