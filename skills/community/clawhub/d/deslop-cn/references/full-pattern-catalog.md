# 完整模式目录

> 29 个 AI 文本模式的详细说明、检测方法和修复示例。
> 按 Tier 分级：Tier 1（3 分）最强信号，Tier 2（2 分）中等，Tier 3（1 分）弱信号。
> 来源：slopbuster (1000+ AI vs 人类样本分析)、humanizer (Wikipedia AI Cleanup)、human-writing (中文技术写作实践)。

---

## Tier 1 — 最强 AI 信号（每个 3 分）

### 1. AI 词汇聚集

**检测词**: delve, tapestry(抽象), testament, interplay, intricacies, landscape(抽象), vibrant, showcasing, underscoring, fostering, garnering

**为什么是强信号**: 这些词在 2023 年后 LLM 文本中出现频率是人类写作的 5-25 倍 (Kobak et al. 2025, Liang et al. 2024)。它们常常聚集出现——看到一个，附近通常还有。

**Before:**
> Additionally, a distinctive feature of Somali cuisine is the incorporation of camel meat. An enduring testament to Italian colonial influence is the widespread adoption of pasta in the local culinary landscape, showcasing how these dishes have integrated into the traditional diet.

**After:**
> Somali cuisine also includes camel meat, considered a delicacy. Pasta, introduced during Italian colonization, remains common in the south.

**修复**: 每个换成更普通的词。"Additionally" → "Also" 或直接开头。"Landscape" → 说出具体领域。"Showcasing" → 删掉，句子本身就在展示。

---

### 2. 意义膨胀

**检测词**: stands/serves as, is a testament/reminder, vital/significant/crucial/pivotal/key role/moment, underscores/highlights its importance, reflects broader, symbolizing its ongoing/enduring, setting the stage for, marks a shift, key turning point, evolving landscape, focal point, indelible mark

**Before:**
> The Statistical Institute of Catalonia was officially established in 1989, marking a pivotal moment in the evolution of regional statistics in Spain.

**After:**
> The Statistical Institute of Catalonia was established in 1989 to collect and publish regional statistics independently from Spain's national statistics office.

**修复**: 说具体发生了什么。不评价宇宙意义。

---

### 3. Copula 回避

**检测词**: serves as, stands as, marks, represents [a], boasts, features, offers [a], functions as, acts as, operates as

**为什么是强信号**: 人类写作大量使用 "is"/"are"/"has"。LLM 系统性地回避这些简单系词，用更花哨的替代。这是最一致和可靠的 AI 信号之一。

**Before:**
> Gallery 825 serves as LAAA's exhibition space for contemporary art. The gallery features four separate spaces and boasts over 3,000 square feet.

**After:**
> Gallery 825 is LAAA's exhibition space for contemporary art. The gallery has four rooms totaling 3,000 square feet.

**修复**: "serves as" → "is"。"features" → "has"。"boasts" → "has"。

---

### 4. 负面并行

**检测词**: Not only... but also..., It's not just about... it's..., It's not merely... it's..., goes beyond... to..., more than just...

**Before:**
> It's not just about the beat riding under the vocals; it's part of the aggression and atmosphere. It's not merely a song, it's a statement.

**After:**
> The heavy beat adds to the aggressive tone.

**修复**: 直接说 Y。"not X" 的铺垫几乎总是废话。

---

### 5. -ing 伪分析

**检测词**: highlighting/underscoring/emphasizing..., ensuring..., reflecting/symbolizing..., contributing to..., cultivating/fostering..., encompassing..., showcasing...

**Before:**
> The temple's color palette resonates with the region's natural beauty, symbolizing Texas bluebonnets, reflecting the community's deep connection to the land.

**After:**
> The temple uses blue, green, and gold. The architect said these were chosen to reference local bluebonnets and the Gulf coast.

**修复**: 砍掉 -ing 短语。如果解释有价值，写成独立句子并标来源。

---

### 6. 推广语言

**检测词**: boasts a, vibrant, rich(比喻), profound, enhancing its, showcasing, exemplifies, commitment to, natural beauty, nestled, in the heart of, groundbreaking(比喻), renowned, breathtaking, must-visit, stunning, state-of-the-art, cutting-edge, world-class, unparalleled, transformative

**Before:**
> Nestled within the breathtaking region of Gonder in Ethiopia, Alamata Raya Kobo stands as a vibrant town with a rich cultural heritage and stunning natural beauty.

**After:**
> Alamata Raya Kobo is a town in the Gonder region of Ethiopia, known for its weekly market and 18th-century church.

**修复**: 用事实描述替换形容词堆砌。什么让它 "stunning"？说那个具体的东西。

---

### 7. 聊天残留

**检测词**: I hope this helps, Of course!, Certainly!, You're absolutely right!, Would you like..., let me know, here is a..., Great question!

**修复**: 全部删除。这些是对话痕迹，不是内容。

---

## Tier 2 — 中等 AI 信号（每个 2 分）

### 8. 模糊归因

**检测词**: Industry reports, Observers have cited, Experts argue, Some critics argue, several sources, studies show, research suggests, it is widely believed

**Before:**
> Experts believe it plays a crucial role in the regional ecosystem.

**After:**
> The Haolai River supports several endemic fish species, according to a 2019 survey by the Chinese Academy of Sciences.

**修复**: 点名来源，否则删掉。"Studies show" 不带引用就是穿着白大褂的观点。

---

### 9. 三的规则

LLM 把一切强制凑成三组。有两个就写两个，有四个就写四个。

**Before:**
> The event features keynote sessions, panel discussions, and networking opportunities. Attendees can expect innovation, inspiration, and industry insights.

**After:**
> The event includes talks and panels. There's also time for informal networking between sessions.

---

### 10. 同义轮换

LLM 有重复惩罚机制，会对同一事物轮换称呼。人类写作中，同一事物用同一个词指称，读者不会注意到重复，但会被强制同义词打断。

**Before:**
> The protagonist faces challenges. The main character must overcome obstacles. The central figure eventually triumphs. The hero returns home.

**After:**
> The protagonist faces many challenges but eventually triumphs and returns home.

---

### 11. 虚假范围

"from X to Y" 但 X 和 Y 不在同一刻度上。

**Before:**
> ...from the singularity of the Big Bang to the grand cosmic web, from the birth and death of stars to the enigmatic dance of dark matter.

**After:**
> The book covers the Big Bang, star formation, and current theories about dark matter.

---

### 12. 公式化挑战

"Despite X... continues to thrive" 模板。可以在任意两篇文章间互换而不改变含义。

**Before:**
> Despite its industrial prosperity, Korattur faces challenges typical of urban areas. Despite these challenges, Korattur continues to thrive.

**After:**
> Traffic congestion increased after 2015 when three new IT parks opened. The municipal corporation began a stormwater drainage project in 2022.

---

### 13. 过度 hedging

**Before:**
> It could potentially possibly be argued that the policy might have some effect on outcomes.

**After:**
> The policy may affect outcomes.

---

### 14. 通用正面结尾

**Before:**
> The future looks bright. Exciting times lie ahead as they continue their journey toward excellence.

**After:**
> The company plans to open two more locations next year.

---

### 15. Em dash 过度

LLM 使用 em dash 的频率远高于人类，模仿"有力"的销售文案风格。一段超过 2 个就要警惕。

**修复**: 大部分可以用逗号、句号或括号替代。

---

### 16. 粗体过度

LLM 机械地给短语加粗。

**修复**: 只在真正需要视觉强调时使用。去掉装饰性粗体。

---

### 17. 竖列表带粗体标题

`- **Header:** description` 是 LLM 最常用的输出格式之一。

**修复**: 能写成段落就写段落。需要列表时用简单列表。

---

### 18. 权威伪装

**检测词**: The real question is, at its core, in reality, what really matters, fundamentally, the deeper issue, the heart of the matter

LLM 用这些短语假装在穿透噪音到达更深层的真相，但后面跟的通常就是一个普通观点。

**修复**: 删前缀，直接说观点。

---

### 19. 路标预告

**检测词**: Let's dive in, let's explore, let's break this down, here's what you need to know, now let's look at, without further ado

**修复**: 删除。直接开始。

---

### 20. 断裂标题

标题后跟一句话重述标题，然后才进入内容。

**Before:**
> ## Performance
>
> Speed matters.
>
> When users hit a slow page, they leave.

**After:**
> ## Performance
>
> When users hit a slow page, they leave.

---

## Tier 3 — 弱信号（每个 1 分）

### 21. 被动语态过度

不是所有被动语态都有问题。但 LLM 系统性地隐藏 actor。

**Before:**
> The results are preserved automatically. No configuration file needed.

**After:**
> The system preserves the results automatically. You do not need a configuration file.

---

### 22. Title Case 标题

LLM 倾向于在标题中大写所有主要词。

**修复**: 用 sentence case。

---

### 23. Emoji 装饰

`🚀 **Launch Phase**` 这种格式。

**修复**: 删 emoji。

---

### 24. 弯引号

ChatGPT 使用弯引号 "..." 而非直引号 "..."。

**修复**: 统一用直引号。

---

### 25. 填充短语

"In order to" → "To"。"Due to the fact that" → "Because"。"It is important to note that" → 删掉。"The system has the ability to" → "The system can"。

---

### 26. 连字符过度统一

LLM 对 "cross-functional"、"high-quality"、"data-driven" 等常见复合词的连字符使用完美一致。人类写作中这些连字符是不一致的。

---

### 27. 说服性权威语气

"The real question is..."、"At its core..." 后面跟的只是一个普通观点包装成顿悟。

---

### 28. 完美对称结构

每个段落同样长度、同样内部结构（claim → evidence → implication）。

**修复**: 让有些段落只有一句话。让有些论点不完全解决。

---

### 29. 修辞性提问立刻回答

**Before:**
> What makes this approach effective? The answer lies in three key factors...

**After:**
> 删掉问题。直接说因素。
