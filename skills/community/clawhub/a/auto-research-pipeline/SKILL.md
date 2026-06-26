---
name: auto-research-pipeline
description: 从 AutoResearch 到完整项目的全自动流水线（实验 → 多 Agent 编排 → 技能封装）
---

# AutoResearch → Agency Agents → Skill Creator 流水线

此技能会在一次调用中完成以下四个阶段：

1. **AutoResearch Setup** – 使用 `/autoresearch setup` 初始化实验配置（目标、指标、可改动文件、运行命令等）。
2. **AutoResearch Run** – 执行 `/autoresearch run`，循环实验并记录 `results.tsv`。
3. **AutoResearch Analyze** – 通过 `/autoresearch analyze` 生成实验报告并挑选最佳改动。
4. **Agency Agents 编排** – 调用 `/openclaw skill use agency-agents --agent orchestrator "依据分析完成项目"`，让编排器依据最佳改动自动调度多个专业 Agent 完成完整项目交付。

**使用方式**
```
/openclaw skill use auto-research-pipeline
```
上述命令将在后台自动完成实验、协作与封装，省去手动敲多条指令的过程。