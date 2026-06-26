**English**

# 追踪建造者，而非网红

一个 AI 驱动的信息聚合工具，追踪 AI 领域最顶尖的建造者——研究员、创始人、产品经理和工程师——并将他们的最新动态整理成易于消化的摘要。

**理念：** 追踪那些真正在做产品、有独立见解的人，而非只会搬运信息的网红。

## 你会得到什么

按需生成的摘要，包含：

- 顶级 AI 播客新节目的精华摘要
- 25 位精选 AI 建造者在 X/Twitter 上的关键观点和洞察
- AI 公司官方博客的完整文章（Anthropic Engineering、Claude Blog）
- 所有原始内容的链接
- 支持英文、中文或双语版本

## 前置要求

### 系统依赖

**yt-dlp**（YouTube 视频列表和字幕获取）
- macOS: `brew install yt-dlp`
- Linux: `pip install yt-dlp` 或 `pipx install yt-dlp`
- Windows: `pip install yt-dlp` 或从 [GitHub Releases](https://github.com/yt-dlp/yt-dlp/releases) 下载
- 如遇到 "Sign in to confirm" 错误，需配置 cookies：在 `.env` 添加 `YT_DLP_COOKIES=chrome`

**Node.js 22+**（Rettiwt-API 依赖要求）

**Twitter/X**：无需 API key，使用免费 guest 认证。如果遇到限流，可配置 user 认证（可选）。

## 快速开始

1. 在你的 AI agent 中安装此 skill（OpenClaw 或 Claude Code）
2. 确保已安装 yt-dlp：
   ```bash
   yt-dlp --version
   ```
3. （可选）如需 Twitter user 认证，添加到 `.env`：
   ```bash
   RETTIWT_API_KEY=your_key_here
   ```
4. 输入 "set up follow builders" 或执行 `/follow-builders`
5. Agent 会以对话方式引导你完成设置

设置完成后，你的第一期摘要会立即生成。

## 修改设置

通过对话即可修改所有设置。直接告诉你的 agent：

- "语言换成中文"
- "把摘要写得更简短一些"
- "显示我当前的设置"
- "添加 Twitter 账号 @username"
- "移除 @username"

## 自定义信息源

你可以完全控制追踪哪些信息源！

### 通过对话（推荐）
- "添加 Twitter 账号 @username"
- "添加播客频道 @channel"
- "列出我的信息源"
- "仅使用我的自定义源"
- "重置为默认源"

### 手动配置

所有配置统一在 `config/config.json` 中：

```json
{
  "sourceMode": "merge",
  "sources": {
    "x_accounts": [
      { "name": "你喜欢的建造者", "handle": "username" }
    ],
    "podcasts": [
      {
        "name": "我的播客",
        "type": "youtube_channel",
        "url": "https://youtube.com/@mypodcast",
        "channelHandle": "mypodcast"
      }
    ]
  }
}
```

**模式说明：**
- `merge` - 使用 config.json 中的源列表（默认）
- `replace` - 同上（源列表即为你自定义的内容）

## 自定义摘要风格

Skill 使用纯文本 prompt 文件来控制内容的摘要方式。你可以通过两种方式自定义：

**通过对话（推荐）：**
直接告诉你的 agent——"摘要写得更简练一些"、"多关注可操作的洞察"、"用更轻松的语气"。Agent 会自动帮你更新 prompt。

**直接编辑（高级用户）：**
编辑 `prompts/` 目录下的文件：
- `summarize-podcast.md` — 播客摘要方式
- `summarize-tweets.md` — Twitter 推文摘要方式
- `summarize-blogs.md` — 博客文章摘要方式
- `digest-intro.md` — 整体摘要格式和语气
- `translate.md` — 英文内容如何翻译成中文

这些都是纯文本说明，不是代码。修改会在下次生成摘要时生效。

## 默认信息源

### 播客（5个）
- [Latent Space](https://www.youtube.com/@LatentSpacePod)
- [Training Data](https://www.youtube.com/playlist?list=PLOhHNjZItNnMm5tdW61JpnyxeYH5NDDx8)
- [No Priors](https://www.youtube.com/@NoPriorsPodcast)
- [Unsupervised Learning](https://www.youtube.com/@RedpointAI)
- [Data Driven NYC](https://www.youtube.com/@DataDrivenNYC)

### AI 建造者（25位）
[Andrej Karpathy](https://x.com/karpathy), [Swyx](https://x.com/swyx), [Josh Woodward](https://x.com/joshwoodward), [Kevin Weil](https://x.com/kevinweil), [Peter Yang](https://x.com/petergyang), [Nan Yu](https://x.com/thenanyu), [Madhu Guru](https://x.com/realmadhuguru), [Amanda Askell](https://x.com/AmandaAskell), [Cat Wu](https://x.com/_catwu), [Thariq](https://x.com/trq212), [Google Labs](https://x.com/GoogleLabs), [Amjad Masad](https://x.com/amasad), [Guillermo Rauch](https://x.com/rauchg), [Alex Albert](https://x.com/alexalbert__), [Aaron Levie](https://x.com/levie), [Ryo Lu](https://x.com/ryolu_), [Garry Tan](https://x.com/garrytan), [Matt Turck](https://x.com/mattturck), [Zara Zhang](https://x.com/zarazhangrui), [Nikunj Kothari](https://x.com/nikunj), [Peter Steinberger](https://x.com/steipete), [Dan Shipper](https://x.com/danshipper), [Aditya Agarwal](https://x.com/adityaag), [Sam Altman](https://x.com/sama), [Claude](https://x.com/claudeai)

### 官方博客（2个）
- [Anthropic Engineering](https://www.anthropic.com/engineering) — Anthropic 团队的技术深度文章
- [Claude Blog](https://claude.com/blog) — Claude 产品公告和更新

## 安装

### OpenClaw
```bash
# 从 ClawHub 安装（即将推出）
clawhub install follow-builders

# 或手动安装
git clone https://github.com/champagne315/follow-aibuilders.git ~/skills/follow-builders
cd ~/skills/follow-builders/scripts && npm install
```

### Claude Code
```bash
git clone https://github.com/champagne315/follow-aibuilders.git ~/.claude/skills/follow-builders
cd ~/.claude/skills/follow-builders/scripts && npm install
```

## 工作原理

1. **本地抓取**：你的 agent 使用 Rettiwt-API（Twitter/X）和 yt-dlp（YouTube）免费抓取内容，同时直接 HTTP 抓取博客
2. **去重机制**：在 `state-feed.json` 中记录已读内容，避免重复
3. **内容重组**：你的 agent 使用可自定义的 prompt 将原始内容处理成易消化的摘要
4. **即时输出**：摘要直接在聊天中显示

**架构优势：**
- ✅ 完全免费，无需付费 API
- ✅ 完全控制信息源
- ✅ 隐私保护：数据本地处理，从不传输
- ✅ 无单点故障
- ✅ 内容和格式完全可定制

## 隐私说明

- 所有内容抓取都从你的本地机器进行，无需付费 API
- Twitter 认证（可选）存储在本地 `.env`
- 你的配置、偏好和阅读记录都保留在你的机器上
- Skill 只读取公开内容（公开博客文章、公开 YouTube 视频、公开 X 推文）

## 常见问题

### "yt-dlp 未安装"
按照前置要求中的说明安装 yt-dlp。

### "yt-dlp 被要求验证身份"
YouTube 要求登录验证。在 `.env` 添加：
```
YT_DLP_COOKIES=chrome
```
（支持 chrome、firefox、edge 等浏览器名，或 cookies.txt 文件路径）

### "Twitter API 速率限制中"
Guest 认证配额已用完。配置 user 认证：
1. 安装 Chrome 扩展 X Auth Helper
2. 在隐身模式登录 Twitter/X
3. 获取 API_KEY 并添加到 `.env`

### "No new updates from your builders today"
这是正常的——表示在回溯窗口内（推文 24 小时，播客/博客 72 小时）没有新内容。

### 想减少抓取时间？
- 使用 `mode: "replace"` 并减少信息源数量
- 对不需要的信息源设置 `enabled: false`

## 迁移

如从使用付费 API 的旧版本升级：

1. 安装 yt-dlp（见前置要求）
2. 确保 Node.js 22+ 已安装
3. 旧的 API keys（X_RAPIDAPI_KEY、SUPADATA_API_KEY）不再需要
4. 运行 `node fetch-and-prepare.js` 验证

## 许可证

MIT
