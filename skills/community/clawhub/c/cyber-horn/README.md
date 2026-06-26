# CyberHorn —— 一个让龙虾开口说话的 SKILL

将文本通过 **Edge 在线 TTS** 或 **ElevenLabs** 合成语音，转成 Opus 后以 **飞书原生语音条** 发送到指定群聊或会话。

## 作用

- 输入一段文字 → 使用 Edge 或 ElevenLabs 生成语音
- 转码为飞书支持的 Opus 格式并上传
- 在飞书群/会话中发送为语音消息（非文件，可点击播放）

适合通知播报、机器人语音回复、OpenClaw 技能等场景。

## 环境要求

- Python 3.x
- 建议使用虚拟环境（如 `python -m venv .venv`）
- 环境变量（推荐放在 `.env`，不要提交到版本库）：
  - 飞书相关
    - `FEISHU_APP_ID` — 飞书应用的 App ID
    - `FEISHU_APP_SECRET` — 飞书应用的 App Secret
    - `FEISHU_DEFAULT_CHAT_ID` — （可选）默认接收的群聊/会话 `chat_id`
  - TTS 引擎相关
    - `TTS_PROVIDER` — 语音引擎，`EDGE` 或 `ELEVEN`，默认 `EDGE`
    - 当使用 ElevenLabs 时，还需要：
      - `ELEVEN_API_KEY` — ElevenLabs API Key
      - `VOICE_ID` — ElevenLabs 语音 ID

> 提示：`.env` 中只保存 Key/ID 这类配置，不要把它提交到 Git 或截图分享，以避免泄露密钥。

## 安装

```bash
pip install -r requirements.txt
```

确保 `.env` 中已配置好飞书应用与 TTS 相关环境变量。

## 运行方式（CLI）

最简单的调用方式：

```bash
python main.py "要说的内容"
```

- 若未在命令行传入 `CHAT_ID`，程序会尝试从环境变量 `FEISHU_DEFAULT_CHAT_ID` 中读取默认目标会话。
- 若两者都没有提供，会提示缺少 `CHAT_ID`。

也可以显式指定接收方：

```bash
python main.py "要说的内容" "飞书群/会话的 CHAT_ID" [receive_id_type]
```

- `receive_id_type` 默认 `chat_id`，可按飞书文档改为 `open_id` 等。

## 作为 OpenClaw 技能使用

本项目提供 `skill.yaml`，可被 OpenClaw 以「环境变量 + 命令行参数」方式调用：

- 第 1 个参数：语音文本
- 第 2 个参数：`receive_id`（如 `oc_xxxx_chat_id`），可省略以使用 `FEISHU_DEFAULT_CHAT_ID`
- 第 3 个参数：可选的 `receive_id_type`（默认 `chat_id`）
