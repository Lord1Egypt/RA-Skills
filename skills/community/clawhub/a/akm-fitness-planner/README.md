<!--
文件：README.md
核心功能：作为 Fitness skill 的英文入口页，说明用途、方法分层、双语文件、公开样本与输出方向。
输入：Fitness 分支的挖掘逻辑、记录模板、执行提示词、公开样本与 skill 设计。
输出：供 GitHub 或技能页直接引用的英文 README。
-->

# Fitness Skill

<p align="center">
  <a href="./README.md">English</a> | <a href="./README.zh-CN.md">简体中文</a>
</p>

## Purpose

The Fitness skill is the operational entry point for AKM in training decision workflows.
It is organized as a three-stage method rather than a single prompt.

## Method Layers

1. elicitation
2. structured record
3. execution decision

## Bilingual Files

- [SKILL.md](./SKILL.md)
- [SKILL.zh-CN.md](./SKILL.zh-CN.md)
- [ELICITATION_PROMPT.md](./ELICITATION_PROMPT.md)
- [ELICITATION_PROMPT.zh-CN.md](./ELICITATION_PROMPT.zh-CN.md)
- [RECORD_TEMPLATE.md](./RECORD_TEMPLATE.md)
- [RECORD_TEMPLATE.zh-CN.md](./RECORD_TEMPLATE.zh-CN.md)
- [EXECUTION_PROMPT.md](./EXECUTION_PROMPT.md)
- [EXECUTION_PROMPT.zh-CN.md](./EXECUTION_PROMPT.zh-CN.md)
- [INPUT_TEMPLATE.md](./INPUT_TEMPLATE.md)
- [INPUT_TEMPLATE.zh-CN.md](./INPUT_TEMPLATE.zh-CN.md)
- [SAMPLE_RECORD.md](./SAMPLE_RECORD.md)
- [SAMPLE_RECORD.zh-CN.md](./SAMPLE_RECORD.zh-CN.md)

## Output Direction

The core output is not generic workout language.
The core output is a constraint-aware training decision.

## Public Sample

- [Sample Record](./SAMPLE_RECORD.md)
- [中文样本](./SAMPLE_RECORD.zh-CN.md)

## Install

```bash
npx skills add https://github.com/sirsws/akm --skill akm-fitness-planner --full-depth
```
