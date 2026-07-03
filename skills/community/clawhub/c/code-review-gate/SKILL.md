---
name: code-review-gate
version: 0.2.1
summary: 自动对 git diff 执行 7 维度结构化代码审查，输出分级报告并阻塞 Critical 问题
description: |
  AI 代码审查门禁 — 对 git diff 执行全面的静态分析，覆盖功能正确性、安全性、
  性能、可读性、可维护性、测试覆盖、文档同步 7 个维度。按 Critical / Important /
  Minor 三级严重度输出结构化报告，存在 Critical 问题时门禁阻塞（exit code 1）。
tags:
  - code-review
  - quality-gate
  - ci-cd
  - static-analysis
  - security-scan
  - developer-tools
  - python
author: Community
license: MIT
homepage: https://github.com/Terr123123/code-review-gate
repository: https://github.com/Terr123123/code-review-gate
runtime: python
requires_python: ">=3.10"
requires_git: ">=2.0"
permissions:
  read:
    - git_diff       # 读取 git diff 内容
    - filesystem     # 读取设计文档（--design 参数）
    - subprocess     # 调用 git diff 命令
  write: []          # 不执行任何写操作
  network: []        # 无网络请求
security_notes: |
  本技能仅执行本地静态分析，不修改任何文件。
  使用 subprocess.run 仅调用 git diff（只读命令），不接受外部输入。
  所有正则匹配在本地内存中执行，不发送任何数据到外部服务。
---

# Code Review Gate — AI 代码审查门禁 Skill

> OpenClaw Skill: 自动对 git diff 执行结构化代码审查，输出分级报告并阻塞 Critical 问题。

## 场景描述 (When to Use)

- 开发者完成一轮代码修改，准备合并到主分支前
- CI/CD 流水线中需要自动化代码审查门禁
- Pull Request 提交后，需要 AI 先做一轮预审
- 任何需要确保代码质量、安全性和设计一致性的场景

## 决策规则 (Decision Rules)

1. **阻塞条件**: 任何 Critical 级别问题（安全漏洞/功能错误/数据风险）未修复 → 门禁不通过，禁止进入下一阶段
2. **警告条件**: Important 级别问题存在但无不阻塞，记录并建议修复
3. **通过条件**: 所有 mandatory 检查项均通过 AND blocking_issues == 0
4. **跳过条件**: 变更规模为 docs/config/prompt/chore 且风险 ≤ low 时，本门禁可跳过（由上游流程判断）

## 审查维度 (Check Categories)

| 维度 | 严重级别 | 说明 |
|------|----------|------|
| 功能正确性 (functional) | Critical | 逻辑错误、边界条件、错误处理、并发问题 |
| 安全性 (security) | Critical | SQL注入、XSS、命令注入、敏感信息泄露、权限控制 |
| 性能 (performance) | Important | O(n²)复杂度、N+1查询、正则回溯、资源泄漏 |
| 可读性 (readability) | Important | 命名规范、职责单一、注释质量、代码简洁 |
| 可维护性 (maintainability) | Important | SOLID原则、依赖关系、配置外部化、日志规范 |
| 测试覆盖 (testing) | Critical | 单元测试、边界测试、异常测试、断言清晰 |
| 文档同步 (documentation) | Minor | API文档、变更记录、README同步 |

## 使用示例 (Usage)

### 基础用法 — 审查当前未提交的改动

```bash
openclaw run code-review-gate --base HEAD~1 --head HEAD
```

### 审查指定 commit 范围

```bash
openclaw run code-review-gate --base abc1234 --head def5678
```

### 审查指定文件

```bash
openclaw run code-review-gate --files "src/api/*.py,src/services/*.py" --design design.md
```

### 传入设计文档做一致性校验

```bash
openclaw run code-review-gate --base main --head feature-branch --design openspec/changes/feat-001/design.md
```

## 参数说明

| 参数 | 必需 | 说明 |
|------|------|------|
| `--base` | 是* | git diff 基准 commit/branch |
| `--head` | 是* | git diff 目标 commit/branch |
| `--files` | 否 | 限定审查的文件路径（glob 模式） |
| `--design` | 否 | 设计文档路径，用于对比实现一致性 |
| `--severity` | 否 | 最低报告级别: critical / important / minor (默认 important) |
| `--format` | 否 | 输出格式: markdown / json / terminal (默认 markdown) |
| `--max-lines` | 否 | 单次审查最大行数限制 (默认 1000) |

> \* `--base` + `--head` 与 `--files` 二选一

## 输出格式 (Output)

审查完成后生成结构化报告：

```markdown
## Code Review Report — [timestamp]

**Range:** abc1234..def5678
**Files Changed:** 12 | **Lines:** +345 -120
**Design Doc:** openspec/changes/feat-001/design.md

---

### Strengths
- Clean separation of concerns in service layer
- Comprehensive error handling with proper fallbacks
- Well-structured test cases covering edge scenarios

### Issues

#### Critical (Must Fix — 2 issues)
1. **SQL Injection in user query** [src/api/users.py:45]
   - What: Raw string formatting used in SQL WHERE clause
   - Risk: Allows arbitrary SQL execution via crafted input
   - Fix: Use parameterized queries with `?` placeholders

2. **Missing auth check** [src/api/admin.py:120]
   - What: Admin endpoint lacks authentication middleware
   - Risk: Unauthenticated access to sensitive admin operations
   - Fix: Add `@require_auth` decorator

#### Important (Should Fix — 3 issues)
1. **N+1 query in list endpoint** [src/services/order.py:78]
   - ...

#### Minor (Nice to Have — 2 issues)
1. **Inconsistent variable naming** [src/utils/parser.py:33]
   - ...

### Design Consistency Check
- ✅ API signature matches design doc
- ⚠️ One endpoint (`GET /api/v2/users`) not documented in design
- ✅ Data model matches schema definition

### Recommendations
- Add input sanitization middleware
- Consider query batching for list endpoints

### Assessment

**Gate: ❌ BLOCKED**

**Reasoning:** 2 critical issues must be resolved before merge — SQL injection and missing authentication. Important issues should be addressed but do not block.
```

## 门禁结果码

| 退出码 | 含义 | CI 行为 |
|--------|------|---------|
| 0 | 通过 — 无 Critical 问题 | 允许合并 |
| 1 | 阻塞 — 存在 Critical 问题 | 阻止合并 |
| 2 | 错误 — 工具自身异常 | 标记为 CI 失败 |
| 3 | 跳过 — 变更不符合审查条件 | 允许合并 |

## 依赖

- `git` — 命令行工具，用于获取 diff
- Python ≥ 3.10
- `bandit` — Python 安全扫描 (可选，增强安全检测)
- `radon` — 代码复杂度分析 (可选)

## 与 OpenClaw 框架的集成

本 Skill 可作为 OpenClaw 流水线中的独立阶段：

```typescript
import { defineAgent } from "openclaw";
import { CodeReviewGateSkill } from "@community/code-review-gate";

const agent = defineAgent({
  name: "dev-workflow-agent",
  description: "Development workflow with code review gate",
  model: "claude-sonnet-4-20250514",
  skills: [
    new CodeReviewGateSkill({
      severity: "critical",
      maxLines: 1000,
    }),
  ],
});
```

## 配置选项

通过 `gate.config.yaml` 自定义检查项：

```yaml
# gate.config.yaml — 可选配置文件
severity_threshold: critical       # 阻塞级别
max_diff_lines: 1000              # 单次最大审查行数
skip_patterns:                    # 跳过审查的文件模式
  - "*.md"
  - "*.json"
  - "docs/**"
  - "*.lock"
require_design_doc: true          # 是否强制要求设计文档
enabled_checks:                   # 启用的检查维度
  - functional
  - security
  - performance
  - testing
  - documentation
auto_fix_suggestions: true        # 是否生成修复建议
```
