---
name: concept-design-cn
description: "仅在显式调用时使用。用 Daniel Jackson 的概念与同步方法设计、实现、审查和重构软件，编写规格并解释软件行为。检查 CONCEPT.md/SYNCS.md 结构，生成 Mermaid 关系图。"
metadata:
  language: zh-CN
  translation_of: concept-design
  version: "2.5.4"
---

# 概念设计

Daniel Jackson 概念设计的方法概括：**应用 = 概念（Concepts）+ 同步规则（Synchronizations）**。

> “With the concepts in hand, we now associate their actions through synchronizations:”
> — Daniel Jackson, [Concept composition and sync](https://essenceofsoftware.com/tutorials/concept-basics/sync/#composing-concepts-with-syncs) (2022-09-14)

从用户需要出发。概念定义独立行为；外部同步规则组合这些行为，规定哪些动作完成后，在什么条件下触发后续动作。

## 核心约束

- 概念围绕一个目的拥有状态与动作；概念之间不互调、不互读状态，外部身份不携带另一概念的内部结构。
- 运作原理（OP）以代表性过程说明目的如何达成，不代替完整契约或进展保证。
- 组合可限制行为，但须保持各概念契约。分别检查契约、OP、目的与应用场景。
- 每项定义只有一处权威来源。区分已确认、建议、推断和未决；以证据、前提和反例检验决定，保留未决与未验证事项。
- 比较备选，包含不改或删减；反复失败时重查前提。重构保持行为，有意改变须明确说明。

涉及工程设计、实现、审查或项目规则时，按[工程架构](references/architecture.md)固定目录、命名、职责与依赖。

## 选择模式

按请求选择模式，只读取该模式及当前步骤所需参考材料。模式文件直接列出所需的全部参考；参考之间的链接仅为另见。意图不清时先只读检查，跨模式沿用已有授权。

| 模式 | 用途 |
| --- | --- |
| [design](references/modes/design.md) | 设计概念与同步 |
| [settle](references/modes/settle.md) | 整理讨论与决定 |
| [prd](references/modes/prd.md) | 编写 PRD、规格与验收 |
| [build](references/modes/build.md) | 按确认规格实现或重构 |
| [review](references/modes/review.md) | 审查设计与实现 |
| [guard](references/modes/guard.md) | 审计、回填、漂移检查、管道规格与关系图 |
| [refine](references/modes/refine.md) | 比较改进方案并按授权修正 |
| [explain](references/modes/explain.md) | 依据规格与源码解释行为 |

审查、审计、漂移及仅规划请求保持只读；其他修改限于授权范围。不得改规格掩盖实现缺陷。

## 表达与验证

默认使用[阅读版](references/spec-reading.md)，需要精确表达时展开[规格记法](references/spec-notation.md)。
运行检查器或生成关系图时读取[工具编码](references/tool-encoding.md)，未支持的内容报告未检查。
图使用 Markdown Mermaid；语法通过不代表目的达成、契约符合或运行正确。

## 参考资料

- 概念与同步：Daniel Jackson，Beyond Objects。
- 工程执行：Meng 与 Jackson，WYSIWID。
