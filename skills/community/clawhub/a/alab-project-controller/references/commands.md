# ALab Project Controller Commands

## Recommended Admin Invocation

Use stdin for the project admin key:

```sh
printf '%s\n' "$ALAB_PROJECT_KEY" | alab --key-stdin project show --project "$ALAB_PROJECT_ID"
```

Do not use shell tracing while secrets are in environment variables. Do not include raw keys in prompts, run messages, summaries, or reports.

## Project-Scoped Surface

A project-level session using `alab-project-controller` may use same-project admin commands:

```text
alab project show|archive|unarchive ...
alab project locks clear-stale ...
alab status --project <project_id>
alab feedback --kind suggestion|question|bug|other --body "<text>"
alab report --project <project_id> [--exp <exp_id>] --out <path> [--overwrite]
alab key list --project <project_id>
alab project config show|export|import|set ...
alab project env set|unset|list ...
alab project secret set|unset|list|gc ...
alab project validate ...
alab project validation archive|unarchive|remove ...
alab source import|list|show|archive|unarchive|remove ...
alab exp create|list|search|show|best|archive|unarchive|remove ...
alab exp checkout ...
alab exp checkout remove ...
alab exp worktree remove|restore ...
alab exp token list|revoke|regenerate ...
alab exp tag add|remove|list ...
alab observe experiments|runs|artifacts|logs|annotations ...
alab annotate add|edit|archive|unarchive|remove ...
alab audit list|show --project <project_id> ...
```

## Function Details

Each entry lists the function, purpose, important parameters, and how to use the result.

- **`project show`**: Inspect one project summary.
  Parameters: Optional `--project <project_id>` when not already in project context.
  Notes: Use for project id, status, task, goal, active config version, default source, runner, reward, visibility, and public experiment policy.
- **`status`**: Get a safe current-state summary.
  Parameters: Optional `--project <project_id>`.
  Notes: Useful before creating worker sessions/subagents or when a context marker is ambiguous.
- **`feedback`**: Leave HOME-level local feedback about ALab behavior, runner issues, docs gaps, or project-operation questions.
  Parameters: Exactly one of `--body <text>` or `--body-file <path>`; optional `--kind suggestion|question|bug|other` and `--title <text>`.
  Notes: Use annotations for project-visible experiment notes; use feedback for local ALab/tooling feedback that should be stored under `ALAB_HOME/feedback/`.
- **`report`**: Export a Markdown evidence report for the project or one visible experiment.
  Parameters: Required `--out <path>` and `--project <project_id>` outside context; optional `--exp <exp_id>` and `--overwrite`.
  Notes: Project reports require admin/root authority. Experiment reports follow observe visibility. Reports include summaries and safe details, but not raw keys, tokens, raw secrets, hidden-log contents, or artifact bytes.
- **`project config show`**: Inspect config details.
  Parameters: Optional `--project`; `--version latest-attempted|active-valid|<n>`.
  Notes: Shows runner/reward/reference-metric/artifact/env/secret fingerprints without raw secret values. Free evaluation projects show `runner type: none` and `reward type: none`.
- **`project config export`**: Write a config snapshot to a file.
  Parameters: Required `--out <path>`; optional `--overwrite`, `--project`, `--version`.
  Notes: Use for review or controlled edits; export never writes raw secret values.
- **`project config import`**: Import a config file and optionally run baseline validation.
  Parameters: Required `--config <path>`; optional `--project`, `--dry-run`, `--skip-baseline-test`; `--dry-run` conflicts with skip.
  Notes: Dry-run parses, canonicalizes, diffs, and checks capabilities without saving changes or running an evaluator. A runtime-affecting free evaluation import with paired `runner.type = "none"` and `reward.type = "none"` sets `validation status: not_required` and becomes active valid without running a baseline evaluator.
- **`project config set`**: Change one non-secret config field.
  Parameters: Required `<field> <toml-literal>`; optional `--project`, `--dry-run`, `--skip-baseline-test`.
  Notes: Replaces whole array/map fields; secret fields must use `project secret`. Use `metrics.reference` to declare optional numeric run metrics for dashboard reference curves; this metadata does not change reward ranking. Do not use single-field `set` to switch into or out of free evaluation because runner and reward `none` must change atomically.
- **`project env set|unset|list`**: Manage plain environment values in project config.
  Parameters: `set <name> <value>`, `unset <name>`, or `list`; optional `--project`. Names must match environment-variable syntax.
  Notes: Values are rendered by `list`; use secrets for sensitive values.
- **`project secret set|unset|list|gc`**: Manage secret environment values and unreferenced secret bytes.
  Parameters: `set <name> --value-stdin|--value-file <path>`, `unset <name>`, `list`, or `gc --dry-run|--apply`; optional `--project`.
  Notes: Raw secret values are never rendered; input must be non-empty single-line UTF-8 without NUL bytes.
- **`project validate`**: Run the active project baseline validation.
  Parameters: Optional `--project <project_id>`.
  Notes: Produces validation id, status, reward, parse status, warning codes, and project status. Free evaluation configs show `validation status: not_required` without running an evaluator.
  Notes: For file and Harbor rewards, `reward.json` metrics must be finite numbers. Non-numeric details belong in artifacts or logs, not the reward metrics object. Declared `metrics.reference` names are optional per run and are plotted only when a run records a matching numeric metric.
- **`project validation archive|unarchive|remove`**: Maintain validation entries and their dependent logs/artifacts.
  Parameters: Required `<validation_id>`; remove requires `--dry-run` or `--force --confirm <validation_id>`, optional `--cascade`, `--reason`, `--project`.
  Notes: Archive active validations is blocked; dry-run before remove.
- **`project locks clear-stale`**: Clear stale project locks.
  Parameters: Optional `--project <project_id>`.
  Notes: Use only for stale locks; output lists cleared lock names and audit id.
- **`source import`**: Add a reusable source snapshot.
  Parameters: Exactly one of `--source-path`, `--source-git`, `--source-empty`; optional `--source-subdir`, `--name`, source size limits, `--project`.
  Notes: Imports are canonical source refs; source limits must be non-negative.
- **`source list|show`**: Inspect sources.
  Parameters: `show` requires `<source_id>`; optional `--project`, `--include-archived` for list.
  Notes: Use to choose source refs for new experiments and verify origin summaries.
- **`source archive|unarchive|remove`**: Maintain project sources.
  Parameters: Required `<source_id>`; remove requires `--dry-run` or `--force --confirm <source_id>`, optional `--cascade`, `--reason`, `--project`.
  Notes: Active/default or referenced sources can block archive/remove.
- **`exp create`**: Create a new experiment worktree and token.
  Parameters: Required `--name`; optional `--project`, `--goal`, `--path`, repeated `--tag`, `--source-ref`, `--source-path`, `--source-git`, `--source-empty`, `--from-exp`, `--from-commit latest|final|best|<sha>`, mutable include/exclude, visibility options.
  Notes: At most one source origin. Raw worktree token is written to token path and never printed.
- **`exp list|search|show|best`**: Inspect and rank project experiments.
  Parameters: Search requires `--query`; filters include status, tags, source id, name query, reward bounds, config version, timestamps, archive flag, pagination, and sorting where supported.
  Notes: Use to pick predecessors, refs, and worker targets. Free evaluation submissions have no run/reward evidence and do not qualify for `best` ranking.
- **`exp archive|unarchive|remove`**: Maintain experiment lifecycle.
  Parameters: Required `<exp_id>`; remove requires `--dry-run` or `--force --confirm <exp_id>`, optional `--cascade`, `--reason`, `--project`.
  Notes: Remove is archive-first and may stage worktrees, inspection paths, logs, artifacts, and branch refs through trash.
- **`exp checkout`**: Create an inspection checkout for a visible experiment commit.
  Parameters: Required `<exp_id> --path <dir>`; optional `--commit final|latest|best|<sha>`, `--project`.
  Notes: Writes an inspection token to token path and never prints it.
- **`exp checkout remove`**: Remove an inspection checkout.
  Parameters: Exactly one of `--token-id` or `--path`; plus `--dry-run` or `--force --confirm <token_id-or-path-hash>`; optional `--project`, `--reason`.
  Notes: Can reconcile already-missing paths; uses trash staging.
- **`exp worktree remove|restore`**: Remove or restore submit-capable worktrees.
  Parameters: Remove requires `<exp_id>` plus `--dry-run` or `--force --confirm <exp_id>`; restore requires `<exp_id> --path <dir>`; optional `--project`.
  Notes: Remove revokes the active worktree token; restore writes a replacement token and never prints it.
- **`exp token list|revoke|regenerate`**: Inspect or replace experiment tokens.
  Parameters: Required `<exp_id>`; selectors `--token-id`, `--mode worktree|inspection`, or `--all`.
  Notes: Regenerate writes the raw token to the registered path and never prints it.
- **`exp tag add|remove|list`**: Manage experiment labels.
  Parameters: Required `<exp_id>`; add/remove also require tag text.
  Notes: Use tags for search, grouping worker sessions/subagents, and comparing related attempts.
- **`observe experiments|runs|artifacts|logs|annotations`**: Read or maintain project-visible evidence.
  Parameters: See observe filters: experiment/runs/artifacts/logs/annotations list filters, `show <id>`, export `--out`, archive/unarchive, and admin-only remove with dry-run/confirm.
  Notes: Hidden logs require root/admin and explicit `--include-hidden`; use observe outputs as evidence for decisions.
- **`annotate add|edit|archive|unarchive|remove`**: Add or maintain project notes.
  Parameters: `add` accepts optional `--target` and one body input. Targetless notes require `--title <title>` plus `--exp <exp_id>` from project context; targeted notes may also use `--title`. Optional `--author`, `--private`, and `--private-to-exp` are available. Edit requires annotation id and body; remove requires dry-run or force/confirm.
  Notes: Use for decision notes, review notes, and project-visible guidance. Omit `--target` only for experiment-scoped notes that are not tied to one object or path.
- **`audit list|show --project`**: Inspect project-scoped audit evidence.
  Parameters: Filters include `--object-type`, `--object-id`, `--action`, `--actor`, time bounds, `--limit`, and `--offset`; show requires `<audit_id>`.
  Notes: Use to verify lifecycle, credential, config, source, validation, and cleanup actions.

Use remove commands conservatively:

- Run `--dry-run` first.
- Require exact `--force --confirm <id>` only after the blocker list is understood.
- Archive targets before hard removal when the command requires archive-first deletion.

## Forbidden Global Surface

A project-level session using `alab-project-controller` must not run root-only commands:

```text
alab auth init
alab auth root regenerate
alab dashboard
alab feedback list|show|archive
alab key create
alab key list --root
alab key revoke
alab project init
alab project remove
alab catalog skydiscover add|update|show|remove
alab cache prune
alab backup prune
```

`alab key list --project <project_id>` is acceptable for same-project inspection when the admin key permits it. Creating or revoking admin keys is a global-admin task.

## Experiment Creation Patterns

Create the experiment first, then use the worktree path from `exp create` for worker handoff. The detailed session/subagent launch requirements live in [Worker Launch Pattern](#worker-launch-pattern).

Keep credentials layer-specific: use the project admin key only for `exp create` and other project-level commands; do not pass it to the experiment worker context.

Default source:

```sh
printf '%s\n' "$ALAB_PROJECT_KEY" | alab --key-stdin exp create \
  --project "$ALAB_PROJECT_ID" \
  --name "$EXPERIMENT_NAME"
```

Continue from a prior best commit:

```sh
printf '%s\n' "$ALAB_PROJECT_KEY" | alab --key-stdin exp create \
  --project "$ALAB_PROJECT_ID" \
  --name "$NEXT_EXPERIMENT_NAME" \
  --from-exp "$SOURCE_EXP_ID" \
  --from-commit best
```

## Worker Launch Pattern

Use this pattern after `exp create` has produced a worktree path. For environments that support creating a new thread/session, prefer that path over running the worker inline in the current project-level session. Different agent launchers use different parameters, so treat the following as launch requirements rather than a literal command:

- Set the worker session/thread or subagent working directory or target context to the experiment worktree path.
- Provide the `alab-experiment-worker` skill/instructions to the worker session/thread or subagent.
- Provide the worker prompt through the launcher's normal private prompt channel, not through a file committed to the source tree.
- Clear admin/root credentials and unrelated ambient tokens from the worker environment. This is equivalent to unsetting `ALAB_PROJECT_KEY`, `ALAB_ROOT_KEY`, `ALAB_KEY`, and any unrelated `ALAB_TOKEN`.
- In shells, the prefix `env -u ALAB_PROJECT_KEY -u ALAB_ROOT_KEY -u ALAB_KEY -u ALAB_TOKEN ...` expresses this cleanup by launching the following process with those variables removed; adapt the same cleanup to non-shell session launchers.
- Let the worker use only the experiment token context for that worktree, preferably the token file already present in the worktree.
- If `ALAB_CMD_PREFIX` is needed so the worker can invoke the correct ALab binary, pass only that non-secret command prefix.

If the worker must run ALab from a sandbox and ALab home/cache are outside the worktree, add only the required non-secret state directories:

```text
--add-dir "$ALAB_EXAMPLE_HOME"
--add-dir "$UV_CACHE_DIR"
--add-dir "$PYTHONPYCACHEPREFIX"
--add-dir "$ALAB_SHARED_DIR"
```

Do not use the repository root as `-C` for a worker. Do not pass the project admin key through argv, stdin prompt text, copied files, inherited environment, `--add-dir "$RUN_DIR"`, `.run/secrets`, or `project.env`. Clear unrelated ambient token variables before launch; an experiment worker session should use only the token context for its own worktree.
Before launching, resolve the worktree path and refuse repo root, the whole `.run` directory, or any secret/control path. Tell worker sessions/subagents that added ALab home/cache/shared directories are CLI state only, not source-editing surfaces.

## Closeout Report

A project-level final report should include:

- project id and active config version,
- experiments created or reused,
- best experiment, run id, reward, parse status, and commit,
- for free evaluation projects, final commits and `final run id: none` submissions instead of best reward evidence,
- worker failures and skipped steps,
- report or artifact paths that are safe to share.
