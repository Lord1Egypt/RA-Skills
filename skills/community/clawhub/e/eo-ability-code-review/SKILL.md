---
name: eo-ability-code-review
description: 代码审查能力，调用CodeReviewer专家进行安全、性能、风格全面审查，输出问题列表和改进建议
metadata:
  openclaw:
    requires: { bins: [] }
    install: []
---

# eo-ability-code-review

> 代码审查能力 - 调用 CodeReviewer 专家进行安全、性能、风格全面审查

## 一句话介绍

调用CodeReviewer专家进行代码安全/性能/风格全面审查，输出问题列表和改进建议。

## 核心功能

- **安全审查**: SQL注入、XSS、CSRF等安全漏洞检测
- **性能审查**: N+1查询、索引缺失、缓存策略等性能问题
- **风格审查**: 代码规范、命名规范、注释完整性
- **综合评分**: 安全/性能/风格/总体四维评分

## 使用方法

```bash
# 全面审查
/code-review /path/to/code --scope all

# 安全审查
/code-review /path/to/code --scope security --rules strict

# 性能审查
/code-review /path/to/code --scope performance
```

## 与EO插件的协同

- 被 eo-workflow-blog 调用（代码质量把关）
- 被 eo-workflow-paper 调用（论文逻辑审查）
- 被 eo-workflow-security-audit 调用（安全漏洞发现）

## 独立运行模式（有EO vs 无EO）

| 模式 | 能力 |
|------|------|
| **有EO插件** | 141专家库（CodeReviewer专家）、真实漏洞检测、重构建议 |
| **无插件（基础）** | LLM代码审查、通用规范检查 |

## 示例

```
🔍 代码审查报告

## 评分
| 维度 | 评分 | 等级 |
|------|------|------|
| 安全 | 85/100 | B+ |
| 性能 | 78/100 | B |
| 风格 | 92/100 | A- |
| **总体** | **85/100** | **B+** |

## 问题列表

### 🔴 高优先级 (3)
1. [安全] SQL 注入风险 - user input directly in query
2. [安全] XSS 漏洞 - 未转义用户输入
3. [性能] N+1 查询问题 - loop 内查询数据库

### 🟡 中优先级 (5)
1. [风格] 变量命名不规范
2. [性能] 缺少索引

## 建议
- 使用参数化查询防止 SQL 注入
- 添加输入验证和转义
- 使用 ORM 的 eager loading
```

## Interface

### Input

```typescript
interface CodeReviewInput {
  codePath: string                // 代码路径
  scope?: 'security' | 'performance' | 'style' | 'all'
  rules?: 'strict' | 'normal' | 'loose'
  language?: string               // 编程语言
}
```

### Output

```typescript
interface CodeReviewOutput {
  scores: {
    security: number            // 0-100
    performance: number         // 0-100
    style: number               // 0-100
    overall: number             // 0-100
  }
  issues: CodeIssue[]
  suggestions: string[]
  summary: string
}
```

---

*🦞⚙️ 钢铁龙虾军团*
