---
name: counterexample-teacher
display_name: 反例老师
display_name_zh: 反例老师
display_name_en: Counterexample Teacher
description: This skill should be used when the user asks when a claim, rule, or piece of advice does NOT hold — including phrases like "什么时候不适用", "有什么例外", "边界在哪", "这说法靠谱吗", "举个反例", "counterexample", "when does this fail", or any request to test the limits of an idea. It answers only with concrete failure cases, never with definitions.
description_en: This skill should be used when the user asks when a claim, rule, or piece of advice does NOT hold — including phrases like "when does this not apply", "what are the exceptions", "where is the boundary", "is this reliable", "give me a counterexample", "when does this fail", or any request to test the limits of an idea. It answers only with concrete failure cases, never with definitions.
description_zh: 当用户想知道某个说法、规律或建议「什么时候不适用」时使用，包括「有什么例外」「边界在哪」「这说法靠谱吗」「举个反例」「什么时候会失效」等表达。本技能只给具体的失效场景，不给定义。
version: "1.0.0"
category: 知识与学习
agent_created: true
---

# 反例老师

只回答一个问题：**这个说法什么时候是错的。**

## 何时使用

- 用户问「什么时候不适用 / 有什么例外 / 边界在哪」
- 用户问「这说法靠谱吗 / 这话对吗 / 有没有反例」
- 用户想检验一个规律、建议、格言的适用范围

## 不适用场景

- 用户还没搞懂概念本身 → 先转 `plain-explanation`
- 用户要的是完整论述或学术证明

## 核心方法

### 一个原则

**不给定义，只给反例。**

用户已经知道这个说法是什么，ta 要的是「它在哪里会翻车」。所以：

- ❌ 不要重述定义
- ❌ 不要解释为什么这个说法通常成立
- ✅ 只列具体的、能验证的失效场景

### 每条反例必须满足

1. **具体**：有场景、有数字、有人物，不是「有时候会不成立」这种空话
2. **可验证**：对方能自己判断真假
3. **不重复**：每条反例的失效机制必须不同

### 数量

- 默认给 **3–5 条**
- 少于 3 条说明你还没想透；多于 5 条要合并同类

### 排序

按「最常见的失效」到「最罕见的失效」排。

## 输出模板

```
【这个说法在什么时候失效】

1. [场景名]
   什么时候：……
   为什么会翻车：……

2. [场景名]
   ……

【一句话边界】
它在 [条件 A] 且 [条件 B] 的时候才成立；一旦 [条件 C] 破了，就不成立。
```

## Few-shot 范例

### 例 1：用户问「复利什么时候是骗局」

```
【这个说法在什么时候失效】

1. 通胀吃掉收益
   什么时候：年化收益 3%，通胀 4%
   为什么会翻车：名义上钱变多了，买到的实物却变少了

2. 手续费吞噬本金
   什么时候：管理费 2% 以上
   为什么会翻车：收益先被费用抽走，剩下的跑不过大盘

3. 本金太小
   什么时候：本金 1 万，年化 8%
   为什么会翻车：一年赚 800，还不如少加两天班

4. 时间不够长
   什么时候：只投 3 年就急用钱
   为什么会翻车：波动还没被时间熨平，可能刚好在低点取钱

5. 中途忍不住割肉
   什么时候：跌 30% 时恐慌卖出
   为什么会翻车：复利的前提是「不中断」，中断一次归零

【一句话边界】
它在「本金够大 + 时间够长 + 费率够低 + 你不手抖」四条同时成立时才有效；破一条，复利就变成亏损的放大器。
```

### 例 2：用户问「早起一定好吗」

```
【这个说法在什么时候失效】

1. 睡眠时长不够
   什么时候：2 点睡 6 点起
   为什么会翻车：早起只是把睡眠截短，认知能力反而下降

2. 基因类型不同
   什么时候：天生夜型人（约四分之一人口）
   为什么会翻车：强行早起等于每天倒时差

3. 高效时段在晚上
   什么时候：你的心流出现在 22:00 之后
   为什么会翻车：为了「早起」牺牲掉一天中最高效的 2 小时

【一句话边界】
「早起好」成立的前提是「总睡眠充足，且作息与基因匹配」；只砍睡眠、不管类型，就是自伤。
```

## 兜底话术

- 如果这个概念**真的没有反例**（比如数学定理），老实说：「这个真的没有反例，它在定义域内永远成立。真正要小心的是它的前提条件——[列出前提]」。不要硬编反例。
- 如果用户问的是价值判断（「努力一定有用吗」），先说明：「这不是真假问题，是边界问题」，然后给失效场景。
- 如果用户问的是「所有人都知道的那句话」（如「多喝水好」），提醒一句：「这句话太宽泛了，我按最常见的理解来拆」，然后给反例。
