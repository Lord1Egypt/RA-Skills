---
name: ai-developer-daily
description: AI开发者日报 - 每天整理国际和中国AI/开发者新闻，国际在前、中国在后。支持编号回复展开详情。自动定时推送或用户主动触发。
metadata:
  {
    "openclaw":
      {
        "requires": { "bins": ["python3"] },
      },
  }
---

# AI 开发者日报

自动整理每日 AI 及开发者圈的重点新闻，分为 **国际** 和 **中国** 两个板块。每条带编号和原文链接，用户回复**编号**，展开深度简报。

## 触发方式

- **定时推送**：每天早上 8:00（Asia/Shanghai）通过 cron 触发
- **主动触发**：用户说"AI开发者日报"、"今天AI圈有什么"、"整理开发者日报" 等

## Workflow Routing

| Workflow | 触发条件 |
|----------|---------|
| **Setup** | 首次部署，用户说"设置定时推送"、"部署开发者日报" 等 |
| **FetchNews** | 定时触发 / 用户主动要求整理新闻 |

## Setup Workflow（自动部署）

由 agent 自动检测当前渠道和用户，无需手动填参数。

### 步骤

**1. 检测渠道**

从会话上下文获取当前渠道和用户：

```
channel: qqbot / telegram / discord / feishu ...
to:     用户ID / chatId / channelId
```

**2. 创建 cron**

```bash
openclaw cron add \
  --name "AI开发者日报" \
  --cron "0 8 * * *" \
  --tz "Asia/Shanghai" \
  --session isolated \
  --agent main \
  --message "整理AI开发者日报" \
  --channel <当前渠道> \
  --to <当前用户> \
  --announce \
  --expect-final
```

**3. 确认结果**

```
✅ AI开发者日报已部署！

配置摘要：
- 时间：每天 08:00（北京时间）
- 渠道：<渠道名>
- 投递：当前对话

明天早上 8 点自动推送第一期 👋
```

### 手动创建参考

如果需要在不同渠道部署，手动替换参数：

| 渠道 | `--channel` | `--to` |
|------|-------------|--------|
| QQ 私聊 | `qqbot` | 用户 QQ 号 |
| Telegram | `telegram` | chatId |
| Discord | `discord` | channelId |
| 飞书 | `feishu` | chatId |

```bash
openclaw cron add \
  --name "AI开发者日报" \
  --cron "0 8 * * *" \
  --tz "Asia/Shanghai" \
  --session isolated \
  --agent main \
  --message "整理AI开发者日报" \
  --channel <渠道> \
  --to <目标> \
  --announce \
  --expect-final
```

### 查看状态

```bash
# 所有 cron 任务
openclaw cron list

# 单条详情
openclaw cron show <id>

# 运行记录
openclaw cron runs --id <id>

# 手动立即触发一次
openclaw cron run <id>
```

## FetchNews Workflow（整理日报）

### 1. 新闻采集

搜索以下来源，获取最近 24 小时内的 AI 开发者相关新闻：

**国际源：**
- Hacker News (news.ycombinator.com)
- GitHub Trending (github.com/trending)
- TechCrunch AI
- The Verge AI
- The Register
- GitHub Blog / Changelog
- Python / Node / Rust 等官方发布

**中国源：**
- OSCHINA 开源资讯 (oschina.net/news)
- 36氪 AI 相关
- 机器之心、量子位
- 知乎 AI 热点
- 腾讯云/阿里云开发者社区

### 2. 筛选标准

只关注开发者真正关心的：
- 模型发布（国际+国内）
- 开源框架/工具更新
- 编程语言新版本
- IDE/DevOps 工具发布
- AI 编程相关技术
- 开发者生态大事

过滤掉：纯商业PR、股市行情、不相关的娱乐消费电子新闻。

### 3. 输出格式

每条新闻格式：
```
**N.** [来源] 标题
一句话摘要
🔗 [阅读原文](url)
```

### 4. 展开深度简报

用户回复编号后，执行：
1. 用 web_fetch 抓取原文
2. 提炼核心信息：做了什么、为什么重要、技术细节（如有）
3. 控制在 200-300 字
4. 推送深度简报给用户

## 自定义配置

可在 workspace 的 `TOOLS.md` 中添加偏好的新闻源或排除的站点。
