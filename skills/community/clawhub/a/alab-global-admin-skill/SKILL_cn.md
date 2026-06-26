---
name: alab-global-admin
description: 当需要使用 root authority 管理 ALab home 时使用，包括 home bootstrap、root 和 project-admin credential management、project initialization 与 handoff、SkyDiscover catalog management、global cache 或 backup pruning，以及 root-level audit/dashboard inspection。不要用于日常 project coordination 或 experiment work。
---

# ALab Global Admin

## 概览

本 skill 用于 ALab 的 root layer。它负责 ALab home setup、root credential rotation、project admin key create/revoke、project initialization、SkyDiscover catalog lifecycle、cache/backup pruning、global audit inspection，以及 root-only local read-only dashboard。

## 分层边界

- 本 skill 不是 project-coordination layer，也不是 experiment-work layer。
- 仅在 root-scoped administration，或明确需要 root authority 的 project operation 中使用 root authority。
- 创建 project、发放 project admin key，或创建 bootstrap experiment 后，把后续 project work 交给使用 `alab-project-controller` 的独立 session/thread 或 subagent。
- Experiment worktree edits 交给位于该 experiment worktree、使用 `alab-experiment-worker` 的独立 session/thread 或 subagent。
- 如果无法启动独立 session，则使用具备等价 project/worktree/token 隔离的 subagent 或 worker process。用户指令优先于此偏好。

## 凭据规则

- 将 root key 视为只渲染一次的本地 secret。
- Root commands 优先使用 `--key-stdin`；避免在 logs 中出现 inline key arguments。
- 不把 raw root/admin keys 存入 tracked files、prompts、commits、screenshots、reports 或 command transcripts。
- 生成的 project admin keys 只保存到 ignored local secret files，例如 example-local `.run/secrets/` 目录，或用户批准的安全位置。
- 委派时，只传递该任务和 scope 所需的 credential。Root keys 只留给 root-admin sessions。Project admin keys 只交给该 project 的 project-level sessions。Experiment worktree 或 inspection tokens 只交给在该 exact worktree 或 checkout 中工作的 sessions。
- 使用 ignored secret files、private environment variables 或 secure stdin 传递 credential，不要写进 prompt text。
- 给被委派的 sessions 或 subagents 提供对应的 ALab skill/instructions：project-level work 使用 `alab-project-controller`，experiment worktree work 使用 `alab-experiment-worker`。
- 如果 root key 丢失，ALab 无法恢复；不要通过编辑本地状态来绕过 credential recovery。

## 功能说明

这是一份能力指南，不是固定步骤。根据 administrative objective 使用合适能力：

- 只有 ALab home 不存在时才用 `alab auth init` bootstrap；用 `alab config show` 或 `alab config validate` 检查 home health。
- 对 local ALab/tooling suggestion、question 或 bug report，使用 `alab feedback` 存到 home 下；使用 root-only `alab feedback list|show|archive` triage 这些 entries。
- 当 root 用户需要在 browser 中只读查看 local home 时，使用 `alab dashboard`。Dashboard 只用于 local-only inspection；不要分享 token URL，也不要把它用于 mutation workflow。
- 谨慎管理 root credentials。只有明确需要时才 rotate root，并把 replacement keys 视为只渲染一次的 secrets。
- 创建、列出和 revoke project admin keys。Revoke 前先识别 key id、project scope 和预期影响。
- 使用 config files，从 local、Git、empty、Harbor 或 SkyDiscover sources 初始化 projects。只捕获一次 generated project admin key，只保存到 ignored secret 位置，并安全 handoff 给 project layer，绝不交给 experiment worker。
- 当 project initialization 在 baseline validation 阶段失败时，保留 redacted logs，并区分 environment/capability failures 与 reward-contract failures，例如 non-numeric reward metrics。
- 管理 SkyDiscover catalog lifecycle，包括 exact commit pinning、不访问网络的 `show`、active-reference blockers，以及带 explicit confirmation 的 remove。
- 使用 cache、trash 和 backup prune commands 维护 global non-authoritative state。
- 查看 global 或 project audit events，验证敏感 lifecycle events、credential changes、catalog changes、cleanup 和 project initialization。
- Destructive removal 前尽量使用 dry-run；除非用户明确要求，否则 lower-layer work 应保持委派。

## 文件导航

- `SKILL.md`：canonical root-layer boundaries、credential rules 和 workflow guidance。
- `SKILL_cn.md`：本文件的同步中文版本。
- `references/commands.md`：详细 root command surface、project initialization、catalog、cleanup 和 handoff reference；root-only actions 或 destructive maintenance 前读取。
- `references/commands_cn.md`：command reference 的同步中文版本。
- `agents/openai.yaml`：UI metadata 和 default prompt；invocation guidance 改变时同步更新。
