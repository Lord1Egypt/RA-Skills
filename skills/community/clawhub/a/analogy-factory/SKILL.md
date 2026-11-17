---
name: analogy-factory
display_name: 类比工厂
display_name_zh: 类比工厂
display_name_en: Analogy Factory
description: This skill should be used when the user wants not one analogy but several from completely different angles — including phrases like "多给几个比方", "用不同角度类比", "换个比喻", "还有什么好比喻", "analogies", "explain with different metaphors". It produces five analogies drawn from five non-overlapping domains.
description_en: This skill should be used when the user wants not one analogy but several from completely different angles — including phrases like "give me more analogies", "different ways to think about it", "another metaphor", "more examples like that", "explain it from several angles". It produces five analogies drawn from five non-overlapping domains.
description_zh: 当用户想要的不是一个比方，而是多个不同角度的比方时使用，包括「多给几个比方」「用不同角度类比」「换个比喻」「还有什么好比喻」等表达。本技能为同一个概念给出 5 个来自完全不同领域的类比。
version: "1.0.0"
category: 知识与学习
agent_created: true
---

# 类比工厂

一个概念，**5 个来自完全不同领域的类比**。

## 何时使用

- 「多给几个比方 / 换个比喻 / 还有什么类比」
- 用户觉得单一个类比不够，想从多角度理解
- 用户想给一个复杂概念找更好的解释角度

## 不适用场景

- 用户还没理解概念本身 → 先转 `plain-explanation`（那里给 1 个最贴切的）
- 用户问的是概念是否成立 → 转 `counterexample-teacher`

## 核心方法

### 一个原则

**跨领域，才叫类比工厂。**

5 个类比必须来自 **5 个互不重叠的领域**，禁止全用同一领域。

推荐领域池（每次挑 5 个不同的）：
做饭 / 运动 / 交通 / 游戏 / 自然 / 家庭 / 看病 / 装修 / 赶集 / 养宠物 / 上课 / 存钱

### 每个类比必须

1. **一句话讲完**（≤ 40 字）
2. **覆盖概念的一个侧面**，5 个合起来接近完整
3. **标注这侧面对应概念里的什么**

### 结尾必须做两件事

- 指出**哪个类比最贴切**，为什么
- 指出**哪个类比会误导人**（类比的边界在哪里断掉）

## 输出模板

```
【概念】xxx

1. 做饭视角：[类比]  → 对应：xxx
2. 交通视角：[类比]  → 对应：xxx
3. 游戏视角：[类比]  → 对应：xxx
4. 自然视角：[类比]  → 对应：xxx
5. 家庭视角：[类比]  → 对应：xxx

【最贴切的】第 X 个，因为……
【容易误导的】第 Y 个，因为……（类比在哪里断掉）
```

## Few-shot 范例

### 例 1：给「神经网络」造 5 个类比

```
1. 做饭视角：像一口大锅，几百种调料按比例倒进去，最后炒出一盘菜 → 对应：多层加权求和
2. 交通视角：像一个城市的路网，每个路口决定要不要放行 → 对应：激活函数
3. 游戏视角：像打怪升级，每打错一次就调一次属性值 → 对应：反向传播
4. 自然视角：像大脑里的神经元互相打电话 → 对应：连接的权重
5. 家庭视角：像一大家子投票决定晚饭吃什么，每人一票但分量不同 → 对应：权重差异

【最贴切的】第 4 个，因为神经网络本来就是模仿神经元设计的
【容易误导的】第 5 个，因为神经网络的「投票」不是商量出来的，是训练出来的
```

## 兜底话术

- 如果概念太抽象，某个领域实在编不出 → 老实标注「这个角度我造不出来」，换一个领域，不硬编。
- 如果用户只要 1 个类比 → 提醒一句「单个的话我推荐第 X 个」，然后只给那个。
- 如果用户给的概念本身是个类比（「帮我解释一下什么叫心流」）→ 说明「这个概念本身已经是比喻了」，然后给 5 个不同领域的落地场景。
