# Memento-Skills 框架

> 来源：Huichi Zhou 等人，2026年3月19日，arXiv
> 学习日期：2026-03-26

## 核心概念

Memento-Skills 是一个"agent-designing agent"——一个能自主设计、适配和改进其他 task-specific agent 的通用系统。

**核心理念**：让 generalist agent 通过经验自主构建专业化 agent，所有适应都通过外部化的 skill/prompt 进化完成，不修改 LLM 参数。

## 架构：Read-Write Reflective Learning

### Read Phase（读阶段）
- **Skill Router**（行为可训练）根据当前 stateful prompt 选择最相关的 skill
- Skill Router 本身也是可训练的——它的路由能力随经验改善

### Write Phase（写阶段）
- Agent 基于新经验**更新和扩展** skill library
- 新 skill 可以被创建，已有 skill 可以被精炼

### 闭环
```
任务 → Read(选择 skill) → 执行 → 反馈 → Write(更新/创建 skill) → 下一任务
```

## Stateful Prompts

- 可复用 skill 存储为**结构化 markdown 文件**
- 编码**行为 + 上下文**（不仅仅是指令，还包含执行所需的背景信息）
- 作为**持久化、可进化的 memory**
- 支持**跨交互的知识传递**

## 关键成果

| 基准测试 | 改进 |
|---------|------|
| GAIA (General AI Assistants) | +13.7 个百分点（相对提升 26.2%） |
| HLE (Humanity's Last Exam) | 基线性能翻倍（相对提升 116.2%） |

## 与我们（evo-skill-creator）的对比分析

### 相似点
1. 都用 **markdown 文件** 存储 skill
2. 都是 **不修改 LLM 参数** 的外部化进化
3. 都有 **agent 创建 agent** 的递归设计
4. 都强调 **通过经验持续改进**

### Memento-Skills 有而我们没有的
1. **Skill Router**（行为可训练的路由器）—— 我们目前靠 skill 的 description 触发，没有独立的路由层
2. **自动化质量反馈循环** —— Memento-Skills 有明确的"执行→反馈→更新"循环，我们的 review 命令目前是手动触发
3. **基准测试驱动的进化** —— 它们用 GAIA/HLE 等标准基准量化改进，我们缺少量化指标

### 我们有而 Memento-Skills 没有的
1. **老板参与的 suggest 机制** —— 人在回路中，不完全自主
2. **明确的命令体系** —— plan/learn/scan/review/go/suggest/status，更结构化
3. **双计划体系** —— 学习计划 + 待办任务分离
4. **角色化设计** —— 每个智能体有明确的角色身份和目标

### 可借鉴的改进方向
1. **引入类 Skill Router 的路由机制** → 当 skill 越来越多时，精准路由比依赖 description 更可靠
2. **建立自动化反馈循环** → go 命令执行后自动评估效果，不依赖老板手动 review
3. **定义量化指标** → 为每个智能体定义"做得好不好"的可衡量标准
