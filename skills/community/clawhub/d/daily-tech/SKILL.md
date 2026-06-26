---
name: daily-tech
description: 每日科技/AI/大模型热榜推送。当用户说"今日科技"、"每日AI"、"科技日报"、"大模型动态"、"AI资讯"、"开启科技推送"时触发。主打AI、大模型、OpenClaw、机器人、GitHubTrending等硬科技，附国际市场动态，来源覆盖中英文。
---

# daily-tech

每日科技热榜推送——AI、大模型、OpenClaw、硬科技领域每日精华。

## 两种模式

### 手动查询

触发词：`今日科技` / `每日AI` / `科技日报`

### 定时推送

触发词：`开启科技推送`

每天07:00（北京）自动推送到飞书。

## 数据来源

### 板块一：AI与大模型（核心）

| 平台 | 路径 | 语言 | 说明 |
|---|---|---|---|
| 掘金·AI本周最热 | `/n/rYqoXz8dOD` | 中文 | AI工具、OpenClaw、GitHub开源 |
| 量子位·每日最新 | `/n/MZd7azPorO` | 中文 | 大模型、机器人、AI前沿 |
| 产品经理AI学习库 | `/n/DOvnyGpoEB` | 中文 | AI行业洞察、论文解读 |
| MIT Technology Review | `/n/7GdabqLeQy` | 英文 | AI政策、深度技术报道 |

### 板块二：科技综合

| 平台 | 路径 | 语言 | 说明 |
|---|---|---|---|
| 36氪·24小时热榜 | `/n/Q1Vd5Ko85R` | 中文 | 科技与商业交叉 |
| 知乎日报 | `/n/KMZd7VOvrO` | 中文 | 深度技术讨论 |
| 哔哩哔哩全站日榜 | `/n/74KvxwokxM` | 中文 | 视频技术内容 |
| 微信公众号24h热文 | `/n/WnBe01o371` | 中文 | 微信科技大号精选 |

### 板块三：国际市场（英文）

| 平台 | 语言 | 说明 |
|---|---|---|
| The Verge | 英文 | 科技文化、大公司动态、深度评论 |
| Ars Technica | 英文 | 深度技术分析、安全、科学 |
| TechCrunch | 英文 | 创业、VC、AI产品发布 |
| MIT Tech Review | 英文 | AI研究、政策、深度报告 |

### 板块四：OpenClaw生态

| 平台 | 说明 |
|---|---|
| OpenClaw GitHub | 最新版本发布、功能更新 |
| OpenClaw Skills (clawhub) | 新上线skill、社区动态 |
| 掘金AI（OpenClaw相关） | OpenClaw实操经验、技巧 |

## 获取方式

```javascript
// 掘金AI
web_fetch("https://tophub.today/n/rYqoXz8dOD", { maxChars: 3000 })

// 量子位
web_fetch("https://tophub.today/n/MZd7azPorO", { maxChars: 3000 })

// 产品经理AI
web_fetch("https://tophub.today/n/DOvnyGpoEB", { maxChars: 3000 })

// MIT Tech Review
web_fetch("https://tophub.today/n/7GdabqLeQy", { maxChars: 3000 })

// 36氪
web_fetch("https://tophub.today/n/Q1Vd5Ko85R", { maxChars: 3000 })

// 知乎日报
web_fetch("https://tophub.today/n/KMZd7VOvrO", { maxChars: 3000 })

// 英文平台用web_fetch直接抓RSS
web_fetch("https://www.theverge.com/rss/index.xml", { maxChars: 3000 })
web_fetch("https://techcrunch.com/feed/", { maxChars: 3000 })
```

## 筛选标准

### 保留
- AI、大模型、LLM相关重大进展（产品、论文、开源）
- OpenClaw更新、插件、技巧
- 机器人、自动驾驶、硬件突破
- GitHub开源项目重大更新
- 科技公司产品发布、财报
- AI安全、政策、监管动态
- 英文优质内容的核心摘要

### 排除
- 纯娱乐/游戏内容
- 广告软文
- 与AI/科技无关的民生新闻
- 情绪化标题

## 输出格式

```
🤖 科技日报 | X月X日

【AI与大模型】
1. [标题] — [核心信息，1-2句]
...

【OpenClaw生态】
1. [标题] — [核心信息]
...

【硬科技/机器人】
1. [标题] — [核心信息]
...

【国际市场】
1. [The Verge/Ars/TC - 标题]
...

#来源：掘金AI · 量子位 · 36氪 · MIT · The Verge · TechCrunch
```

总条数5-10条，每条简洁有信息量。分割线用"======"代替"---"。

## 定时推送设置

当用户说"开启科技推送"时，执行：

```bash
openclaw cron add \
  --name "每日科技推送" \
  --agent main \
  --message "今日科技" \
  --cron "0 7 * * *" \
  --tz "Asia/Shanghai" \
  --channel feishu
```
