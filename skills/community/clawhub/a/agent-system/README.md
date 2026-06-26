# OpenClaw Agent System Skill

> 🤖 核心智能调度系统 Skill for OpenClaw

---

## 📁 目录结构

```
agents/
├── SKILL.md                    # ⭐ Skill 主定义（触发条件和指导）
├── README.md                   # 本文件
├── orchestrator.js             # Node.js 参考实现
├── test.js                     # 测试脚本
├── references/
│   └── orchestrator-reference.md  # 代码架构参考
└── rules/
    └── AGENT_RULES.md          # Agent 执行规则手册
```

---

## 🚀 快速开始

### 方式一：在 OpenClaw 中直接使用

当用户输入包含以下关键词时，AI 会自动参考 SKILL.md 中的指导：

- "分析"、"原因"、"为什么"
- "规划"、"计划"
- "帮我"、"处理"、"执行"
- "拆解任务"、"分步骤"
- "复杂任务"

### 方式二：运行测试

```bash
cd agents
node test.js
```

### 方式三：作为独立服务运行

```javascript
import { dispatch } from './orchestrator.js';

const result = await dispatch('帮我分析销售下滑的原因');
console.log(result.content);
```

---

## 🎯 核心能力

### 智能复杂度评估

自动判断任务复杂度（1-10），决定执行路径：

| 复杂度 | 执行路径 |
|--------|----------|
| ≤ 3 | Executor → 直接输出 |
| 4-5 | Executor → Reviewer → 输出 |
| > 5 | Planner → Executor → Reviewer → [Heal] → 输出 |

### 意图识别

自动识别用户意图：
- `analysis` — 分析类任务
- `generation` — 生成类任务
- `coding` — 编程任务
- `decision` — 决策类任务
- `planning` — 规划类任务

### 自愈机制

当输出质量不达标时自动重试：
- 第1次：详细推理策略
- 第2次：反向推理策略
- 第3次：降级模式（输出简化结果）

---

## 📋 工作流程

```
用户输入
    ↓
┌─────────────────┐
│   Planner       │ ← 意图识别 + 复杂度评估
│   complexity?   │   - intent
└────────┬────────┘   - complexity
         │            - tasks[]
    ┌────┴────┐
   ≤3        >3
    │         │
    ▼         ▼
 Executor   Planner
    │         ↓
    │      Executor × N
    │         ↓
    │      Reviewer
    │         ↓
    │    score ≥ 70?
    │         │
    │    ┌────┴────┐
    │    │         │
    │   Yes       No
    │    │         │
    │    ▼         ▼
    │  输出    Self-Heal
    │           ↓
    └─────────→ 输出
```

---

## 🔧 配置

### 触发条件

在 `SKILL.md` 的 frontmatter 中定义：

```yaml
---
name: agent-system
description: |
  OpenClaw 核心 Agent 调度系统。当用户描述需要"分析"、"规划"、"拆解任务"时激活。
---
```

### 质量阈值

| 阈值 | 行为 |
|------|------|
| score ≥ 70 | 直接输出 |
| score < 70 | 触发自愈 |
| 重试 ≥ 2 | 降级模式 |

### Token 限制

- 最大输出：2000 tokens（约4000字符）
- 超长自动截断，标注 `[已截断]`

---

## 📊 日志格式

```json
{
  "timestamp": "2026-04-02T11:40:00+08:00",
  "level": "INFO | WARNING | ERROR",
  "module": "orchestrator | planner | executor | reviewer | self_heal",
  "event": "dispatch_start | planner_complete | ... ",
  "details": {}
}
```

---

## 🧪 测试结果

```
==================================================
Agent System 测试开始
==================================================

📝 测试: 简单任务
   Intent: generation
   Complexity: 3
   Tasks: 1
   ✅ 通过

📝 测试: 复杂任务 - 销售分析
   Intent: analysis
   Complexity: 6
   Tasks: 3
   ✅ 通过

📝 测试: 中等任务 - 写邮件
   Intent: generation
   Complexity: 4
   Tasks: 1
   ✅ 通过

==================================================
测试完成 - 3/3 通过 ✅
==================================================
```

---

## 🔗 相关文件

| 文件 | 用途 |
|------|------|
| `SKILL.md` | ⭐ OpenClaw Skill 定义（触发 + 指导） |
| `orchestrator.js` | Node.js 参考实现 |
| `references/orchestrator-reference.md` | 代码架构文档 |
| `rules/AGENT_RULES.md` | Agent 执行规则详细说明 |

---

## 📌 待集成事项

- [ ] 接入真实 LLM API（当前是模拟执行）
- [ ] 持久化 metrics 到文件
- [ ] 增加更多意图识别模式
- [ ] 支持流式输出

---

*最后更新：2026-04-02*
