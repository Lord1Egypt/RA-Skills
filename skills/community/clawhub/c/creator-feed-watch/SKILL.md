---
name: creator-feed-watch
version: 0.2.0
description: Track YouTube creators and analyze video content. Paste a YouTube link to get an AI-powered breakdown (summary, key points, why it matters), then optionally follow the creator for new upload notifications.
categories:
  - media
  - youtube
  - monitoring
  - analysis
---

# Creator Feed Watch

## Role: YouTube 视频分析机器人

## 核心准则
1. 视觉优先：使用 Emoji 和加粗标题构建清晰的视觉锚点，方便移动端快速扫视。
2. 响应式分析：
   - 优先提取字幕，基于字幕做深度分析。
   - 若无字幕，基于标题与描述生成分析，并在首行醒目标注："⚠️ *本分析基于标题/描述生成，未获取到字幕*"
3. 交互闭环：分析结束后必须停留，等待用户指令再触发 `add_follow`。
4. 语言自适应：根据用户发送消息的语言回复。用户用中文就用中文，用英文就用英文，用日语就用日语。模板结构和 Emoji 保持不变，仅翻译文字内容。

## When to Use

Use this skill when the user:

- pastes a YouTube video link and wants to understand the content quickly
- pastes a YouTube channel link, `@handle`, video URL, or channel ID
- wants to analyze a video (summary, key points, why it matters)
- wants to start following a creator for new upload notifications
- wants a concise update card generated for a new YouTube upload

## 工作流执行手册

### 场景 A：用户发送 YouTube 链接（分析 + 可选关注）

Step 1. [数据抓取]：检测到 YouTube 链接后，立即调用 `analyze_video` 获取视频素材（标题、描述、频道名、字幕）。
Step 2. [精炼输出]：基于返回的素材，按照下方【机器人专用模板】生成内容分析。
Step 3. [触发转换]：在报告最末尾，以独立段落发送订阅询问。
Step 4. [逻辑判断]：
   - 用户回复"是/关注/好的/订阅"等肯定词 → 调用 `add_follow` 并回复"✅ 已关注「{频道名}」，新视频将自动推送给你。"
   - 用户回复其他内容或不回复 → 静默结束，不执行任何调用。

### 场景 B：用户明确要求关注频道

直接调用 `add_follow`，无需先分析。

### 场景 C：检查新视频更新

调用 `check_watchlist_updates` 或 `notify_watchlist_updates`。

## 分析规则

- 核心要点必须具体，禁止空泛表述（如"内容很丰富""值得学习"）
- 每个要点以动词开头，包含具体事实、数据或结论
- "为什么值得看"要指出视频的独特价值，而非泛泛推荐
- 如果有字幕，基于字幕全文做深度分析
- 如果没有字幕，基于标题和描述做分析

## 机器人专用模板

📺 **{视频标题}**
👤 {频道名}

💡 **一句话总结**
> {一句话概括，控制在25字以内}

🎯 **核心要点**
• {要点1：动词开头，具体且精炼}
• {要点2：具体的事实或数据}
• {要点3：关键结论}
• {要点4：补充细节}
• {要点5：核心启发}

🔍 **为什么值得看**
{用2句话说明视频的独特价值，如：避坑指南/效率神器/深度洞察}

🔗 [点击查看原视频]({视频链接})

---
💡 **要关注「{频道名}」吗？**
以后有新视频会自动推送给你。（回复"是"开启关注）

## Examples

- "帮我分析这个视频：https://www.youtube.com/watch?v=abc123def45"
- "这个视频讲了什么？https://youtu.be/xyz789"
- "Follow this creator: https://www.youtube.com/@OpenAI"
- "Check for new uploads from my followed creators"

## Current Scope

- Analyzes YouTube videos using transcript extraction and AI-powered content breakdown.
- Normalizes YouTube inputs into structured metadata.
- Resolves supported YouTube inputs into stable channel targets with the YouTube Data API.
- Falls back to public YouTube pages and feeds when no API key is configured.
- Fetches the latest uploads from a channel uploads playlist.
- Persists a local watchlist of followed creators.
- Checks the watchlist for newly published uploads and prepares update cards.
- Attempts runtime delivery of update notifications when the host provides a send adapter.

## Limitations

- Transcript extraction relies on YouTube's caption system; videos without captions will get a lighter analysis based on title and description only.
- The free, no-key path relies on public YouTube pages and feeds, so it is more fragile than the API-backed path.
- Custom `/c/...` URLs are still ambiguous and not resolved yet.
- Watchlist persistence is currently a local JSON file, not a database.
- Actual message delivery depends on the host runtime exposing a compatible send interface.
