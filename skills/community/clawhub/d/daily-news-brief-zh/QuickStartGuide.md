# Daily News Brief 快速开始指南

一分钟快速上手新闻聚合 Skill。

## 前置要求

- Node.js 18+ 和 npm
- macOS 或 Linux（推荐），Windows 也可使用

## 快速安装

### 步骤 1：创建配置目录

```bash
mkdir -p ~/.daily-news-brief/logs
```

### 步骤 2：创建配置文件

创建 `~/.daily-news-brief/config.json` 文件：

```json
{
  "newsSources": [
    {
      "name": "36氪",
      "url": "https://36kr.com/feed",
      "type": "rss",
      "category": "科技"
    },
    {
      "name": "虎嗅网",
      "url": "https://www.huxiu.com/rss/0.xml",
      "type": "rss",
      "category": "科技"
    },
    {
      "name": "财新网",
      "url": "https://www.caixin.com/rss/rss_newstech.xml",
      "type": "rss",
      "category": "财经"
    },
    {
      "name": "机器之心",
      "url": "https://www.jiqizhixin.com/rss",
      "type": "rss",
      "category": "AI"
    }
  ],
  "schedule": "0 21 * * *",
  "saveLocalDoc": true,
  "localDocPath": "~/daily-news-brief/每日新闻/",
  "maxNewsPerCategory": 10,
  "maxPerSourcePerCategory": 3,
  "summaryMaxPerCategory": 5,
  "summaryMaxPerSource": 2,
  "push": {
    "enabled": true,
    "channels": ["telegram", "feishu"]
  }
}
```

### 步骤 3：安装依赖

```bash
cd /path/to/daily-news-brief/tools
npm install rss-parser cheerio
```

### 步骤 4：测试运行

```bash
node FetchNews.ts --test
```

如果看到类似输出，说明安装成功：

```text
[2026-03-17T...] 开始抓取新闻...
正在抓取：36氪...
正在抓取：虎嗅网...
共抓取 35 条新闻
新闻分类完成
新闻分组完成
每类限制为 10 条

📰 2026-03-17 新闻简报

【科技】10 条（摘要显示 5 条）
- AI 芯片新进展（来源：36氪）
- 云计算价格战（来源：虎嗅网）
- …

【AI】12 条（摘要显示 5 条）
- 多模态模型发布（来源：机器之心）
- …

本地文档：~/daily-news-brief/每日新闻/2026-03-17.md
```

## 配置 OpenClaw 推送渠道

根据需要启用通道（仅需一次）：

```bash
# Telegram
openclaw channels login --channel telegram

# 飞书
openclaw channels login --channel feishu

# WhatsApp
openclaw channels login --channel whatsapp
```

提示：目标（群/频道/联系人）由 OpenClaw 内部配置管理，本技能仅保存通道列表。
如果 OpenClaw 未设置默认目标，可在 `~/.daily-news-brief/config.json` 里配置 `push.targets`。

## 配置定时任务

### 推荐：OpenClaw cron（统一调度）

```bash
openclaw cron add "0 21 * * *" "运行 Daily News Brief：node tools/FetchNews.ts --push"
```

### macOS / Linux

编辑 crontab：

```bash
crontab -e
```

添加以下内容（每天晚上 9 点执行）：

```cron
0 21 * * * cd /path/to/daily-news-brief/tools && node FetchNews.ts >> ~/.daily-news-brief/logs/cron.log 2>&1
```

保存后，定时任务就会自动运行。

### Windows

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器：每天 21:00
4. 操作：启动程序
   - 程序：`C:\Program Files\nodejs\node.exe`
   - 参数：`C:\path\to\daily-news-brief\tools\FetchNews.ts`
   - 起始于：`C:\path\to\daily-news-brief\tools`

## 日常使用

### 手动获取新闻

```bash
# 在项目根目录执行
# 获取当天新闻
node tools/FetchNews.ts

# 获取指定分类
node tools/FetchNews.ts --category AI

# 测试模式（少量新闻）
node tools/FetchNews.ts --test
```

### 查看本地文档

```bash
# 查看今日新闻
cat ~/daily-news-brief/每日新闻/$(date +%Y-%m-%d).md

# 列出所有历史文档
ls -la ~/daily-news-brief/每日新闻/
```

### 在 AI 聊天中使用

```text
你："整理今天的新闻"
AI：运行 FetchNews workflow
输出：今日新闻汇总

你："只看 AI 新闻"
AI：运行 FetchNews workflow --category AI
输出：AI 领域新闻
```

## 修改配置

### CLI 快速修改（可选）

```bash
# 快速修改定时表达式
node tools/Configure.ts --schedule "0 8 * * *"

# 添加新闻源
node tools/Configure.ts --add-source "新智元,https://xinzhiyuan.ai/feed,rss,AI"

# 删除新闻源
node tools/Configure.ts --remove-source "新智元"

# 修改每类新闻数
node tools/Configure.ts --max-news 20

# 修改每类每来源上限
node tools/Configure.ts --max-per-source 3

# 修改摘要每类条数
node tools/Configure.ts --summary-max 5

# 修改摘要每类每来源上限
node tools/Configure.ts --summary-max-per-source 2

# 设置推送渠道
node tools/Configure.ts --channels "telegram,feishu"

# 开启/关闭推送
node tools/Configure.ts --push on
node tools/Configure.ts --push off

# 恢复默认配置
node tools/Configure.ts --reset
```

### 修改定时时间

编辑 `~/.daily-news-brief/config.json`，修改 `schedule` 字段：

```json
{
  "schedule": "0 8 * * *"  // 改为早上 8 点
}
```

然后更新 cron 任务。

### 添加/删除新闻源

编辑 `~/.daily-news-brief/config.json`，在 `newsSources` 数组中添加或删除源：

```json
{
  "newsSources": [
    {
      "name": "新智元",
      "url": "https://xinzhiyuan.ai/feed",
      "type": "rss",
      "category": "AI"
    }
  ]
}
```

### 修改每类新闻数量

编辑 `~/.daily-news-brief/config.json`，修改 `maxNewsPerCategory`：

```json
{
  "maxNewsPerCategory": 20
}
```

### 删除本地文档

```bash
# 删除所有历史文档
rm ~/daily-news-brief/每日新闻/*

# 禁用本地文档保存
# 编辑 config.json，设置 saveLocalDoc: false
```

## 常见问题

**Q: 新闻抓取失败？**
A: 检查网络连接，查看日志文件 `~/.daily-news-brief/logs/fetch-news.log`

**Q: 定时任务没执行？**
A: 检查 cron 日志：`tail -f ~/.daily-news-brief/logs/cron.log`

**Q: 如何查看可用新闻源？**
A: 查看 SKILL.md 中的"新闻源说明"章节

**Q: 如何修改新闻分类规则？**
A: 编辑 `tools/NewsClassifier.ts` 中的 `categoryKeywords` 对象

**Q: 如何停止定时任务？**
A: 删除 cron 任务：`crontab -e`，删除相关行

## 卸载

```bash
# 停止定时任务
crontab -e  # 删除相关行

# 删除配置和数据
rm -rf ~/.daily-news-brief
rm -rf ~/daily-news-brief

# 可选：删除 Skill
rm -rf /path/to/daily-news-brief
```

## 进阶功能

### 自定义新闻源

除了 RSS，还可以使用网页抓取：

```json
{
  "name": "某个新闻网站",
  "url": "https://example.com/news",
  "type": "web",
  "category": "科技"
}
```

注意：网页抓取需要根据不同网站的 DOM 结构调整代码。

### 自定义分类

编辑 `tools/NewsClassifier.ts`，添加自定义分类和关键词：

```typescript
const categoryKeywords = {
  '我的分类': ['关键词1', '关键词2'],
  // ...
};
```

### 生成统计报告

```bash
# 统计各分类新闻数量
grep "## " ~/daily-news-brief/每日新闻/*.md | cut -d ' ' -f2 | sort | uniq -c
```

## 获取帮助

- 查看 SKILL.md 了解完整功能
- 查看 workflows/ 目录了解详细流程
- 查看 tools/ 目录了解工具实现
- 查看日志文件排查问题

## 更新日志

- v1.0.0 (2026-03-17): 初始版本
  - 支持多源新闻抓取
  - 支持自动分类
  - 支持定时任务
  - 支持本地文档保存
