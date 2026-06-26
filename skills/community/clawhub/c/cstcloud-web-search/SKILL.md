---
name: cstcloud-web-search
description: 使用中国科技云（CSTCloud）Web Search API 进行网络搜索。无需 Brave/Perplexity 等国外 API key，适合国内用户，直接通过"帮我搜 xxx"调用。
homepage: https://clawhub.ai/shcw0405/cstcloud-web-search
repository: https://github.com/shcw0405/cstcloud-web-search
metadata: {"clawdbot":{"emoji":"🔍","requires":{"bins":["bash","curl","jq"],"env":["CSTCLOUD_API_KEY"]},"primaryEnv":"CSTCLOUD_API_KEY"}}
---

# CSTCloud Web Search

基于中国科技云（Uni-API）Web Search API 的网络搜索技能。适合 OpenClaw AI 助手使用，直接说"帮我搜 xxx"即可触发。

## 功能特性

- 🔍 基于中国科技云搜索服务，国内访问稳定
- 🌐 无需国外 API key，适合国内用户
- 📊 返回标题、URL、来源、摘要
- ⚡ 配置简单，一个环境变量即可

## 安装

```bash
# 通过 ClawHub 安装（推荐）
npx clawhub install cstcloud-web-search

# 或手动安装到 ~/.openclaw/workspace/skills/
```

## 配置

### 1. 设置环境变量

编辑 `~/.openclaw/.env` 文件，添加：

```
CSTCLOUD_API_KEY=你的API密钥
```

或通过命令行：

```bash
export CSTCLOUD_API_KEY=你的API密钥
```

### 2. 重启 OpenClaw Gateway

```bash
openclaw gateway restart
```

## 使用方法

在 OpenClaw 对话中直接说：

```
帮我搜一下 xxx
```

或通过命令行直接调用：

```bash
# 默认 5 条结果
cstcloud-web-search "搜索关键词"

# 指定结果数量（最多 10 条）
cstcloud-web-search "搜索关键词" 10
```

## API 信息

- **Base URL**: `https://uni-api.cstcloud.cn`
- **Endpoint**: `POST /v1/web-search`
- **认证方式**: Bearer Token
- **模型名**: `web-search`

## 结果示例

```
找到 10 条结果（显示前 3 条）：

1. OpenClaw 进入"日更级"狂飙模式:刚刚、2026.3.12 版本发布
   URL: https://www.163.com/dy/article/KNUJILQP0511D6RL.html
   来源: 网易
   摘要: 刚刚,OpenClaw发布了2026.3.12版本...

2. OpenClaw推出新版本 89项更新重磅来袭
   URL: https://news.china.com/socialgd/10000169/20260310/49307835.html
   来源: 中华网新闻频道
   摘要: OpenClaw推出新版本...

=== 搜索完成 ===
```

## 参考与致谢

本 skill 参考了以下项目：

- [bailian-web-search](https://github.com/openclaw/skills/tree/main/skills/krisyejh/bailian-web-search)（OpenClaw 官方 Skills）

**改动说明：**

- bailian-web-search 使用阿里云 MCP 协议（Streamable HTTP + JSON-RPC），需要 4 个请求才能完成一次搜索
- 本 skill 改为直接调用 CSTCloud REST API，一个请求即可完成搜索，逻辑更简单直接
- API 格式、认证方式、返回结构均基于 CSTCloud Uni-API 文档实现

## License

MIT-0
