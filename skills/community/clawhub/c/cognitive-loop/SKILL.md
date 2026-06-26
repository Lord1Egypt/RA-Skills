---
name: cognitive-loop
description: 认知闭环执行 Skill - 实现「思考-行动-反思-测试」四环闭环的高自主性 Agent 架构。当需要任务规划、多步骤执行、错误恢复、测试验证时激活。
install:
  verify:
    - Inspect source code at https://github.com/World-peace001/cognitive-agent
    - Check npm package integrity at https://www.npmjs.com/package/cognitive-agent
  sandbox: memory/patterns memory/lessons memory/successes memory/knowledge
  allow:
    exec: false
    env: false
---

# 🧠 Cognitive Loop - 认知闭环 Skill

## 概述

认知闭环是 OpenClaw Agent 的核心执行引擎，实现高自主性的「思考 - 行动 - 反思」闭环。

## ⚠️ 安全使用指南

使用前请务必：
1. **审核代码**：检查 GitHub 仓库源代码
2. **沙箱执行**：首次使用时在沙箱环境中测试
3. **路径限制**：仅允许写入 `memory/` 子目录
4. **禁止自主执行**：复杂操作需用户确认

## 四大核心模块

| 模块 | 职责 | 能力体现 |
|------|------|----------|
| **规划器 (Planner)** | 任务分解、路径规划、策略选择 | Chain-of-Thought / Tree-of-Thought 推理 |
| **执行监控器 (Monitor)** | 实时跟踪、错误检测、动态调整 | 自动重试、降级、异常恢复 |
| **反思器 (Reflector)** | 执行复盘、经验沉淀、策略优化 | 自主学习、模式提取、教训总结 |
| **测试器 (Tester)** | 测试生成、结果验证、闭环修复 | TDD 驱动、覆盖率分析、自动修复 |

## 激活条件

收到以下类型任务时**必须**激活：

1. **开发任务**：前端页面、后端 API、数据库设计、DevOps 部署
2. **多步骤任务**：需要拆解为多个子任务、有依赖关系
3. **TDD/测试任务**：用户明确要求测试驱动开发
4. **重构优化**：性能优化、代码重构、架构调整
5. **复杂需求**：需求模糊或涉及多个功能模块

## 安装方式

### 方式一：npm 安装（推荐）

```bash
npm install cognitive-agent
```

### 方式二：ClawHub 安装

```bash
openclaw skills install cognitive-loop
```

### 方式三：源码安装

```bash
git clone https://github.com/World-peace001/cognitive-agent.git
cd cognitive-agent
npm install
```

## 激活方式

### 重要：必须先审核代码

首次使用时，请：
1. 检查 GitHub 仓库的源代码
2. 确认 npm 包的完整性
3. 在沙箱环境中测试

### 激活方式

当收到符合激活条件的任务时：

1. **用户确认**：必须获得用户明确同意
2. **代码审核**：自行或让用户审核将执行的代码
3. **沙箱执行**：建议在沙箱环境中首次运行

### 推荐的闭环模式

```javascript
// 伪代码示例 - 实际使用需先安装 cognitive-agent 包
import CognitiveOrchestrator from 'cognitive-agent';

const orchestrator = new CognitiveOrchestrator();

const result = await orchestrator.闭环(
  '任务描述',
  async (task, context) => {
    // 执行实际任务
    return { status: 'success' };
  }
);
```

## 闭环执行流程

```
用户需求
    │
    ▼
┌────────┐ → 任务理解 → 策略选择 → 执行计划
│ 规划器 │
└────────┘
    │
    ▼
┌────────┐ → 执行 → 进度追踪 → 异常处理
│ 执行监控│
└────────┘
    │
    ▼
┌────────┐ → 评估结果 → 经验入库 → 优化建议
│ 反思器 │
└────────┘
    │
    ▼
┌────────┐ → 测试生成 → 覆盖率验证 → 闭环修复
│ 测试器 │
└────────┘
```

## 记忆系统

经验自动保存到 `memory/` 目录（沙箱限制）：

```
memory/
├── patterns/     # 可复用执行模式
├── lessons/     # 失败教训
├── successes/   # 成功案例
└── knowledge/   # 知识积累
```

## 自主能力等级

| 等级 | 能力 | 表现 |
|------|------|------|
| L1 | 基础执行 | 接收指令，执行任务 |
| L2 | 规划执行 | 理解需求，拆解任务，选择策略 |
| L3 | 自主监控 | 实时追踪，自动纠错，动态调整 |
| L4 | 反思学习 | 评估结果，提取经验，更新记忆 |
| L5 | 完全自主 | 闭环优化，TDD 驱动，持续进化 |

## 项目信息

- **GitHub**: https://github.com/World-peace001/cognitive-agent
- **npm**: https://www.npmjs.com/package/cognitive-agent
- **ClawHub**: https://clawhub.ai/skills/cognitive-loop
- **版本**: 1.0.0

## 安全声明

本 Skill 已通过基础安全审核，但用户/代理在使用前应：
1. 自行审核源代码
2. 使用沙箱环境测试
3. 限制持久化路径
4. 监控内存使用

## 许可

MIT License
