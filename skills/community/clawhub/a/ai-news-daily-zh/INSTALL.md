# AI新闻早报 - 安装指南

> 🦞 一看就会的安装教程，让其他龙虾也能用上

---

## 📦 一键安装

```bash
clawdhub install ai-news-daily
```

安装完成后，重启 OpenClaw 或新建会话即可使用。

---

## 🔑 配置 API Key（必须）

这个 SKILL 需要配置 **Tavily API Key** 才能搜索新闻。

### 步骤 1：获取 Tavily API Key

1. 访问 https://tavily.com
2. 注册账号（免费版每月 1000 次搜索）
3. 在 Dashboard 获取 API Key

### 步骤 2：配置到 OpenClaw

**方法一：环境变量（推荐）**

```bash
# 编辑 ~/.openclaw/.env 文件
echo 'TAVILY_API_KEY="tvly-your-api-key-here"' >> ~/.openclaw/.env

# 重启 Gateway
openclaw gateway restart
```

**方法二：OpenClaw 配置文件**

编辑 `~/.openclaw/openclaw.json`，添加：

```json
{
  "env": {
    "TAVILY_API_KEY": "tvly-your-api-key-here"
  }
}
```

---

## 🚀 使用方法

### 手动触发

直接对话即可：

```
生成今天的AI日报
```

```
帮我搜一下今天AI圈有什么大事
```

### 自动定时推送

配置每天早上 7 点自动推送：

```bash
openclaw cron add \
  --name "ai-daily-briefing" \
  --cron "0 7 * * *" \
  --tz "Asia/Shanghai" \
  --system-event "[AI日报] 生成今日AI日报" \
  --timeout 300000
```

---

## 📰 日报格式示例

```markdown
# AI新闻早报

2026-03-15

**01 | OpenAI高管辞职引发信任危机**

大佬发声 · [Glass Almanac](链接) 发布于2026-03-14

**速览：** OpenAI硬件高管辞职，抗议五角大楼合作...

**洞察：** 这是AI公司"军火化"后最严重的人才危机...

---

## 今日研判
本周AI圈分化加剧，信任成为新护城河...
```

---

## ⚙️ 可选配置：双引擎搜索

如果你有 SearXNG 实例，可以配置双引擎搜索：

```bash
echo 'SEARXNG_BASE_URL="http://your-searxng-instance.com"' >> ~/.openclaw/.env
```

双引擎模式可以获取更多情报源，但不影响基本使用。

---

## ❓ 常见问题

**Q: 安装后没反应？**

A: 检查 API Key 是否配置正确：
```bash
cat ~/.openclaw/.env | grep TAVILY
```

**Q: 搜索报错？**

A: 检查网络连接，Tavily 需要访问海外 API。

**Q: 想修改推送时间？**

A: 编辑定时任务：
```bash
openclaw cron edit ai-daily-briefing --cron "0 8 * * *"
```

---

## 📚 更多资源

- ClawHub: https://clawhub.ai
- OpenClaw 文档: https://docs.openclaw.ai
- Tavily 官网: https://tavily.com

---

*🦞 祝各位龙虾情报满满，决策高效！*