---
name: axioma-skill-evaluator
description: "Axioma 技能评估系统 — OpenClaw 代理的高级技能评估工具。使用此技能来评估和改进你的技能，结合双评估系统：(1) Axioma 5维框架（Structure结构20%、Clarity清晰度20%、Completeness完整性20%、Consistency一致性20%、Functionality功能性20%，满分100分），(2) ISO 25010国际标准框架（8个类别25项标准，满分100分）。包含彩色终端输出、自动结构检查（13项测试）、25项标准评分表、自包含的 evaluator.py 和 eval-skill.py 脚本。适用于：发布前评估技能、根据评估结果改进技能、使用自动+手动分析检查技能质量、任何技能审计或质量检查。触发词：评估技能、发布前评估、改进技能、技能审计、检查技能质量。使用方法：运行 evaluator.py 进行5维评估，运行 eval-skill.py 进行ISO 25010检查。Use when evaluating a skill before publishing, improving a skill based on evaluation results, checking skill quality with automated and manual analysis, or any skill audit or quality check."
---

# 🧪 Axiomata Skill Evaluator — 技能评估系统

> Axiomata 技能评估系统 — OpenClaw 代理的高级技能评估

| 信息 | 值 |
|------|-----|
| **版本** | 2.2.0 — 2026-05-07 |
| **状态** | 运行中 ✅ |
| **评估系统** | 双评估（Axioma 5维 + ISO 25010） |
| **目标分数** | 70+（5维），90%+（ISO自动化），80+（手动） |

---

## 1. 目的和范围

### 目标

结合双评估系统（Axioma 5维 + ISO 25010）全面评估技能质量。
Axiomata 评估系统是自包含的，包含所有必需的工具和脚本。

### 使用时机

| 触发器 | 行动 |
|--------|------|
| "评估技能" | 运行双评估系统 |
| "发布前评估" | 运行完整评估流程 |
| "改进技能" | 分析报告并修复问题 |
| "技能审计" | 执行完整审计 |
| "检查技能质量" | 运行自动化检查 |

### Axiomata 设计原则

```
Axiomata = 自包含 + 通用 + 可改进
```

| 原则 | 描述 |
|------|------|
| 自包含 | 所有工具捆绑在技能内部 |
| 通用 | 适用于任何 OpenClaw 代理 |
| 可改进 | 提供 --improve 选项自动改进 |

---

## 2. 双评估系统

```
╔═══════════════════════════════════════════════════════════╗
║              双评估系统架构                              ║
╠═══════════════════════════════════════════════════════════╣
║                                                           ║
║  ┌─────────────────────────────────────────────────┐      ║
║  │  1. Axioma 5维评估（100分）                    │      ║
║  │                                                │      ║
║  │ 维度：
║  │  ├─ Structure（结构）     → 20%                │      ║
║  │  ├─ Clarity（清晰度）     → 20%                │      ║
║  │  ├─ Completeness（完整性） → 20%                │      ║
║  │  ├─ Consistency（一致性） → 20%                │      ║
║  │  └─ Functionality（功能性） → 20%              │      ║
║  │                                                │      ║
║  │ 目标：70+ 分数 ✅                               │      ║
║  └─────────────────────────────────────────────────┘      ║
║                       ↓                                  ║
║  ┌─────────────────────────────────────────────────┐      ║
║  │  2. ISO 25010 评估（100分）                   │      ║
║  │                                                │      ║
║  │ 类别：8个类别，25项标准                         │      ║
║  │ 自动化检查：13项测试                            │      ║
║  │                                                │      ║
║  │ 目标：自动化 90%+ ✅                           │      ║
║  └─────────────────────────────────────────────────┘      ║
║                       ↓                                  ║
║  ┌─────────────────────────────────────────────────┐      ║
║  │  3. 手动评估（25项标准）                       │      ║
║  │                                                │      ║
║  │ 使用 25项标准评分表手动评估                     │      ║
║  │                                                │      ║
║  │ 目标：80+ 分数                                  │      ║
║  └─────────────────────────────────────────────────┘      ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
```

---

## 3. 捆绑工具

| 文件 | 系统 | 用途 |
|------|------|------|
| `evaluator.py` | Axioma 5维 | 彩色5维评估，捆绑在 skills/axioma-skill-evaluator/ |
| `eval-skill.py` | ISO 25010 | 自动结构检查（13项测试），捆绑在 skills/axioma-skill-evaluator/scripts/ |
| `references/rubric.md` | 评分表 | 25项标准手动评分表 |

### 工具路径

```bash
# evaluator.py 路径
/media/ezekiel/Merlin/.openclaw/workspace/skills/axioma-skill-evaluator/evaluator.py

# eval-skill.py 路径
/media/ezekiel/Merlin/.openclaw/workspace/skills/axioma-skill-evaluator/scripts/eval-skill.py
```

---

## 4. 评估命令

### 完整评估流程

```bash
# 1. Axioma 5维评估（带改进建议）
python3 /media/ezekiel/Merlin/.openclaw/workspace/skills/axioma-skill-evaluator/evaluator.py <skill-path> --verbose --improve

# 2. ISO 25010 自动化检查
python3 /media/ezekiel/Merlin/.openclaw/workspace/skills/axioma-skill-evaluator/scripts/eval-skill.py <skill-path> --verbose
```

### 单独运行

```bash
# 仅 Axioma 5维评估
python3 evaluator.py <skill-path> --verbose

# 仅 ISO 25010 检查
python3 eval-skill.py <skill-path> --verbose

# 带改进建议
python3 evaluator.py <skill-path> --improve
```

### 完整示例

```bash
# 评估 core-files-management
SKILL_PATH=/media/ezekiel/Merlin/.openclaw/workspace/skills/core-files-management

# 运行双评估
python3 evaluator.py $SKILL_PATH --verbose --improve
python3 eval-skill.py $SKILL_PATH --verbose
```

---

## 5. Axioma 5维评估维度

### Structure（结构）— 20%

| 检查项 | 最高分 | 描述 |
|--------|--------|------|
| Header | /5 | frontmatter 完整，包含 name 和 description |
| Sections | /5 | 部分数量充足（至少3个主要部分） |
| Formatting | /5 | 格式化质量（表格、列表、代码块） |
| Meta | /5 | 元信息完整 |

### Clarity（清晰度）— 20%

| 检查项 | 最高分 | 描述 |
|--------|--------|------|
| Description | /5 | 描述完整、清晰 |
| Commands | /5 | 命令存在且正确 |
| Examples | /5 | 示例存在且具体 |
| Constraints | /5 | 约束记录清楚 |

### Completeness（完整性）— 20%

| 检查项 | 最高分 | 描述 |
|--------|--------|------|
| Tools | /5 | 工具记录完整 |
| Prerequisites | /5 | 前提条件明确 |
| Errors | /5 | 错误处理文档化 |
| Edge Cases | /5 | 边缘情况覆盖 |

### Consistency（一致性）— 20%

| 检查项 | 最高分 | 描述 |
|--------|--------|------|
| Axioma Alignment | /5 | Axiomata 系统对齐 |
| Style | /5 | 样式一致性 |
| Naming | /5 | 命名一致性 |
| Integration | /5 | 集成度 |

### Functionality（功能性）— 20%

| 检查项 | 最高分 | 描述 |
|--------|--------|------|
| Commands | /10 | 命令语法正确 |
| Results | /5 | 结果正确性 |
| Integration | /5 | 集成功能 |

---

## 6. ISO 25010 评分表（25项标准）

| 类别 | 最高分 | 检查项 |
|------|--------|--------|
| 功能适用性 | /12 | 技能是否按描述工作 |
| 可靠性 | /12 | 错误处理、稳定性 |
| 性能 | /8 | 资源使用、响应时间 |
| 可用性（AI） | /12 | 命令清晰度、结构化 |
| 可对用性（人类） | /8 | 可读性、导航 |
| 安全性 | /12 | 权限、安全检查 |
| 可维护性 | /12 | 代码质量、文档 |
| 代理特定 | /24 | 代理集成、Axiomata 对齐 |

---

## 7. 评估目标

| 系统 | 指标 | 目标 | 当前状态 |
|------|------|------|----------|
| Axioma 5维 | 总分 | 70+ | ✅ 达标 |
| ISO 25010 | 自动化检查 | 90%+ (12/13) | ⚠️ 需改进 |
| 手动 | 25项标准 | 80+ | 需手动检查 |

---

## 8. 分数解释

| 分数范围 | 状态 | 说明 |
|----------|------|------|
| 90-100 | 🟢 优秀 | 卓越品质，准备发布 |
| 70-89 | 🟡 良好 | 通过，可以发布 |
| 50-69 | 🟠 需要工作 | 需要改进 |
| 0-49 | 🔴 不合格 | 严重问题，需要大量工作 |

---

## 9. 改进建议

### 低分修复指南

| 维度 | 低于15分时的修复 |
|------|-----------------|
| **Structure** | 添加缺失部分、改进格式、确保 frontmatter 完整 |
| **Clarity** | 添加示例、命令、约束、改进描述 |
| **Completeness** | 添加工具、前提条件、错误处理、边缘情况 |
| **Consistency** | 添加 Axiomata 标记、样式一致性、统一命名 |
| **Functionality** | 修复命令语法、验证结果、测试集成 |

### 自动化检查失败

```
ISO 25010 失败检查项 → 对应修复：
- Frontmatter 缺失 → 添加完整的 ---
- 没有 description → 添加清晰的 description
- 没有 usage 部分 → 添加工具和使用说明
```

---

## 10. 自包含工作流程

```
╔═══════════════════════════════════════════════════════════╗
║            自包含评估工作流程                            ║
╠═══════════════════════════════════════════════════════════╣
║                                                           ║
║  Step 1: 读取技能                                         ║
║  → 读取 SKILL.md 和所有相关文件                          ║
║                                                           ║
║  Step 2: 自动化检查                                       ║
║  → eval-skill.py (ISO 25010)                              ║
║  → 目标: 90%+ (12/13)                                    ║
║                                                           ║
║  Step 3: Axioma 5维评估                                   ║
║  → evaluator.py                                           ║
║  → 目标: 70+                                              ║
║                                                           ║
║  Step 4: 手动 25项评分                                    ║
║  → 使用 rubric.md                                         ║
║  → 目标: 80+                                              ║
║                                                           ║
║  Step 5: 改进                                             ║
║  → --improve 标志生成改进建议                             ║
║                                                           ║
║  Step 6: 重新评估                                         ║
    → 重复 Step 2-4 直到目标达成
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
```

---

## 11. 边缘情况

| 情况 | 处理方法 |
|------|----------|
| 评估超时 | 增加超时时间或减少测试数量 |
| 路径无效 | 使用绝对路径 |
| 分数不达标 | 首先修复最低维度 |
| 自动化失败 | 检查文件权限 |
| 找不到 evaluator.py | 检查技能目录结构 |
| 没有 SKILL.md | 创建基础 SKILL.md 然后重新评估 |

---

## 12. 评分报告格式

```
╔═══════════════════════════════════════════════════════════╗
║              评分报告格式                                ║
╠═══════════════════════════════════════════════════════════╣
║                                                           ║
║  ╔═══════════════════════════════════════════════════╗   ║
║  ║  📊 SKILL EVALUATION REPORT — <skill-name>       ║   ║
║  ╠═══════════════════════════════════════════════════╣   ║
║  ║  Path: <path>                                   ║   ║
║  ║  Score: XX/100 🟡 GOOD                          ║   ║
║  ╠═══════════════════════════════════════════════════╣   ║
║  ║  STRUCTURE       XX/20 [████████████████████░░] ║   ║
║  ║  CLARITY        XX/20 [████████████████████░░]  ║   ║
║  ║  COMPLETENESS   XX/20 [████████████████████░░]  ║   ║
║  ║  CONSISTENCY    XX/20 [████████████░░░░░░░░░░░] ║   ║
║  ║  FUNCTIONALITY  XX/20 [████████████░░░░░░░░░░░] ║   ║
║  ╠═══════════════════════════════════════════════════╣   ║
║  ║  STATUS: ✅ APPROVED / ❌ NEEDS WORK            ║   ║
║  ╚═══════════════════════════════════════════════════╝   ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
```

---

## 13. 相关技能

| 技能 | 描述 |
|------|------|
| clawhub-publish-workflow | 发布技能到 ClawHub 的完整工作流程 |
| core-files-management | 管理核心文件 |

---

_In Altum Per Quality._
🧪 Axiomata Skill Evaluator v2.2