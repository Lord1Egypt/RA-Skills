---
name: lightpanda
description: 从零构建的轻量级无头浏览器，专为 AI 智能体和自动化设计，比 Headless Chrome 快 9 倍、内存占用低 16 倍，兼容 CDP 和 Playwright/Puppeteer，内置 MCP 服务器
version: 0.1.1
metadata:
  openclaw:
    requires:
      bins:
        - node
        - npx
    emoji: 🐼
    homepage: https://lightpanda.io
---

# Lightpanda — 为 AI 智能体设计的极速无头浏览器

Lightpanda 是用 Zig 从零构建的新一代无头浏览器，不基于 Chromium 或 WebKit，专为 AI 智能体和大规模自动化设计。在处理 100 个真实网页时，执行时间仅需 5 秒（vs 46 秒），峰值内存仅 123MB（vs 2GB）。完整支持 Chrome DevTools Protocol（CDP），现有 Puppeteer/Playwright 脚本无需改动即可切换使用，同时内置 MCP 服务器让 AI 助手直接控制浏览器。

## 核心使用场景

- **大规模网页爬取**：替换 Headless Chrome 降低云端成本，处理更多并发请求
- **AI 智能体浏览**：通过 MCP 服务器让 Claude/Cursor 等 AI 直接控制浏览器访问网页
- **Puppeteer/Playwright 加速**：无需修改代码，将 `browserWSEndpoint` 指向 Lightpanda
- **HTML/Markdown 转储**：快速将网页内容转为 Markdown 供 AI 分析
- **服务器端自动化**：内存极低，适合在资源受限的容器或 VPS 中运行

## AI 辅助使用流程

1. **安装二进制** — AI 下载对应平台的预编译二进制（Linux/macOS/Docker）
2. **启动 CDP 服务器** — AI 执行 `./lightpanda serve` 在 9222 端口启动 CDP 服务器
3. **连接 Puppeteer/Playwright** — AI 将现有脚本的 `browserWSEndpoint` 指向 Lightpanda
4. **或配置 MCP 服务器** — AI 将 Lightpanda 配置为 Claude Code 的 MCP 工具
5. **执行自动化操作** — AI 通过 CDP 或 MCP 控制浏览器，导航、提取、交互
6. **转储页面内容** — AI 用 `lightpanda fetch --dump markdown` 将页面转为 AI 可读格式

## 关键章节导航

- [安装指南](guides/01-installation.md) — 二进制下载、Docker 安装、从源码构建
- [快速开始](guides/02-quickstart.md) — CDP 服务器、Puppeteer 集成、MCP 配置、CLI 转储
- [高级用法](guides/03-advanced-usage.md) — Playwright 集成、代理、遥测配置、AI 场景
- [故障排查](troubleshooting.md) — 兼容性、Beta 限制、网络问题

## AI 助手能力

使用本技能时，AI 可以：

- ✅ 下载并安装 Lightpanda 二进制（Linux/macOS）
- ✅ 启动 CDP 服务器（`./lightpanda serve --host 127.0.0.1 --port 9222`）
- ✅ 将 Puppeteer 脚本连接到 Lightpanda（修改 `browserWSEndpoint`）
- ✅ 配置 Lightpanda 作为 Claude Code 的 MCP 工具
- ✅ 使用 `lightpanda fetch --dump markdown` 将网页转为 Markdown
- ✅ 使用 Docker 镜像快速部署（`docker run lightpanda/browser:nightly`）
- ✅ 配置代理和遥测选项

## 核心功能

- ✅ **极速渲染** — 比 Headless Chrome 快 9 倍，100 页仅需 5 秒
- ✅ **极低内存** — 峰值 123MB（vs Chrome 2GB），降低 16 倍
- ✅ **CDP 兼容** — 完整支持 Chrome DevTools Protocol，现有脚本无需改动
- ✅ **Puppeteer/Playwright 集成** — 通过 `browserWSEndpoint` 零成本迁移
- ✅ **MCP 服务器** — 让 AI 工具直接控制浏览器，支持 MCP JSON-RPC 2.0
- ✅ **HTML/Markdown 转储** — 直接将网页内容转为 Markdown（AI 友好格式）
- ✅ **robots.txt 遵守** — `--obey-robots` 选项，合规爬取
- ✅ **代理支持** — 内置代理配置
- ✅ **网络拦截** — 可拦截和过滤网络请求
- ✅ **Docker 镜像** — 官方多架构镜像（amd64/arm64）
- ✅ **Cookie 管理** — 完整 Cookie 支持
- ✅ **JavaScript 执行** — v8 引擎，支持 Ajax/XHR/Fetch API

## 快速示例

```bash
# 下载安装（macOS）
curl -L -o lightpanda https://github.com/lightpanda-io/browser/releases/download/nightly/lightpanda-aarch64-macos
chmod a+x ./lightpanda

# 转储网页为 Markdown
./lightpanda fetch --dump markdown https://example.com

# 启动 CDP 服务器
./lightpanda serve --host 127.0.0.1 --port 9222

# Docker 运行
docker run -d --name lightpanda -p 127.0.0.1:9222:9222 lightpanda/browser:nightly
```

```json
// MCP 配置（添加到 AI 工具 MCP 配置文件）
{
  "mcpServers": {
    "lightpanda": {
      "command": "/path/to/lightpanda",
      "args": ["mcp"]
    }
  }
}
```

## 安装要求

| 依赖 | 版本 |
|------|------|
| Linux | x86_64 或 aarch64（glibc 发行版） |
| macOS | aarch64 或 x86_64 |
| Windows | 通过 WSL2 使用 Linux 二进制 |
| Docker | 任意版本（推荐生产使用） |

**注意：** Lightpanda 当前为 Beta 阶段，部分 Web API 尚未完全实现。不适用于依赖 WebGL/WebRTC 等高级特性的场景。

## 项目链接

- GitHub：https://github.com/lightpanda-io/browser
- 文档：https://lightpanda.io/docs
- MCP 文档：https://lightpanda.io/docs/open-source/guides/mcp-server
- Docker Hub：https://hub.docker.com/r/lightpanda/browser
- Discord：https://discord.gg/K63XeymfB5
