# Dream Interpretation

## Overview
Use this skill to turn a free-form dream description into a concise, internet-grounded Zhougong-style dream interpretation. Prefer web evidence over guessing, and clearly separate common traditional interpretations from uncertainty.

## Workflow

1. Extract the key dream symbols, actions, people, places, objects, colors, and emotions from the user's description.
2. Search the web for Zhougong dream interpretations of the most important symbols and combinations.
3. Read 2–4 relevant sources and compare overlaps instead of trusting a single page.
4. Synthesize a short answer that explains:
   - the main symbols in the dream
   - the most common interpretation patterns
   - any conflicting or low-confidence points
5. If the dream is vague, ask 1–3 clarifying questions before interpreting.

## Search Strategy
Prefer Chinese search queries and keep them concrete.

Recommended query patterns:
- `Zhougong dream interpretation <core symbol>`
- `dream of <core symbol> Zhougong dream interpretation`
- `dream of <action> <object> interpretation`
- `Zhougong dream interpretation <symbol A> <symbol B>`

Examples:
- `周公解梦 掉牙`
- `梦见 蛇 周公解梦`
- `梦到 考试迟到 解梦`
- `周公解梦 飞行 追赶`

When the dream contains many details, prioritize the 1–3 strongest symbols instead of searching every minor element.

## Interpretation Rules

- Ground the answer in what multiple sources commonly say.
- Do not present folklore as fact; frame it as traditional interpretation.
- If sources disagree, say so directly.
- Do not invent citations or claim certainty you do not have.
- Keep the tone helpful and light; dream interpretation is suggestive, not diagnostic.
- By default for Chinese users, provide a dual-perspective answer: Zhougong interpretation + modern psychology.
- If the user explicitly wants only Zhougong-style interpretation or only psychological interpretation, follow that preference.

## Response Pattern
Default structure:

### Key Signals in the Dream
- List the top symbols or events.

### Common Traditional Interpretations
- Summarize the overlapping interpretations from the sources.

### Modern Psychology View
- Offer a grounded, non-mystical interpretation based on emotion, stress, recent experiences, unfinished concerns, relationships, or subconscious rehearsal.
- Keep this section clearly separate from folk explanations.

### A Balanced Takeaway
- Give a practical interpretation tied to the user's actual dream details.

### Reminder
- Mention that Zhougong dream interpretation is a traditional folk framework for reference only and should not replace real-world judgment.

## Clarification Triggers
Ask follow-up questions when any of these block a useful search:
- the main symbol is unclear
- multiple unrelated scenes are mixed together
- the dream depends on who a person is but their relationship is unknown
- the user only says “I had a strange dream” without details

Example clarifying questions:
- What was the strongest image in the dream?
- What stood out most: a person, an animal, or an action?
- Did you feel more nervous, afraid, happy, or calm in the dream?

## Output Quality Bar

- Be concise by default.
- Use plain Chinese unless the user asks for another language.
- Prefer natural trigger language in Chinese scenarios, such as: “help me interpret a dream,” “Zhougong dream meaning,” “what does dreaming of XX mean,” or “what does dream XX represent.”
- Do not over-expand into mysticism.
- Cite source URLs or source names when the user asks for evidence, or when confidence is low.

---

## 🚀 First-Success Path

**30秒快速上手：三步解读你的梦**

1. **描述你的梦** — 告诉我你梦到了什么，尽量包含关键符号、人物和情绪
2. **获取双重视角解读** — 我会给出周公解梦传统解释 + 现代心理学视角
3. **得到平衡建议** — 综合两个视角，给出贴近你实际生活的实用建议

> 示例："我昨晚梦见自己牙齿掉了，一碰就碎，很害怕。这是什么意思？"

---

## 📝 Sample Prompts

### 示例 1：梦见掉牙
**用户输入：**
```
梦见牙齿掉了，没有出血，但就是一颗一颗松动掉下来，感觉很害怕。这梦是什么意思？
```

**期望输出：**
```
### 梦境关键信号
- 牙齿松动/掉落
- 无出血
- 情绪：害怕、无助

### 🏮 周公解梦（传统解读）
- **掉牙**：传统象征"骨肉分离"，可能预示长辈健康需要关注，或担心与亲人关系疏远（常见的民间对应是担心父母身体）。
- **一碰就碎**：暗示对自身根基或防线（如健康、工作稳定）的不安感。
- **无出血**：传统认为无血比有血更偏"精神层面"的损耗，而非具体的身体伤害。

### 🧠 现代心理学视角
- **控制感缺失**：掉牙是梦境中最常见的焦虑符号之一，反映现实生活中感到"无力控制"或"失去了某些能力"。
- **外在形象焦虑**：牙齿也是门面，梦见掉牙可能和社交形象、表达能力的焦虑有关。
- **过渡期信号**：很多人在生活发生变化（换工作、进入新环境、年龄增长）时做掉牙梦。

### ⚖️ 平衡建议
这个梦更可能是对近期压力或变动（如工作变动、家庭关系、年龄焦虑）的情绪反应。建议：
1. 回顾最近是否有让你感觉"根基不稳"的事情
2. 如果确实担心长辈健康，不妨打个电话问候
3. 适当增加放松活动，每天留点时间给自己

✨ 周公解梦是传统文化参照，请勿过度担忧。
```

### 示例 2：梦见蛇
**用户输入：**
```
梦见一条大蛇在房间里，没有攻击我，就在那盘着，我特别害怕不敢动
```

**期望输出：**
```
### 梦境关键信号
- 蛇（大型、房间里）
- 蛇没有攻击
- 情绪：恐惧、动弹不得

### 🏮 周公解梦（传统解读）
- **梦见蛇**：经典包含多重象征——蛇是"小龙"，常预示财运或贵人运。但蛇也是隐忧的象征。
- **蛇盘踞不动**：传统说法认为，蛇不动代表"潜伏的机遇"或"隐藏的隐患正在形成，但尚未爆发"。
- **在自己房间**：与自身家庭、私密空间相关，预示家中可能有"潜藏的变化"。

### 🧠 现代心理学视角
- **蛇是潜意识的经典符号**：在荣格心理学中，蛇常象征被压抑的本能、恐惧或性心理。
- **不敢动的状态**：反映了你在现实中面对某些事情（可能是人际、工作或关系）时"不敢行动"的僵持状态。
- **盘踞的蛇**：代表某个你虽然看见但不敢处理的问题——你知道它在，但选择不动。

### ⚖️ 平衡建议
梦中的蛇不是预言，而是你内心状态的一面镜子：
1. 想一想最近有没有让你"僵住不敢动"的事情？
2. 蛇未攻击——说明你担心的那个问题可能并没有你想象的那么危险
3. 可以列一个"最近在回避什么"的清单，挑一个最轻的尝试面对
```

### 示例 3：梦见考试迟到
**用户输入：**
```
总是梦见考试迟到，找不到考场，或者卷子发下来全不会做。我明明毕业好多年了，这是怎么回事？
```

**期望输出：**
```
### 梦境关键信号
- 考试
- 迟到 / 找不到考场
- 卷子不会做
- 场景：已毕业仍梦见

### 🏮 周公解梦（传统解读）
- **梦见考试**：传统上不直接指考试本身，而是象征"被考验"或"过坎"。
- **找不到考场**：预示在现实中有方向不明确、目标模糊的感觉。
- **卷子不会做**：暗示任务或责任超出当前能力认知范围。

### 🧠 现代心理学视角
这是成年人最常见的"高压型梦境"之一：
- **迟到/找不到**：≈ 现实中担心错过机会、错失截止时间
- **不会做题**：≈ 感觉被要求完成自己没有准备或不胜任的任务
- **反复出现**：说明触发这个焦虑的场景在现实中反复出现（如定期的工作汇报、项目截止日）

### ⚖️ 平衡建议
这个梦的核心不是考试，而是**评估焦虑**：
1. 最近是否有定期"被评价"的场景？（述职、汇报、绩效考核）
2. 试着把焦虑转化为具体的准备动作——"复习"能有效降低这类梦的频率
3. 一些简单的睡前放松（如呼吸练习）也有帮助
```

### 示例 4：梦见飞行
**用户输入：**
```
梦见自己在城市上空飞，飞得很高很快，感觉很自由很开心，但是飞着飞着突然掉下来了
```

**期望输出：**
```
### 梦境关键信号
- 飞行（城市上空、很高很快）
- 情绪：自由、开心
- 转折：突然坠落

### 🏮 周公解梦（传统解读）
- **梦见飞行**：传统的吉利征兆——"飞黄腾达"、地位上升、大志得伸。
- **城市上空飞行**：与事业、社会地位关联，预示在工作或社会活动中将受瞩目。
- **坠落**：传统说法叫"梦高忽坠，防乐极生悲"，提醒成功后不可得意忘形。

### 🧠 现代心理学视角
- **飞行**：典型的"掌控感"和"成就感"象征。梦见飞说明近期自我感觉良好、能力得到了释放。
- **自由开心**：可能是现实中刚取得某个成就或突破。
- **突然坠落**：这是一个常见的转折意象——反映了潜意识中对"高峰后跌入低谷"的隐忧，或担心自己无法维持当前的良好状态。

### ⚖️ 平衡建议
这是一个"先扬后抑"的梦，从兴奋到不安的转变值得关注：
1. 享受飞行部分——你确实在进步，值得肯定
2. 坠落不是预言，而是提醒：给自己留一些"安全网"
3. 不要因为害怕坠落而不敢飞——保持自信，但适度规划风险
```

### 示例 5：梦见已故亲人
**用户输入：**
```
梦到我已经去世的奶奶，她在梦里和以前一样对我笑，给我做饭，我感觉特别温暖但醒来后很难过
```

**期望输出：**
```
### 梦境关键信号
- 已故亲人（奶奶）
- 日常场景（做饭、微笑）
- 情绪：温暖的 → 醒来后难过

### 🏮 周公解梦（传统解读）
- **梦见已故亲人**：传统说法多样——有些认为"亡人托梦"是有事相托；多数认为是你对亲人的思念在梦中延续。
- **奶奶做饭/微笑**：是非常正面的象征——传统认为故人在梦中以温馨日常出现，说明她在另一个世界安好，也是在安慰你。
- **温暖→难过**：恰恰说明亲情的深层联结仍在。

### 🧠 现代心理学视角
- **思念的延续**：这类梦几乎是"哀伤过程"的自然部分，表明你和奶奶的依恋关系很深。
- **温暖的梦**：说明你对这段关系没有未解的创伤，更多的是爱与怀念。
- **醒来的难过**：这是正常的——当你重新回到"她已经离开"的现实中，悲伤是健康的情绪反应。

### ⚖️ 平衡建议
1. 这种梦不是灵异事件，而是爱的延续。不用害怕。
2. 如果醒来难过，可以翻翻老照片、和家里人聊聊奶奶的故事
3. 也可以把梦记下来——这类梦其实是一份很珍贵的情绪礼物
4. 如果每次梦见后都陷入长时间悲伤，可以考虑找亲友聊聊，给自己多一些情感支持
```

---

## 📋 Real Task Examples

| 场景 | 用户输入示例 | 技能输出要点 |
|------|-------------|-------------|
| **常见梦境** | "梦见被追赶但跑不动，是什么意思？" | 提取"被追赶""跑不动"两个核心符号 → 周公解梦（压力/逃避责任） → 心理学（焦虑/无力感） → 建议面对问题 |
| **复杂叙事** | "梦见在一个古堡里，有个戴面具的人给我一把钥匙，然后我打开了一扇门看到很多镜子" | 分解多个符号（古堡、面具人、钥匙、门、镜子） → 按强→弱排列 → 组合解读 → 心理学视角的探索/自我认知主题 |
| **重复梦境** | "连续三天梦见同一个人，每次场景不同，但那个人都一样" | 关注重复出现的核心元素（人物） → 思考该人物在现实中的意义 → 周公解梦（缘分/心结） → 心理学（未完成的事务） |
| **情感安慰** | "做了个噩梦，很害怕，想知道是不是不好的预兆" | 先安抚情绪 → 确认不是预言 → 用"噩梦解压"视角解释 → 给缓解焦虑的实用建议 |
| **文化解读** | "梦到发洪水但自己站在高处，老家说法说发水梦是发财" | 尊重民间文化解读 → 叠加搜索验证 → 心理学视角（洪水=情感冲击、站高处=安全感） → 平衡不迷信也不否定的态度 |