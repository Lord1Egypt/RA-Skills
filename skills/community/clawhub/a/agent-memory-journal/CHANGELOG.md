# Changelog

## 0.2.3 (2026-04-25)
- fix `digest` CLI command crashing with `AttributeError` on `MemoryPaths.v2_root`
- make `rebuild_agent_md(max_chars=...)` honour its caller argument and apply the 256-char floor only to config-derived values; `doctor` and `review` use the same effective budget instead of a hard-coded 2048
- wire `archive_unpinned_core` into `ingest_cycle` so the documented 30-day decay actually happens; `IngestReport` now includes `archived_count`
- BM25 normaliser now keeps token multiplicity, so repeated terms increase TF as the index promised; cache version bumped
- `AGENT.md` is rendered with claim text only (metadata stays in `core/`), recovering ~70% of the hot budget for actual content
- `Journal.remember(..., pinned=True)` and `Journal.forget(...)` now rebuild `AGENT.md` synchronously instead of waiting for the next ingest
- `recall_core` updates `last_seen` in a single batched rewrite per file and refreshes the manifest, so `doctor` stays `OK` after recall
- core writes (`append_core_memory`, `supersede_memory`) refresh the integrity manifest, so `doctor` no longer reports `ISSUES_FOUND` after every legitimate write
- new `recall_recent(root, days, k)` function; `agent-memory-journal recent` now works without `--grep`
- `Journal.recall(tier="all")` weights warm hits 2× and fetches a wider per-tier window before merging
- `_count_pinned_core_items` filters superseded entries so the review report matches what `AGENT.md` actually contains
- CLI `--version` is sourced from `importlib.metadata` instead of a hard-coded literal
- new tests: end-to-end CLI coverage, ingest+decay, recall ranking, hot metadata stripping
- new `tests.yml` GitHub Actions workflow runs pytest on Python 3.10/3.11/3.12

## 0.2.2 (2026-04-25)
- make decay use `last_seen` as the primary activity signal, with `created` as fallback
- add `hot_path` validation so hot-memory promotion stays confined to the workspace or memory root
- make supersedes fail fast when the target id does not exist
- move `LegacyJournal` out of `api.py` into a dedicated `legacy.py` module
- harden hot-set config handling with bounded character budgets and cleaner rebuild logic
- version BM25 cache invalidation against normalizer changes

## 0.2.1 (2026-04-25)
- add agent installation guide for workspace embedding and CLI bootstrap
- add `.memory/config.json` support for overriding the hot promotion target, header, and character budget
- document how to promote pinned hot memory into files like root-level `AGENTS.md`
- clarify that hot memory limits are currently character-based, not token-based

## 0.2.0 (2026-04-25)
- **3-Tier Memory Architecture**: Implemented `.memory/` layout with Hot (`AGENT.md`), Warm (`core/`), and Cold (`episodic/`) tiers.
- **Probabilistic Retrieval**: Replaced substring search with **BM25 ranking** for all recall operations.
- **Weighted Recall**: Warm (Core) memories now outrank Episodic logs in unified search (1.5x score multiplier).
- **Atomic Persistence**: Implemented "write-to-temp-then-rename" for all file operations to prevent corruption.
- **"Forget" Capability**: Added `forget` command and API method to supersede memories by ID.
- **Autonomous Promotion**: Automated detection and promotion of repeated facts from episodic to core memory.
- **Integrity Doctor**: Manifest-based verification of core memory files with SHA256 checksums.
- **Safety Boundary**: Strict sanitation for Hot/Core tiers while allowing raw evidence in Episodic logs.
- **Session Support**: Isolated session memory tracking with cross-session klustering.
- **Decay & Archive**: 30-day unpinned memory archival to prevent "junk drawer" core files.
- **Migration Path**: Built-in `migrate` command to port legacy `MEMORY.md` and `memory/` folders.

## 0.1.0
- initialize standalone `agent-memory-journal` repository
- rename CLI engine to `agent_memory_journal.py`
- decouple memory root from workspace-specific hard-coded paths
- add JSON config for trigger patterns
- add agent-facing `SKILL.md` and installation guidance
- expand README with layout, config, testing, and roadmap
- add CLI, JSON, config, and help/version tests
