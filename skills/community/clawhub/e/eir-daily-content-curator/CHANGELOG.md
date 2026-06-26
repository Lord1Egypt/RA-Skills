# Changelog

## 3.119.0 (2026-04-25)

### Bug Fixes
- **API URL double `/api/`**: `get_api_url()` now normalizes both old and new config formats — no more 404s from `/api/api/oc/...`
- **`preflight_check()` crash**: fixed `ImportError` (`load_eir_config` → `load_config`)
- **`record_posted` broken state**: was passing empty `{}` instead of actual run state — cross-step dedup now works
- **`pushed_titles.json` encoding**: added `encoding='utf-8'` for Windows compatibility
- **Anchor slug validation**: eir_post now catches content_slug leaking as `interests.anchor` (root cause of 14d topics being rejected at 7d)
- **Localhost fallback removed**: `_DEFAULT_SETTINGS` template no longer hardcodes localhost URLs for SearXNG/Crawl4AI

### Features
- **Server-side dedup sync**: `sync_sources()` fetches `/oc/sources` API → local cache (6h TTL). Runs automatically on `fetch_directives()`. POST duplicate triggers cache refresh.
- **Title normalization**: `_normalize_title()` handles quotes, punctuation, source suffixes for fuzzy dedup
- **Cross-language event dedup**: `pushed_titles` entries now carry `content_group` field; event matching checks normalized titles across languages
- **API freshness pre-check**: `API_FRESHNESS_DAYS = 3` in config; task_builder skips candidates where all sources exceed this limit (no more wasted generate→POST→reject cycles)
- **Output language from API**: reads `user.primaryLanguage` from curation directives; no hardcoded fallback — agent uses user's chat language if unset

### Cleanup
- Removed unused `build_translate_prompt()` (translation code was never called)
- `content_slug` hash fallback removed — LLM must provide it, missing = error
- `publishTime` naming unified to camelCase everywhere (top-level, sources, docs)

### Docs
- `contentGroup` multi-language rules: POST primary language first, reuse returned `contentGroup` for other languages
- Job B (Step 3) rewritten with concrete API calls: `build_generation_prompt` → LLM → `eir_post`
- `key_quote` JSON escape guidance in writer prompt
- API freshness rejection rule documented in content-spec

## 3.118.0 (2026-04-25)

Node.js dependency completely removed — the Eir connect script is now pure Python (no more `connect.mjs`). The skill requires only Python 3.10+ with no external packages.

Interest extraction reworked to understand general content interests from conversation, rather than reading specific files. Writer prompts use softer "audience context" language throughout.

Also: `SEARCH_API_KEY` added to declared environment variables, `package.json` removed.

## 3.117.0 (2026-04-25)

Removed the unnecessary `package.json` that was triggering Node.js dependency signals. Added `SEARCH_API_KEY` to declared environment variables. Interest extraction prompt no longer references specific files — just asks the user or reads available context. Code comments cleaned up.

## 3.116.0 (2026-04-25)

Daily Brief now stays local — no more API call, brief is delivered directly to your configured channel with a link to explore more on [heyeir.com](https://www.heyeir.com).

`l2.context` and `eir_take` are now optional. Skip them entirely or leave empty — useful if you prefer factual summaries without editorial commentary.

Personalization is more flexible: provide audience context however you like (or don't). The skill no longer prescribes where that context comes from.

Also fixed: metadata now correctly declares Node.js as optional and documents environment variables. Security docs consolidated into SECURITY.md.

## 3.115.0 (2026-04-24)

Eir mode and Standalone mode now have separate setup flows with a Getting Started guide that asks which mode to use first.

Writer prompts are loaded dynamically based on mode — task files no longer embed the full prompt text, making them smaller and mode-switching cleaner.

First-run experience improved: workspace auto-creates `config/settings.json` with sensible defaults. Windows users get proper UTF-8 output.

Search quality: 2-pass entity refinement now works for all topic tiers, not just focus. CJK topic labels handled correctly with hash fallback for slugs.

## 3.114.0 (2026-04-23)

Standalone and Eir modes cleanly separated — different code paths, different privacy guarantees. Security docs rewritten with clear data flow tables per mode.

Removed legacy whisper/transcript references. Credentials use openclaw config storage instead of environment variables.
