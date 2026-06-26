---
name: morning-brief
description: 每日AI早报。抓取多路信源（HuggingFace Blog、人人都是产品经理、blogwatcher订阅、36氪/知乎/Reddit/Twitter工具网关），LLM智能筛选最有价值的10条，推送到Telegram。内置OpenRouter榜单快照。使用场景：每天定时生成个性化AI资讯早报，过滤低信噪比内容，突出竞品动态和变现机会。
metadata:
  openclaw:
    requires:
      bins: [python3]
      env:
        - API_HUB_BASE_URL
        - API_HUB_KEY
---

# 每日AI早报 Morning Brief

每天抓取多路 AI 信源，LLM 筛选后推送到 Telegram。

## 信源覆盖

- **直接 RSS**：HuggingFace Blog、人人都是产品经理
- **blogwatcher**：36氪、量子位、Product Hunt、RadarAI（需已配置 blogwatcher）
- **工具网关**：36氪热榜、InfoQ、知乎热榜、r/LocalLLaMA、Twitter/@xuezhiqian123
- **榜单快照**：OpenRouter Global Top Apps（需预先抓取缓存）

## 筛选逻辑

优先级从高到低：
1. AI工具平台动态（OpenAI/Google/Meta/Anthropic 等头部进展；OpenClaw竞品更新/暴雷）
2. AI Agent 新进展、普通人用 AI 变现案例
3. 资本市场：融资/裁员/暴雷/政策
4. 内容运营/流量变现：小红书/公众号新打法、闲鱼变现机会

竞品特别标注（优先入选）：Hermes Agent、Cline、Roo Code、Agent Zero、Gobii

过滤掉：纯技术/学术论文、HuggingFace 官方自我宣传类内容（开源现状报告等）

## 快速开始

### 1. 配置环境变量

```bash
export API_HUB_BASE_URL=https://api.mulerun.com
export API_HUB_KEY=your_key_here
```

编辑脚本顶部，填入你的 Telegram Bot Token 和 Chat ID：

```python
TELEGRAM_TOKEN = "your_bot_token"
CHAT_ID = "your_chat_id"
CLAWDCHAT_API_KEY = "your_clawdchat_key"  # 可选，用于工具网关
```

### 2. 手动运行

```bash
python3 ~/.openclaw/skills/morning-brief/scripts/morning-brief.py
```

### 3. 定时运行（推荐）

在 OpenClaw 中设置每日定时任务（9:40 AM）：

```
每天早报任务，按以下步骤执行：

步骤1：用 firecrawl 抓取 https://openrouter.ai/apps，提取 Global Ranking 前20名保存到
~/.openclaw/workspace/data/openrouter-top-apps.json
格式：{"fetched_at": "ISO时间", "apps": [{"rank": 1, "name": "...", "tokens": "...", "trend": "..."}]}

步骤2：运行早报脚本
python3 ~/.openclaw/skills/morning-brief/scripts/morning-brief.py

步骤3：把早报正文通过 send_message 发到网页端
```

推荐 cron 时间：`40 9 * * *`（UTC+8 09:40）

## 定制过滤规则

过滤逻辑在脚本 `llm_filter()` 函数的 prompt 中，直接修改文字即可调整：

- `⚡ 特别标注`：添加你关注的竞品名称
- `❌ 一律不选`：添加要过滤的内容类型
- `✅ 优先选`：调整优先级规则

## 依赖

- Python 3.8+（标准库，无需额外安装）
- Telegram Bot（需自行申请 @BotFather）
- ClawdChat API Key（可选，用于36氪/知乎/Reddit/Twitter工具网关）
- blogwatcher（可选，用于订阅源管理）
- firecrawl（可选，用于 OpenRouter 榜单抓取）

## 输出示例

```
⚡ 2026-04-21 Mon 早报

1. [Gemini 2.5 Pro 正式发布，编程能力大幅提升](https://...)
   _Google最新旗舰模型上线，对OpenClaw用户有直接影响_ `HuggingFace Blog`

2. [OpenRouter 榜单新入榜：Perplexity Deep Research...](https://...)
   ...

共 10 条 · 09:41 更新
```
