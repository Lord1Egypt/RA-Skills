---
name: alab-project-controller
description: 当需要使用 project admin key 管理一个已有 ALab project、创建和协调 experiments、验证或调整 project config、管理 project-scoped source/lifecycle state、观察 project evidence，并在不暴露 admin credential 的前提下启动 experiment worker sessions 或 subagents 时使用。
---

# ALab Project Controller

## 概览

本 skill 用于 ALab 的 project layer。它使用 project admin key 协调一个已有 project：创建 experiments、启动 experiment worker sessions 或 subagents、观察 project-visible evidence、比较 best runs，并管理 project-scoped config、source、validation、annotation、token 和 lifecycle state。

## 分层边界

- 本 skill 不是 root-administration layer，也不是 experiment-work layer。
- 不得初始化 ALab home、轮换 root credential、管理 SkyDiscover catalog、prune global cache/backup，或创建/revoke project admin keys。
- 创建 experiment 后，把 worktree changes 交给位于该 experiment worktree、使用 `alab-experiment-worker` 的独立 session/thread 或 subagent。
- 如果后续 project-level coordination 需要自己的执行 context，使用带 project admin key 和本 skill 的独立 session/thread 或 subagent。
- 如果无法启动独立 session，则使用具备等价 project/worktree/token 隔离的 subagent 或 worker process。用户指令优先于此偏好。

## 凭据规则

- Project admin key 只能来自私有 environment variable 或 secure stdin。
- ALab admin commands 优先使用 `--key-stdin`；避免在可能被记录的 command 中写 inline key。
- 永不打印、提交、写入 prompt，或传递 project admin key 给 experiment worker sessions/subagents。
- 委派时，只提供被委派任务所需的 credential。Project-level coordination 可以通过私有 environment variable、ignored secret file 或 secure stdin 接收 project admin key。Experiment work 只能使用该 experiment 的 worktree token context。
- Project admin key 只用于 project-level commands，例如 experiment creation、config/source/lifecycle maintenance、observe、report 和 audit。它不得被 experiment worker sessions 继承。
- Experiment worker sessions 不应接收 root/admin keys 或无关的 ambient tokens。优先使用 worktree 中已有的 token file；如果必须显式提供 token，只能通过私有通道提供该 exact worktree 或 inspection checkout 对应的 token。
- 给任何被委派的 experiment worker session/thread 或 subagent 提供 `alab-experiment-worker` skill/instructions。
- 启动 worker 时，将目标设为 experiment worktree，并清除 admin/root credentials 和无关 ambient tokens。Environment 和 path requirements 见 command reference。

## 功能说明

这是一份能力指南，不是固定步骤。根据 project objective 使用合适能力：

- 用 `alab project show`、`alab project config show`、`alab status` 以及 project-scoped audit/observe commands 检查 project state。
- 对于 ALab/tooling suggestion、question 或 bug report，使用 `alab feedback` 存到 local home，而不是混入 project annotations。
- 在 default source、explicit sources 或可见 predecessor experiments 基础上创建新 experiments；需要延续时再使用 from-experiment，然后从该 worktree 委派 worktree changes。
- 记录 experiment ids、worktree paths、source refs、tags、from-experiment choices，以及 `best`、`final`、`latest` 等 selected commits，保持 experiment lineage 清楚。
- 在 experiment worktrees 中启动带 `alab-experiment-worker` skill/instructions 的 experiment worker sessions 或 subagents，但不传递 project admin 或 root credentials。只提供任务说明和非 secret helper variables；让 workers 使用自己的 worktree token 执行 `alab run` 和 `alab submit`。
- 如果 project 使用 free evaluation（`runner.type = "none"` 且 `reward.type = "none"`），应告知 experiment worker sessions/subagents 不运行 `alab run`，直接 submit；final run id 会是 `none`，结果不会进入 best reward ranking。
- 跨 experiments、runs、artifacts、logs 和 annotations 观察 project-visible evidence。优先依据 reward、parse status、warning codes、metrics、best/final commits 和 submitted refs，而不是 free-form worker claims。
- 先把 reward parse failures 当作 contract failures 处理。对于 file 或 Harbor rewards，检查 reward JSON 是否只包含 finite numeric metrics，并把详细 diagnostics 放到 artifacts 或 hidden/visible logs 中。
- 只有 requested project objective 需要时，才管理 project-scoped config、environment variables、secrets、validation、sources、tags 和 lifecycle state。
- Destructive lifecycle actions 前先使用 dry-run remove，并在 force/confirm 前记录 blockers 或 cleanup 后果。
- Project-level summary 应说明创建或改变了什么、哪些 experiments/runs 重要、哪些 credentials 被刻意 withheld from experiment workers，以及剩余 follow-up。

## 文件导航

- `SKILL.md`：canonical project-layer boundaries、credential rules 和 coordination workflow。
- `SKILL_cn.md`：本文件的同步中文版本。
- `references/commands.md`：详细 project command surface、experiment creation、worker launch、observe 和 lifecycle reference；project-scoped admin commands 或 worker handoff 前读取。
- `references/commands_cn.md`：command reference 的同步中文版本。
- `agents/openai.yaml`：UI metadata 和 default prompt；invocation guidance 改变时同步更新。
