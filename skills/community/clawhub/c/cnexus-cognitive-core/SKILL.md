---
name: cnexus-cognitive-core
description: CNexus 2.0 — local personal second brain. 6-step cognitive loop, memory graph, JSON persistence, one-click clear. Python stdlib + static UI.
---

# CNexus 2.0 — Personal Cognitive OS

**Repo:** https://github.com/plusunm/CNexus2.0

本地运行的个人第二大脑：把对话与文档变成可关联、可持久化、可清空的认知网络。

## 能做什么

| 维度 | 能力 |
|------|------|
| 记忆 | 结构化记忆单元、记忆流图、激活扩散、语义虫洞、REM 整理 |
| 认知 | 六步闭环 OBSERVE→REFLECT、决策链回放、Ollama 本地优先 |
| 持久化 | 自动写入 `data/cnexus_personal_state.json`，重启恢复 |
| 清空 | UI 一键清空 + `POST /api/memory/clear` |
| 多模态 | 代码 AST 投影、架构图视觉解析（可选 Ollama） |

## 快速启动

```bash
git clone https://github.com/plusunm/CNexus2.0.git
cd CNexus2.0
python app_v2.py
```

打开 http://127.0.0.1:7864（Windows 可双击 `start_cnexus.bat`）

Python 3.10+，核心网关**无第三方依赖**。Ollama 可选。

## 主要 API

| 端点 | 说明 |
|------|------|
| `POST /api/converse` | 认知对话 |
| `GET /api/status` | 状态 + 记忆图谱 |
| `POST /api/memory/clear` | 清空记忆 |
| `POST /v1/memory/rem-sleep` | REM 深度整理 |
| `POST /api/ingest/code` | 代码 AST 投影 |
| `POST /api/ingest/image` | 架构图解析 |

## 安装（OpenClaw）

```bash
openclaw skills install @plusunm/cnexus-cognitive-core
```

完整运行时请克隆上方 GitHub 仓库。

**CNexus remembers what you think, and understands how you think.**
