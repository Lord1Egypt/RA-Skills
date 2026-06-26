# 🛫 AirplaneAI — 断网也能用 AI 聊天

> **断网、飞机上、高铁里 —— AI 照样聊。**

AirplaneAI 是一个完全本地运行的 AI 聊天网页壳。只要你已经在电脑上用 LM Studio 或 Ollama 跑起了本地大模型，运行一个 Python 脚本就能在浏览器里和 AI 聊天。

**不需要 API Key，不依赖云端，不上传聊天内容。**

> ⚠️ AirplaneAI 不会替你下载模型。你需要先在 LM Studio / Ollama 中加载好一个本地模型。

---

## 👤 适合谁？

- 已经在用 LM Studio / Ollama 跑本地模型的人
- 想在断网环境下和本地模型聊天的人
- 想给本地模型加一个简单浏览器界面的人
- 想把私人资料留在自己电脑里处理的人

## ❌ 不适合谁？

- 还没下载过任何本地模型的人
- 希望它能像 ChatGPT 一样联网搜索的人
- 希望它直接替代云端大模型能力的人

---

## 🚀 三步跑起来（Mac + LM Studio）

### 1. 确认 LM Studio 在跑

打开 LM Studio → 加载模型（推荐 Qwen2.5-7B）→ Developer 标签 → 打开 Local Server → 确认 `http://127.0.0.1:1234`

### 2. 启动 AirplaneAI

```bash
python3 scripts/offline_chat.py
```

脚本会自动探测你加载的模型名。如果不放心，先跑诊断：

```bash
python3 scripts/offline_chat.py --check
```

### 3. 打开浏览器

自动跳转到 `http://127.0.0.1:8765`，开始聊天。

---

## 🔌 用其他后端？

```bash
# Ollama
python3 scripts/offline_chat.py \
  --llm-url "http://127.0.0.1:11434/v1/chat/completions"

# 任何 OpenAI 兼容 API
python3 scripts/offline_chat.py \
  --llm-url "http://127.0.0.1:8080/v1/chat/completions"
```

---

## 🎭 自定义 AI 性格

```bash
python3 scripts/offline_chat.py --persona-file my-persona.txt
```

---

## 📂 读本地文件

聊天中 AI 输出 `<<READ:/路径>>` → 自动读取 → 追加到对话。

---

## 🩺 出问题了？

```bash
python3 scripts/offline_chat.py --check
```

一键诊断 Python 版本、端口、LLM 连接、WiFi 状态。

---

## 🍎 打包成 macOS App

双击启动，不用开终端 → 见 `references/macos-app-guide.md`

---

## 📄 License

MIT
