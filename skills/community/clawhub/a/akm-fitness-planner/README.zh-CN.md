<!--
文件：README.zh-CN.md
核心功能：作为 Fitness skill 的中文入口页，说明用途、方法分层、双语文件、公开样本与输出方向。
输入：Fitness 分支的挖掘逻辑、记录模板、执行提示词、公开样本与 skill 设计。
输出：供 GitHub 中文页或技能页直接引用的中文 README。
-->

# Fitness Skill

<p align="center">
  <a href="./README.md">English</a> | <a href="./README.zh-CN.md">简体中文</a>
</p>

## 作用

Fitness skill 是 AKM 在训练决策工作流里的操作入口。
它不是单 prompt，而是一套三段式方法。

## 方法分层

1. elicitation
2. structured record
3. execution decision

## 双语文件

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

## 输出方向

核心输出不是泛泛的训练语言。
核心输出是一个考虑约束的训练决策。

## 公开样本

- [Sample Record](./SAMPLE_RECORD.md)
- [中文样本](./SAMPLE_RECORD.zh-CN.md)

## Install

```bash
npx skills add https://github.com/sirsws/akm --skill akm-fitness-planner --full-depth
```
