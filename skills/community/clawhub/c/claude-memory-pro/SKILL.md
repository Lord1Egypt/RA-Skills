---
name: claude-memory-pro
description: 进化版统一记忆系统，融合Claude Code的5层记忆架构+Token预算管理+智能成本追踪。当用户要求记忆跨会话信息、智能管理Token预算、优化AI调用成本、构建个人知识库、跨项目学习进化时使用。
---

# Claude Memory Pro

> 进化版统一记忆系统 - Claude Code核心技能提炼与升级

## 核心能力

1. **5层记忆架构** - 热记忆 → 会话记忆 → 长期记忆 → 实体银行 → 反思层
2. **Token预算管理** - 智能追踪、边际收益检测、自动决策
3. **成本追踪优化** - 多维度统计、实时显示、优化建议
4. **跨会话学习** - 从历史交互中持续进化

## 记忆类型（4类）

| 类型 | 用途 | 示例 |
|-----|------|------|
| user | 用户偏好、背景 | 语言习惯、工作风格 |
| feedback | 工作指导、纠正 | 代码规范、回复偏好 |
| project | 项目上下文、决策 | 技术选型、截止日期 |
| reference | 外部系统指针 | API文档、数据库地址 |

## 5层记忆架构

```
memory/
├── hot/                     # Layer 1: 热记忆（当前对话）
│   └── current_turn.md
├── session/                 # Layer 2: 会话记忆
│   └── session_YYYY-MM-DD.md
├── typed/                   # Layer 3: 长期记忆
│   ├── user/
│   ├── feedback/
│   ├── project/
│   └── reference/
├── bank/                    # Layer 4: 实体银行
│   ├── entities/
│   └── procedures/
└── reflections/             # Layer 5: 反思层
```

## Token预算管理

### 预算阈值配置

```typescript
const BUDGET_CONFIG = {
  completionThreshold: 0.9,    // 90% 触发完成检查
  diminishingThreshold: 500,   // 边际收益递减阈值
  maxContinuations: 10,        // 最大继续次数
  warningThreshold: 0.75       // 75% 警告阈值
}
```

### 决策流程

```
Token使用检查
      ↓
< 75% → 正常继续
      ↓
< 90% → 继续 + nudge
      ↓
边际递减？ → 停止（边际收益递减）
      ↓
之前有继续？ → 停止（正常完成）
```

### 边际收益检测

```typescript
function isDiminishing(tracker): boolean {
  return tracker.continuationCount >= 3 &&
         delta < 500 &&
         lastDelta < 500
}
```

## 成本追踪

### 成本指标

| 类型 | 说明 | 优化价值 |
|-----|------|---------|
| input_tokens | 输入tokens | 高 |
| output_tokens | 输出tokens | 中 |
| cache_read | 缓存命中 | 低成本 |
| cache_creation | 缓存创建 | 一次性成本 |
| web_search | 搜索请求 | 按需优化 |

### 优化策略

1. **复用缓存** - 相同上下文用cache_read
2. **压缩上下文** - 减少input_tokens
3. **精简输出** - 减少output_tokens
4. **批量操作** - 减少API调用

## 记忆保存流程

### 对话前
1. 读取MEMORY.md获取索引
2. 按需加载typed/相关记忆

### 对话中
- 热记忆写入hot/current_turn.md
- 实时成本监控

### 对话后
1. 评估值得保留的信息
2. 选择正确的记忆层
3. 更新MEMORY.md索引

## 决策树

```
用户给反馈/纠正
├─ 关于用户本身 → typed/user/
├─ 关于工作方式 → typed/feedback/
├─ 关于项目 → typed/project/
└─ 关于外部系统 → typed/reference/

了解用户背景 → typed/user/
项目决策/变化 → typed/project/
外部系统位置 → typed/reference/
复杂档案 → bank/entities/
可复用流程 → bank/procedures/
自我反思 → reflections/
```

## 不保存内容

- 代码模式（可从代码推导）
- Git历史（git log权威）
- 临时任务状态（用tasks）
- 已文档化的内容（CLAUDE.md）
- 未经证实的推断
- 整段对话记录
- 大段代码

## 快速开始

### 初始化
```bash
mkdir -p memory/{hot,session,typed/{user,feedback,project,reference},bank/{entities,procedures},reflections}
```

### 创建记忆
```markdown
---
name: 用户回复偏好
type: feedback
created: 2026-04-02
---

用户不希望在每次回复末尾总结。

**Why:** 用户说"我能直接读懂diff"
**How to apply:** 保持简洁，不添加总结性语句
```

## 维护检查

- [ ] 每月检查typed/过时记忆
- [ ] 每季度清理reflections/
- [ ] 验证实体银行信息准确性
- [ ] 检查Token预算使用效率
- [ ] 评估成本优化效果

## 与其他技能对比

| 特性 | 基础版 | Pro版 |
|-----|-------|-------|
| 记忆层数 | 3层 | 5层 |
| Token管理 | 无 | 智能预算 |
| 成本追踪 | 无 | 多维度统计 |
| 跨会话学习 | 基础 | 反思进化 |
| 优化建议 | 无 | 自动生成 |
