---
name: alab-skills
description: 作为 ALab agent-facing role skills 的顶层指南使用。它说明如何安装 ALab CLI package、root/project/experiment skill hierarchy、各 subskill 的使用时机，以及三种 role skills 的差异，而不一次性加载所有 command reference。
---

# ALab Skills

## 安装 ALab

ALab 以 `alab-cli` Python package 形式安装，并提供 `alab` console command。

从 PyPI 安装：

```sh
python -m pip install alab-cli
alab help
```

## 概览

ALab 是本地 agent-first experiment workbench。它把 root home administration、project coordination 和 experiment worktree work 分层，使 agents 可以协作，同时避免共享不必要的 credentials 或在错误层级 mutation。

需要先理解 ALab role-skill system、再选择具体 subskill 时，使用这个顶层 skill。实际操作时，应加载最窄匹配的 subskill，并且只在需要时读取它的 command reference。

## Skill 层级

- `alab-global-admin`：Root layer。用于 ALab home bootstrap、root credential rotation、project admin key creation/revocation、project initialization、SkyDiscover catalog lifecycle、global cache/backup pruning、root dashboard，以及 root/global audit inspection。它应把 project coordination 交给 `alab-project-controller`，把 worktree work 交给 `alab-experiment-worker`。
- `alab-project-controller`：Project layer。使用一个 project admin key 来创建和协调 experiments、管理 project-scoped config/source/validation/lifecycle state、观察 evidence、比较 runs，并启动 experiment worker sessions 或 subagents。除非用户明确要求，否则它不得执行 root administration，也不应在当前 session 内直接做 experiment work。
- `alab-experiment-worker`：Experiment worktree layer。在一个 experiment worktree 内、使用该 worktree token context，检查 visible evidence、修改 candidate source、运行 evaluation、记录有用 annotation，并提交 final results。它不得接受 project admin/root keys，也不得执行 project/root operations。

## 选择规则

- 从用户请求的 authority 和当前 path context 开始判断。Root key 对应 `alab-global-admin`；project admin key 对应 `alab-project-controller`；experiment worktree token context 对应 `alab-experiment-worker`。
- 优先使用能完成任务的 least-privileged subskill。
- 创建或继续 experiment work 时，先在更高层创建 project/experiment，再把 worktree changes 交给使用匹配 lower-layer skill、且只带匹配 credential/token context 的独立 session/thread 或 subagent。
- 用户指令优先于委派偏好，但不覆盖 credential hygiene 或 ALab command authorization。

## 共享原则

- Credentials 保持 layer-specific：root keys 只留给 root-admin sessions，project admin keys 只留给匹配 project 的 project-level sessions，worktree 或 inspection tokens 只留给在该 exact worktree 或 checkout 中工作的 sessions。
- 给被委派的 sessions 或 subagents 提供匹配的 subskill/instructions。
- Raw keys 和 tokens 不得进入 prompts、tracked files、logs、screenshots、reports、shared non-secret directories 或 copied source files。
- Command references 是详细操作材料。除非任务需要，不要一次性加载所有 command reference。

## 文件

- `SKILL.md`：这个顶层 ALab skill guide 和 subskill router。
- `SKILL_cn.md`：本文件的同步中文版本。
- `agents/openai.yaml`：顶层 skill 的 UI metadata 和 default prompt。
- `alab-global-admin/`：Root-layer subskill，包含其 `SKILL.md`、`SKILL_cn.md`、`agents/openai.yaml` 和 `references/commands*.md`。
- `alab-project-controller/`：Project-layer subskill，包含其 `SKILL.md`、`SKILL_cn.md`、`agents/openai.yaml` 和 `references/commands*.md`。
- `alab-experiment-worker/`：Experiment-worktree subskill，包含其 `SKILL.md`、`SKILL_cn.md`、`agents/openai.yaml` 和 `references/commands*.md`。
