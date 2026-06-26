---
name: ai-code-migration-risk-assessor
description: 深度分析代码变更风险，评估影响范围并生成可靠重构方案
category: AI
triggers: 代码变更风险, 重构评估, 影响范围分析, 迁移风险, 代码改动分析, PR风险评估
version: 1.0.0
author: OpenClaw Agent
tags:
  - code-analysis
  - risk-assessment
  - refactoring
  - github
  - devops
dependencies:
  - github
  - code-review-skill
  - agentic-devops
---

# AI 代码变更风险评估器 (Code Migration Risk Assessor)

从代码变更出发，深度分析影响范围、关联模块与迁移风险，并生成可落地的重构方案与执行计划。

## 核心价值

- **精准风险识别**：基于 GitHub API 分析变更文件、提交历史与依赖关系，量化风险等级
- **影响范围评估**：智能识别受影响的模块、接口与调用方，降低遗漏风险
- **重构方案生成**：结合代码审查最佳实践，生成分步骤可执行的重构方案
- **一键执行辅助**：通过 agentic-devops 生成变更 diff，验证重构正确性

## 适用场景

- 团队进行大规模代码重构，不确定改动范围
- 合并外部开源项目代码，担心引入未知风险
- 大型 API 协议升级，需要评估波及范围
- Code Review 时需要快速定位高风险改动区域

## 工作流程（4步）

```
Step 1 → 获取变更（github: list-commits / compare / search-code）
   ↓
Step 2 → 深度代码审查（code-review-skill: analyze-diff）
   ↓
Step 3 → 风险量化评估（agentic-devops: audit-logs）
   ↓
Step 4 → 生成重构方案 + 行动计划
```

## 使用方法

### 方式一：完整工作流（推荐）

触发词：
- "帮我分析这个 PR 的风险"
- "评估这次重构的影响范围"
- "分析代码变更风险并生成方案"

### 方式二：指定仓库分析

触发词：
- "分析 /path/to/repo 的变更风险"

### 环境变量

```bash
GITHUB_TOKEN=your_github_pat_token  # GitHub 个人访问令牌
```

## 技术架构

```
GitHub API (变更数据)
    ↓
code-review-skill (Diff 解析 + 模式识别)
    ↓
agentic-devops (依赖关系图谱 + 风险建模)
    ↓
输出: 风险报告 + 重构方案
```

## 风险等级说明

| 等级 | 标识 | 说明 |
|------|------|------|
| P0 | 🔴 严重 | 破坏性变更，影响生产环境核心功能 |
| P1 | 🟠 高危 | 涉及 API 兼容性变更或数据迁移 |
| P2 | 🟡 中危 | 逻辑重构，存在潜在 Bug 风险 |
| P3 | 🟢 低危 | 纯代码格式优化，无运行时影响 |

## 依赖 Skill 说明

### github
提供变更数据获取能力：提交历史、文件差异、代码搜索、仓库信息。

### code-review-skill
对 diff 进行深度审查，识别：潜在 Bug、安全漏洞、性能问题、代码风格问题。

### agentic-devops
提供依赖关系分析、变更审计日志、进程健康监控，辅助风险量化。