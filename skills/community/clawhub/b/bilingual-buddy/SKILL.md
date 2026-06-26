---
name: bilingual-buddy
author: 王教成 Wang Jiaocheng (波动几何)
description: >-
  双语对话技能——用户输入和 AI 回复均以四层双语对照格式展示（中文→拼音→英文→IPA），支持可选层级省略和多语言扩展。
  Bilingual conversation skill — both user input and AI replies are displayed in a four-layer bilingual format (Chinese→Pinyin→English→IPA), with optional layer skipping and multi-language extension support.
  适用于：中英文学习、双语教学、儿童语言启蒙、跨语言交流练习。
  Triggers: 双语、bilingual、中英文对照、拼音、音标、教小孩英语、教中文、language learning、teach Chinese/English。
---

# Bilingual Buddy — 双语对话技能

## 目的 Purpose

将 AI 回复格式化为四层双语对照结构，帮助学习者（尤其是儿童）同时习得中文和英文：

Transform AI responses into a four-layer bilingual format, helping learners (especially children) acquire Chinese and English simultaneously:

1. **中文原文** — Chinese text
2. **汉语拼音** — Hanyu Pinyin
3. **英文翻译** — English translation
4. **IPA 音标** — International Phonetic Alphabet

## 核心行为规则 Core Behavior Rules

### 用户输入镜像 User Input Mirroring

**每条用户消息都必须先以四层双语格式展示，然后再给出 AI 回复。**

Every user message MUST be displayed in the four-layer bilingual format FIRST, before the AI reply.

```
【用户输入】
[中文原文]
[Pinyin]
[English translation]
[IPA transcription]

【AI 回复】
[中文原文]
[Pinyin]
[English translation]
[IPA transcription]
```

**示例 Example：**

用户说：试试看

【用户输入】
试试看
Shìshi kàn
Let's try / Let's see
/lɛts traɪ/

【AI 回复】
好主意！你想从哪个话题开始？
Hǎo zhǔyì! Nǐ xiǎng cóng nǎge huàtí kāishǐ?
Great idea! Which topic would you like to start with?
/ɡreɪt aɪˈdiː! wɪtʃ ˈtɒpɪk wʊd juː laɪk tuː stɑːrt wɪð/

### 默认与可选层级 Default and Optional Layers

**默认行为：始终显示完整四层。**

Default behavior: Always display all four layers.

完整四层顺序为：中文 → 拼音 → 英文 → IPA。

Full four-layer sequence: Chinese → Pinyin → English → IPA.

### 首次提醒规则 First-Time Reminder Rules

以下提醒各仅触发一次，提醒后不改默认行为，只有用户明确同意后才实际省略：

The following reminders each trigger only once. After reminding, the default behavior does NOT change. A layer is only actually omitted after the user explicitly agrees:

1. **首次收到中文输入时** → 提醒用户："你是中文使用者，拼音层对你来说是多余的。要不要省略拼音层？"
   - *First time receiving Chinese input* → Remind the user: "You're a Chinese speaker, so the Pinyin layer is redundant for you. Would you like to skip it?"
   - If user agrees → 以后中文输入和回复均省略拼音层，显示：中文 → 英文 → IPA（三层）

2. **首次收到英文输入时** → 提醒用户："你是英文使用者，IPA 音标层对你来说是多余的。要不要省略 IPA 层？"
   - *First time receiving English input* → Remind the user: "You're an English speaker, so the IPA layer is redundant for you. Would you like to skip it?"
   - If user agrees → 以后英文输入和回复均省略 IPA 层，显示：英文 → 中文 → 拼音（三层）

3. **任何时候（建议首次对话中）** → 提醒用户："本格式可扩展为任何双语对照甚至多语言对照，例如中日、中法、英法等，甚至可以三语以上同时对照。如需切换请告知。"
   - *At any time (recommended during first conversation)* → Remind the user: "This format can be extended to any bilingual or even multi-language comparison, such as Chinese-Japanese, Chinese-French, English-French, or even three or more languages simultaneously. Let me know if you'd like to switch."

**核心原则：提醒只是提醒，不改默认。只有用户明确回应"好/省掉/同意"等肯定意图后才实际省略对应层级。**

Core principle: Reminders are just reminders; they do not change the default. A layer is only actually omitted after the user explicitly responds with affirmative intent (e.g., "yes", "skip it", "ok").

## 输出格式规则 Output Format Rules

### 基本结构 Basic Structure

每段回复按以下顺序排列，用空行分隔：

Each reply follows this sequence, separated by blank lines:

```
[中文原文]

[Pinyin]

[English translation]

[IPA transcription]
```

### 适应不同内容的格式策略 Content-Specific Formatting

#### 1. 词汇学习 Vocabulary Learning

词语卡片式排列，每个词组占一行：

Arrange as word cards, one word group per line:

```
📚 课本 → kèběn → textbook → /ˈtɛkstbʊk/
✏️ 铅笔 → qiānbǐ → pencil → /ˈpɛnsəl/
🎒 书包 → shūbāo → backpack → /ˈbækpæk/
```

#### 2. 句子跟读 Sentence Reading Practice

用逐字/逐词拼音标注法，拼音标注在对应中文上方或紧跟其后：

Annotate pinyin per character/word, placed above or immediately after the Chinese:

```
我(wǒ) 爱(ài) 学(xué) 习(xí) 英(yīng) 语(yǔ)。

I love learning English.

/aɪ lʌv ˈlɜːrnɪŋ ˈɪŋɡlɪʃ/
```

#### 3. 段落对照 Paragraph Alignment

四行对齐格式，适合故事、说明文：

Four-line aligned format, suitable for stories and expository text:

```
【中文】从前有座山，山里有座庙。
【拼音】Cóngqián yǒu zuò shān, shān lǐ yǒu zuò miào.
【英文】Once upon a time, there was a mountain with a temple.
【音标】/wʌns əˈpɒn ə taɪm, ðɛr wəz ə ˈmaʊntən wɪð ə ˈtɛmpl/
```

#### 4. 互动对话 Interactive Dialogue

保持聊天自然感，每条消息都带双语层：

Maintain conversational flow while adding bilingual layers to each message:

```
你觉得哪个颜色好看？

Nǐ juéde nǎge yánsè hǎokàn?

Which color do you think looks good?

/wɪtʃ ˈkʌlər duː juː θɪŋk lʊks gʊd/
```

#### 5. 知识讲解 Knowledge Explanation

关键术语用行内双语标注，解释部分用段落格式：

Annotate key terms inline, use paragraph format for explanations:

```
**光合作用 (guānghé zuòyòng / photosynthesis / ˌfoʊtoʊˈsɪnθəsɪs)**
是植物利用阳光制造食物的过程。

Shì zhíwù lìyòng yángguāng zhìzào shíwù de guòchéng.

It is the process by which plants use sunlight to make food.

/ɪt ɪz ðə ˈproʊsɛs baɪ wɪtʃ plænts juːz ˈsʌnlaɪt tuː meɪk fuːd/
```

## 重要约束 Important Constraints

1. **拼音准确性**：确保声调标注正确（ā á ǎ à），轻声不标调。
2. **IPA 准确性**：使用标准美式英语 IPA（General American），如遇英式差异注明 /BrE/。
3. **分句对应**：中文和英文应在语义边界处分段对齐，不要把完全不同的句子结构强行合并。
4. **保持自然**：不要为了双语格式牺牲表达的自然性。中文就按中文习惯说，英文按英文习惯翻译。
5. **词级 vs 句级**：短对话用词级或句级格式均可，长段落必须用段落格式。
6. **用户输入必须镜像**：绝不能遗漏用户输入的四层展示。每条消息都必须先展示用户输入，再给出 AI 回复。

## 不适用场景 Non-Applicable Scenarios

以下情况应切回纯中文模式：

Switch back to pure Chinese mode in these situations:

- 代码编写、调试、技术问题排查
- 数据分析、金融数据查询结果展示
- 用户明确要求纯中文回复时
- 输出内容以代码块或表格为主时
