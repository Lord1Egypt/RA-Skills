# Content Repurposer - Multi-Platform Content Adaptor

Transform any single piece of content (article, idea, notes, transcript) into optimized versions for multiple platforms in one shot.

---

## 📖 如何使用 / How to Use

### 安装 / Install
```bash
openclaw skills install content-repurposer-cn
```

### 使用步骤 / Steps
1. 把你的文章/笔记/想法粘贴到 OpenClaw
2. 触发：

```
帮我把这段内容一稿多发，适配各个平台
```
```
只需要微信公众号和小红书版本
```
```
我有个主题："年轻人为什么越来越不愿意加班"，帮我生成各平台内容
```

### 支持的输出平台 / Output Platforms

| 平台 | 格式 | 字数 |
|------|------|------|
| 微信公众号 | 长文，带标题+摘要+分节 | 800-1500字 |
| 知乎 | 问答格式，自动生成问题 | 500-1000字 |
| 小红书 | 轻松口语，带话题标签 | 200-500字 |
| 抖音/TikTok | 口播脚本，带镜头提示 | 30-60秒 |
| 头条号 | 短段落，移动端友好 | 600-1200字 |
| Twitter Thread | 5-8条推文，英文 | 280字/条 |
| LinkedIn | 专业风格，英文 | 150-300字 |

### 追问示例 / Follow-up Prompts
```
小红书那版改得更接地气一点，像普通女生写的
抖音脚本改成带字幕的格式
微信文章标题帮我想5个备选，A/B测试用
```

### 常见问题 / FAQ
- **可以从零开始吗？** 可以，给主题或关键词，skill 自动展开内容
- **只发某几个平台？** 告诉它你需要哪几个平台就行
- **中英文都支持吗？** 支持，中文内容自动翻译+适配英文平台
- **需要额外配置吗？** OpenClaw 配置好 AI 即可使用，支持阿里云百炼、DeepSeek 等，录入 Key 就行
- **有问题找谁？** ClawHub 页面留言或联系 @ShuaigeSkillBot
- **需要帮你配置好直接用？** Telegram 私信 @ShuaigeSkillBot，配置服务 ¥99，配好即用

---

## Trigger

When the user says any of: "repurpose", "distribute", "cross-post", "adapt for", "rewrite for platforms", "content matrix", "multi-platform", "分发", "一稿多发", "多平台", "改写", "转发各平台"

## Workflow

### Step 1: Analyze the Source Content
Read the user's input (text, file, or URL). Identify:
- Core message / thesis
- Key data points or quotes
- Target audience
- Tone (professional / casual / educational / entertaining)

### Step 2: Generate Platform-Specific Versions

Produce ALL of the following in a single response. Each version must feel **native** to that platform — not just reformatted, but genuinely rewritten:

---

#### Twitter/X Thread (English)
- 5-8 tweets, each under 280 characters
- Hook in tweet 1 (question, bold claim, or surprising stat)
- Use line breaks for readability
- End with CTA (follow, retweet, link)
- No hashtag spam (max 2)

#### LinkedIn Post (English)
- 150-300 words
- Professional but human tone
- Start with a hook line (insight, lesson, or question)
- Use short paragraphs (1-2 sentences each)
- End with a question to drive comments

#### WeChat Article (公众号 - Chinese)
- 800-1500 words
- Title: clickable but not clickbait (< 30 chars)
- Opening: hook within first 2 sentences
- Structure: subheadings every 200-300 words
- Include a 摘要 (abstract) under 120 chars
- Tone: authoritative but accessible
- End with: 引导关注 + 引导转发

#### Zhihu Answer (知乎 - Chinese)
- 500-1000 words
- Frame as answering a question (generate the question too)
- Data-driven, cite sources where possible
- Logical structure with numbered points
- Tone: expert sharing knowledge
- End with: "以上，希望对你有帮助"

#### Xiaohongshu Note (小红书 - Chinese)
- 200-500 words
- Title with emoji (not excessive, 1-2 max)
- Casual, first-person, story-driven
- Break into short paragraphs
- Include 3-5 relevant tags at the end
- Tone: like sharing with a friend

#### Douyin/TikTok Script (Chinese)
- 30-60 second script
- Hook in first 3 seconds (question or shocking statement)
- 3-act structure: hook → content → CTA
- Spoken language, not written language
- Include stage directions [镜头切换] [展示画面]

#### Toutiao Article (头条 - Chinese)
- 600-1200 words
- Title: curiosity-driven, slightly provocative
- Dense information, numbered lists preferred
- Shorter paragraphs than WeChat (mobile-first)
- Embedded question hooks every 200 words

---

### Step 3: Output Format

Present each version under a clear heading with platform name and character/word count. Use markdown formatting.

At the end, provide a **Distribution Checklist**:
- [ ] WeChat: schedule via editor
- [ ] Zhihu: post as answer to relevant question
- [ ] Xiaohongshu: add cover image
- [ ] Douyin: record using script
- [ ] Toutiao: submit to relevant channel
- [ ] Twitter: schedule thread
- [ ] LinkedIn: post during business hours (Tue-Thu)

## Rules
1. Never produce generic "one size fits all" content. Each platform version must feel native.
2. Chinese platforms get Chinese content. English platforms get English content.
3. Preserve the core message but adapt framing, length, tone, and structure per platform.
4. If source content is in Chinese, still produce English versions (translate + adapt). Vice versa.
5. If the user specifies only certain platforms, produce only those.
6. Include estimated reading time for long-form content.

---
📢 每日市场数据播报，关注 Telegram 频道：https://t.me/shuaigeclaw
