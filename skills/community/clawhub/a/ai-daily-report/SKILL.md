---
name: ai-daily-report
description: |
  每日自动生成 AI 资讯日报并发送。使用场景：用户说 “生成 AI 日报” 或者系统通过定时任务触发。关键词包括：AI日报、AI资讯、开源AI项目、每日报告。
---

# AI 每日报告 Skill

## 目标
- 自动抓取最近 24 小时内的 AI 相关新闻（约 5 条）
- 拉取 GitHub 上最近 24 小时星增量最高、且星数>10k 的优秀开源 AI 项目（约 3 条）
- 将信息整理成 Markdown 报告
- 用 SVG 生成一页可视化报告页面
- 将 SVG 转为 PNG 并通过 Feishu 把图片发送给用户

## 工作流概述
1. **抓取新闻** – `scripts/fetch_news.py` 使用公开的 RSS/新闻 API，返回 JSON 列表 `[{title, link, source, date}]`。
2. **抓取项目** – `scripts/fetch_top_projects.py` 调用 GitHub Search API（需要 `GITHUB_TOKEN` 环境变量），返回 `[{name, html_url, stars, description}]`。
3. **生成报告** – `scripts/generate_report.py` 接收新闻+项目数据，生成 `report.md` 同时渲染 `report.svg`（基于 Jinja2 SVG 模板 `references/report_template.svg`）。
4. **SVG→PNG** – `scripts/svg_to_png.py` 调用 `rsvg-convert`（或 `magick convert`）把 `report.svg` 转成 `report.png`。
5. **发送** – `scripts/send_report.py` 使用 Feishu doc API (`feishu_doc` action=upload_file) 把 PNG 作为文件上传到当前会话并返回链接。

## 触发方式
- **自然语言触发**（聊天）: 当用户说出以下任意词句时，Skill 自动启动：
  - “生成 AI 日报”
  - “帮我做 AI 资讯报告”
  - “每日 AI 报告”
- **定时触发**（cron）: 可以在 `HEARTBEAT.md` 或系统 cron 中调用 `scripts/run_daily_report.sh`，该脚本内部执行同样的 pipeline 并使用 `feishu_doc` 发送给预设的聊天 ID（可通过环境变量 `FEISHU_CHAT_ID`）

## 资源结构
```
ai-daily-report/
├── SKILL.md                     # 本文件
├── scripts/
│   ├── fetch_news.py
│   ├── fetch_top_projects.py
│   ├── generate_report.py
│   ├── svg_to_png.py
│   ├── send_report.py
│   └── run_daily_report.sh      # 用于 cron 调用（可选）
└── references/
    └── report_template.svg      # Jinja2 SVG 模板
```

## 示例调用（聊天）
> 用户: 生成 AI 日报

OpenClaw 读取 `description`，匹配成功 → 加载 `SKILL.md`，按上述步骤执行。最终在聊天中返回一条包含 PNG 报告的消息，例如：
```
已为您生成今日 AI 报告，请查收附件。
```（图片作为附件发送）

---
## 参考文档
- `references/report_template.svg` – SVG 布局模板，使用 Jinja2 变量 `{{date}}`, `{{news}}`, `{{projects}}`。
- `references/github_search.md` – GitHub Search API 使用说明。
- `references/rss_news.md` – 常用 AI 新闻 RSS 源列表。

---
## 常见问题
- **需要 GitHub Token 吗？** 是的，请在 `~/.openclaw/env` 或系统环境变量中设置 `GITHUB_TOKEN`。
- **每日运行在哪里配置？** 在 `HEARTBEAT.md` 添加行 `run: /home/ft/.openclaw/workspace/skills/ai-daily-report/scripts/run_daily_report.sh`，或者使用系统 `cron`。
- **如果 Feishu 上传失败怎么办？** `send_report.py` 会捕获错误并返回文字提示，建议检查 `FEISHU_CHAT_ID` 是否正确，以及机器人的文件上传权限。
