---
name: alab-experiment-worker
description: 当位于一个 ALab experiment worktree 中，并且只应使用该 worktree token context 检查状态、修改 candidate source、运行 evaluation、提交最终结果、读取可见实验证据，而不能使用 project admin 或 root 权限时使用。
---

# ALab Experiment Worker

## 概览

本 skill 用于 ALab 的 experiment worktree layer。它改进一个 candidate source tree，读取该 worktree token 可见的 evidence，在 standard projects 中通过 worktree token context 运行 evaluation，并在当前 project mode 允许时提交最终结果。

## 分层边界

- 本 skill 不是 project-coordination layer，也不是 root-administration layer。
- 不得使用 project admin keys、root keys、catalog commands、cache commands、project configuration mutation、credential management、audit commands 或 lifecycle removal commands。
- 如果需要 project-level 或 root authority，停止该分支并向 project-level 或 root-admin session 报告所需操作，不要请求更高权限 key。

## 操作规则

- 只信任当前 worktree context 及其 `.alab/token`。
- 不接受 root keys、project admin keys，或其他 worktrees / inspection checkouts 的 tokens。如果 launcher 显式提供 token，使用前先确认它属于当前 worktree context。
- 不读取、打印、复制、提交或重写 raw token/key。
- 不编辑 `.alab/`、ALab home state、cache directories、shared run directories、hidden evaluator assets、secret files 或 project control files。
- 只修改 experiment worktree 内与任务相关的 source files。
- 明确分离 source editing 和 CLI state。Experiment worktree 是唯一可编辑 source surface；任何额外加入的 ALab home、uv cache、pycache 或 shared directory 只供 `alab run`/`submit` 写状态，不得检查、patch、复制或提交其中内容。
- 保持改动可审查：优先小步、聚焦、可复现的 iteration，并使用简洁 run message。
- 如果 launcher 提供 `ALAB_CMD_PREFIX`，ALab 调用应使用该 launcher 提供的 command prefix；否则使用 `alab`。
- Git 可用时，在重要 run 或 submit 前检查 `git status --short`，并确保 generated/untracked files 都是有意保留的。
- 不熟悉 command 时先运行 `alab help`；worktree token surface 之外的 command 应视为不可用。
- 如果 ALab 返回 `COMMAND_UNAVAILABLE`，停止该分支并报告缺失能力，不尝试绕过。

## 工作流程

不要把这里当成固定 checklist。先主动理解当前 worktree 的任务、本地说明、已有 candidate 和 ALab context。需要时查看可见 prior experiments、runs、artifacts、logs、annotations 或 inspection checkouts，从中获得参考和灵感。

围绕 candidate 做聚焦修改和轻量本地检查。在 standard evaluation projects 中，当 candidate 准备好时运行 `alab run --message "<brief reason>"`。在 ALab 直接指向 submit 的 free evaluation projects 中，或 `alab run` 因没有 evaluator 返回 `COMMAND_UNAVAILABLE` 时，跳过 run evidence 并准备直接 submit。

使用可见 evidence 诊断 weak 或 failed results；只要还有合理优化路径，就继续改进。发现后续 workers 不应丢失的重要上下文时，用 annotations 记录，尤其是 decision rationale、failed approaches、remaining risks 和 next-step context。对于不再需要、不再有效，或可能误导后续 workers 的 annotations，应 archive 和 remove。

Standard evaluation mode 下只有 supporting passed run 才 submit；free evaluation mode 下只在 documented direct-submit behavior 存在时 submit。Standard mode 没有 supporting passed run 时，不要 submit；报告当前最好 evidence 和 blocker。

## 能力说明

这是一份能力指南，不是固定步骤。根据任务需要使用下列能力：

- 用 `alab status` 和 `alab help` 检查当前 context。
- 发现 ALab/tooling suggestion、question 或 bug，且不应混入 experiment submission feedback 时，用 `alab feedback` 留 HOME-level feedback。
- 读取 worktree 中已有的任务文件和项目说明。
- 用 `alab observe experiments ...` 以及相关的可见 runs、artifacts、logs、annotations 查看历史 experiments。可以用这些证据寻找有希望的方案、避免重复失败，并理解 prior best 或 final commits。可见性仍由 ALab 强制执行；不要尝试访问 hidden 或 unavailable items。
- 当某个可见历史 experiment 看起来相关时，用 `alab exp checkout <exp_id> --path <dir> --commit best|final|latest` 创建 inspection checkout，记录输出中的 inspection commit，阅读其中与任务相关的文件，并先与当前 worktree 对比后再决定是否复制。需要时使用常规 Git 对比工具，例如 `git diff --stat <inspection_commit>..HEAD`、`git diff <inspection_commit> -- <path>`，或用 `git diff --no-index <inspection_checkout>/<source_path> <current_worktree>/<source_path>` 直接比较文件/子目录。只有在确实有帮助时，才把任务相关的 source files 或 snippets 复制到当前 experiment worktree；绝不复制 `.alab/`、raw token、hidden assets、secret files、ALab home/cache files 或 project control files。
- 修改 worktree 内与任务相关的 source files，并保持改动足够清晰，方便后续 worker 延续。
- 当 tags 对后续 project-level sessions 或 workers 有证据价值时，可以为当前 experiment 添加或列出 tags；tags 不授予 visibility。
- 保持 runner outputs 可被机器解析。若任务写 reward file，只把配置要求的 numeric metrics 放入该 reward file；case details、trace 或 explanation 应在允许时放到单独的可见 artifact/log。
- 若存在本地轻量检查，先运行这些检查；standard evaluation projects 再用 `alab run --message "<brief reason>"` 运行 evaluation。Free evaluation projects 不要强行 run，direct submit 是预期流程。
- 使用可见 stdout/stderr preview、warning code、artifact、log、metric 和 annotation 诊断 failed 或 weak runs。
- 当预期修改已经完成，并且当前 worktree 满足其 project mode 所需的支撑条件时，使用事实性的 message、summary、feedback 和 refs 提交。

## 提交指引

- Standard evaluation mode 下，只有当前 candidate 有 passed run 支撑时才 submit。Free evaluation mode 下允许 direct submit，final run id 会渲染为 `none`。
- 把 submit refs 当成便于后续 review 和继续优化的 provenance links，而不是装饰性字段。
- 对于影响了策略、source changes、comparison baseline、failure avoidance 或 continuation path 的可见 experiments，应积极添加 `--ref <exp_id>`。
- 只有结果没有依赖或有意引用任何历史 experiment 时，才使用 `--ref none`。
- 不要编造 refs，不要引用不可访问的 experiment ids，也不要只因为某个 visible experiment 存在就引用它。
- `--message` 保持简短。实质记录写入 `--summary`/`--summary-file` 和 `--feedback`/`--feedback-file`：改了什么、哪个 passed run 支撑或为什么 free evaluation 没有 run、存在时的关键 metrics、哪些 refs 有意义，以及剩余风险。
- 如果没有 submit，应明确说明阻塞原因和当前最好的 run evidence。

## 文件导航

- `SKILL.md`：canonical experiment-worktree boundaries、operating rules、workflow 和 submit guidance。
- `SKILL_cn.md`：本文件的同步中文版本。
- `references/commands.md`：详细 worker command surface、observe patterns、inspection checkout rules、evaluation 和 submit reference；不熟悉 ALab commands 或 run/submit flows 前读取。
- `references/commands_cn.md`：command reference 的同步中文版本。
- `agents/openai.yaml`：UI metadata 和 default prompt；invocation guidance 改变时同步更新。
