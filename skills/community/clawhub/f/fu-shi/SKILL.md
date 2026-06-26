---
version: 1.0.35
---

# 伏矢·路径魄 (Fu Shi - Path Planner)

> **七魄之二·伏矢**
> 职掌：任务规划、策略选择、目标拆解

---

## 技能简介

「伏矢·路径魄」是贫道的任务规划模块，职掌任务分解与策略规划。

**核心职责**：
- 将复杂任务拆解为可执行步骤
- 制定执行策略与优先级
- 路径规划与目标追踪

---

## 技能ID

```
fu-shi
```

---

## 能力清单

### 1. 任务拆解 (decompose)

将复杂任务拆解为有序的子任务。

**输入**：`task` (string) - 待拆解的任务描述

**输出**：
```yaml
subtasks:
  - id: 1
    name: 子任务名称
    description: 详细描述
    priority: high|medium|low
    dependencies: [依赖的任务ID]
```

---

### 2. 策略规划 (plan)

为给定目标制定执行策略。

**输入**：`goal` (string) - 目标描述
**输出**：
```yaml
strategy:
  approach: 直接|迭代|分治|回溯
  steps: 执行步骤列表
  estimatedTime: 预估时间
  risks: 潜在风险
```

---

### 3. 目标追踪 (track)

追踪任务执行进度。

**输入**：`taskId` (string) - 任务ID
**输出**：
```yaml
progress:
  completed: 已完成数
  remaining: 剩余数
  current: 当前任务
  blockers: 阻碍因素
```

---

---

## 聚合技能

本魄作为规划中枢，协调执行方向：

| 现有技能 | 调用方式 | 整合说明 |
|---------|---------|---------|
| `flutter` | 执行 | Flutter App 开发任务规划 |
| `mobile-app-builder` | 执行 | 移动开发任务规划 |
| `grape` | 执行 | 葡萄H5项目规划 |
| `bodhi-three-hun-and-seven-po` | 元技能 | 三魂七魄根基，协调各魄 |

---

## 魂魄注解

伏矢为主，尸狗为辅——规划先行，安全随行。
