---
name: "akm-fashion-strategist"
description: "AKM 在衣橱与穿搭决策工作流中的实现，在输出穿搭决定前先建模体型语境、场景、衣橱资产与功能限制。"
---

<!--
文件：SKILL.zh-CN.md
核心功能：作为 AKM Fashion skill 的中文正式说明页，定义其定位、输入要求、工作流、输出契约、双语规则与边界。
输入：Fashion 分支方法结构、提示词文件、记录模板与公开 skill 设计。
输出：供 GitHub 中文页、技能市场或代理工具直接引用的中文 skill 文档。
-->

# AKM Fashion Skill

<p align="center">
  <a href="./SKILL.md">English</a> | <a href="./SKILL.zh-CN.md">简体中文</a>
</p>

**没有衣橱模型，就没有严肃穿搭决策。**

AKM Fashion 是一个面向真实场景与资产约束的衣橱 / 穿搭决策 skill 包。
它处理的是体型语境、现有衣橱、场景要求和功能限制都会实质影响穿搭选择的场景。

## 定位

AKM Fashion 不是情绪板生成器。
它把穿搭重写成“画像优先的决策流程”。

## 必需输入

- `body shape or posture notes`
- `primary scenes`
- `style preferences`
- `wardrobe assets already owned`
- `functional constraints`

缺关键输入时，skill 必须显式输出 `MissingInputs`，而不是假装衣橱已经已知。

## 工作流

1. `ELICITATION_PROMPT.md`
2. `RECORD_TEMPLATE.md`
3. `EXECUTION_PROMPT.md`

## 输出契约

输出应包含：

- `SceneJudgment`
- `OutfitRecommendation`
- `WhyThisWorks`
- `GapAnalysis`
- `PurchasePriority`
- `MissingInputs`

## 双语规则

公开落地页采用英文主页 + 中文切换。
字段 key 保持英文，以保证输出稳定。
实际提示词提供英文版和中文版。

## 边界

- 不是图像识别工具
- 不是真人试衣产品
- 不是泛审美生成器
- 不能用漂亮措辞掩盖缺失上下文
