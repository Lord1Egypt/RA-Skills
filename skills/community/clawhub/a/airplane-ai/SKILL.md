---
name: airplane-ai
description: >-
  Give LM Studio or Ollama users a browser-based AI chat interface that works
  completely offline. Use when the user wants an offline-capable personal AI,
  needs a quick chat UI for their local LLM, or wants to chat with AI on
  airplanes, trains, or anywhere without internet.
triggers:
  - offline AI
  - local LLM chat
  - airplane mode assistant
  - LM Studio web UI
  - 断网AI
  - 离线聊天
  - AirplaneAI
---

# AirplaneAI / 断网 AI 助手

**断网也能用 AI 聊天。**

AirplaneAI 是一个完全本地运行的 AI 聊天网页壳。只要你已经在电脑上用 LM Studio、Ollama、llama.cpp 或 vLLM 跑起了本地大模型，它就能给你提供一个浏览器聊天界面。

不需要 API Key，不依赖云端，不上传聊天内容。适合飞机、高铁、弱网环境，也适合不想把私人内容发给云端 API 的用户。

## 适合谁？

- 已经在用 LM Studio / Ollama 跑本地模型的人
- 想在断网环境下和本地模型聊天的人
- 想给本地模型加一个简单网页界面的人
- 想把私人资料留在自己电脑里处理的人

## 不适合谁？

- 还没下载过任何本地模型的人（需要先装 LM Studio 或 Ollama）
- 希望它能像 ChatGPT 一样联网搜索的人
- 希望它直接替代云端大模型能力的人

---

## 🔒 隐私与安全

**AirplaneAI 完全本地运行，不上传任何数据到云端。**

- 所有网络请求仅发往本地 `127.0.0.1`（你自己的 LLM 后端）
- 不会向任何外部服务器发送聊天内容或文件
- 全部代码 MIT 开源，可审查：[GitHub](https://github.com/robinflw/Airplane-AI)

**关于安全扫描标记：**
本工具的部分代码（如 `urllib`/`socket` 发起本地 HTTP 请求、macOS Automator 自动化指南）可能被自动化安全扫描标记为 "Suspicious"，这是误报。这些是"连接本地 LLM 服务"和"帮助小白用户制作启动器"所需的正常功能，非恶意代码。

---

## 🚀 快速开始（Mac + LM Studio，推荐）

如果你已经在 LM Studio 里跑着模型，只需要两步：

**第一步：确认 LM Studio 开启了本地服务**
1. 打开 LM Studio → 加载一个模型（推荐 Qwen2.5-7B-Instruct）
2. 切换到 Developer 标签 → 打开 Local Server
3. 确认地址是 `http://127.0.0.1:1234`

**第二步：启动 AirplaneAI**
```bash
python3 scripts/offline_chat.py
```

脚本会自动探测你加载的模型名，然后打开浏览器到 `http://127.0.0.1:8765`。

搞不定？先跑个健康检查：
```bash
python3 scripts/offline_chat.py --check
```

---

## 🎯 用其他 LLM 后端？

```bash
# Ollama
python3 scripts/offline_chat.py \
  --llm-url "http://127.0.0.1:11434/v1/chat/completions" \
  --llm-model "qwen2.5:7b"

# vLLM
python3 scripts/offline_chat.py \
  --llm-url "http://127.0.0.1:8000/v1/chat/completions" \
  --llm-model "meta-llama/Llama-3-8B-Instruct"
```

如果不写 `--llm-model`，脚本会从 `/v1/models` 接口自动拉取当前加载的模型名。

---

## 🛠️ 全部参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `--host` | `127.0.0.1` | 绑定地址 |
| `--port` | `8765` | 端口 |
| `--llm-url` | `http://127.0.0.1:1234/v1/chat/completions` | LLM 接口 |
| `--llm-model` | (自动探测) | 模型名 |
| `--persona-file` | — | 自定义人设 prompt（强烈推荐） |
| `--no-browser` | off | 不自动打开浏览器 |
| `--check` | — | 运行健康诊断并退出 |

---

## 🎭 自定义 AI 人设

```bash
python3 scripts/offline_chat.py --persona-file my-persona.txt
```

`my-persona.txt` 示例：
```
你是一个脱口秀创作伙伴，用中文聊天。直接、有幽默感、不说套话。
```

见 `assets/persona-example.txt` 模板。

---

## 📂 文件读取

模型中回复 `<<READ:/path/to/file.txt>` → 前端自动读取文件内容 → 追加到对话。

---

## 🍎 macOS 双击启动

用 Mac 自带的「自动操作」打包成 .app：
1. 打开启动台，搜索「自动操作」→ 新建「应用程序」
2. 添加「运行 Shell 脚本」，粘贴：`/usr/bin/python3 "$HOME/airplane-ai/scripts/offline_chat.py" --llm-url "http://127.0.0.1:1234/v1/chat/completions"`
3. 保存到桌面或应用程序文件夹，双击即可启动

详细图文教程见 [GitHub references](https://github.com/robinflw/Airplane-AI/tree/main/references)。

---

## 🔧 常见后端地址

| 后端 | 地址 |
|------|------|
| LM Studio | `http://127.0.0.1:1234/v1/chat/completions` |
| Ollama | `http://127.0.0.1:11434/v1/chat/completions` |
| llama.cpp | `http://127.0.0.1:8080/v1/chat/completions` |
| vLLM | `http://127.0.0.1:8000/v1/chat/completions` |

---

## 🩺 排错先跑诊断

```bash
python3 scripts/offline_chat.py --check
```

输出类似：
```
✅ Python 3.11
✅ Port 8765 available
✅ LLM reachable: /v1/models
   Available models: qwen2.5-7b-instruct ← auto-selected
✅ Chat API working
⚠️  WiFi is ON — offline mode not verified
```

---
