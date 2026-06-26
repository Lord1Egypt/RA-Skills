---
name: eo-ability-dream
description: 自我进化能力(Dream Module)，空闲时自动分析失败案例，学习新模式，更新Pattern库
metadata:
  openclaw:
    requires: { bins: [] }
    install: []
---

# eo-ability-dream

> 自我进化能力 (Dream Module) - 睡觉时也在进化，自动学习新模式

## 一句话介绍

灵感来自"钢铁龙虾军团睡觉时也在进化"，空闲时自动分析失败案例，学习新模式，更新Pattern库。

## 核心功能

- **失败分析**: 空闲时分析失败案例，找出问题根因
- **模式学习**: 学习新的专家协作模式
- **Pattern更新**: 自动更新Pattern Library
- **Checkpoint优化**: 优化验证策略

## 使用方法

### 启动 Dream

```bash
# 启动做梦模式
/dream

# 指定学习方向
/dream "重点学习架构设计模式"

/dream "分析最近3次失败的代码审查"
```

### 查看状态

```bash
# 查看 Dream 状态
/dream status

# 输出：
# 🌙 Dream Module 状态
# 状态: sleeping
# 上次活跃: 2026-04-07 10:00
# 学到的模式: 15
# 改进建议: 3
```

## 与EO插件的协同

- 独立使用
- 被案例7（多智能体团队协作）展示

## 独立运行模式（有EO vs 无EO）

| 模式 | 能力 |
|------|------|
| **有EO插件** | 空闲时自动触发、分析真实工作日志、更新Pattern库 |
| **无插件（基础）** | 手动触发、通用模式学习 |

## Dream Process

```
1. 分析最近的工作日志
2. 识别失败模式
3. 学习成功案例
4. 更新 Pattern Library
5. 优化 Checkpoint 策略
6. 生成改进建议
```

## Interface

### Input

```typescript
interface DreamInput {
  action: 'sleep' | 'wake' | 'status' | 'learn' | 'report'
  focus?: string[]          // 重点学习方向
  analyzeCases?: string[]   // 要分析的案例
}
```

### Output

```typescript
interface DreamOutput {
  status: 'sleeping' | 'working' | 'idle'
  improvements: Improvement[]
  patternsLearned: number
  dreamLog?: string
}
```

---

*🦞⚙️ 钢铁龙虾军团 - 让进化永不停歇*
