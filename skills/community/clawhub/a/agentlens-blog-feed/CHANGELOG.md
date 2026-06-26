# Changelog

## [0.1.0] - 2026-06-08

### Added
- Initial release of `agentlens-blog-feed`: discovers newly published AgentLens blogs from
  the public API (`https://agentlens-core.archlab.workers.dev`), fetches each new blog's
  body, and de-duplicates via a local memory file so every blog surfaces exactly once.
- Two-step workflow: read-only **Detect** (returns new blogs to the caller without writing
  memory) and **Commit** (records consumed blog IDs atomically). Downstream use is left to
  the caller — no drafting, language choice, vault saving, or scheduling.
