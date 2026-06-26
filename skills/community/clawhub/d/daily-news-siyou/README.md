# 📰 Daily News Skill - 每日新闻播报

自定义新闻类型，自动从互联网抓取最新消息，语音播报！

## ✨ 功能特点

- ✅ **自定义类别**：科技/财经/体育/娱乐等
- ✅ **自动抓取**：从互联网获取最新新闻
- ✅ **语音播报**：NoizAI TTS 生成语音
- ✅ **定时发送**：每天早上自动推送

## 🚀 快速开始

### 1. 配置环境变量

```bash
export FEISHU_APP_ID="cli_xxx"
export FEISHU_APP_SECRET="xxx"
export FEISHU_CHAT_ID="oc_xxx"
export NOIZ_API_KEY="xxx"
export TAVILY_API_KEY="tvly_xxx"  # 可选
```

### 2. 定制新闻类别

编辑 `news_config.conf`：

```
科技，AI 人工智能，5
财经，股票 股市，3
体育，NBA 足球，2
```

### 3. 运行播报

```bash
bash scripts/news_broadcast.sh
```

### 4. 设置定时任务

```bash
crontab -e
0 8 * * * bash /path/to/news_broadcast.sh
```

## 💡 使用场景

- 🌅 晨间播报：每天早上 8 点听新闻
- 💼 财经追踪：关注股市/行业动态
- 🎮 娱乐资讯：游戏/电影/音乐
- 🌍 国际时事：全球重要事件

## 📖 详细文档

查看 [SKILL.md](SKILL.md) 获取完整使用说明。

---

**Made with ❤️ by 司幼 (SiYou)**
