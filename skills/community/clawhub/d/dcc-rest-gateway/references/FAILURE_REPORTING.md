## Step 5 — Analyze Failures and Report Bugs

Do not guess a root cause or blindly replay a mutation. Preserve `request_id`, `trace_id`, `job_id`, tool slug, instance id, sanitized arguments, error code, and validation result.

```bash
dcc-mcp-cli doctor
dcc-mcp-cli stats --range 24h --status failure --session-id task-42
dcc-mcp-cli feedback --tool-name maya_geometry__create_sphere --intent "Create a sphere" \
  --blocker "Radius was ignored" --severity blocked \
  --dcc-type maya --instance-id <live-or-dead-instance-id> \
  --request-id <request-id>
```

Use `doctor` for profile, registry, daemon, binary, and readiness failures. For a tool failure, refresh `describe`, compare the schema/annotations with the attempt, inspect failure-only stats, and call the gateway-owned `feedback` command. Its severity is `blocked`, `workaround_found`, or `suggestion`; it remains available after the target instance exits, records a bounded entry in `resources://gateway/events`, and does not create an external issue. Instance-level `dcc_feedback__report` is the live-adapter Finding v1 entry point: supply phase, severity, intent, observed, expected, exactly one repro argv/steps list, and tool_slug or evidence.error_kind; Core fills runtime identity, fingerprint, and `needs-review` redaction state, forwards to the same gateway, and has no local-success fallback. A failed `DccServerBase.start()` also persists one `needs-review` startup Finding with no `request_id`; treat its exception-derived observed text as local evidence until reviewed and redacted. Review persisted reports newest first with `feedback list`, or request the largest bounded structured window with `feedback export`; both accept `--range`, `--dcc`, `--severity`, `--limit`, and `--json`. Treat `skipped_invalid` and `deduplicated` as source-set evidence, and treat any read or capacity error as an incomplete export.

When a Finding v1 file is available, use `feedback route` to resolve exact ownership offline; missing or conflicting catalog/Skill metadata fails closed, and the read-only result never authorizes issue creation. After human review sets `public-safe` and every exclusion flag, use `feedback bundle` for the bounded Finding, redacted doctor, version matrix, safe issue report, and exact-file host-error projection. If `install --execute --json` produced a terminal Install SOP v1 report, save its single stdout object and pass the regular non-symlink file with `--install-report`; the CLI caps it at 256 KiB, binds DCC/core/adapter identity to the Finding, and emits only public-safe fields. Raw input is validated against the published Draft 2020-12 schema before typed projection; `command` and `file_edit` are mutually exclusive. Public output redacts sensitive option/value pairs, relative or absolute report paths, and every URL scheme, and omits `file_edit.content` plus the input report path. Malformed, non-terminal, oversized, or mismatched reports fail closed; a missing report remains explicitly unavailable, and any unavailable component or `complete=false` means incomplete evidence. Then run `feedback file <finding> --json` without a decision to get a read-only dedup plan. Accept only one exact-fingerprint recommendation automatically; keyword-only, multiple, or truncated candidates require review. An external comment or create operation requires explicit user authorization and exact execution of the returned `next_step.argv`; never reconstruct it from `--existing`/`--create` or add `--yes` on the agent's own authority. The replay argv binds the canonical Finding path, canonical catalog path or exact bundled-catalog sentinel, Finding content SHA-256, fingerprint, repository, and catalog SHA-256; any drift, body above 65,536 Unicode scalar values, full-process-tree tracker timeout, or changed exact match fails closed before mutation. For a gateway-routed failure, use the CLI-returned `request_id` to read `/v1/debug/agent-traces/<request_id>` and public-safe `/v1/debug/issue-reports/<request_id>`. Never publish raw evidence without human review. Detailed flags and bounds are in the CLI cheatsheet.

Route schema/script/Skill defects to the owning package and `dcc-mcp-skills-creator`; dispatch/readiness/install/wiring defects to the adapter and `dcc-mcp-creator`; shared gateway/CLI/protocol defects to `dcc-mcp-core`. Include the smallest reproduction and safe report, not hidden reasoning.

### Review Reusable Friction

```bash
dcc-mcp-cli stats --range 24h --dcc-type maya --session-id task-42
```

Only after acceptance, inspect `stats_coverage`. Gateway SQLite excludes `local_mcp_direct`; `configured_route_recorded=false` cannot support reflection. Re-run through `--require-gateway`; zero calls means missing evidence.

Load `dcc-mcp-skills-creator` and request `review_skill_improvement` with bounded task, stats, validation, and existing-skill summaries. Stats are not root-cause proof; prefer `no_change`, then `update_existing`, and create only for a repeated stable workflow. The review never authorizes out-of-scope changes.
