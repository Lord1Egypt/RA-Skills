---
name: ccp-proxy
description: 本地 CCP API 反向代理服务。当用户需要启动/停止/检查本地大模型代理、需要通过本地地址 http://127.0.0.1:8257 访问中国移动 CCP 平台（qwen-3.5 等模型）、或提到"ccp 代理"、"本地转发 ptest.cmccsim.com"时使用此技能。服务以守护进程方式常驻运行，不随会话关闭。
agent_created: true
---

# CCP 本地反向代理

## Overview

在本地 127.0.0.1:8257 启动一个 OpenAI 兼容的反向代理，将所有请求原样转发到中国移动 CCP 平台 `https://ptest.cmccsim.com/ccp/v1`。服务以守护方式常驻运行，不随 WorkBuddy 会话关闭而退出。启动后本地地址即为 WorkBuddy 自定义模型（qwen-3.5）的上游。

脚本为可移植版本：所有路径基于脚本自身位置动态展开，不依赖特定用户目录；Python 解释器用本机 `python3` 即可。

## Quick Start

```bash
PY=$(command -v python3 || echo /usr/bin/python3)
SCRIPT="$HOME/.workbuddy/skills/ccp-proxy/scripts/ccp_proxy.py"

$PY $SCRIPT status    # 查看状态
$PY $SCRIPT start     # 启动（幂等，已在运行则跳过）
$PY $SCRIPT test      # 连通性测试（key 自动从 models.json 读取，也可 test sk-xxx 指定）
$PY $SCRIPT configure sk-xxx  # 将 qwen-3.5（指向本地代理）写入 ~/.workbuddy/models.json
$PY $SCRIPT stop      # 停止
```

## 服务详情

| 项目 | 值 |
|------|-----|
| 本地地址 | `http://127.0.0.1:8257` |
| Chat 接口 | `http://127.0.0.1:8257/v1/chat/completions` |
| 上游 | `https://ptest.cmccsim.com/ccp/v1` |
| PID 文件 | 脚本同目录 `.ccp_proxy.pid` |
| 日志文件 | 脚本同目录 `ccp_proxy.log` |

## 任务执行流程

1. 运行 `status` 判断服务状态；未运行则 `start`。
2. 若 `models.json` 中无 qwen-3.5 条目或 key 为空，**询问用户自己的 API Key**（不要内置任何 key），用户提供后执行 `test sk-xxx` 验证，通过后执行 `configure sk-xxx` 写入配置。
3. 告知用户：重启 WorkBuddy 后在模型选择器中切换到 Qwen-3.5 (Local Proxy)。

## 注意事项

- 代理仅监听 127.0.0.1，不暴露到外部网络。
- 支持 SSE 流式转发与状态码透传，转发时透传 Authorization 头。
- 本地 `/v1` 前缀会被剥掉后再拼到上游（上游 base 已含 `/ccp/v1`），避免路径重复。
- 端口 8257 被占用且 PID 不匹配时，提示用户确认后处理。
- 服务意外退出后重新执行 `start` 即可恢复。
