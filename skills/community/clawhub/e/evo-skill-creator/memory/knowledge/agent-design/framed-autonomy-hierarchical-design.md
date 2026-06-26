# Framed Autonomy 与层级化 Agent 设计

## 概述
Agentic Business Process Management 提出"受限自治"（Framed Autonomy）——agent 在明确的流程框架内自主操作，要求可解释性和基于经验的自我修正。Manager-Expert 层级设计中，Expert 不仅报告成功/失败，还报告失败原因和新发现的约束，实现动态计划优化。

## 关键概念

### 受限自治（Framed Autonomy）
- Agent 在明确的流程框架内自主操作
- 必须具备可解释性
- 能够基于经验进行自我修正

### Manager-Expert 层级设计
- **Manager Agent**：负责任务分解、计划制定、资源调度
- **Expert Agent**：负责具体任务执行、技术实现
- **双向通信**：
  - Manager → Expert：任务分配、约束说明
  - Expert → Manager：执行结果、失败原因、新发现的约束

## 与我们系统的关联

### 创建者-子智能体关系
在 evo-skill-creator 系统中：
- **创建者 (Creator Agent)** 类似于 Manager Agent
- **子智能体 (Child Agent)** 类似于 Expert Agent

这种关系已经具备层级结构的基本特征：
1. 创建者负责定义子智能体的角色、目标和工作流程
2. 子智能体在其定义的范围内自主执行任务
3. 子智能体可以向创建者报告状态和问题

### 在 suggest 命令中的体现
"受限自治" 如何体现在 suggest 命令的设计中：
1. 当老板提出建议时，evo-skill-creator 首先表达自己的观点（保持自治）
2. 然后解读老板建议，进行对比验证（不盲从，有自己的立场）
3. 充分思考后给出结论，更新到知识库或学习计划（基于经验的修正）

## 改进建议

为了更好地实现"受限自治"和层级化设计，可以考虑：

1. **明确的框架约束**：
   - 为子智能体定义明确的边界和约束条件
   - 在 SKILL.md 中明确声明数据目录和权限范围

2. **增强的反馈机制**：
   - 子智能体在完成任务时，不仅报告成功/失败，还应提供：
     - 遇到的具体问题
     - 解决过程中发现的新约束
     - 对流程改进的建议

3. **动态计划优化**：
   - 基于子智能体的反馈，创建者可以调整学习计划和工作流程
   - 定期审查和更新子智能体的角色定义和目标

4. **可解释性要求**：
   - 子智能体的决策过程应该是可解释的
   - 重要决策应记录 rationale（理由）以便审计和学习

## 参考资料
- Hierarchical AI Agent Architecture: How Parent Agents Are Redefining AI Collaboration (Medium article, 2026-03-02)
- Autonoma: A Hierarchical Multi-Agent Framework for End-to-End Workflow Automation (arXiv:2603.19270, 2026-03-22)
- DEPART: A hierarchical multi-agent system for multi-turn interaction (Amazon Science)