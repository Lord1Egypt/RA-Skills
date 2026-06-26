<!--
文件：clawhub-copy.zh-CN.md
核心功能：作为 Fashion skill 的中文长版发布页文案，供 ClawHub / OpenClaw 或同类技能市场直接复用。
输入：Fashion 分支的 AKM 定位、方法结构与使用边界。
输出：可直接上线的中文技能页文案。
-->

# AKM Fashion ClawHub Skill Page

## Skill Title

**AKM Fashion：场景感知衣橱策略师**

## One-line Description

先把用户的体型、场景、衣橱和约束模型建出来，再做真正合适的穿搭和采购决策。

## What It Is

多数穿搭智能体答得太早。

它们并不知道用户有什么衣服、哪些场景重要、体型问题是什么、功能限制在哪里。
这就是泛化穿搭建议的起点。

AKM Fashion 的修正方式，是先建立可用的穿搭画像：

- 体型语境
- 核心场景
- 风格偏好
- 衣橱资产
- 功能性约束
- 反模式

只有在这些信息清楚之后，它才输出穿搭与衣橱决策。

## What Makes It Different

这不是一个“造型师人格 prompt”。
它是一套三段式方法：

1. elicitation
2. structured record
3. execution decision

输出也不是 moodboard。
它输出的是考虑衣橱和场景约束的判断。

## Best Fit

适合这些情况：

- 用户需要场景化穿搭决策
- 现有衣橱会实质限制解空间
- 舒适性与功能性和审美一样重要
- 用户想要采购优先级，而不是空泛审美话术

## Boundary

- 不是图像识别工具
- 不是真人试衣产品
- 不会把未知衣橱资产假装成已知
- 不会用模糊风格标签代替场景判断

## Closing Line

**没有衣橱模型，就没有严肃穿搭建议。**
