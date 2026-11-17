---
name: favicondl
displayName: 任意网站 Favicon 下载工具 · FaviconDL
description: "通过 HTTPS API 或零依赖 CLI 下载任意网站的可用 favicon，支持尺寸偏好、图片重定向、JSON 元数据和 Windows/Linux/macOS。"
version: 2.0.0
---

# FaviconDL

FaviconDL 提供一套稳定的 REST API、公开 OpenAPI 规范、`llms.txt`，以及两个零依赖的 CLI 脚本（PowerShell + Bash），帮助 agent 在不写爬虫代码的情况下，从任意域 / URL 获取可用的 favicon 图标。

> 公开接口：<https://favicondl.com> · OpenAPI 规范：<https://favicondl.com/openapi.yaml> · llms.txt：<https://favicondl.com/llms.txt> · 源码仓库：<https://github.com/sweesama/favicondl.com>

---

> ## 📌 这是 OpenClaw 分发版（v2.0.0） / Distribution note
>
> 本文件是 **OpenClaw / ClawHub skill catalog 分发版**，通过 `openclaw skills install favicondl` 安装到本机 agent 时使用。
>
> **Canonical Agent API 文档**（所有 agent 默认应该优先看的那一份）位于 GitHub：
> <https://github.com/sweesama/favicondl.com/blob/main/SKILL.md>
>
> 两版一致的部分：
> - 主接口：<https://favicondl.com/api/extract>
> - JSON 模式：<https://favicondl.com/api/extract?url=github.com&size=128&format=json>
> - 不宣传公网 MCP endpoint（`https://favicondl.com/mcp` 不存在）
> - 不假定所有图像都是 PNG（SVG / PNG / ICO / WebP 都可能）
> - 不建议 agent 失败时切换到 Google Favicon 之类的第三方方案
>
> 本分发版额外包含：
> - ClawHub / OpenClaw 安装命令（`openclaw skills install favicondl`）
> - 本地 stdio MCP 适配器的可选说明（来自 GitHub `mcp/`，明确为**本机进程**）
> - OpenClaw 水产市场（openclawmp）资产链接
> - 旧端点 `/api/favicon` 的兼容说明（旧集成仍可用）
>
> 任何 agent 默认应该**优先读 GitHub canonical 版**，本版只在安装到 OpenClaw / ClawHub 时随包附带，主要目的是补安装和兼容元数据。两版在事实描述上不应矛盾。

---

## 这个 skill 能做什么 / What it supports

- 偏好尺寸 16~512 像素；服务端会自动 clamp，超出范围会取最接近的合法值
- 多级图标发现：HTML `<link>` → SVG → Apple Touch Icon → Web Manifest → Android assets → 安全兜底
- 默认返回 `HTTP 302`，跟随重定向即可下载图像
- 加 `format=json` 可拿到元数据 JSON：`ok`、`domain`、`size`、`iconUrl`、`proxyUrl`、`source`
- 通过受保护的 Cloudflare Worker 做图片代理（`proxyUrl`），绕过 CORS / 反盗链
- 拒绝非 HTTPS 协议、私网地址、超大代理响应、非图像响应
- 任何能做 `HTTPS GET` 的 agent / 脚本 / 浏览器都能调用

返回的图像格式由目标网站决定，**不要假定都是 PNG**：SVG、PNG、ICO、WebP 都可能。脚本默认把保存文件的扩展名记作 `.img`，避免伪造。

---

## 安装 CLI / Install the CLI wrappers

> 通过 raw.githubusercontent.com 直接下载到本地（**公开地址可直接 HTTP 200 拉取**）：

### Windows PowerShell

```powershell
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/sweesama/favicondl.com/main/favicondl.ps1" -OutFile "$env:USERPROFILE\favicondl.ps1"
```

### Linux / macOS（Bash）

```bash
curl -fsSL -o ~/favicondl.sh "https://raw.githubusercontent.com/sweesama/favicondl.com/main/favicondl.sh"
chmod +x ~/favicondl.sh
```

脚本只依赖 PowerShell 自身或系统 `curl`，无需 API Key、无需包管理器。

---

## CLI 用法 / CLI usage

### PowerShell（支持单域 / 多域）

```powershell
.\favicondl.ps1 -Domain "github.com"
.\favicondl.ps1 -Domain "github.com" -Size 256
.\favicondl.ps1 -Domain "github.com" -Size 128 -Output "C:\icons\github.img"

# 一次下载多个域名，-Output 指向目录即可
.\favicondl.ps1 -Domain "github.com", "openai.com", "anthropic.com" -Output "C:\icons"
```

### Bash

```bash
./favicondl.sh github.com
./favicondl.sh github.com 256
./favicondl.sh https://github.com/docs 128 ./icons/github.img
```

输出文件后缀是 `.img`，这是**故意的**——目标网站控制实际图像格式。下载时不要硬改后缀。

---

## REST API

> 主接口：`GET https://favicondl.com/api/extract`

### 下载模式（默认 302）

```text
GET https://favicondl.com/api/extract?url=github.com&size=128
```

默认响应 `302 Found`，跟随重定向即可下载图像。

```bash
curl -fL -o github-favicon.img "https://favicondl.com/api/extract?url=github.com&size=128"
```

### JSON 元数据模式

```text
GET https://favicondl.com/api/extract?url=github.com&size=128&format=json
```

JSON 响应字段：`ok`、`domain`、`size`、`iconUrl`、`proxyUrl`、`source`。

```json
{
  "ok": true,
  "domain": "github.com",
  "size": 128,
  "iconUrl": "https://github.com/favicon.ico",
  "proxyUrl": "https://favicondl.com/api/proxy?url=...",
  "source": "html"
}
```

`source` 取值：`direct`（目标站直接提供）/ `html`（解析 HTML `<link>` 标签得到）/ `google_s2`（站内多级发现全部失败后，服务端最后一次兜底）。

> ⚠️ 关于 `google_s2`：这是**站内实现细节**，仅用于让 agent 排查"为什么这个站这么久才拿到图"。**不要**把 `google_s2` 当成"Agent 应当主动切换到 Google Favicon API" 的信号——本服务其他多级发现失败时已经自动走一次，Agent 失败时应按"错误处理"段退避重试，不要再外跳第三方。

### 参数

| 参数 | 必填 | 默认 | 说明 |
|---|---:|---:|---|
| `url` | ✅ | — | 域名或完整 HTTP(S) URL，例如 `github.com` 或 `https://github.com/docs` |
| `size` | ❌ | `128` | 偏好尺寸，自动 clamp 到 `16`-`512` |
| `format` | ❌ | `redirect` | 用 `json` 取元数据；不传或 `redirect` 都返回 302 图像 |

---

## 可选的本地 MCP 适配器 / Optional local MCP adapter

> ⚠️ 这是高级用户可选项 —— **仅作为本机 MCP 进程**，不是公网远程 MCP。

favicondl 仓库 `mcp/` 目录下提供了一份 **stdio MCP server** 实现。它是**用户本机运行的本地 MCP**：在用户电脑上启动一个 Node 进程，进程通过 stdio 暴露 `extract_favicon` 工具给支持 MCP 的客户端（Claude Desktop / Cursor / Windsurf / OpenClaw MCP 客户端 等）。它**不是** `https://favicondl.com/mcp` 这种远程端点，没有公网 MCP endpoint，也没有"远程托管的 MCP 服务"。

工具签名：

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `url` | string | ✅ | 域名或完整 HTTP(S) URL |
| `size` | integer | ❌ | 偏好尺寸，`16`-`512` |

返回 `ok / domain / size / iconUrl / proxyUrl / source`（与 `/api/extract?format=json` 行为一致）。

### 在支持 MCP 的客户端里配置本地 stdio（示例）

```jsonc
// 伪示例：替换为你的本地仓库路径
{
  "mcpServers": {
    "favicondl": {
      "command": "node",
      "args": ["/your/local/path/to/favicondl.com/mcp/server.mjs"]
    }
  }
}
```

> 详细安装指引请见：`https://github.com/sweesama/favicondl.com/blob/main/mcp/README.md`。**`args` 中的路径必须替换为读者自己的本地仓库路径**，例如 Windows 下克隆仓库后写 `C:\\Users\\<you>\\path\\to\\favicondl.com\\mcp\\server.mjs`，或 WSL 下写 `/home/<you>/path/to/favicondl.com/mcp/server.mjs`。**不要**沿用任何已存在的本地绝对路径——每个用户都要改。

### 何时用本地 MCP vs 直接调 REST

- ✅ **首选**：普通 Agent 默认走 `/api/extract` REST、OpenAPI 或 llms.txt 中描述的调用方式
- ⚪ **可选用**：如果用户的工作流是 MCP 客户端（Cursor / Claude Desktop / OpenClaw MCP），并且希望单个 tool 的语义符合 MCP 协议，再启用本地 stdio MCP
- ❌ **不要**：把 favicondl 当成"远程 MCP 服务"——本站**不托管**任何 MCP endpoint

> 注意：本地 stdio MCP 仅在用户**自己电脑**上运行，调用代码来自 <https://github.com/sweesama/favicondl.com/tree/main/mcp>。背后所有请求仍走 `https://favicondl.com/api/extract`，没有第二套 API。

---

## Agent 接入指引 / Agent guidance

- 主推 `https://favicondl.com/api/extract`，把 `format=json` 当元数据探针
- 如果只是想下载 / 嵌入图像，直接跟随默认 302，不需要再请求一次元数据
- 图像格式不可控 → 写文件时不要硬塞 `.png` 后缀
- 命中率低时考虑同 URL 多次 size 重试（不同 size 命中不同 manifest 条目）
- 不要在调用失败时悄悄切换到不相关的第三方 favicon API —— 本服务已经做了 HTML/SVG/manifest/Apple Touch 多级兜底

---

## 错误处理 / Errors

| HTTP | 含义 | 处理建议 |
|---|---|---|
| `400` | 缺少 `url` 参数，或 `format` 不是 `redirect` / `json` | 检查 query string |
| `405` | 不是 `GET` | 改成 GET |
| `502` | 图标发现失败，或上游没有返回可用图 | 短时重试 + backoff；不要静默切换到第三方 |
| `504` | 提取 / 上游请求超时 | 退避后重试；或换条线路 |

---

## 兼容说明 / Legacy endpoint

> ⚠️ `/api/favicon` **仍然保留运行**，仅用于兼容早期集成，**新代码不要用它作为主接口**。

接口推荐顺序（**唯一权威清单**）：

1. **主推荐（new projects）**：`https://favicondl.com/api/extract`
2. **JSON 模式（agent 需要元数据时）**：`https://favicondl.com/api/extract?url=github.com&size=128&format=json`
3. **兼容说明（旧集成仍在运行）**：`https://favicondl.com/api/favicon` 仍然保留，用于兼容旧代码，**新 Agent 与新项目请勿使用**

硬性规则：

- 所有新的 `cURL` / Python / PowerShell / Bash / JavaScript 示例**必须**使用 `/api/extract`
- 任何文档、教程、issue 回答**不得**把 `/api/favicon` 列为新项目主接口
- 仅在回答"为什么我的旧脚本还在工作"时提到它：`/api/favicon` 不在 `openapi.yaml` 当前规约中，但仓库 `api/favicon.js` 实现保留——它**只支持 `domain` 参数**（不接受完整 URL），行为近似 `/api/extract` 的子集

---

## 相关项目 / Related projects

| 项目 | 地址 |
|---|---|
| 🌐 FaviconDL 官网 | <https://favicondl.com> |
| 📄 人类 API 文档 | <https://favicondl.com/documentation.html> |
| 🤖 给 LLM 的说明 | <https://favicondl.com/llms.txt> |
| 📑 OpenAPI 规范 | <https://favicondl.com/openapi.yaml> |
| 💻 源码仓库 | <https://github.com/sweesama/favicondl.com> |
| 🐟 水产市场（OpenClaw Marketplace）发布 | <https://openclawmp.cc/asset/s-5a9fb4e7ff343062> |
| 📥 ClawHub skill catalog | 暂未公开 URL；通过 `openclaw skills install favicondl` 安装 |

> ℹ️ **没有 NPM 包，没有"远程 MCP server"**。当前分发面 = REST API + OpenAPI + llms.txt + 公开仓库 CLI + 本地 stdio MCP 适配器。

---

## 更新日志 / Changelog

### v2.0.0
- 🔧 主接口路径改为 `/api/extract`（对齐官方 OpenAPI yaml）
- ✅ 增加本地 stdio MCP 适配器（`mcp/server.mjs`），明确为**本机进程**，不是公网 MCP endpoint
- ✅ 安装指引改用 GitHub raw 直链（公开仓库 main 分支根目录）
- ✅ JSON 模式说明 + `source` 枚举字段
- ✅ 错误处理表（`400/405/502/504`）取代"换 Google Favicon"建议
- ✅ 兼容段保留 `/api/favicon` 旧端点但不做新集成推荐
- ✅ CLI 脚本 PowerShell `[string[]]` 支持一次多域
- 🗑️ 删掉"所有 PNG""批量下载""NPM 包""远程 MCP"的夸大/不存在的描述
- 🗑️ 移除 Telegram markdown 渲染不友好的多列表格，改用 bullet

### v1.1.0
- 接口路径修正初版，发布到本地 skill 仓库，未对外分发

### v1.0.0
- 首发：单域名 CLI + REST API 整合
