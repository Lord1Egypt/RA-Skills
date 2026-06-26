---
name: daily-news-skill
description: "自定义新闻类型，自动从互联网抓取最新消息，用语音播报。支持科技/财经/体育/娱乐等多个类别，定时发送。"
---

# Daily News Skill - 每日新闻播报技能

自定义新闻类型，自动抓取最新消息，语音播报！

## 🎯 功能特点

- ✅ **自定义类别**：科技/财经/体育/娱乐/国际等
- ✅ **自动抓取**：从互联网获取最新新闻
- ✅ **语音播报**：用 NoizAI TTS 生成语音
- ✅ **定时发送**：每天早上自动推送
- ✅ **多源聚合**：支持多个新闻源
- ✅ **智能摘要**：AI 总结新闻要点

## 📋 使用场景

- 🌅 晨间播报：每天早上 8 点听新闻
- 💼 财经追踪：关注股市/行业动态
- 🎮 娱乐资讯：游戏/电影/音乐新闻
- 🌍 国际时事：全球重要事件
- 🏀 体育快讯：比赛结果/转会消息

## 🔧 前置要求

### 1. Feishu 应用配置

同 Feishu Voice Skill

### 2. 新闻源 API

- Tavily API（推荐）
- 或免费新闻 RSS

### 3. 系统依赖

```bash
# 安装 jq
yum install -y jq
```

## 🚀 快速开始

### 步骤 1：配置环境变量

```bash
export FEISHU_APP_ID="cli_xxx"
export FEISHU_APP_SECRET="xxx"
export FEISHU_CHAT_ID="oc_xxx"
export NOIZ_API_KEY="xxx"
export TAVILY_API_KEY="tvly_xxx"  # 可选
```

### 步骤 2：定制新闻类别

编辑 `news_config.conf`：

```bash
# 格式：类别名称，关键词，新闻数量
科技，AI 人工智能 机器学习，5
财经，股票 股市 金融，3
体育，篮球 足球 NBA，2
```

### 步骤 3：运行播报

```bash
# 手动运行一次
bash scripts/news_broadcast.sh

# 加入定时任务（每天早上 8 点）
crontab -e
0 8 * * * bash /path/to/news_broadcast.sh
```

## 💡 使用示例

### 1. 只关注科技新闻

```bash
cat > news_config.conf << EOF
科技，AI 人工智能 芯片 互联网，10
EOF

bash scripts/news_broadcast.sh
```

### 2. 财经 + 体育

```bash
cat > news_config.conf << EOF
财经，股票 股市 基金，5
体育，NBA 足球 网球，3
EOF

bash scripts/news_broadcast.sh
```

### 3. 定制个性化播报

```bash
cat > news_config.conf << EOF
科技，OpenAI Google 苹果，5
财经，A 股 美股 比特币，3
娱乐，电影 音乐 游戏，2
EOF

bash scripts/news_broadcast.sh
```

## 📖 命令参数

```bash
bash scripts/news_broadcast.sh [选项]

选项:
  -c, --config <file>     配置文件路径
  -o, --output <type>     输出格式（voice/text/both）
  --limit <num>           每类新闻数量上限
  --no-voice              只输出文字，不生成语音
  -h, --help              显示帮助
```

## 🎤 播报格式

司幼会用温暖的声音播报：

> "主人早上好～ 今天是 3 月 7 日，星期六。司幼给您播报今天的新闻～
>
> 【科技】
> 1. OpenAI 发布新模型...
> 2. 苹果推出新产品...
>
> 【财经】
> 1. A 股今日上涨...
> 2. 比特币突破...
>
> 播报完毕～ 祝主人一天好心情！🌸"

## ⚙️ 高级配置

### 1. 自定义播报时间

```bash
# 编辑 config.sh
BROADCAST_TIME="08:00"  # 早上 8 点
```

### 2. 自定义播报风格

```bash
# 正式风格
BROADCAST_STYLE="formal"

# 轻松风格
BROADCAST_STYLE="casual"

# 可爱风格（司幼默认）
BROADCAST_STYLE="cute"
```

### 3. 新闻源配置

```bash
# 使用 Tavily API
NEWS_SOURCE="tavily"

# 使用 RSS
NEWS_SOURCE="rss"

# 使用搜索引擎
NEWS_SOURCE="search"
```

## 📦 文件结构

```
daily-news-skill/
├── SKILL.md
├── README.md
├── reference.md
├── scripts/
│   ├── news_broadcast.sh    # 主脚本
│   ├── fetch_news.sh        # 抓取新闻
│   ├── summarize.sh         # 摘要生成
│   └── config.sh            # 配置文件
├── examples/
│   ├── news_config.conf     # 配置示例
│   └── crontab.txt          # 定时任务示例
└── news_config.conf         # 用户配置
```

## 💰 商业授权

- **个人使用**：免费
- **商业使用**：请联系作者获取授权

---

**Made with ❤️ by 司幼 (SiYou)**
