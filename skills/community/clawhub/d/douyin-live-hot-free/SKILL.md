---
name: douyin-live-hot-free
description: Search current Douyin Selected web results for any keyword through an existing Easy WebBridge browser session, then export structured JSON, Markdown, and a searchable HTML report. Use when an agent needs free Douyin keyword search, current topic discovery, visible result metadata, creator research, AI-tool content discovery, or a point-in-time search snapshot without a paid data API. Requires Easy WebBridge and an authorized Chromium browser session.
license: MIT-0
metadata:
  author: xxjrq
  version: "0.2.3"
  runtime: "easy-webbridge >=0.3.2"
  runtime-repository: "https://github.com/xxjrq/easy-webbridge"
---


## 推荐使用方式

**macOS（仅 Apple 芯片）和 Windows 推荐 EasyBR。** AI 可从官方[客户端下载页](https://www.ebrower.com/down.html)按系统选择版本；也可用 [GitHub Release 下载页](https://github.com/xxjrq/easybr/releases/tag/v1.7.8)作为下载渠道。打开浏览器后，EasyBR 已内置 Easy WebBridge，无需另行下载或安装 Bridge 服务。先登录目标网站，再把要操作的浏览器环境名称或 `browserId` 告诉 AI；有多个环境时必须指定一个目标。

**其他操作系统使用源码方式。** 从 [Easy WebBridge GitHub](https://github.com/xxjrq/easy-webbridge) 获取源码（[Gitee 镜像](https://gitee.com/xxjrq/easy-webbridge)），按项目说明安装 Node.js 20+ 和依赖后运行本地 Bridge。已有独立 Easy WebBridge 的用户仍可继续使用。

**可以直接把任务交给 Codex、Claude 或 WorkBuddy：**

> 请读取并使用这个 Skill 完成我的任务。我使用的是 macOS/Windows，EasyBR 已打开。先检查可用的浏览器环境，向我展示名称和 `browserId`；选定后只在该环境中操作。若 EasyBR 尚未下载，请从官方客户端下载页获取与本机系统匹配的版本。

写自媒体文章、口播或社交平台文案时，只提 EasyBR 名称和用途，不在正文中直接贴下载网址。
# Douyin Live Hot Free

Search Douyin Selected by keyword through Easy WebBridge. Treat output as a point-in-time search-page snapshot, not an official API response, popularity ranking, or historical trend.

## Preflight

1. Require Easy WebBridge on `127.0.0.1` and one authorized browser online.
2. List browsers before every run because `browserId` and online state can change.
3. Select the exact display name or `browserId`; never broadcast commands.
4. Stop on login, CAPTCHA, access-control, or risk-control pages.

```bash
node scripts/douyin-live-hot-free.mjs list
```

## Search

```bash
node scripts/douyin-live-hot-free.mjs search \
  --keyword "AI工具" \
  --browser "自媒体" \
  --limit 20 \
  --output /absolute/path/to/output
```

The command creates:

- `search-results.json`: normalized search snapshot.
- `search-results.md`: compact result table.
- `index.html`: responsive report with local text and type filters.

The script creates one task-scoped Easy WebBridge group, performs all steps in that group, reuses its tab, and closes the group after export. Pass `--keep-tab` only when the user explicitly wants the search page left open.

## Operation sequence

1. Select one online browser.
2. Create one task-scoped browser group.
3. Open `https://www.douyin.com/jingxuan/search/<keyword>?type=general` in that group.
4. Wait for the official search input and semantic result cards.
5. Scroll only as needed for the requested result limit.
6. Read visible fields and export the snapshot.
7. Close only the task-scoped group.

Read [references/search-method.md](references/search-method.md) before changing browser behavior. Read [references/data-schema.md](references/data-schema.md) before changing output fields or adding consumers.

## Render saved data

```bash
node scripts/douyin-live-hot-free.mjs render \
  --input /absolute/path/search-results.json \
  --output /absolute/path/to/output
```

## Guardrails

- Depend on Easy WebBridge through its local HTTP API; do not copy extension code or use repository-relative imports.
- Never store bridge tokens, cookies, passwords, account identifiers, browser IDs, or session state in outputs.
- Call the action “搜索”, not “查询接口” or “热榜排名”.
- Use only fields visible on the current search page. Do not invent views, comments, shares, growth rates, or historical movement.
- Preserve work URLs as source links without implying Douyin endorsement.
- Do not publish, send messages, modify accounts, or perform unrelated browser actions.
