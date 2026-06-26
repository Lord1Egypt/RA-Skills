# Changelog

## v1.1.3 (2026-03-30)

QA fix release — all 5 findings from QA review addressed.

### Changes

**`src/workflow-executor.py`:**
- Bumped version to `1.1.3`.
- Fixed deprecated `datetime.utcnow()` in `StructuredLogger._log()` → replaced with `datetime.now(timezone.utc)` for Python 3.12+ forward compatibility (Minor #1).
- Fixed schema path resolution: now looks for `workflow-schema.json` in `src/` first (bundled), falls back to runtime `WORKFLOWS_DIR` (Suggestion #4).

**`config/workflow-executor.service`:**
- Added `# Platform: Linux ONLY` header comment with reference to macOS LaunchAgent alternative (Minor #3).
- Updated `ExecStart` from single-threaded Flask dev mode (`python3 workflow-executor.py`) to production Gunicorn startup script (`/bin/bash /path/to/flowclaw/src/scripts/start-workflow-executor.sh`) (Minor #2).
- Added inline comment explaining Gunicorn is the production startup method.

**`SKILL.md`:**
- Bumped version to `1.1.3`.
- Updated `## Requirements` section: n8n and Notion marked as optional (consistent with README) (Suggestion #5).

---

## v1.1.2 (2026-03-30)

Cross-platform compatibility review — documenting Unix/macOS-only support:

### Decision: Option B — Document Unix/macOS only

FlowClaw's production stack depends on Gunicorn (no Windows support), bash startup scripts, macOS LaunchAgent, and Linux systemd. Adding first-class Windows support would require a different WSGI server (e.g. Waitress), a PowerShell startup script, and a Windows Service alternative. This is deferred; the scope of changes is documented for future contributors.

### Changes

**`src/workflow-executor.py`:**
- Bumped version to `1.1.2`.
- Added platform note to module docstring: `macOS ✅ Linux ✅ Windows ❌`.
- Added inline comment to openclaw binary candidate list clarifying Unix/macOS-only paths.

**`src/scripts/start-workflow-executor.sh`:**
- Added `Platform Support` note to script header: macOS ✅, Linux ✅, Windows ❌.
- Documents that Gunicorn and bash are unavailable on Windows.

**`config/launchagent.plist`:**
- Added explicit `Platform: macOS ONLY` comment at the top of the file.
- References Linux systemd alternative and notes Windows is not applicable.

**`tests/test_security.py`:**
- `TestSafePathFunction`: Replaced hardcoded `/tmp/flowclaw` Unix paths with `tempfile.mkdtemp()`.
  - Tests now correctly handle macOS (where `/tmp` is a symlink to `/private/tmp`) and any CI host.
  - `test_safe_path_rejects_absolute_escape`: Updated to use `os.path.dirname(tmpdir)` instead of a hardcoded `/etc/passwd` path.
  - Added `setUp`/`tearDown` lifecycle to clean up temp dirs after each test.

**`README.md`:**
- Added **Platform Support** section before "Before You Start".
  - Table: macOS ✅, Linux ✅, Windows ❌ with per-platform notes.
  - "Why Windows is not supported" subsection listing concrete blockers.
  - Guidance for contributors who want to add Windows support in future.
- Updated version reference in "Before You Start" from `v1.1.0` → `v1.1.2`.
- Updated `## Requirements` to state macOS or Linux requirement with link to Platform Support section.
- Added note to `## Testing` explaining `tempfile.mkdtemp()` usage.

**`SKILL.md`:**
- Added `version: 1.1.2` field.
- Added `platforms: [macOS, Linux]` field to metadata.

## v1.1.1 (2026-03-30)

QA findings resolved — documentation, validation, and code quality fixes:

### Documentation
- `config/example.env`: Added `OPENCLAW_GATEWAY_TOKEN` with description of when it is required vs optional.
- `README.md`: Added `OPENCLAW_GATEWAY_URL` and `OPENCLAW_GATEWAY_TOKEN` rows to the Required Environment Variables table; documented optional/conditional usage.

### Startup Script
- `src/scripts/start-workflow-executor.sh`: Added validation for `PORT` (must be integer 1–65535), `HOST` (no shell metacharacters), and `MAX_WORKERS` (must be integer 1–64) before passing values to Gunicorn. Malformed values now exit with a clear error message instead of causing an ungraceful Gunicorn crash.

### Code Quality
- `src/workflow-executor.py`: Added `as exc` to all five bare `except Exception:` clauses (lines 189, 357, 390, 1795, 1907) and log the captured exception. Consistent with rest of codebase.

### Testing
- `tests/test_security.py`: Renamed `test_placeholder_not_in_allowlist` → `test_placeholder_passes_local_validation_fails_at_discord` to accurately reflect the behaviour being documented (local validation accepts it; Discord API rejects it as an invalid snowflake).

## v1.1.0 (2026-03-30)

Production-grade hardening — complete security and code audit with all issues resolved:

### Security Fixes

**Input validation at every HTTP boundary:**
- `/workflow/execute`: Added `Content-Type: application/json` enforcement, type checks on `context` (must be dict), type check on `workflowName` (must be string), length validation on `taskId` (max 64 chars).
- `/workflow/approve`: Added Content-Type enforcement, type checks on all fields (`run_id`, `approved_by`, `notes`), format validation on `run_id` via `_VALID_RUN_ID_RE`, length limits on `approved_by` (max 128 chars) and `notes` (silently truncated to 1000 chars).
- `/workflow/resume`: Full parity with `/approve` — Content-Type, type checks, `run_id` format validation.
- `/workflow/history`: Added length check on `task_id` query parameter.
- `/notion/update`: Added Content-Type enforcement, UUID validation on `pageId` via `_VALID_NOTION_ID_RE`, strict `status` allowlist (`_VALID_NOTION_STATUSES`).
- `/notion/create-subtask`: Added Content-Type enforcement, type checks, `name` length limit (512 chars), `assignedTo` allowlist, `dueDate` ISO 8601 format validation, `NOTION_TASKS_DATABASE_ID` moved from hardcoded `"YOUR_DATABASE_ID"` to `NOTION_TASKS_DATABASE_ID` environment variable (with UUID validation).
- `/notify/discord`: Refactored to use `Content-Type` enforcement; channel allowlist now correctly rejects empty/unconfigured channel IDs; improved error messages.

**Agent spawn hardening:**
- Task text capped at 50,000 chars before subprocess launch.
- `isinstance` check on task text to ensure it's always a string.
- Timeout values across all step handlers (`_step_spawn_agent`, `_step_wait_completion`, `_step_wait_approval`) now use `try/except (TypeError, ValueError)` safe coercion — no crashes if YAML supplies a float or string.

**Deploy step hardening:**
- `prod` field safely coerced to bool: Python `bool`, string `"false"/"no"/"0"/"off"` → `False`; everything else → `True`.
- `project` name validated against `_VALID_NAME_RE` before use as working directory — prevents path traversal via workflow YAML.

**QA step hardening:**
- QA scripts must have `.py` extension — shell scripts and binaries cannot be executed.
- `stagingUrl` must start with `http://` or `https://` — rejects `file://`, `javascript:`, and other URI schemes.

**Discord channel configuration:**
- `DISCORD_CHANNELS` dict with hardcoded `"YOUR_CHANNEL_ID"` placeholders replaced by `_build_discord_channels()` function that reads from `DISCORD_CHANNEL_PROJECT_UPDATES`, `DISCORD_CHANNEL_PROJECT_CALLS`, `DISCORD_CHANNEL_CHATTERIA` environment variables.
- Empty channel IDs are treated as disabled — notifications are skipped with a warning log.

**Gateway URL placeholder fixed:**
- `"http://[IP_ADDRESS]:18789"` replaced with `"http://127.0.0.1:18789"` in gateway fallback block.

**Notion database ID:**
- Hardcoded `"YOUR_DATABASE_ID"` removed from `/notion/create-subtask`. Replaced with `NOTION_TASKS_DATABASE_ID` environment variable (required for that endpoint, validated as UUID).

**Startup initialization:**
- `_on_startup()` double-call fixed: module-level call now only fires in gunicorn context (`else` branch of `if __name__ == "__main__"`). Dev mode (`python3 workflow-executor.py`) calls it once via `main()`.

### New Validation Constants
- `_VALID_NOTION_ID_RE` — UUID validation for Notion page/database IDs
- `_VALID_RUN_ID_RE` — Format validation for run IDs
- `_VALID_ISO_DATE_RE` — ISO 8601 date validation for `dueDate`
- `_VALID_NOTION_STATUSES` — Allowlisted Notion status values
- `_MAX_TASK_ID_LEN`, `_MAX_RUN_ID_LEN`, `_MAX_APPROVED_BY_LEN`, `_MAX_NOTES_LEN`, `_MAX_TASK_TEXT_LEN`, `_MAX_NAME_LEN`, `_MAX_STATUS_LEN` — Input length limits

### Configuration
- `config/example.env`: Added `NOTION_TASKS_DATABASE_ID`, `DISCORD_CHANNEL_PROJECT_UPDATES`, `DISCORD_CHANNEL_PROJECT_CALLS`, `DISCORD_CHANNEL_CHATTERIA` with documentation; added `.gitignore` note; improved security warnings.
- `config/launchagent.plist`: Fixed `ProgramArguments` to use the startup script; added `ThrottleInterval`; improved instructions.
- `src/scripts/start-workflow-executor.sh`: Complete rewrite — safe `.env` loader (no `eval`), credential validation at startup, gunicorn search covers venv paths, configurable bind via `HOST`/`PORT` env vars.

### Testing
- `tests/test_security.py`: New security test suite — **81 tests, all passing.**
  - `TestRegexValidation` — All input regex validators
  - `TestSafePathFunction` — Path traversal prevention
  - `TestAgentAllowlist` — Agent ID validation
  - `TestProdBoolCoercion` — `prod` field type safety
  - `TestTimeoutCoercion` — Timeout type safety
  - `TestNotionStatusAllowlist` — Status value validation
  - `TestDiscordChannelAllowlist` — Channel allowlist enforcement
  - `TestTaskTextLength` — Task text size limits
  - `TestQAScriptValidation` — Script extension and URL validation
  - `TestAssignedToAllowlist` — `assignedTo` field validation
  - `TestDueDateValidation` — ISO 8601 date validation
  - `TestNotesLengthLimit` — Notes truncation

### Documentation
- `README.md`: Full Security section documenting all validation rules, API surface, required env vars, and testing instructions.

## v1.0.3 (2026-03-30)

Security hardening (audit response):

- **Credential isolation:** `_load_env_from_openclaw()` is now opt-in only. FlowClaw no longer silently reads `~/.openclaw/openclaw.json` at startup. Set `FLOWCLAW_LOAD_OPENCLAW_CONFIG=true` to enable. Gateway URL fallback block gated by the same variable.
- **Agent spawn validation:** Added `ALLOWED_AGENTS` allowlist check in `_step_spawn_agent`. Unknown agent IDs are rejected before any subprocess is launched.
- **Deploy path validation:** `_step_deploy` fallback path (`WORKSPACE / project`) now goes through `_safe_path()`, preventing path traversal via workflow YAML config.
- **Dead code removed:** `import pickle` (unused) removed from module imports.
- **Redundant call removed:** `_load_env_from_openclaw()` call inside `_on_startup()` removed (module-level call suffices).
- `config/example.env`: Added `FLOWCLAW_LOAD_OPENCLAW_CONFIG=false` with documentation; updated stale NOTE comment.
- `README.md`: Updated Security Notes to reflect new opt-in credential loading behaviour.

## v1.0.2 (2026-03-30)

- Security: default bind address changed to 127.0.0.1 (local only)
- Added credential loading documentation
- Declared required/optional environment variables in skill metadata

## v1.0.1 (2026-03-30)

- Clarified that Notion, n8n, and Discord integrations are optional

## v1.0.0 (2026-03-30)

First public release.

- Multi-step workflow execution defined in YAML
- Human-in-the-loop approval gates
- Notion task sync (optional)
- n8n HTTP trigger integration (optional)
- Discord notifications (optional)
- 5 workflow templates included
- macOS and Linux service templates
