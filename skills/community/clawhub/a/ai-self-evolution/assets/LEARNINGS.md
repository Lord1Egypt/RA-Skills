# 经验模板

用于记录开发过程中的纠正、洞察与知识缺口。

**Categories**: correction | insight | knowledge_gap | best_practice
**Areas**: frontend | backend | infra | tests | docs | config
**Statuses**: pending | in_progress | resolved | wont_fix | promoted | promoted_to_skill

## 状态定义

| 状态 | 含义 |
|--------|---------|
| `pending` | 尚未处理 |
| `in_progress` | 正在处理 |
| `resolved` | 问题已修复或知识已吸收 |
| `wont_fix` | 决定不处理（原因写入 Resolution） |
| `promoted` | 已提升到 CLAUDE.md 或 AGENTS.md |
| `promoted_to_skill` | 已抽取为可复用 skill |

## Skill 抽取字段

当某条 learning 提升为 skill 时，补充以下字段：

```markdown
**Status**: promoted_to_skill
**Skill-Path**: skills/skill-name
```

示例：
```markdown
## [LRN-20250115-001] best_practice

**Logged**: 2025-01-15T10:00:00Z
**Priority**: high
**Status**: promoted_to_skill
**Skill-Path**: skills/docker-m1-fixes
**Area**: infra

### Summary
Apple Silicon 上 Docker 构建因平台不匹配而失败
...
```

---
