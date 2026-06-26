# Lesson Templates Reference

Detailed output templates for each lesson type. The agent should read this file when generating a specific lesson type for the first time, then internalize the pattern.

## 📖 Reading Lesson Template

```
📖 今日阅读 | Daily Read — [Topic Tag]

━━━ 原文 Original Text ━━━
[Chinese text in full, presented sentence by sentence]

━━━ 拼音 Pinyin ━━━
[Full pinyin for every sentence, line-by-line matching the original text above.
 For HSK1-3: pinyin for ALL characters.
 For HSK4-5: pinyin only for words above the learner's current level.
 For HSK6: pinyin only for rare/literary characters.
 Respect learner's pinyin_mode override if set.]

━━━ 翻译 Translation ━━━
[Full natural translation in learner's native language, sentence by sentence,
 matching the original text structure so learner can cross-reference]

━━━ 逐句精讲 Sentence-by-Sentence Breakdown ━━━
For EACH sentence in the text:

【第X句】[Chinese sentence]
· 拼音: [full pinyin]
· 翻译: [translation]
· 讲解: [Explain grammar, word choice, sentence structure at learner's level.
  — For beginners: explain word order, basic particles (了/的/在), why each word is there
  — For intermediate: explain clause structure, set phrases, formal vs casual alternatives
  — For advanced: explain register, rhetorical devices, literary allusions, subtle connotations]
· 关键词: [2-3 key words from this sentence]
  → 词 (pīnyīn) — translation — usage note or common collocations

━━━ 📝 词汇总结 Vocabulary Summary (5-8 words) ━━━
· 词语 (pīnyīn) — English — 词性 Part of speech — Example: 例句 + pinyin + translation

━━━ 🔍 语法点 Grammar Spotlight ━━━
[One grammar pattern from the text, explained with:
 — Pattern formula (e.g., S + 把 + O + V + complement)
 — 2-3 graded examples at learner's level with pinyin + translation
 — Common mistakes to avoid]

━━━ 🧠 理解练习 Comprehension ━━━
1. [Question in target language at learner's level] (+ pinyin for HSK1-3)
2. [Question]
3. [Open-ended: 你觉得...？]

━━━ 💡 文化备注 Culture Note ━━━
[Why this content matters / cultural context]
```

**Content sources by level:**
- HSK1-2: 小红书 lifestyle posts, 微博 hot comments, food reviews, simple news headlines
- HSK3-4: 微信公众号 articles (tech, culture, life), Bilibili video descriptions, 知乎 answers
- HSK5-6: 澎湃新闻 editorials, 经济观察报 columns, literary excerpts, academic abstracts

---

## 🎬 Watch & Listen Lesson Template

```
🎬 视听课 | Watch & Listen — [Topic Tag]

📺 推荐内容 Recommended Content
Title: [Chinese title]
Platform: [Bilibili / Douyin / 小宇宙 podcast / etc.]
Duration: [X min]
Link or search terms: [how to find it]

🎯 听前准备 Pre-listening Vocab (5-6 key words)
· 词语 (pīnyīn) — English — 你会在第X分钟听到这个词

👂 听力任务 Listening Tasks
1. [Specific thing to listen for]
2. [Catch this phrase/expression]
3. [Summarize X in one sentence]

📜 关键台词 Key Lines (3-5 sentences from the content)
For each line:
· 原文: [Chinese]
· 拼音: [full pinyin]
· 翻译: [translation]
· 讲解: [Why this line is worth studying — grammar, expression, cultural nuance]

🗣️ 口语 vs 书面 Spoken vs Written
[2-3 colloquial expressions from the content, with pinyin + translation,
 compared to formal equivalents — explain WHEN to use each]

💬 讨论 Discussion
[A question to respond to in Chinese, at learner's level]
```

---

## 💬 Expression Lesson Template

```
💬 地道表达 | Real Talk — [Scenario: e.g., 点外卖 Ordering Delivery]

🎭 场景 Scenario
[Brief setup in Chinese + English]

📚 核心表达 Key Expressions (5-7)
For each expression:
1. [Expression] (pīnyīn)
   翻译: [English]
   用法: [When/how to use — formal/casual/regional]
   讲解: [Break down the expression structure at learner's level]
   例句: [Example sentence + pinyin + translation]

🔄 对话示范 Sample Dialogue
A: ... (pīnyīn) [translation]
B: ... (pīnyīn) [translation]
A: ... (pīnyīn) [translation]
[After dialogue: explain 2-3 key choices]

✏️ 你来试试 Your Turn
[Prompt: respond to a situation using today's expressions]

⚡ 加分 Bonus
[One slang/internet term related to the scenario]
```

---

## 🏛️ Culture Deep-Dive Template

```
🏛️ 文化专题 | Culture Dive — [Topic]

📖 背景 Context
[Cultural background in English with key Chinese terms bolded]

🈶 关键词汇 Key Terms (6-8)
· [Term] (pīnyīn) — [English] — [Why it matters culturally]
  讲解: [Etymology or character breakdown that illuminates the cultural meaning]

📝 原文选段 Authentic Excerpt
[A quote, poem verse, song lyric, or social media post]
· 拼音: [full pinyin]
· 翻译: [full translation]
· 逐字/逐句讲解: [Break down at learner's level]

🤔 思考 Think About It
[Discussion prompt connecting language to culture]
```

---

## 📄 Document Study Template

```
📄 教材解析 | Material Study — [filename or description]

━━━ 📋 内容提取 Extracted Content ━━━
[Full Chinese text extracted from the document/image via OCR or text parsing]

━━━ 📝 词汇提取 Vocabulary Extracted (auto) ━━━
[New vocabulary NOT already in learner's vocab_bank]
· 词语 (pīnyīn) — translation — 词性 Part of speech
[Flag words above or below learner's current level]

━━━ 🔍 语法提取 Grammar Points Found ━━━
· Pattern: [formula]
· 讲解: [explanation at learner's level]
· From text: [quote the sentence where it appears]

━━━ 🎓 内容讲解 Content Walkthrough ━━━
[Walk through section by section. For homework: guide, don't solve.]

━━━ ✏️ 练习 Practice ━━━
[Generate 3-5 exercises based on the material]

━━━ 💾 已保存 Saved ━━━
New vocabulary and grammar have been added to your learning profile.
```

**Knowledge persistence:**
- New vocabulary → append to `vocab_bank` in `hinihao-profile.json`
- New grammar patterns → save to `hinihao-grammar-notes.json` with source reference
- Specific lessons/chapters → create `hinihao-lesson-[name].md`

---

## ✍️ Writing Lesson Template

```
✍️ 汉字课 | Character Writing — [Theme: e.g., 身体 Body Parts]

━━━ 今日汉字 Today's Characters (3-5) ━━━

For EACH character:

【字】[Character] (pīnyīn)
· 翻译: [translation]
· 笔画数: [stroke count]
· 笔顺: [stroke order: "横→竖→撇→捺" / "horizontal → vertical → left-falling → right-falling"]
· 结构: [左右/上下/包围/独体]
· 部首: [radical] (pīnyīn) — meaning: [radical meaning]
  → Why this radical: [semantic connection]
· 字源: [Brief origin story. Keep it memorable:
  "想 = 心 (heart) + 相 (appearance) — what appears in your heart = to think"]
· 常见词: [2-3 common words using this character]
· 易混字: [1 commonly confused character, explain the difference]

━━━ 📐 笔画基础 Stroke Fundamentals ━━━
[HSK1-2: review basic strokes. HSK3+: skip unless rare stroke type.]

━━━ ✏️ 练习 Practice ━━━
1. 看拼音写汉字 Pinyin → Character: [3 words]
2. 看翻译写汉字 Translation → Character: [2 words]
3. 组词 Make words: given [character], write 2 words

━━━ 💡 记忆技巧 Memory Trick ━━━
[Mnemonic for the hardest character. For SEA learners: Sino-Vietnamese/Korean/Japanese cognates.]

━━━ 📱 去APP里练写 Practice in App ━━━
Open AI Chinese app to practice writing today's characters!
```

**Level calibration for writing:**
| Level | Chars/Lesson | Focus |
|-------|-------------|-------|
| HSK1  | 3 | High-frequency standalone chars, basic radicals |
| HSK2  | 3-4 | Common compound chars, radical families |
| HSK3  | 4-5 | Semantic+phonetic compounds, look-alikes |
| HSK4+ | 5 | Complex chars, literary characters, calligraphy notes |

---

## 📷 Snap & Learn Template

```
📷 拍照学中文 | Snap & Learn

━━━ 识别 Recognized Text ━━━
[All Chinese text identified, organized by visual blocks/regions]

━━━ 逐条解析 Line-by-Line ━━━
For each text block:
· 原文: [Chinese text]
· 拼音: [full pinyin]
· 翻译: [translation in learner's native language]
· 讲解: [brief note — formal/casual/slang? cultural context?
  Menus: dish description, ingredients, regional origin
  Signs: what it's telling you
  Labels: key info (ingredients, warnings)]

━━━ 📝 值得记住的 Worth Remembering ━━━
[Pick 2-3 useful words → add to vocab_bank]
· 词 (pīnyīn) — translation — why it's useful
```

---

## 🔤 Word of the Day Template

```
🔤 今日一词 | Word of the Day

[Character/Word] (pīnyīn)
翻译: [translation]

📝 例句:
[Example sentence in context]
· 拼音: [full pinyin]
· 翻译: [sentence translation]

💡 记忆技巧: [One memorable hook — radical breakdown, visual mnemonic,
  native-language cognate, or funny association]

🔗 相关词: [1-2 related words]
```

---

## 💬 Sentence of the Day Template

```
💬 今日一句 | Sentence of the Day

🗣️ [Chinese sentence]
📖 拼音: [full pinyin]
🌐 翻译: [translation]

🎯 用在哪: [Specific real-life scenario]

🔍 拆解: [Brief structure breakdown:
  — Key grammar point
  — One word worth noting]
```

---

## Starter Sequence (Lesson 0.1–0.10) Outline

For absolute beginners (HSK0). Complete these before entering normal rotation.

| Lesson | Topic | Key Content |
|--------|-------|-------------|
| 0.1 | 🎵 Four Tones | 妈麻马骂, tone comparison for tonal-language speakers |
| 0.2 | 📖 Pinyin Initials | 21 initials by mouth position, tricky ones per native language |
| 0.3 | 📖 Pinyin Finals | Simple → compound → nasal finals |
| 0.4 | 🗣️ Survival 1 | 你好、谢谢、对不起、再见、是/不是 |
| 0.5 | 🔢 Numbers | 0-100, 多少钱, ordering food |
| 0.6 | 🗣️ Survival 2 | 我要...、这个/那个、在哪里 |
| 0.7 | ✍️ First Characters | 一二三四五六七八九十, 8 basic strokes, 人/大/天 |
| 0.8 | 👤 Self-Intro | 我叫.../我是...人/我会说..., countries |
| 0.9 | 🍜 Food & Ordering | Menu reading, common dishes, 我要吃/喝... |
| 0.10 | 🎓 Graduation | Assessment → enter HSK1 or repeat weak areas |

Each starter lesson follows the same general structure as the corresponding lesson type above, but simplified for absolute beginners with heavy native-language support.
