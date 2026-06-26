# Skill Domain Landscape - 统一 Spec

## 基本信息

- 名称：`skill-domain-landscape`
- 目标：让 `skill-factory` 获得稳定的任务域地图和执行面判断框架
- 当前阶段：研究与设计输入，不进入脚本实现

## 必须满足的要求

### 要求 1

后续研究新方向时，需要先识别主任务域和次任务域。

### 要求 2

每个任务域都要至少给出：

- 高频任务集合
- 代表性 Skill
- 推荐 CLI
- 推荐 API 或 MCP
- 主要风险边界

### 要求 3

研究时优先使用官方文档和官方示例仓库，再补充社区扩展。

### 要求 4

输出结论时，需要明确该任务更适合：

- Skill-only
- Skill + CLI
- Skill + API/MCP
- Skill + CLI + API/MCP

### 要求 5

至少为第一层优先任务域保留正式研究产物。

## 输入

- OpenAI、Anthropic、Gemini 的官方 Skill 或扩展资料
- 官方 Skill 仓库
- 社区扩展目录
- Agent Skills 开放标准资料

## 输出

- 一份任务域研究摘要
- 一份代表性 Skill 与执行面分析
- 一份设计摘要
- 一份统一 spec
- 一份后续构建计划

## 成功标准

- 当前仓库已经形成任务域地图的正式产物
- 任务域优先级已经清楚
- 高频任务和执行面分层已经清楚
- 后续可以直接基于这份结果继续扩展主 Skill
