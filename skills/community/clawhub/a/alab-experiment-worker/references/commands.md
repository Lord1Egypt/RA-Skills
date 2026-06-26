# ALab Experiment Worker Commands

## Invocation Prefix

Command snippets below use `alab`. If the launcher provides `ALAB_CMD_PREFIX`, invoke ALab through that prefix exactly as instructed instead of hard-coding `alab`. Do not print, inspect, or rewrite launcher-provided credential material. Use only the current worktree's token context; do not accept root keys, project admin keys, or tokens for other worktrees.

## Allowed Surface

Use these commands from inside an active experiment worktree:

```text
alab status
alab help
alab feedback --kind suggestion|question|bug|other --body "<text>"
alab run --message "<message>"
alab submit --message "<message>" --summary "<text>" --feedback "<text>" --ref none
alab exp checkout <exp_id> --path <dir> [--commit final|latest|best|<sha>]
alab exp tag add|remove|list <exp_id> ...
alab report --exp <exp_id> --out <path> [--overwrite]
alab observe experiments list|search|show|best ...
alab observe runs list|show ...
alab observe artifacts list|show|export ...
alab observe logs list|show|export ...
alab observe annotations list|show ...
alab annotate add|edit|archive|unarchive ...
```

Worker lifecycle permissions are intentionally narrow:

- `run` and `submit` require the valid worktree token from the current experiment.
- A worker session should use the current worktree's token file when available. If a token is supplied explicitly, it must match this worktree or inspection checkout.
- Observe commands show only items visible to the current token.
- `exp checkout` can create an inspection checkout only for experiments visible to the current token.
- Experiment tags are labels only; they never expand visibility.
- Hidden logs require root/admin and are outside this skill.
- Worker annotation mutation is limited to visible targets and annotations created by the worker token.
- Project-level or root-required operations should be reported to a project-level session with the project admin key or to a root-admin session; do not request those keys in the worker session.

## Function Details

Each entry lists the function, purpose, important parameters, and how to use the result.

- **`alab status`**: Check the current experiment/project state and next action hint.
  Parameters: Optional `--project <project_id>` only when explicitly provided by a project-level session; normally run without flags in the worktree.
  Use the output for: Confirm context type, project id, experiment id, project status, experiment status, and whether work can continue.
- **`alab help`**: Inspect the commands available to the current worktree token.
  Parameters: `--all --explain` may show locked commands and safe reasons.
  Use the output for: Avoid trying admin/root commands and identify available observe or annotation commands.
- **`alab feedback`**: Leave a HOME-level local note for tooling suggestions, questions, bugs, or other agent observations.
  Parameters: Exactly one of `--body <text>` or `--body-file <path>`; optional `--kind suggestion|question|bug|other` and `--title <text>`.
  Use the output for: The stored feedback id and file paths under `ALAB_HOME/feedback/`. Use this for ALab/tooling feedback, not for experiment submission summaries.
- **`alab run`**: Evaluate the current candidate and save run evidence.
  Parameters: Required `--message <text>`; keep it short and specific.
  Use the output for: Run id, status, reward, parse status, warnings, previews, artifact count, and next action.
  Notes: Reward files should contain only parseable numeric metrics expected by the configured reward parser. Keep explanatory details in separate artifacts or visible logs; worker tokens cannot inspect hidden verifier logs. In free evaluation projects, `alab run` returns `COMMAND_UNAVAILABLE`; use direct submit instead.
- **`alab submit`**: Close the experiment with final summary and feedback after a supporting passed run.
  Parameters: Required `--message`, one of `--summary`/`--summary-file`, one of `--feedback`/`--feedback-file`, and at least one `--ref`; optional `--rerun`.
  Use the output for: Final run id, final commit, stored summary/feedback, experiment status, and submitted refs.
  Notes: Standard evaluation projects require a supporting passed run or `--rerun` to create one. Free evaluation projects do not have an evaluator; omit `--rerun`, submit directly, and expect `final run id: none`.
- **`alab exp checkout`**: Create an inspection checkout of a visible historical experiment at a selected commit.
  Parameters: Required `<exp_id>` and `--path <dir>`; optional `--commit final|latest|best|<sha>`. Use an empty path outside the current worktree and other ALab contexts.
  Use the output for: A read-only comparison workspace from a visible prior experiment. Read it for useful task ideas, then copy only genuinely useful task-relevant source files or snippets into the current worktree. Do not copy `.alab/`, raw tokens, hidden assets, or project control files. Record any inspection path you create so a project-level session can clean it up later; do not edit inside inspection checkouts.
- **`alab exp tag add|remove|list`**: Add or inspect tags on the current experiment.
  Parameters: `add`/`remove` require `<exp_id> <tag>`; `list` requires `<exp_id>`.
  Use the output for: Marking useful worker-local evidence such as `promising`, `needs-review`, or task-specific labels when the project-level session expects tags. Tags are not authorization and should not replace submit refs.
- **`alab report`**: Export a Markdown report for a visible experiment.
  Parameters: Required `--exp <exp_id> --out <path>`; optional `--overwrite`. In a worktree context, `--project` is usually supplied by the context.
  Use the output for: A local handoff/evidence file containing safe details, runs, submission text, and visible artifact/log summaries. Worker reports cannot include hidden logs, raw secrets, tokens, or artifact bytes.
- **`observe experiments list`**: See visible experiments in the project.
  Parameters: Filters include `--status`, repeated `--tag`, `--source-id`, `--name-query`, reward bounds, config version, timestamps, and `--include-archived`; pagination uses `--limit`/`--offset`; sorting uses `--sort <field>:<asc|desc>`.
  Use the output for: Find prior attempts, similar tags, source lineage, closed experiments, and possible refs.
- **`observe experiments search`**: Search visible experiment corpus for ideas or prior failures.
  Parameters: Required `--query <text>` plus the same main experiment filters as list.
  Use the output for: Locate relevant summaries, feedback, task text, names, goals, tags, latest annotation titles, and latest annotation bodies.
- **`observe experiments show`**: Inspect one visible experiment.
  Parameters: Required `<exp_id>`.
  Use the output for: Confirm source ref, latest/final/best commits, tags, status, and whether it should be cited as a ref.
- **`observe experiments best`**: Find visible experiments ranked by reward policy.
  Parameters: Optional experiment filters; no custom sort.
  Use the output for: Identify strong baselines or inspiration candidates while respecting incomparable-run warnings.
- **`observe runs list`**: Inspect visible run history.
  Parameters: Filters include `--exp`, `--status`, `--config-version`, `--commit`, reward bounds, `--runner-type`, `--exit-code`, `--failure-reason-query`, timestamps, and `--include-archived`.
  Use the output for: Compare candidate quality, find failure modes, or inspect current experiment runs.
- **`observe runs show`**: Inspect one visible run.
  Parameters: Required `<run_id>`.
  Use the output for: Read reward, parse status, warning codes, stdout/stderr previews, artifact count, hidden-log availability, and timestamps.
- **`observe artifacts list/show/export`**: Inspect or export visible captured artifacts.
  Parameters: List filters include `--exp`, `--run`, `--validation`, `--root workspace|run`, `--status`, `--path-query`, `--content-hash`, size bounds, timestamps, and `--include-archived`; export requires `<artifact_id> --out <path>` and optional `--overwrite`/`--include-archived`.
  Use the output for: Examine outputs, generated reports, or files that explain prior results. Artifact bytes are not guaranteed to be secret-redacted; inspect only what is needed and do not paste raw artifact contents into final feedback unless it is clearly safe and relevant.
- **`observe logs list/show/export`**: Inspect or export visible logs.
  Parameters: List filters include `--exp`, `--run`, `--validation`, `--stream stdout|stderr|hidden_stdout|hidden_stderr`, `--truncated`, timestamps, and archive flags. Worker tokens cannot use hidden logs.
  Use the output for: Diagnose failures using visible stdout/stderr content and previews. Quote only short, relevant visible snippets in summaries; never request or reproduce hidden-log content in the worker session.
- **`observe annotations list/show`**: Read visible notes and review comments.
  Parameters: List filters include `--target-type`, `--target-id`, `--author`, `--created-by`, `--private`, `--query`, timestamps, and `--include-archived`; show accepts `<annotation_id>` and optional `--history`. Use `--target-type none` to find targetless notes.
  Use the output for: Capture prior guidance, known issues, and rationale attached to experiments, runs, or artifacts.
- **`annotate add/edit/archive/unarchive`**: Add or maintain worker-visible notes.
  Parameters: `add` accepts an optional `--target <target>` and one of `--body`/`--body-file`; targetless notes require `--title <title>` and bind to the current experiment. Targeted notes may also use `--title`. Optional `--author` and `--private` are available. `edit` requires `<annotation_id>` and one body input. Archive/unarchive require `<annotation_id>`.
  Use the output for: Leave useful evidence for later workers without changing project configuration. Common targets are `exp:<exp_id>`, `run:<run_id>`, `artifact:<artifact_id>`, `path:<repo_path>`, `lines:<repo_path>:<start>-<end>`, `path:<exp_id>@<commitish>:<repo_path>`, and `lines:<exp_id>@<commitish>:<repo_path>:<start>-<end>`. Omit `--target` and provide `--title` for a current-experiment note that is not tied to one object or path. In experiment context, path/line shorthand requires a clean worktree. Do not use admin/root-only `--exp` from the worker session.

## Working Flow

```text
alab status
alab help
alab observe experiments best
alab observe experiments search --query "<keyword>"
# edit task-relevant source
git status --short
alab run --message "try focused improvement"
alab observe runs show <run_id>
```

This is an example shape, not a required sequence. Start by understanding the current task, candidate, and context. Use visible history only when it can inform the change. Keep local checks cheap and task-specific. Run `alab run --message "<brief reason>"` when a standard evaluation candidate is ready, diagnose weak or failed results from visible evidence, and keep iterating while there is a plausible improvement path. In free evaluation projects, ALab points directly to submit and no run evidence is expected. If `git status --short` shows unrelated generated files, remove or ignore them through normal project mechanisms before running or submitting.

Submit only when the work is complete or further useful optimization is exhausted and either a passed run supports the final candidate in standard mode or free evaluation direct submit is the expected mode. If no passed run supports a standard evaluation candidate, report the best run evidence and the reason no submit was performed.

## Visible History

Workers may use ALab observe commands to study visible historical experiments before deciding what to change:

```text
alab observe experiments list
alab observe experiments search --query "<keyword>"
alab observe experiments best
alab observe experiments show <exp_id>
alab observe runs list --exp <exp_id>
alab observe runs show <run_id>
alab observe artifacts list --exp <exp_id>
alab observe logs list --exp <exp_id>
alab observe annotations list --target-type experiment --target-id <exp_id>
```

Use visible history as evidence and inspiration, not as permission expansion. Prefer high-reward passed runs, useful warning patterns, clear annotations, and comparable task/source lineage. Submit refs are provenance links for later review and optimization: if a prior experiment influenced the final strategy, source changes, comparison baseline, failure avoidance, or continuation path, include it with repeated `--ref <exp_id>`.

When a visible experiment looks potentially useful, inspect its task-relevant files instead of relying only on summaries:

```text
alab exp checkout <exp_id> --path /tmp/alab-inspect-<exp_id> --commit best
```

Use `best` for reward-led exploration, `final` to inspect a submitted candidate, and `latest` when the current branch tip is what matters. Record the `inspection commit` rendered by `exp checkout`; use it for normal Git comparisons from the current worktree:

```text
git diff --stat <inspection_commit>..HEAD
git diff <inspection_commit> -- <path>
```

For direct file or subtree comparisons against the inspection checkout path, use `git diff --no-index` on task source paths only:

```text
git diff --no-index /tmp/alab-inspect-<exp_id>/<source_path> <current_worktree>/<source_path>
```

`git diff --no-index` returns exit code `1` when differences exist; treat that as useful comparison output, not as an ALab failure. Read and compare the checkout before copying anything. Copy only source content that advances the current task, adapt it to the current worktree, and keep the copied influence visible in the final `--ref <exp_id>` and feedback. Never copy `.alab/`, token files, ALab home/cache files, hidden evaluator assets, secret files, or project control files.

Inspection checkouts are comparison surfaces, not editable source surfaces. Keep their paths out of commits and final artifacts. If cleanup is needed, report the path to a project-level session unless `alab help` in the checkout context explicitly shows a self-removal command available to that inspection token.

## Forbidden Surface

Do not run these from the worker session:

```text
alab auth ...
alab key ...
alab project config ...
alab project env ...
alab project secret ...
alab project validate ...
alab project remove ...
alab source remove ...
alab catalog ...
alab cache prune ...
alab backup prune ...
alab audit ...
alab exp remove ...
alab exp worktree remove|restore ...
alab exp token ...
```

Also avoid direct file edits outside the current experiment worktree. If a launcher added ALab home/cache directories for CLI state, use them only through ALab commands.

If one of these is necessary, report the need to a project-level session or root-admin session.

## Evaluation Pattern

```text
alab status
alab run --message "try focused improvement"
alab observe runs show <run_id>
```

Use visible stdout/stderr previews, warning codes, artifacts, and logs for diagnosis. Do not ask for hidden evaluator logs unless the user explicitly switches you into an admin role. If the run fails because a needed admin/root operation is unavailable, stop and report the exact missing capability.

## Submit Pattern

Prepare summary and feedback in temporary files when they are more than one sentence:

```text
alab submit \
  --message "final candidate" \
  --summary-file /tmp/alab-summary.txt \
  --feedback-file /tmp/alab-feedback.txt \
  --ref none
```

Use `--ref none` only when no historical experiment materially influenced the result. Prefer explicit refs whenever visible experiments were used as inspiration, source continuation, comparison baselines, or failure examples:

```text
alab submit \
  --message "final candidate" \
  --summary-file /tmp/alab-summary.txt \
  --feedback-file /tmp/alab-feedback.txt \
  --ref <exp_id_that_inspired_or_was_continued> \
  --ref <another_relevant_exp_id>
```

The summary should describe the final change and supporting passed run. The feedback should include useful operational notes: key metrics, failure modes avoided, why each ref matters, and remaining risks. Clear ref explanations make it easier for later workers to inspect the lineage and continue optimization. Do not include raw tokens, hidden-log content, or inaccessible experiment ids.
In free evaluation mode, state that there is no evaluator run and that `final run id` is `none`.

The final worker response should include:

- changed strategy or source area,
- final run id and status, or `final run id: none` for free evaluation,
- reward and key metrics when present,
- submit refs used, or `ref none` with a reason,
- final commit if ALab rendered one,
- tags added, if any,
- inspection checkout paths created, if any,
- remaining risks or known failures.
