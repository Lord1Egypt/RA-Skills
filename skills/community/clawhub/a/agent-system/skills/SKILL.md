---
name: agent-system
description: |
  OpenClaw 核心 Agent 调度系统。当用户描述需要"分析"、"规划"、"拆解任务"、"多步骤处理"、"自动执行复杂任务"时激活。
  基于复杂度自动选择最优执行路径。
---

# OpenClaw Agent System

## 核心概念

这是一个**智能调度框架**，包含：
- 🎯 **Orchestrator** - 调度中枢，根据复杂度路由
- 📋 **Planner** - 任务规划 + 复杂度评估
- ⚡ **Executor** - 任务执行
- 🔍 **Reviewer** - 质量审查
- 🔧 **Self-Heal** - 自愈重试
- 📊 **Metrics** - 指标追踪

## 调度规则

### 复杂度阈值

| 复杂度 | 路径 |
|--------|------|
| ≤ 3 | Executor → 直接输出 |
| 4-5 | Executor → Reviewer → 输出 |
| > 5 | Planner → Executor → Reviewer → [Heal] → 输出 |

### 复杂度评估

**高复杂度指标**（满足任一即提升复杂度）：
- 包含"分析"、"原因"、"为什么"
- 包含"比较"、"规划"、"设计"
- 包含"系统"、"复杂"、"全面"、"详细"

**复杂度等级**：
- 1-3：简单任务（直接执行）
- 4-5：中等任务（执行+审查）
- 6-10：复杂任务（规划+执行+审查+自愈）

## 执行流程

```
用户输入
    ↓
┌─────────────────┐
│   Planner       │ ← 意图识别 + 复杂度评估
│   complexity?   │
└────────┬────────┘
         │
    ┌────┴────┐
   ≤3        >3
    │         │
    ▼         ▼
 Executor   Planner
    │         ↓
    │      [任务拆解]
    │         ↓
    │      Executor
    │      (多任务)
    │         ↓
    │      Reviewer
    │      (质量评分)
    │         ↓
    │    score < 70?
    │         │
    │    ┌────┴────┐
    │    │         │
    │   Yes       No
    │    │         │
    │    ▼         ▼
    │  Self-Heal  输出
    │    ↓
    │  重试 < 3?
    │    │
    │  ┌─┴────────┐
    │ │          │
    │ Yes       No → degraded_mode
    │  │
    │  └──────────→ 重试
    │
    └──────────────→ 输出
```

## 意图识别

自动识别用户意图：

| Intent | 关键词 |
|--------|--------|
| analysis | 分析、原因、为什么、分析一下 |
| generation | 写、生成、创建、编写 |
| coding | 代码、编程、写程序、开发 |
| decision | 选择、决定、哪个好、比较 |
| planning | 计划、安排、规划 |

## 输出规范

### 标准响应格式

```json
{
  "success": true,
  "content": "执行结果内容",
  "plan": {
    "intent": "analysis | generation | ...",
    "complexity": 1-10,
    "tasks": [
      {
        "task_id": "t1",
        "type": "analysis | generate | transform | validate",
        "description": "任务描述",
        "input": "输入内容",
        "expected_output": "预期输出"
      }
    ]
  },
  "metrics": {
    "tokens": 1500,
    "truncated": false,
    "quality_score": 85,
    "heal_triggered": false,
    "degraded_mode": false
  }
}
```

### 质量阈值

- `score ≥ 70` → 直接输出
- `score < 70` → 触发 Self-Heal
- 重试次数 ≥ 2 → 进入 `degraded_mode`（降级模式）

## 自愈规则

### 触发条件

满足任一即触发自愈：
- `score < 70`
- 检测到占位符 `{xxx}`
- 检测到禁止提问语句

### 重试策略

| 重试次数 | 策略 | 说明 |
|----------|------|------|
| 第1次 | detailed_reasoning | 增加思考链长度 |
| 第2次 | reverse_reasoning | 反向推理（从目标倒推） |
| 第3次 | degraded_mode | 降级，输出简化结果 |

### 禁止提问规则

**不允许**出现以下语句：
- "请提供…"
- "你可以告诉我…"
- "我需要更多信息…"

**条件分支**：
- 若信息足以完成任务 → 不得提问，直接执行
- 若信息不足以完成任务 → 填充默认值或标注缺失项，继续执行
- 绝对不卡死等待用户回复

## 推断结论标注

当信息不足需要推断时，必须标注置信度：

```
[推断结论 · 置信度: 高/中/低 · 待数据验证]
```

## Token 控制

- 最大输出：`2000 tokens`（约4000字符）
- 超长输出自动截断，标注 `[已截断]`

## 日志格式

所有 Agent 日志输出 JSON：

```json
{
  "timestamp": "2026-04-02T11:40:00+08:00",
  "level": "INFO | WARNING | ERROR",
  "module": "orchestrator | planner | executor | reviewer | self_heal",
  "event": "事件名称",
  "details": {}
}
```

### 日志级别

- `INFO`：正常流程（开始/完成/切换）
- `WARNING`：异常但未失败（占位符已填充/置信度低）
- `ERROR`：执行失败/触发自愈

## 指标追踪

每次执行记录：
- `error_rate` - 错误率
- `output_score` - 质量评分
- `heal_trigger_count` - 自愈触发次数
- `degraded_mode_count` - 降级模式次数

## 参考实现

`src/orchestrator.js` 包含完整的参考实现，可作为：
1. 独立调度服务运行
2. 代码级参考
3. 未来集成到 OpenClaw 内核

## 使用示例

### 简单任务
用户："今天天气怎么样"  
→ complexity = 3 → Executor → 直接输出

### 复杂任务
用户："帮我分析销售下滑的原因"  
→ complexity = 6 → Planner → Executor × 3 → Reviewer → [自愈] → 输出

### 中等任务
用户："帮我写一封道歉邮件"  
→ complexity = 4 → Executor → Reviewer → 输出

---

*本 Skill 提供工作流指导，实际执行由 AI 基于上下文判断*
