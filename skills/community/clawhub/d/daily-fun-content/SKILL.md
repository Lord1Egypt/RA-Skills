---
name: daily-fun-content
description: "每日趣味内容生成器 - 每天早上搜索网络，预缓存一天的笑话、热梗、聊天技巧。包括搞笑段子、网络热梗解释、高情商对话示例。用 cron 触发，内容缓存到文件，心跳时随机取用。"
license: MIT
metadata:
  clawdbot:
    emoji: "🎉"
    os: ["darwin", "linux"]
    requires:
      env: []
---

# Daily Fun Content

每天早上自动搜索网络，生成并缓存一天的趣味内容。

## 功能

- **搞笑段子** - 从网络搜索最新笑话、段子
- **网络热梗** - 搜索最近流行的梗、表情包梗、流行语
- **聊天技巧** - 高情商对话示例、接话技巧
- **预缓存** - 每天早上生成 6-8 条内容，存到 `cache/daily-fun.json`
- **随机取用** - 心跳时从缓存随机取一条分享

## 使用方式

### 1. 每日生成（Cron）

每天早上 6:00 自动生成：

```bash
openclaw cron add \
  --name "Daily Fun Content Generator" \
  --cron "0 6 * * *" \
  --tz "Asia/Shanghai" \
  --session isolated \
  --wake now \
  --message "Generate daily fun content: search web for jokes, memes, and chat tips. Cache 6-8 items to cache/daily-fun.json"
```

### 2. 手动生成

```bash
node {baseDir}/scripts/generate.mjs
```

### 3. 获取内容

心跳时调用：

```bash
node {baseDir}/scripts/get-content.mjs
```

返回随机一条缓存的内容。

## 内容格式

缓存文件 `cache/daily-fun.json`：

```json
{
  "date": "2026-03-09",
  "generated": "2026-03-09T06:00:00Z",
  "items": [
    {
      "type": "joke",
      "content": "朋友问我'你周末干嘛了'，我说'躺了一天'。他说'那多无聊啊'。我说'你不懂，躺平也是一种技术，我得练'。"
    },
    {
      "type": "meme",
      "title": "我悟了",
      "content": "最近'我悟了'这个梗挺火。用法：当别人说了个常识，你装作恍然大悟。\n朋友：'多喝水对身体好'\n你：'我悟了'"
    },
    {
      "type": "chat_tip",
      "content": "别人问'在干嘛'，别说'没干嘛'。说'刚在想你上次说的那个事'或者'在发呆，你呢？'— 把球抛回去，对话才能继续。"
    }
  ]
}
```

## 内容类型

| 类型 | 说明 | 来源 |
|------|------|------|
| `joke` | 搞笑段子、生活笑话 | 搜索"最新笑话 2026"、"搞笑段子" |
| `meme` | 网络热梗、流行语 | 搜索"最近流行梗"、"网络热词 2026" |
| `chat_tip` | 聊天技巧、高情商对话 | 搜索"聊天技巧"、"高情商回复" |

## 搜索策略

生成时会搜索：
1. 中文搞笑内容（豆瓣、知乎、微博等）
2. 最近 7 天的网络热梗
3. 实用的聊天技巧

确保内容：
- 真正好笑，不冷
- 热梗解释清楚用法
- 聊天技巧实用不油腻
- 不冒犯、不敏感

## 心跳集成

更新 `HEARTBEAT.md`：

```markdown
### 6. 趣味内容分享（每 2-3 小时）
- **条件**：距离上次分享 > 2 小时
- **动作**：`node skills/daily-fun-content/scripts/get-content.mjs`
- **报告**：直接分享返回的内容
- **回退**：如果缓存为空，现场生成一条
```

## 文件结构

```
skills/daily-fun-content/
├── SKILL.md              # 本文件
├── scripts/
│   ├── generate.mjs      # 每日生成脚本
│   └── get-content.mjs   # 获取随机内容
└── cache/
    └── daily-fun.json    # 缓存文件（gitignore）
```

## 依赖

- 需要网络搜索能力（可用 `perplexity` skill 或 `glm-web-search` skill）
- Node.js 18+

## 发布到 ClawHub

```bash
# 1. 测试
node scripts/generate.mjs
node scripts/get-content.mjs

# 2. 发布
clawhub publish ./skills/daily-fun-content \
  --slug daily-fun-content \
  --name "Daily Fun Content" \
  --version 1.0.0 \
  --changelog "Initial release - daily jokes, memes, and chat tips"
```

## 示例输出

**笑话：**
> 去面试，面试官问"你最大的缺点是什么"，我说"太诚实"。他说"我不觉得这是缺点"。我说"我不在乎你怎么想"。

**热梗：**
> "破防了" - 原意是游戏里防御被打破，现在指心理防线崩溃。
> 用法：看到戳中自己的内容时用。
> 朋友：发了个扎心的视频
> 你："破防了"

**聊天技巧：**
> 如何优雅地结束对话？
> 别说"我去洗澡了"（太假）。
> 说"我得去处理点事，回头聊"或者"不早了，你先忙"。
> 给对方台阶，也给自己留余地。

---

**原则**：轻松、有趣、不油腻。质量 > 数量。
