---
name: ai-native-bootstrap
display_name: AI原生研发接入
display_name_en: AI-Native-Bootstrap
description: 为既有或新建代码仓库建立可审计的 AI 原生研发流程，生成工程规范、验证入口、证据模板与风险护栏；写入默认关闭、检查未配置即阻断、不伪造通过。触发词：初始化项目研发规范、AI 原生研发流程、接入 AGENTS.md、生成 Intent/Spec/Plan 模板、配置质量门禁、项目工程规则、bootstrap、AI-native SDLC、spec-driven workflow、evidence-based review、engineering guardrails。不适用于：普通功能开发与代码编写（应直接实现）、CI 与生产发布授权（应改用平台部署审批流程）、真实项目验收结论（应由人工结合真实测试与权限记录判定）。
description_zh: 一次安装、多项目复用；只读审计先行，写入须显式授权，检查与 Evals 未配置即返回 BLOCKED，交付可复核的 A-H 报告而非占位文档。
description_en: Install once, reuse across repositories. Read-only audit comes first, every write is opt-in, unverified checks fail closed, and delivery is an auditable A-H report instead of placeholder Markdown.
version: 1.0.0
author: 擎漫网络
agent_created: true
examples_zh:
  - 审计当前仓库并给出接入方案，不改动任何文件
  - 在干净功能分支生成 Intent/Spec/Plan/Acceptance 模板与本地检查入口
  - 核查已有接入是否漂移，输出文件级哈希结果与 CONDITIONAL 判定
examples_en:
  - Audit the repository and propose an adoption plan without writing any file
  - Scaffold the templates and a local check entrypoint on a clean feature branch
  - Verify an existing adoption for drift and report file-level hashes with a CONDITIONAL verdict
---

# AI-Native Bootstrap v1.0.0

Use this skill to build **auditable working controls**, not a collection of placeholder Markdown files. The source-of-truth policy is `references/implementation-standard.md` (read for full requirements). The operational distinctions and tool paths are in `references/adapters-and-safety.md`.

## Entry points

Use the directory containing this SKILL.md as `<SKILL_ROOT>`. All bundled scripts use Python 3.9+ standard library only.

1. **Install the reusable skill once** (user-scoped or project-scoped):
   `python3 <SKILL_ROOT>/scripts/install.py --agent codex --scope user --apply`
   Replace `codex` with `claude` or `opencode`. The installer has **no write side effects without `--apply`** and never silently replaces existing installations.
2. **Read-only inspect a project:**
   `python3 <SKILL_ROOT>/scripts/bootstrap.py audit --project <REPO>`
   `python3 <SKILL_ROOT>/scripts/bootstrap.py plan --project <REPO>`
3. **Bootstrap explicitly, after evaluating the plan and approvals:**
   `python3 <SKILL_ROOT>/scripts/bootstrap.py init --project <REPO> --adapter codex --apply`
   Supported adapters: `codex`, `claude`, `opencode`, `all`. Changes require a clean Git worktree and non-default branch; an empty, unversioned directory may be bootstrapped with an explicit warning. An existing `AGENTS.md` must **not** be overwritten.
4. **Verify files after bootstrap:**
   `python3 <SKILL_ROOT>/scripts/bootstrap.py verify --project <REPO>`
5. **Review / configure project-specific real checks:**
   Edit the generated candidate-check manifest in the target repository to confirm the observed commands; set each verified entry's `enabled` to `true`. Then run the generated local check entrypoint (`check.py`). Until enabled, it must fail `BLOCKED` (exit 2), not fake success. For authentic deterministic Evals, fill the generated cases file (empty by default) and run the evaluation entrypoint (`eval.py`); an empty suite also fails BLOCKED.

## Execution protocol for the acting Agent

- Read repository instructions and inspect git status, architecture, tests, deployment and CI before making changes. Avoid reading `.env`, secret values, key material, production data, or raw sensitive logs.
- For **audit/plan/harness-only** requests, perform no application coding, commits, pushes or deployments. For bootstrap, only create the approved engineering harness files; do not alter business logic or lock files.
- Classify risk R0-R3 following `references/implementation-standard.md`. A request to bootstrap **does not** authorize R2/R3 actions, CI credential changes, remote pushes or production releases. Higher-risk actions require separate explicit approval and enforced authority at the actual target system.
- Respect the current repository's source of truth. `AGENTS.md` is preferred only when no authoritative file exists; preserve existing `AGENTS.md` and `CLAUDE.md`. Treat generated Claude pointer as an adapter, not another policy owner.
- Never call a scaffolded test entrypoint "complete" until real commands have been configured and run, with actual exit codes. Keep Evals as a plan until real accepted cases and an evaluation runner exist.
- If the worktree is dirty, the current branch is protected/default, files conflict, or parent directories are symlinked, do not force writes. Report the exact blocker and choose a safely isolated branch/worktree through user-authorized means.
- Record evidence as `PASS`, `FAIL`, `BLOCKED`, `NOT RUN`, or `N/A` and label unverified CI/production permissions `UNVERIFIED`. Agent `PASS` is not human approval.
- Conclude with the full A-H report specified in section 12 of `references/implementation-standard.md`, including changed paths, evidence, negative tests, rollback and unresolved items. Never report an unperformed action as successful.

## Required follow-through after scaffolding

1. Inspect the detected candidate-check manifest: every candidate is **unverified and disabled** by default. Confirm real project commands and safe environment, then enable only those verified and run them.
2. Add **one genuine project regression** if a real historical failure/test fixture is available, or mark D05 `BLOCKED` with a collection plan. No synthetic success fixtures may be claimed as a project regression.
3. Inspect existing CI and add deterministic gates only if safe and approved. Never infer branch protection or remote approval from a local file.
4. Use a fresh-context read-only reviewer for important changes. Verify against `intent/spec/plan` and classify findings `IMPORTANT/NIT/UNKNOWN`.
5. For every R2/R3 or production transition, stop at preparation, leave evidence and request approval at the actual execution boundary.

## Bundle self-test

Run `python3 <SKILL_ROOT>/scripts/validate_bundle.py` and `python3 -m unittest discover -s <SKILL_ROOT>/tests -v`. Check `references/adapters-and-safety.md` when adapting tooling. Do not automatically install dependencies or use network access.

## Provenance

- 产物版本：1.0.0；构建与上架迁移日期：2026-11-13。
- 构建器：SkillBuddy v2.4.6（静态审核、缺陷修复与 WorkBuddy 上架迁移）。
- 署名主体：擎漫网络；关联品牌 Qomob.AI。
- 方法来源：包内实施标准标注为 Anthropic《The AI-Native SDLC Playbook》（54 页）及针对现有项目的工程化扩展；发布方另提供「基于 Claude《The AI-Native SDLC Playbook 2》提炼」的表述。两种表述尚未核对统一，对外文案引用前须由发布方确认原始出处；本包不宣称其为原文逐条规定。
- 关键假设：目标项目可由 Python 3.9+ 标准库只读审计；Git 非强制前提；生产权限与审批不由包内文件强制。
- 已验证范围：包内离线自检 22/22（macOS / Python 3.13.12）；SkillBuddy 静态预检、官方校验与行为沙盘结果见随包审核报告。证据级 E2（静态 + 沙盘模拟）。
- 未验证：WorkBuddy 宿主 T1/T2/T3 实测、平台审核结果、真实项目接入、Python 3.9-3.12 兼容矩阵、Codex/Claude/OpenCode 会话内的技能发现。`behavior_verification: not_run`。

## 免责声明

本技能会在本地读写仓库文件、执行项目中已有的检查命令，并检查 Git 状态与目录结构。所有写入默认关闭，须显式 `--apply`；审计与计划阶段为只读。请在干净、隔离的分支或工作树中使用，启用任何项目检查前先自行审查命令内容与运行环境。本包不会读取或上传 `.env`、令牌、私钥等凭据值，不联网、不推送、不部署；但也正因如此，它**不能替代 CI、分支保护与生产审批等真实执行侧的强制措施**。生成的报告属于技术建议，不构成人工验收或生产发布授权；重要场景请在真实环境复验后再投入使用。
