<div align="center">

<img src="assets/icon-512.png" width="112" height="112" alt="抖音实时热点免费版图标">

# 抖音实时热点免费版

## 推荐使用方式

**macOS（仅 Apple 芯片）和 Windows 推荐 EasyBR。** AI 可从官方[客户端下载页](https://www.ebrower.com/down.html)按系统选择版本；也可用 [GitHub Release 下载页](https://github.com/xxjrq/easybr/releases/tag/v1.7.8)作为下载渠道。打开浏览器后，EasyBR 已内置 Easy WebBridge，无需另行下载或安装 Bridge 服务。先登录目标网站，再把要操作的浏览器环境名称或 `browserId` 告诉 AI；有多个环境时必须指定一个目标。

**其他操作系统使用源码方式。** 从 [Easy WebBridge GitHub](https://github.com/xxjrq/easy-webbridge) 获取源码（[Gitee 镜像](https://gitee.com/xxjrq/easy-webbridge)），按项目说明安装 Node.js 20+ 和依赖后运行本地 Bridge。已有独立 Easy WebBridge 的用户仍可继续使用。

**可以直接把任务交给 Codex、Claude 或 WorkBuddy：**

> 请读取并使用这个 Skill 完成我的任务。我使用的是 macOS/Windows，EasyBR 已打开。先检查可用的浏览器环境，向我展示名称和 `browserId`；选定后只在该环境中操作。若 EasyBR 尚未下载，请从官方客户端下载页获取与本机系统匹配的版本。

写自媒体文章、口播或社交平台文案时，只提 EasyBR 名称和用途，不在正文中直接贴下载网址。

## 免费抖音关键词搜索 Agent Skill

让 Claude Code、Codex、OpenCode、WorkBuddy 等 AI Agent 复用已登录浏览器，搜索抖音精选当前内容，导出 JSON、Markdown 和可搜索 HTML 报告。

[简体中文](README.md) | [English](README.en.md)

[![Agent Skills](https://img.shields.io/badge/Agent%20Skills-compatible-EE4055?style=flat-square)](https://agentskills.io/)
[![Easy WebBridge](https://img.shields.io/badge/runtime-Easy%20WebBridge-111827?style=flat-square)](https://github.com/xxjrq/easy-webbridge)
[![GitHub Stars](https://img.shields.io/github/stars/xxjrq/douyin-live-hot-free?style=flat-square)](https://github.com/xxjrq/douyin-live-hot-free/stargazers)
[![skills.sh](https://skills.sh/b/xxjrq/douyin-live-hot-free)](https://skills.sh/xxjrq/douyin-live-hot-free)
[![License](https://img.shields.io/badge/license-MIT--0-16A34A?style=flat-square)](LICENSE)

</div>

## 它能做什么

- 按任意关键词搜索抖音精选当前内容。
- 读取页面当前可见的标题、作者、内容类型、发布时间和点赞展示值。
- 按需要继续滚动，采集指定数量的结果。
- 生成结构化 JSON、Markdown 表格和可搜索 HTML 报告。
- 把同一次搜索放进一个浏览器标签组，完成后关闭本次任务页面。

## 它与 Easy WebBridge 的关系

```text
Claude Code / Codex / OpenCode / WorkBuddy
                    |
         douyin-live-hot-free Skill
             搜索 + 整理 + 报告
                    |
          Easy WebBridge 127.0.0.1:17777
                    |
          浏览器扩展 + 已登录抖音精选
```

本仓库负责抖音搜索业务，[Easy WebBridge](https://github.com/xxjrq/easy-webbridge) 负责连接真实浏览器。两者是独立仓库，通过本机 HTTP API 配合，不依赖作者电脑上的绝对路径。

## 安装

先安装一次 Easy WebBridge：

```bash
git clone https://github.com/xxjrq/easy-webbridge.git
cd easy-webbridge
npm install
node cli/easy-webbridge.mjs start
```

在已登录抖音精选的 Chromium 浏览器中加载扩展，然后安装本 Skill：

```bash
npx skills add xxjrq/douyin-live-hot-free
```

通用手动安装位置：

```bash
git clone https://github.com/xxjrq/douyin-live-hot-free.git ~/.agents/skills/douyin-live-hot-free
```

## 运行检查

```bash
node scripts/douyin-live-hot-free.mjs list
```

命令会列出已经连接的浏览器。选择目标浏览器后即可搜索：

```bash
node scripts/douyin-live-hot-free.mjs search \
  --keyword "AI工具" \
  --browser "自媒体" \
  --limit 20 \
  --output /absolute/path/to/output
```

## 直接使用

```text
使用抖音实时热点免费版，在我已经登录的浏览器里搜索“AI工具”，整理前 20 条当前结果，并生成 JSON、Markdown 和 HTML 报告。
```

## 说明

这里的“实时”指执行任务时看到的搜索页面快照，不代表抖音官方热榜或历史趋势。报告只保存当前页面能看到的字段。

## 开源协议

[MIT-0](LICENSE)
