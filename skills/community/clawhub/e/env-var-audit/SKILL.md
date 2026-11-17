---
name: env-var-audit
description: 环境变量审计器 — 代码里 os.getenv 了三个新变量忘写进 .env.example，新人克隆跑不起来；更怕的是哪个密码被硬编码进了源码（零依赖，确定性输出，rc=0/1/2，--json 机器可读） 适用场景：当需要环境变量审计器能力时使用本技能；触发词：env-var-audit。
slug: env-var-audit
version: 1.0.1
display_name: 环境变量审计器
display_name_en: Environment Variable Auditor
agent_created: true
author: 诺声(Logos)@SynomosAI
license: MIT
license_scope: 代码（.py 文件）MIT；本 SKILL.md 与其中理论文本不在 MIT 覆盖范围内（见文末「License & attribution」）
allowed-tools: Read, Glob, Grep, Bash
category: 安全合规
platforms: [claude, codex, cursor, windsurf, workbuddy]
copyright: SynomosAI
description_zh: "环境变量审计器 — 代码里 os.getenv 了三个新变量忘写进 .env.example，新人克隆跑不起来；更怕的是哪个密码被硬编码进了源码（零依赖，确定性输出，rc=0/1/2，--json 机器可读）"
description_en: "Audit environment-variable usage: find os.getenv calls missing from .env.example and hardcoded passwords in source code (zero-dependency, deterministic output, --json)."
classification:
  internal: ["organizational governance & security"]
  skillhub: ["security-compliance"]
  clawhub: ["development"]
  iso_25010: ["Security"]
risk_tier: medium
risk_rationale: "门禁批量补丁默认 medium（内部约定：本 skill 设计为中等风险）：调用 API/读写文件/本地执行，最小权限，密钥走 Secret；若实际涉对外代执行(push/发布/发送/上架)须人工复评，改 high 并走负责人批准。"
tags: [env-var-audit, 安全合规, 环境变量, 硬编码密钥, secret扫描]
read_when:
  - CI/CD 合并/发布前要扫源码里硬编码的敏感凭证
  - pre-commit 要保证 os.getenv 变量已同步进 .env.example
  - 新项目初始化要查未记录的运行时环境变量防止部署失败
  - 用户说「新人克隆跑不起来」「密码是不是写死在源码里」
ai_protocol: true

---
> 凡自治之物 · LGD 治理学 · 创造术家族 ｜ 评测协议：skill-quality-gate

## English

### When to use
1. CI/CD security gate: before code merge or release, auto-scan source for hardcoded sensitive credentials.
2. Instant developer feedback: with a pre-commit hook, ensure the `os.getenv` variables in committed code are synced to `.env.example`.
3. New-project initialization: check new config scripts for undocumented runtime env vars, preventing missing-dependency deployment failures.

### Usage
- Command: `python env_var_audit.py --path <project dir> --check-hardcoded-sec --json`
- Parameters:
  - `--path`: the source directory or file to scan.
  - `--check-hardcoded-sec`: detect hardcoded secrets (passwords, API keys).
  - `--check-env-examples`: flag variables used in code but not defined in `.env.example`.
  - `--json`: machine-readable JSON report for automation.
- Exit codes: 0 (no findings); 1 (undocumented variables, acceptable); 2 (hardcoded secret or high-priority risk).

### Workflow
1. Prepare the project layout; ensure `.env.example` exists with the needed variable placeholders.
2. Run `python env_var_audit.py --path . --json` to scan the repo.
3. Observe the terminal output and the script's return code (rc).
4. If rc ≠ 0, read the JSON to locate the variable name, file line and risk type.
5. Add the missed variables to `.env.example`, or remove the hardcoded secret.
6. Re-run until rc returns to 0, clearing the audit.

### Evidence & safety statement
- Evidence: TBD (no evaluation / badge link yet; update here once it is produced)
- Version: 1.0.1
- Security: no independent security scan has been performed (TBD); the conclusion is pending and no endorsement is given until it is completed.

## 中文

### 何时用
1. CI/CD 流水线安全门禁：在代码合并或发布前，自动扫描源码中是否存在硬编码的敏感凭证。
2. 开发者即时反馈：结合 Pre-commit hook 使用，确保提交代码中的 `os.getenv` 变量已同步更新到 `.env.example`。
3. 新项目初始化验证：检查新配置脚本是否包含未记录的运行时环境变量，防止依赖缺失导致部署失败。

### 用法
- 命令格式：`python env_var_audit.py --path <项目目录> --check-hardcoded-sec --json`
- 参数说明：
  - `--path`: 指定需要扫描的源代码目录或文件路径。
  - `--check-hardcoded-sec`: 检测硬编码密钥（如密码、API Key）。
  - `--check-env-examples`: 识别代码中使用了但未在 `.env.example` 定义的新变量。
  - `--json`: 生成机器可读的 JSON 报告，便于自动化工具解析。
- 返回码定义：0（无风险问题）；1（发现变量缺失文档但可接受）；2（检测到硬编码密钥或高优先级风险）。

### 流程
1. 准备项目文件结构，确保 `.env.example` 模板存在且包含必要变量占位符。
2. 运行命令 `python env_var_audit.py --path . --json` 扫描当前仓库目录。
3. 观察终端输出结果及 Python 脚本返回码（rc）。
4. 若返回码不为 0，阅读 JSON 输出定位具体的变量名、文件行及风险类型。
5. 将检测到的遗漏变量补充至 `.env.example` 或移除硬编码密钥代码。
6. 重新执行扫描直至返回码恢复为 0，确保审计通过。

### 证据与安全声明
- 证据：TBD（暂无评测/徽章链接；产生后在此更新实际链接）
- 版本：1.0.1
- 安全：未做独立安全扫描（TBD），结论待补；补全前不作推荐背书。
