---
name: badge-studio
description: "Generate ORCID-style fresh badges (20px, color-coded, thin type) for any project. 为任意项目生成 ORCID 清新风格徽章（20px、四色、细字）。 适用场景：当需要为项目或技能生成 SVG 徽章时使用本技能；触发词：badge、studio、徽章、VERIFIED。"
slug: badge-studio
title: badge-studio
version: 1.0.1
license: MIT
category: 设计
author: SynomosAI (LGD initiative)
platforms: [windows, macos, linux]
tags: [badge,studio]
description_zh: "为任意项目生成 ORCID 清新风格徽章（20px、四色、细字、shields 兼容 SVG）。"
description_en: "Generate ORCID-style fresh badges (20px, color-coded, thin type, shields-compatible SVG) for any project."
read_when:
  - 为项目/技能生成 20px 标准高、四色图标块、细字 SVG 徽章
  - 把评分结果渲染为零依赖 SVG 徽章（REG/TRUST/SAFE/MACH/LGD/VERIFIED）
risk_tier: medium
ai_protocol: true
spec: usk/1.0
interface:
  type: cli
  entry_point: scripts/badge_studio.py
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
- 20px standard height, shields-compatible
- Color-coded icon blocks (REG blue / TRUST teal / SAFE green / MACH violet)
- Zero-dependency SVG output

### When to use
- Generate an ORCID-fresh-style badge (20px height, four-color blocks, thin type, shields-compatible) for a project or skill.
- Render a score as a zero-dependency SVG badge (REG / TRUST / SAFE / MACH / LGD / VERIFIED palettes).

### Usage
```bash
python scripts/badge_studio.py --label LGD --score 90/100 [--color 2563eb] [--out out.svg]
```

### Flow
1. Run `python scripts/badge_studio.py --label <text> --score <e.g. 90/100> [--icon LGD] [--color <hex>] [--out out.svg]`.
2. The script draws a 20px SVG using built-in COLORS (REG=2563eb / TRUST=0d9488 / SAFE=16a34a / MACH=7c3aed; `--color` overrides).
3. Write the badge file to `--out` (default `badge.svg`).

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
- 20px 标准高度，与 shields 兼容
- 四色图标块（REG蓝 / TRUST青 / SAFE绿 / MACH紫）
- 零依赖 SVG 输出

### 何时用
- 当需要为项目或技能生成 ORCID 清新风格徽章（20px 标准高、四色图标块、细字、shields 兼容）时使用本技能。
- 当需要把评分结果渲染为零依赖 SVG 徽章（REG/TRUST/SAFE/MACH/LGD/VERIFIED 配色）时使用本技能。

### 用法
```bash
python scripts/badge_studio.py --label LGD --score 90/100 [--color 2563eb] [--out out.svg]
```

### 流程
1. 运行 `python scripts/badge_studio.py --label <文字> --score <如 90/100> [--icon LGD] [--color <hex>] [--out out.svg]`。
2. 脚本按内置 COLORS 映射（REG=2563eb / TRUST=0d9488 / SAFE=16a34a / MACH=7c3aed，`--color` 可覆盖）绘制 20px 高 SVG。
3. 写出 `--out` 指定的徽章文件（默认 badge.svg）。

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
