# ALab Global Admin Commands

## Recommended Root Invocation

Use stdin for root key commands:

```sh
printf '%s\n' "$ALAB_ROOT_KEY" | alab --key-stdin key list --root
```

Disable shell tracing and redact command transcripts before sharing. Use ignored local files for generated keys.

## Root Surface

Global admins may use:

```text
alab auth init
alab auth root regenerate
alab config show|set|reset|validate
alab feedback --kind suggestion|question|bug|other --body "<text>"
alab feedback list|show|archive ...
alab dashboard [--port <0-65535>] [--no-open] [--refresh-seconds <0-3600>]
alab report --project <project_id> [--exp <exp_id>] --out <path> [--overwrite]
alab key create --project <project_id> --role admin
alab key list --root
alab key list --project <project_id>
alab key revoke <key_id>
alab context show|repair
alab project init local|git|empty|harbor|skydiscover ...
alab project list|show|archive|unarchive|remove ...
alab catalog skydiscover add|update|show|remove ...
alab cache prune ...
alab backup prune ...
alab audit list|show ...
```

## Function Details

Each entry lists the function, purpose, important parameters, and how to use the result.

- **`auth init`**: Create a new ALab home and root key.
  Parameters: Optional `--home <path>`; no credential required.
  Notes: Prints the raw root key exactly once; store it only in an ignored or secure location.
- **`auth root regenerate`**: Replace the active root key.
  Parameters: Use root credential through global `--key-stdin` or equivalent secure input.
  Notes: Revokes the previous root verifier and prints the replacement root key exactly once.
- **`config show`**: Inspect ALab home-level config and validity.
  Parameters: No required args.
  Notes: Shows home config values and validity.
- **`config set`**: Change one ALab home-level setting.
  Parameters: Required `<field> <toml-literal>`; use `alab help` or `config show` to confirm allowed fields.
  Notes: `output.format` only accepts TOML string `"text"`.
- **`config reset`**: Reset one home-level setting or all config.
  Parameters: Required `<field>` or `--all`.
  Notes: Use to recover from bad local config values; no root key required.
- **`config validate`**: Validate home config and optionally refresh runtime capability checks.
  Parameters: Optional `--refresh-capabilities`.
  Notes: Use before Docker/runner-sensitive work or after environment changes. Unsupported/error capability results include an actionable `next` remediation and should be refreshed again after the local runtime is fixed.
- **`feedback`**: Leave HOME-level feedback about ALab operation, docs, environment issues, or bugs.
  Parameters: Exactly one of `--body <text>` or `--body-file <path>`; optional `--kind suggestion|question|bug|other` and `--title <text>`.
  Notes: Feedback is local home-level text and does not affect project evidence.
- **`feedback list|show|archive`**: Inspect and archive HOME-level feedback.
  Parameters: `list` accepts optional `--kind`, `--query`, `--limit`, `--offset`, and `--include-archived`; `show` requires `<feedback_id>`; `archive` requires `<feedback_id>` and optional `--reason <text>`.
  Notes: Root-only. Archive is idempotent and does not affect project evidence.
- **`dashboard`**: Open the root-only local read-only dashboard.
  Parameters: Optional `--port <0-65535>`, `--refresh-seconds <0-3600>`, and `--no-open`.
  Notes: Requires root credential, binds only to `127.0.0.1`, renders a token URL, and blocks until interrupted. Do not share the token URL; the dashboard can read hidden/full logs and artifacts but must not mutate ALab state.
- **`report`**: Export a Markdown project or experiment evidence report.
  Parameters: Required `--project <project_id>` and `--out <path>`; optional `--exp <exp_id>` and `--overwrite`.
  Notes: Root can export project-wide or experiment-scoped reports. Reports intentionally omit raw keys, tokens, secret values, hidden-log contents, and artifact bytes.
- **`key create`**: Create a project admin key for a project-level session.
  Parameters: Required `--project <project_id>`; optional `--role admin`.
  Notes: Root-only; prints raw admin key exactly once.
- **`key list --root`**: Inspect root credentials.
  Parameters: Required `--root`; conflicts with `--project`.
  Notes: Use to confirm active/revoked root credential ids without exposing raw keys.
- **`key list --project`**: Inspect project admin credentials.
  Parameters: Required `--project <project_id>` unless project context supplies it.
  Notes: Root/admin may inspect project credentials; does not render raw admin keys.
- **`key revoke`**: Revoke a credential by id.
  Parameters: Required `<key_id>`; optional `--project <project_id>`.
  Notes: Root-only for revocation; do not revoke the wrong active key without checking audit and scope.
- **`context show`**: Inspect path context markers and registered ALab paths.
  Parameters: Optional `--path <dir>`; default `.`.
  Notes: Use before repair or when a command is running in an unexpected project/experiment/inspection context.
- **`context repair`**: Repair a path context marker when authorized.
  Parameters: Required `--path <dir>`.
  Notes: Root/admin can repair in scope; token self-repair has strict Git branch or pinned-commit checks.
- **`project init`**: Create a project, source, config version, baseline validation, and project admin key.
  Parameters: Mode `local|git|empty|harbor|skydiscover`; required `--config`; common `--name`, `--task`, `--goal`, `--skip-baseline-test`; mode-specific source/task fields; source size limits.
  Notes: Runtime behavior comes from config only. Generated project admin key is printed once after the project is created.
- **`project list|show`**: Inspect projects.
  Parameters: `list` accepts `--include-archived`; `show` accepts optional `--project <project_id>`.
  Notes: Use to find project ids, statuses, active config version, default source, runner, reward, and visibility.
- **`project archive|unarchive`**: Toggle project lifecycle status.
  Parameters: Optional `--project <project_id>`.
  Notes: Archive can be blocked by active locks or maintenance.
- **`project remove`**: Remove an archived project by audited cascade.
  Parameters: Required `--cascade`; plus `--dry-run` or `--force --confirm <project_id>`; optional `--project`, `--reason`.
  Notes: Root-only and destructive. Always dry-run first; actual remove moves removable paths through ALab trash.
- **`catalog skydiscover add|update`**: Install or change the pinned SkyDiscover catalog.
  Parameters: Optional `--origin-url <url>`; exactly zero or one of `--ref <ref>` or `--commit <full_sha>`.
  Notes: Prefer `--commit` when reproducibility matters. `update` requires a clean ALab-managed catalog.
- **`catalog skydiscover show`**: Inspect active SkyDiscover catalog state.
  Parameters: No catalog selector needed.
  Notes: Must not fetch from the network; use to confirm pinned commit and local path.
- **`catalog skydiscover remove`**: Remove active SkyDiscover catalog state and local checkout.
  Parameters: Required `--force --confirm skydiscover`; optional `--reason`.
  Notes: Blocked while active configs or open experiments reference the catalog.
- **`cache prune`**: Remove ALab-owned non-authoritative caches.
  Parameters: Selectors: `--docker-images`, `--skydiscover-envs`, `--trash --older-than <days>`, `--trash-all`, or `--all`.
  Notes: `--all` conflicts with individual selectors; trash retention days must be non-negative.
- **`backup prune`**: Remove old pre-upgrade backups.
  Parameters: Exactly one of `--keep <n>` or `--older-than <days>`.
  Notes: Retention values must be zero or greater; output includes pruned paths and audit id.
- **`audit list`**: Search global or project-scoped audit events.
  Parameters: Optional `--project`, `--object-type`, `--object-id`, `--action`, `--actor`, time bounds, `--limit`, `--offset`.
  Notes: Root can query globally; project admin is scoped to the project.
- **`audit show`**: Inspect one audit event and redacted details.
  Parameters: Required `<audit_id>`; optional `--project <project_id>`.
  Notes: Use to verify credential, project, catalog, cleanup, repair, and remove actions without raw secrets.

Root can also inspect or maintain project-scoped resources when needed, but should delegate normal experiment coordination to a project-level session with the project admin key and `alab-project-controller` skill/instructions.

## Project Initialization

After `project init` succeeds, treat the printed project admin key as handoff material. Keep this session focused on root-scoped setup, credentials, catalogs, cleanup, audit, and handoff unless the user explicitly asks otherwise.

Use the layer-specific credential rules from `SKILL.md`: project-level work receives only the project admin key and `alab-project-controller` skill/instructions; experiment work receives only the experiment worktree token context and `alab-experiment-worker` skill/instructions.

Local project:

```sh
printf '%s\n' "$ALAB_ROOT_KEY" | alab --key-stdin project init local \
  --config alab.project.toml \
  --source-path . \
  --name "$PROJECT_NAME" \
  --task "$TASK"
```

SkyDiscover project:

```sh
printf '%s\n' "$ALAB_ROOT_KEY" | alab --key-stdin catalog skydiscover add --commit "$SKYDISCOVER_COMMIT"

printf '%s\n' "$ALAB_ROOT_KEY" | alab --key-stdin project init skydiscover \
  --config alab.project.toml \
  --name "$PROJECT_NAME" \
  --task "$TASK"
```

`project init` prints the generated project admin key exactly once after the project is created. Capture it into an ignored local secret file, such as an example `.run/secrets/project.env`, or an approved secret store. Pass only the project admin key to the delegated project-level session, never to experiment workers.
Configs with paired `runner.type = "none"` and `reward.type = "none"` create free evaluation projects for direct submit without baseline evaluator runs; use them only with `local`, `git`, or `empty` project init modes, not Harbor or SkyDiscover adapter init.
Configs may also declare `metrics.reference` entries for optional numeric run metrics that the dashboard plots as reference curves; these declarations do not affect reward ranking or baseline execution.

## Catalog Rules

- Pin SkyDiscover with `--commit` when reproducibility matters.
- `catalog skydiscover show` must not fetch from the network.
- Missing catalog paths do not auto-update.
- `catalog skydiscover remove` is blocked while active configs or open experiments reference the catalog.

## Cleanup Rules

Use cleanup only for non-authoritative data:

```text
alab cache prune --docker-images
alab cache prune --skydiscover-envs
alab cache prune --trash --older-than <days>
alab cache prune --trash-all
alab cache prune --all
alab backup prune --keep <n>
alab backup prune --older-than <days>
```

For destructive project or lifecycle removal, run dry-run first, review blockers, then require exact confirmation.

## Handoff

A global admin handoff should include:

- ALab home path and home id when safe,
- project id, project name, and active config version,
- generated project admin key delivery path or confirmation that it was handed off through an ignored/secure secret location,
- follow-up session/thread or subagent handoff target when further project or experiment work remains,
- matching ALab skill/instructions provided to that target (`alab-project-controller` for project-level work, `alab-experiment-worker` for experiment worktree work),
- credential delivery path or secure-channel note for any delegated session that needs a key/token,
- catalog pinned commit when applicable,
- validation id and validation status,
- cleanup or audit actions performed.
