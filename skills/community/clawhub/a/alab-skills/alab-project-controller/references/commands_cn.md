# ALab Project Controller Commands

## 推荐的 Admin Invocation

通过 stdin 传递 project admin key：

```sh
printf '%s\n' "$ALAB_PROJECT_KEY" | alab --key-stdin project show --project "$ALAB_PROJECT_ID"
```

环境变量中有 secrets 时不要打开 shell tracing。不要把 raw keys 写入 prompts、run messages、summaries 或 reports。

## Project-Scoped Surface

使用 `alab-project-controller` 的 project-level session 可以使用 same-project admin commands：

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

## 功能明细

每项说明功能、作用、关键参数和输出/注意点。

- **`project show`**：查看单个 project summary。
  关键参数：不在 project context 中时使用可选 `--project <project_id>`。
  注意点：用于确认 project id、status、task、goal、active config version、default source、runner、reward、visibility 和 public experiment policy。
- **`status`**：获取安全的当前状态 summary。
  关键参数：可选 `--project <project_id>`。
  注意点：创建 worker sessions/subagents 前或 context marker 不明确时很有用。
- **`feedback`**：为 ALab behavior、runner issues、docs gaps 或 project-operation questions 留 HOME-level local feedback。
  关键参数：`--body <text>` 或 `--body-file <path>` 二选一；可选 `--kind suggestion|question|bug|other` 和 `--title <text>`。
  注意点：project-visible experiment notes 用 annotations；local ALab/tooling feedback 用 feedback，存储在 `ALAB_HOME/feedback/`。
- **`report`**：导出 project 或一个 visible experiment 的 Markdown evidence report。
  关键参数：必须提供 `--out <path>`；不在 context 中时提供 `--project <project_id>`；可选 `--exp <exp_id>` 和 `--overwrite`。
  注意点：Project report 要求 admin/root authority。Experiment report 遵循 observe visibility。Report 包含 summaries 和 safe details，但不包含 raw keys、tokens、raw secrets、hidden-log contents 或 artifact bytes。
- **`project config show`**：查看 config details。
  关键参数：可选 `--project`；`--version latest-attempted|active-valid|<n>`。
  注意点：显示 runner/reward/reference-metric/artifact/env/secret fingerprints，但不显示 raw secret values。Free evaluation projects 会显示 `runner type: none` 和 `reward type: none`。
- **`project config export`**：将 config snapshot 写入文件。
  关键参数：必需 `--out <path>`；可选 `--overwrite`、`--project`、`--version`。
  注意点：用于 review 或受控编辑；export 永不写出 raw secret values。
- **`project config import`**：导入 config file，并按需运行 baseline validation。
  关键参数：必需 `--config <path>`；可选 `--project`、`--dry-run`、`--skip-baseline-test`；`--dry-run` 与 skip 冲突。
  注意点：Dry-run 会 parse、canonicalize、diff 并检查 capabilities，不保存更改，也不运行 evaluator。Runtime-affecting free evaluation import 如果成对设置 `runner.type = "none"` 和 `reward.type = "none"`，会设置 `validation status: not_required`，不运行 baseline evaluator，并成为 active valid config。
- **`project config set`**：修改一个 non-secret config field。
  关键参数：必需 `<field> <toml-literal>`；可选 `--project`、`--dry-run`、`--skip-baseline-test`。
  注意点：Array/map 字段整体替换；secret fields 必须用 `project secret`。使用 `metrics.reference` 声明 dashboard reference curves 使用的 optional numeric run metrics；该 metadata 不改变 reward ranking。不要用单字段 `set` 切入或切出 free evaluation，因为 runner 和 reward 的 `none` 必须原子更新。
- **`project env set|unset|list`**：管理 project config 中的 plain environment values。
  关键参数：`set <name> <value>`、`unset <name>` 或 `list`；可选 `--project`。名称必须符合 environment-variable 语法。
  注意点：`list` 会渲染 values；敏感值应使用 secrets。
- **`project secret set|unset|list|gc`**：管理 secret environment values 和 unreferenced secret bytes。
  关键参数：`set <name> --value-stdin|--value-file <path>`、`unset <name>`、`list` 或 `gc --dry-run|--apply`；可选 `--project`。
  注意点：Raw secret values 永不渲染；输入必须是非空 single-line UTF-8，且无 NUL bytes。
- **`project validate`**：运行 active project baseline validation。
  关键参数：可选 `--project <project_id>`。
  注意点：输出 validation id、status、reward、parse status、warning codes 和 project status。Free evaluation configs 会显示 `validation status: not_required`，不运行 evaluator。
  注意点：对于 file 和 Harbor rewards，`reward.json` metrics 必须是 finite numbers。非 numeric details 应放入 artifacts 或 logs，而不是 reward metrics object。声明的 `metrics.reference` names 对每个 run 都是 optional，只有 run 记录了 matching numeric metric 时才绘制。
- **`project validation archive|unarchive|remove`**：维护 validation entries 及其 dependent logs/artifacts。
  关键参数：必需 `<validation_id>`；remove 需要 `--dry-run` 或 `--force --confirm <validation_id>`，可选 `--cascade`、`--reason`、`--project`。
  注意点：Active validation 不能 archive；remove 前先 dry-run。
- **`project locks clear-stale`**：清理 stale project locks。
  关键参数：可选 `--project <project_id>`。
  注意点：只用于 stale locks；输出 cleared lock names 和 audit id。
- **`source import`**：添加 reusable source snapshot。
  关键参数：`--source-path`、`--source-git`、`--source-empty` 三选一；可选 `--source-subdir`、`--name`、source size limits、`--project`。
  注意点：Imports 会生成 canonical source refs；source limits 必须是非负数。
- **`source list|show`**：查看 sources。
  关键参数：`show` 需要 `<source_id>`；list 可选 `--project`、`--include-archived`。
  注意点：用于选择新 experiments 的 source refs，并验证 origin summaries。
- **`source archive|unarchive|remove`**：维护 project sources。
  关键参数：必需 `<source_id>`；remove 需要 `--dry-run` 或 `--force --confirm <source_id>`，可选 `--cascade`、`--reason`、`--project`。
  注意点：Active/default 或 referenced sources 可能阻止 archive/remove。
- **`exp create`**：创建新的 experiment worktree 和 token。
  关键参数：必需 `--name`；可选 `--project`、`--goal`、`--path`、重复 `--tag`、`--source-ref`、`--source-path`、`--source-git`、`--source-empty`、`--from-exp`、`--from-commit latest|final|best|<sha>`、mutable include/exclude、visibility options。
  注意点：最多一个 source origin。Raw worktree token 写入 token path，永不打印。
- **`exp list|search|show|best`**：查看并排序 project experiments。
  关键参数：Search 需要 `--query`；filters 包括 status、tags、source id、name query、reward bounds、config version、timestamps、archive flag、pagination，以及支持处的 sorting。
  注意点：用于选择 predecessors、refs 和 worker targets。Free evaluation submissions 没有 run/reward evidence，不会进入 `best` ranking。
- **`exp archive|unarchive|remove`**：维护 experiment lifecycle。
  关键参数：必需 `<exp_id>`；remove 需要 `--dry-run` 或 `--force --confirm <exp_id>`，可选 `--cascade`、`--reason`、`--project`。
  注意点：Remove 是 archive-first，可能把 worktrees、inspection paths、logs、artifacts 和 branch refs stage 到 trash。
- **`exp checkout`**：为可见 experiment commit 创建 inspection checkout。
  关键参数：必需 `<exp_id> --path <dir>`；可选 `--commit final|latest|best|<sha>`、`--project`。
  注意点：会把 inspection token 写到 token path，永不打印。
- **`exp checkout remove`**：移除 inspection checkout。
  关键参数：`--token-id` 或 `--path` 二选一；再加 `--dry-run` 或 `--force --confirm <token_id-or-path-hash>`；可选 `--project`、`--reason`。
  注意点：可 reconcile 已缺失路径；使用 trash staging。
- **`exp worktree remove|restore`**：移除或恢复 submit-capable worktrees。
  关键参数：Remove 需要 `<exp_id>` 加 `--dry-run` 或 `--force --confirm <exp_id>`；restore 需要 `<exp_id> --path <dir>`；可选 `--project`。
  注意点：Remove revoke active worktree token；restore 写 replacement token，永不打印。
- **`exp token list|revoke|regenerate`**：查看或替换 experiment tokens。
  关键参数：必需 `<exp_id>`；selectors 为 `--token-id`、`--mode worktree|inspection` 或 `--all`。
  注意点：Regenerate 会把 raw token 写到 registered path，永不打印。
- **`exp tag add|remove|list`**：管理 experiment labels。
  关键参数：必需 `<exp_id>`；add/remove 还需要 tag text。
  注意点：用于 search、worker sessions/subagents 分组和比较相关 attempts。
- **`observe experiments|runs|artifacts|logs|annotations`**：读取或维护 project-visible evidence。
  关键参数：使用对应 observe filters：experiment/runs/artifacts/logs/annotations list filters、`show <id>`、export `--out`、archive/unarchive，以及 admin-only remove dry-run/confirm。
  注意点：Hidden logs 需要 root/admin 和显式 `--include-hidden`；observe outputs 是决策证据。
- **`annotate add|edit|archive|unarchive|remove`**：添加或维护 project notes。
  关键参数：`add` 接受可选 `--target` 和一个 body input。Project context 中 targetless notes 必须提供 `--title <title>` 和 `--exp <exp_id>`；targeted notes 也可以使用 `--title`。可选 `--author`、`--private`、`--private-to-exp`。Edit 需要 annotation id 和 body；remove 需要 dry-run 或 force/confirm。
  注意点：用于 decision notes、review notes 和 project-visible guidance。只有当 note 不绑定单个 object 或 path、而是归属某个 experiment 时，才省略 `--target`。
- **`audit list|show --project`**：查看 project-scoped audit evidence。
  关键参数：Filters 包括 `--object-type`、`--object-id`、`--action`、`--actor`、time bounds、`--limit`、`--offset`；show 需要 `<audit_id>`。
  注意点：用于验证 lifecycle、credential、config、source、validation 和 cleanup actions。

谨慎使用 remove commands：

- 先运行 `--dry-run`。
- 只有理解 blocker list 后，才使用精确的 `--force --confirm <id>`。
- 如果 command 要求 archive-first deletion，先 archive target，再 hard remove。

## 禁止的 Global Surface

使用 `alab-project-controller` 的 project-level session 不应运行 root-only commands：

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

当 admin key 允许时，`alab key list --project <project_id>` 可用于 same-project inspection。创建或 revoke admin key 属于 global-admin task。

## Experiment Creation Patterns

先创建 experiment，然后使用 `exp create` 输出的 worktree path 做 worker handoff。详细 session/subagent launch requirements 见 [Worker Launch Pattern](#worker-launch-pattern)。

保持 credentials layer-specific：project admin key 只用于 `exp create` 和其他 project-level commands；不要传给 experiment worker context。

Default source：

```sh
printf '%s\n' "$ALAB_PROJECT_KEY" | alab --key-stdin exp create \
  --project "$ALAB_PROJECT_ID" \
  --name "$EXPERIMENT_NAME"
```

从 prior best commit 继续：

```sh
printf '%s\n' "$ALAB_PROJECT_KEY" | alab --key-stdin exp create \
  --project "$ALAB_PROJECT_ID" \
  --name "$NEXT_EXPERIMENT_NAME" \
  --from-exp "$SOURCE_EXP_ID" \
  --from-commit best
```

## Worker Launch Pattern

在 `exp create` 生成 worktree path 后使用此模式。对于支持创建新 thread/session 的环境，优先使用新 session，而不是在当前 project-level session 中 inline 运行 worker。不同 agent launcher 的参数不同，因此下面是 launch requirements，不是 literal command：

- 将 worker session/thread 或 subagent 的 working directory 或 target context 设为 experiment worktree path。
- 给 worker session/thread 或 subagent 提供 `alab-experiment-worker` skill/instructions。
- 通过 launcher 正常的私有 prompt channel 提供 worker prompt，不要把 prompt 写入会提交到 source tree 的文件。
- 从 worker environment 中清除 admin/root credentials 和无关 ambient tokens。这等价于 unset `ALAB_PROJECT_KEY`、`ALAB_ROOT_KEY`、`ALAB_KEY` 以及任何无关的 `ALAB_TOKEN`。
- 在 shell 中，前缀 `env -u ALAB_PROJECT_KEY -u ALAB_ROOT_KEY -u ALAB_KEY -u ALAB_TOKEN ...` 表达的就是这个清理动作：用移除了这些变量的环境启动后续 process；如果使用非 shell 的 session launcher，也要做等价清理。
- 让 worker 只使用该 worktree 的 experiment token context，优先使用 worktree 中已有的 token file。
- 如果 worker 需要 `ALAB_CMD_PREFIX` 才能调用正确的 ALab binary，只传递这个非 secret command prefix。

如果 worker 在 sandbox 中运行 ALab，且 ALab home/cache 位于 worktree 外，只加入必需的非 secret state directories：

```text
--add-dir "$ALAB_EXAMPLE_HOME"
--add-dir "$UV_CACHE_DIR"
--add-dir "$PYTHONPYCACHEPREFIX"
--add-dir "$ALAB_SHARED_DIR"
```

不要把 repository root 作为 worker 的 `-C`。不要通过 argv、stdin prompt text、copied files、inherited environment、`--add-dir "$RUN_DIR"`、`.run/secrets` 或 `project.env` 传递 project admin key。启动前清掉无关的 ambient token variables；experiment worker session 只应使用自己 worktree 对应的 token context。
启动前解析 worktree path，并拒绝 repo root、整个 `.run` 目录或任何 secret/control path。告知 worker sessions/subagents：加入的 ALab home/cache/shared directories 只是 CLI state，不是 source-editing surface。

## Closeout Report

Project-level final report 应包含：

- project id 与 active config version；
- 创建或复用的 experiments；
- best experiment、run id、reward、parse status 和 commit；
- 对于 free evaluation projects，报告 final commits 和 `final run id: none` submissions，而不是 best reward evidence；
- worker failures 与 skipped steps；
- 可安全分享的 report 或 artifact paths。
