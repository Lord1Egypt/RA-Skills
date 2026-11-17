---
name: context-token-budget
description: "Guard AI context usage with a fail-closed token budget — stop burning tokens. 用 fail-closed 的 token 预算守护 AI 上下文，防止积分烧光。 适用场景：当需要估算上下文 token 用量并执行 fail-closed 预算（防止超限烧积分）时使用本技能；触发词：context、token、budget、上下文预算、限额。"
slug: context-token-budget
title: context-token-budget
version: 1.0.1
license: MIT
category: 效率
author: SynomosAI (LGD initiative)
platforms: [windows, macos, linux]
tags: [context,token,budget]
description_zh: "用 fail-closed 的 token 预算守护 AI 上下文，防止积分烧光：中英文感知 token 估算 + 超额退出码 1 + SHA-256 锚点。"
description_en: "Fail-closed token budget guard for AI context: CJK/English-aware token estimation, PASS/FAIL verdict and SHA-256 content anchor."
read_when:
  - 估算一段文本/文件的 token 用量（中英文感知）并执行 fail-closed 预算
  - 上下文超限/积分烧光前要 PASS/FAIL 判定与处置建议
risk_tier: medium
ai_protocol: true
spec: usk/1.0
interface:
  type: cli
  entry_point: scripts/budget.py
  runtime: python3
  call_pattern: args
input_schema:
  args:
    type: string
    description: "命令行参数透传给主脚本，具体取值见 --help"
    required: false
output_schema:
  stdout:
    type: string
    description: "标准输出为 JSON 结果或结构化文本，含逐项检查与总体结论"
  exit_code:
    type: integer
    description: "0=OK/PASS; 1=findings/warnings; 2=usage or argument error"
capabilities:
  - cli_tool
permissions:
  network: false
  filesystem: false
  subprocess: false
requirements:
  python_packages: []
  min_python: "3.8"
changelog: "1.0.1: Bilingual rewrite (full EN+ZH, English first); 1.0.0: initial upload"
---

> 凡自治之物 · LGD 治理学 · 创造术家族 ｜ 评测协议：见平台质量门禁规范

## English

### Capabilities
- CJK/English-aware token estimation.
- Fail-closed budget enforcement with verdict.
- SHA-256 content anchor for reproducibility.

### When to use
- Estimate token usage of a text or file (CJK-aware) and enforce a fail-closed budget.
- Get a PASS/FAIL verdict plus a trim or raise-limit recommendation before context overflows.

### Usage
```bash
python scripts/budget.py <file-or-text> [--limit N] [--json]
```

### Flow
1. Run `python scripts/budget.py <file-or-text> [--limit 8000] [--json]`.
2. Estimate tokens per CJK-aware rules (1.5 chars/token CJK, 4 chars/token others); compute `used_pct`.
3. Output tokens / limit / used% and PASS/FAIL; over-budget → exit code 1 (fail-closed) with trim or raise-limit advice.

### LGD alignment
| Law | How this skill satisfies it |
|---|---|
| Registered | Complete frontmatter (name/description/license/version); clear author & namespace |
| Evidenced | Reproducible output (SHA-256 anchor / structured JSON) with verification method |
| Gated | Minimal privilege, fail-closed exit codes, dangerous ops denied by default |

### Safety boundary
- Static analysis only; never auto-executes external commands.
- On risk detection → FAIL (fail-closed); human decides.
- Does not delete / modify / publish anything on the user's behalf.

### Evidence & safety
- Evidence: TBD. Version: 1.0.1. Security: no independent scan (TBD).

## 中文

### 功能
- 中英文感知的 token 估算
- fail-closed 预算执行与判定
- SHA-256 内容锚点保证可复现

### 何时用
- 当需要估算一段文本或文件的 token 用量（中英文感知）并执行 fail-closed 预算时使用本技能。
- 当需要在上下文超限/积分烧光前得到 PASS/FAIL 判定与处置建议时使用本技能。

### 用法
```bash
python scripts/budget.py <file-or-text> [--limit N] [--json]
```

### 流程
1. 运行 `python scripts/budget.py <file-or-text> [--limit 8000] [--json]`。
2. 脚本按中英文感知规则估算 token（中文 1.5 chars/token、其他 4 chars/token）并计算使用率 used_pct。
3. 输出 tokens/limit/used% 与 PASS/FAIL；超预算（tokens > limit）时退出码为 1（fail-closed），并给出 trim context 或上调 --limit 的建议。

### 三律对齐
| 律 | 本技能如何满足 |
|---|---|
| 有籍 Registered | frontmatter 完整（name/description/license/version），作者与命名空间明确 |
| 有证 Evidenced | 输出可复现（SHA-256 锚点/结构化 JSON），含验证方式 |
| 有门禁 Gated | 最小权限、fail-closed 退出码、危险操作默认拒绝 |

### 安全边界
- 只做静态分析，不自动执行任何外部命令。
- 检出风险即 FAIL（fail-closed），由人决策。
- 不代用户删除/修改/发布任何内容。

### 证据与安全声明
- 证据：TBD（暂无评测/徽章链接；产生后在此更新实际链接）
- 版本：1.0.1
- 安全：未做独立安全扫描（TBD），结论待补；补全前不作推荐背书。
