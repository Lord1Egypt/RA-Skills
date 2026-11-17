# 出处与致谢

本技能是独立实现，把下面这篇文章的思路改写成 agent 可执行的工作流。除标注的短引文外，文字均为我们自己的表述。

## 主要来源
- **Felix Rieseberg**，《How to be more ambitious: A tutorial for humans with models》，2026 年 10 月 13 日发布。
  https://felixrieseberg.com/how-to-be-more-ambitious-a-tutorial-for-humans-with-models/
  - 借用的思路包括：
    - 野心分为速度、高度、深度、广度四类；
    - QBR 三级阶梯；"让应用保持零崩溃"；
    - 用专家的工具而不是专家的说法；
    - 把不合理的目标当作合理来提（10 秒 → 200 毫秒）；
    - 用原始数据挑战既有假设，产出新知识并在没见过的数据上验证；
    - 用外部裁判代替自评；
    - 名词换动词（原文注明出自 Tom Kelley 与 Jonathan Littman 的《The Art of Innovation》）；
    - 组建包含对手的团队，但不搞角色扮演；
    - 自我效能的论证。
  - 第 3 步改编的"更深，而不是更大"四问提示词出自该文。
  - 使用的短引文："the goal beyond the goal"；"deeper version of this task, not a bigger one"；"Don't ask the model to write like a short seller, ask it to do what a short seller does"。
- 中文译文（量子位，微信公众号）：https://mp.weixin.qq.com/s/DSkimaN8KLtSRI0UFNFaPA

## 原文引用的研究（见 self-efficacy.md）
- Edwin Locke 与 Gary Latham 的目标设定理论：回顾约 35 年的研究，发现具体且困难的目标胜过"尽力而为"。
- Albert Bandura 的自我效能（原文点名的心理学概念）。
- Patrick Collison 的 "Fast" 清单（https://patrickcollison.com/fast）。
- W. Timothy Gallwey，《The Inner Game of Tennis》。
- 原文中的小故事：George Dantzig 把未解难题当作业做出来；Roger Bannister 与四分钟一英里。

## 本技能在原文之外补充的内容
原文是写给"给模型下指令的人"的。本技能让 agent 自己完成这部分工作并一路执行到底。补充了以下几点：
- 适用判断，决定什么时候*不*拔高；
- 明确的审批关卡；
- 必须先做的准备步骤（数据、环境、裁判、基线）；
- 坚持规则：不降目标、至少两种不同思路、如实报告；
- 逐条外部验证；
- 同时对照字面要求和野心目标的差距报告。

## 相关的已有作品（未抄录）
2026 年 10 月出现了许多基于同一篇文章的技能，例如 DannyMac180/skills 的 `be-ambitious`、wanderingspirit03/ambition-skill、robonuggets/be-ambitious、ClawHub 上的 `@abhione/ambition`。本技能没有抄录它们的任何文字。

## 与英文版的关系
本目录是 `ambition-loop`（英文版）的中文对应版，两者流程、关卡、步骤编号保持一致。修改任一版本时请同步另一版。
