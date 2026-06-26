# ALab Experiment Worker Commands

## 调用前缀

下面的 command snippets 使用 `alab`。如果 launcher 提供 `ALAB_CMD_PREFIX`，应按 launcher 指示通过该 prefix 调用 ALab，而不是 hard-code `alab`。不要打印、检查或改写 launcher 提供的 credential material。只使用当前 worktree 的 token context；不要接受 root keys、project admin keys，或其他 worktrees 的 tokens。

## 允许的 Surface

在 active experiment worktree 内使用这些 commands：

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

Worker lifecycle 权限有意保持很窄：

- `run` 和 `submit` 需要当前 experiment 的 valid worktree token。
- Worker session 应优先使用当前 worktree 的 token file。如果显式提供 token，它必须匹配这个 worktree 或 inspection checkout。
- Observe commands 只显示当前 token 可见的 items。
- `exp checkout` 只能为当前 token 可见的 experiments 创建 inspection checkout。
- Experiment tags 只是 labels；它们绝不会扩展 visibility。
- Hidden logs 需要 root/admin，不属于本 skill。
- Worker annotation mutation 只限于 visible targets 和由该 worker token 创建的 annotations。
- Project-level 或 root-required operations 应报告给带 project admin key 的 project-level session 或 root-admin session；不要在 worker session 中请求这些 keys。

## 功能明细

每项说明功能、作用、关键参数和输出/注意点。

- **`alab status`**：检查当前 experiment/project 状态和 next action hint。
  关键参数：只有 project-level session 明确给出时才使用可选 `--project <project_id>`；通常在 worktree 内不带 flags 运行。
  输出用途：确认 context type、project id、experiment id、project status、experiment status，以及是否可继续工作。
- **`alab help`**：查看当前 worktree token 可用 commands。
  关键参数：`--all --explain` 可以显示 locked commands 和安全原因。
  输出用途：避免误用 admin/root commands，并识别可用 observe 或 annotation commands。
- **`alab feedback`**：为 tooling suggestions、questions、bugs 或其他 agent observations 留 HOME-level local note。
  关键参数：`--body <text>` 或 `--body-file <path>` 二选一；可选 `--kind suggestion|question|bug|other` 和 `--title <text>`。
  输出用途：获取 `ALAB_HOME/feedback/` 下保存的 feedback id 和文件路径。该命令用于 ALab/tooling feedback，不替代 experiment submission summary。
- **`alab run`**：评估当前 candidate，并保存 run evidence。
  关键参数：必需 `--message <text>`；保持简短且具体。
  输出用途：获取 run id、status、reward、parse status、warnings、previews、artifact count 和 next action。
  注意点：Reward files 应只包含 configured reward parser 期望的可解析 numeric metrics。解释性 details 应放在单独 artifacts 或可见 logs；worker tokens 不能查看 hidden verifier logs。Free evaluation projects 中 `alab run` 会返回 `COMMAND_UNAVAILABLE`；应改用 direct submit。
- **`alab submit`**：在有 passed run 支撑后，提交最终 summary 和 feedback 并关闭 experiment。
  关键参数：必需 `--message`、`--summary`/`--summary-file` 二选一、`--feedback`/`--feedback-file` 二选一，以及至少一个 `--ref`；可选 `--rerun`。
  输出用途：获取 final run id、final commit、stored summary/feedback、experiment status 和 submitted refs。
  注意点：Standard evaluation projects 需要 supporting passed run，或用 `--rerun` 创建一个。Free evaluation projects 没有 evaluator；省略 `--rerun`，直接 submit，并预期输出 `final run id: none`。
- **`alab exp checkout`**：在选定 commit 上为一个可见历史 experiment 创建 inspection checkout。
  关键参数：必需 `<exp_id>` 和 `--path <dir>`；可选 `--commit final|latest|best|<sha>`。使用当前 worktree 和其他 ALab contexts 之外的空路径。
  输出用途：得到一个来自可见 prior experiment 的只读比较 workspace。阅读其中与任务相关的文件来寻找有用思路，然后只把确实有用、任务相关的 source files 或 snippets 复制到当前 worktree。不要复制 `.alab/`、raw tokens、hidden assets 或 project control files。记录自己创建的 inspection path，方便 project-level session 后续清理；不要在 inspection checkouts 内编辑。
- **`alab exp tag add|remove|list`**：为当前 experiment 添加或查看 tags。
  关键参数：`add`/`remove` 需要 `<exp_id> <tag>`；`list` 需要 `<exp_id>`。
  输出用途：当 project-level session 预期 tags 时，标记有用的 worker-local evidence，例如 `promising`、`needs-review` 或任务相关标签。Tags 不是 authorization，也不能替代 submit refs。
- **`alab report`**：为一个 visible experiment 导出 Markdown report。
  关键参数：必需 `--exp <exp_id> --out <path>`；可选 `--overwrite`。在 worktree context 中，`--project` 通常由 context 提供。
  输出用途：生成本地 handoff/evidence 文件，包含 safe details、runs、submission text，以及可见 artifact/log summaries。Worker report 不包含 hidden logs、raw secrets、tokens 或 artifact bytes。
- **`observe experiments list`**：查看 project 中当前 token 可见的 experiments。
  关键参数：Filters 包括 `--status`、重复 `--tag`、`--source-id`、`--name-query`、reward bounds、config version、timestamps 和 `--include-archived`；pagination 使用 `--limit`/`--offset`；sorting 使用 `--sort <field>:<asc|desc>`。
  输出用途：查找 prior attempts、similar tags、source lineage、closed experiments 和可能的 refs。
- **`observe experiments search`**：搜索可见 experiment corpus，寻找思路或历史失败。
  关键参数：必需 `--query <text>`，并可加主要 experiment filters。
  输出用途：定位相关 summary、feedback、task text、name、goal、tags、latest annotation titles 和 latest annotation bodies。
- **`observe experiments show`**：查看一个可见 experiment。
  关键参数：必需 `<exp_id>`。
  输出用途：确认 source ref、latest/final/best commits、tags、status，以及是否应作为 ref 引用。
- **`observe experiments best`**：按 reward policy 排序查找可见 best experiments。
  关键参数：可加 experiment filters；不支持 custom sort。
  输出用途：识别强 baseline 或 inspiration candidates，并注意 incomparable-run warnings。
- **`observe runs list`**：查看可见 run history。
  关键参数：Filters 包括 `--exp`、`--status`、`--config-version`、`--commit`、reward bounds、`--runner-type`、`--exit-code`、`--failure-reason-query`、timestamps 和 `--include-archived`。
  输出用途：比较 candidate 质量、定位 failure modes，或查看当前 experiment runs。
- **`observe runs show`**：查看一个可见 run。
  关键参数：必需 `<run_id>`。
  输出用途：读取 reward、parse status、warning codes、stdout/stderr previews、artifact count、hidden-log availability 和 timestamps。
- **`observe artifacts list/show/export`**：查看或导出可见 captured artifacts。
  关键参数：List filters 包括 `--exp`、`--run`、`--validation`、`--root workspace|run`、`--status`、`--path-query`、`--content-hash`、size bounds、timestamps 和 `--include-archived`；export 需要 `<artifact_id> --out <path>`，可选 `--overwrite`/`--include-archived`。
  输出用途：检查 outputs、generated reports 或解释 prior results 的文件。Artifact bytes 不保证已经 secret-redacted；只检查必要内容，除非明确安全且相关，不要把 raw artifact contents 粘贴到最终 feedback。
- **`observe logs list/show/export`**：查看或导出可见 logs。
  关键参数：List filters 包括 `--exp`、`--run`、`--validation`、`--stream stdout|stderr|hidden_stdout|hidden_stderr`、`--truncated`、timestamps 和 archive flags。Worker tokens 不能使用 hidden logs。
  输出用途：用可见 stdout/stderr content 和 previews 诊断失败。Summary 中只引用短小、相关的可见片段；worker session 下绝不请求或复述 hidden-log content。
- **`observe annotations list/show`**：读取可见 notes 和 review comments。
  关键参数：List filters 包括 `--target-type`、`--target-id`、`--author`、`--created-by`、`--private`、`--query`、timestamps 和 `--include-archived`；show 接受 `<annotation_id>` 和可选 `--history`。使用 `--target-type none` 可查找 targetless notes。
  输出用途：捕获 prior guidance、known issues，以及挂在 experiments、runs、artifacts 上的 rationale。
- **`annotate add/edit/archive/unarchive`**：添加或维护 worker-visible notes。
  关键参数：`add` 接受可选 `--target <target>` 和 `--body`/`--body-file` 二选一；targetless notes 必须提供 `--title <title>`，并绑定当前 experiment。Targeted notes 也可使用 `--title`。可选 `--author`、`--private`。`edit` 需要 `<annotation_id>` 和一个 body input。Archive/unarchive 需要 `<annotation_id>`。
  输出用途：给后续 workers 留下有用证据，不改变 project configuration。常用 targets 包括 `exp:<exp_id>`、`run:<run_id>`、`artifact:<artifact_id>`、`path:<repo_path>`、`lines:<repo_path>:<start>-<end>`、`path:<exp_id>@<commitish>:<repo_path>` 和 `lines:<exp_id>@<commitish>:<repo_path>:<start>-<end>`。如果 note 不绑定单个 object 或 path，可省略 `--target` 并提供 `--title`，作为当前 experiment note。在 experiment context 中，path/line shorthand 要求 clean worktree。Worker session 不要使用 admin/root-only 的 `--exp`。

## 工作流程

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

这只是一个示例形态，不是必需顺序。先理解当前任务、candidate 和 context。只有当可见历史能指导改动时才使用它。本地检查应保持轻量且与任务相关。Standard evaluation candidate 准备好时运行 `alab run --message "<brief reason>"`；根据可见证据诊断 weak 或 failed results；只要还有合理优化路径，就继续迭代。Free evaluation projects 中 ALab 会直接指向 submit，且不需要 run evidence。如果 `git status --short` 显示无关 generated files，应通过项目正常机制删除或忽略后再 run 或 submit。

只有当工作完成或已经没有有价值的继续优化路径，并且 standard mode 有 passed run 支撑 final candidate，或 free evaluation direct submit 是预期模式时才 submit。如果 standard evaluation candidate 没有 passed run 支撑，应报告最好的 run evidence 和没有 submit 的原因。

## 可见历史

Worker 可以在决定修改方向前，用 ALab observe commands 研究可见范围内的历史 experiments：

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

可见历史用于提供证据和灵感，不用于扩展权限。优先参考 high-reward passed runs、有用 warning patterns、清晰 annotations，以及可比较的 task/source lineage。Submit refs 是便于后续 review 和继续优化的 provenance links：如果某个 prior experiment 影响了最终策略、source changes、comparison baseline、failure avoidance 或 continuation path，应通过重复 `--ref <exp_id>` 显式引用。

当某个可见 experiment 看起来可能有借鉴价值时，查看其中与任务相关的文件，不要只依赖 summary：

```text
alab exp checkout <exp_id> --path /tmp/alab-inspect-<exp_id> --commit best
```

用 `best` 做 reward-led exploration，用 `final` 查看已提交 candidate，用 `latest` 查看当前 branch tip。记录 `exp checkout` 输出中的 `inspection commit`，然后可以在当前 worktree 中用常规 Git 命令比较：

```text
git diff --stat <inspection_commit>..HEAD
git diff <inspection_commit> -- <path>
```

如果要直接和 inspection checkout path 下的文件或子目录比较，只对任务相关 source paths 使用 `git diff --no-index`：

```text
git diff --no-index /tmp/alab-inspect-<exp_id>/<source_path> <current_worktree>/<source_path>
```

`git diff --no-index` 在发现差异时会返回 exit code `1`；这代表有可用的对比输出，不应视作 ALab failure。先阅读并对比 checkout，再决定是否复制。只复制能推进当前任务的 source content，并根据当前 worktree 进行调整；如果最终结果受该内容影响，应在 final `--ref <exp_id>` 和 feedback 中保留引用。绝不复制 `.alab/`、token files、ALab home/cache files、hidden evaluator assets、secret files 或 project control files。

Inspection checkouts 是比较 surface，不是 editable source surface。不要把它们的路径写入 commits 或 final artifacts。如果需要清理，应把 path 报告给 project-level session；只有在该 checkout context 的 `alab help` 明确显示 inspection token 可用 self-removal command 时才自行清理。

## 禁止的 Surface

Worker session 不要运行这些 commands：

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

也不要直接编辑当前 experiment worktree 之外的文件。如果 launcher 为 CLI state 加入了 ALab home/cache directories，只通过 ALab commands 使用它们。

如果确实需要其中某项能力，应报告给 project-level session 或 root-admin session。

## Evaluation Pattern

```text
alab status
alab run --message "try focused improvement"
alab observe runs show <run_id>
```

使用可见 stdout/stderr preview、warning code、artifact 和 log 诊断。除非用户明确把你切换到 admin role，不要请求 hidden evaluator logs。如果 run 失败是因为需要 admin/root operation 且当前不可用，应停止并报告具体缺失能力。

## Submit Pattern

summary 和 feedback 超过一句话时，优先写入临时文件：

```text
alab submit \
  --message "final candidate" \
  --summary-file /tmp/alab-summary.txt \
  --feedback-file /tmp/alab-feedback.txt \
  --ref none
```

只有没有历史 experiment 对结果产生实质影响时，才使用 `--ref none`。当可见 experiments 被用作 inspiration、source continuation、comparison baseline 或 failure example 时，应优先显式传入 refs：

```text
alab submit \
  --message "final candidate" \
  --summary-file /tmp/alab-summary.txt \
  --feedback-file /tmp/alab-feedback.txt \
  --ref <exp_id_that_inspired_or_was_continued> \
  --ref <another_relevant_exp_id>
```

summary 应描述最终改动和支撑它的 passed run。feedback 应包含有用的操作备注：关键 metrics、避开的 failure modes、每个 ref 为什么相关，以及剩余风险。清楚解释 refs 可以让后续 workers 更容易检查 lineage 并继续优化。不要包含 raw tokens、hidden-log content 或不可访问的 experiment ids。
Free evaluation mode 中，应说明没有 evaluator run，且 `final run id` 为 `none`。

Worker 的最终回复应包含：

- 调整过的策略或 source area；
- final run id 和 status，或 free evaluation 的 `final run id: none`；
- 存在时的 reward 与关键 metrics；
- 使用的 submit refs，或说明为什么是 `ref none`；
- 如果 ALab 渲染了 final commit，则记录它；
- 添加的 tags（如果有）；
- 创建的 inspection checkout paths（如果有）；
- 剩余风险或已知失败。
