# Setup Workflow

新闻聚合 Skill 的首次安装和配置流程。

## 工作流程

### 步骤 1：检查环境和依赖

```bash
# 检查 Node.js 是否安装
node --version

# 检查 npm 是否安装
npm --version

# 检查是否有抓取工具（playwright 或 curl）
which playwright
which curl
```

**如果未安装 Node.js**：
- macOS：`brew install node`
- Ubuntu：`sudo apt install nodejs npm`

### 步骤 2：选择新闻源

向用户展示推荐的免费新闻源列表：

```text
请选择要使用的新闻源（可多选）：

【科技类】
[ ] 36氪 (36kr.com) - RSS
[ ] 虎嗅网 (huxiu.com) - RSS
[ ] 澎湃科技 (thepaper.cn/tech) - RSS

【财经类】
[ ] 财新网 (caixin.com) - RSS
[ ] 澎湃财经 (thepaper.cn/finance) - RSS

【AI 类】
[ ] 机器之心 (jiqizhixin.com) - RSS
[ ] 新智元 (xinzhiyuan.ai) - RSS

【智能体类】
[ ] AI 研习社 - RSS
[ ] InfoQ AI 专栏 - RSS

输入选择的序号（用逗号分隔），例如：1,2,5,6,7,8
```

**默认选择**：所有源

### 步骤 3：选择推送渠道（OpenClaw）

由 OpenClaw 智能体询问用户希望的推送渠道，并引导完成通道登录：

```text
请选择要启用的推送渠道（可多选）：

【常用】
[ ] Telegram
[ ] 飞书（Feishu）
[ ] WhatsApp

【其他】
[ ] Slack
[ ] Discord

提示：OpenClaw 会使用内部配置的默认目标发送，无需在本技能配置 target。
```

**建议动作（按用户选择执行）**：
```bash
# Telegram
openclaw channels login --channel telegram

# 飞书
openclaw channels login --channel feishu

# WhatsApp
openclaw channels login --channel whatsapp
```

由 OpenClaw 智能体记录用户选择并写入 `~/.daily-news-brief/config.json` 的 `push.channels` 与 `schedule`。

### 步骤 4：配置推送时间

询问用户定时任务时间：

```text
默认时间：每天晚上 21:00

要修改定时时间吗？(Y/n)
如果输入 Y，请输入时间（格式：HH:MM，例如：08:00）
```

**默认时间**：21:00

### 步骤 5：配置本地文档保存

询问用户是否保留本地文档：

```text
是否保存本地 Markdown 文档？(Y/n)
默认：Y

如果保存，默认路径为：~/daily-news-brief/每日新闻/
要修改保存路径吗？(Y/n)
```

**默认**：保存到 `~/daily-news-brief/每日新闻/`

### 步骤 6：创建配置文件

在 `~/.daily-news-brief/` 目录下创建配置文件 `config.json`：

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

### 步骤 7：创建定时任务

**推荐：使用 OpenClaw cron（统一调度与日志）**

```bash
openclaw cron add "0 21 * * *" "运行 Daily News Brief：node tools/FetchNews.ts --push"
```

**备选：macOS/Linux（使用系统 cron）：**

```bash
# 编辑 crontab
crontab -e

# 添加定时任务
0 21 * * * /path/to/node /path/to/daily-news-brief/tools/FetchNews.ts >> ~/.daily-news-brief/logs/cron.log 2>&1
```

**Windows（使用任务计划程序）：**

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器：每天 21:00
4. 操作：运行脚本 `node C:\path\to\daily-news-brief\tools\FetchNews.ts`

### 步骤 8：测试新闻抓取

运行一次新闻抓取，确保配置正确：

```bash
node tools/FetchNews.ts --test
```

**检查项**：
- [ ] 能够成功抓取新闻
- [ ] 新闻分类正确
- [ ] 生成的 MD 文档格式正确
- [ ] 聊天窗口能收到新闻

### 步骤 9：完成确认

输出确认信息：

```text
✅ Daily News Brief 配置完成！

配置摘要：
- 新闻源：36氪、虎嗅网、财新网、机器之心等
- 定时时间：每天 21:00
- 本地文档：保存到 ~/daily-news-brief/每日新闻/

接下来：
- 定时任务将自动运行
- 可随时手动触发：'整理今天的新闻'
- 修改配置：运行 Configure workflow

首次运行将于今天晚上 21:00 执行。
```

## 常见问题

**Q1: RSS 源无法访问？**
A: 某些网站可能屏蔽抓取，尝试使用网页抓取模式或更换新闻源。

**Q2: 新闻抓取速度慢？**
A: 可以减少新闻源数量，或者调整 `maxNewsPerCategory` 参数。

**Q3: 定时任务没有执行？**
A: 检查：
- cron 日志：`tail -f ~/.daily-news-brief/logs/cron.log`
- 权限问题：确保脚本有执行权限
- 路径问题：使用绝对路径

**Q4: 如何停止定时任务？**
A: 删除 cron 任务或禁用任务计划程序中的任务。

## 后续操作

- 运行 `FetchNews` workflow 手动获取新闻
- 运行 `Configure` workflow 修改配置
- 查看 `QuickStartGuide.md` 了解详细使用说明
