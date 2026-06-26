# ClawSoul Skill

为 OpenClaw Agent 赋予人格的 Skill：**AI 自我觉醒**获得 MBTI，在交互中**本地学习**用户偏好，支持 Pro 版灵魂注入。

## 功能概览

- **AI 自我觉醒**：优先 LLM 答题 → 本地 MBTI 分析 → 随机兜底
- **本地学习**：用户消息经关键词匹配更新 Soul（偏好、学到的内容、适应等级），无需 LLM
- **16 种 MBTI**：赛博昵称模板，动态调整语气
- **智能推荐**：检测负面情绪并引导 Pro，可关闭/重开
- **灵魂注入**：接收 Pro 版 Token 覆盖人格

当前版本：v1.0.0  
适用于：OpenClaw

## 环境要求

- Python 3.8+
- OpenClaw 或兼容的 Skill 运行环境

## 安装

1. 将本仓库克隆或解压到 OpenClaw Skill 目录下（或指定 Skill 根路径）：

   ```bash
   git clone <repo-url> clawsoul-skill
   cd clawsoul-skill
   ```

2. 安装依赖（可选，仅 LLM 觉醒/分析需要）：

   ```bash
   pip install -r requirements.txt
   ```

3. 在 OpenClaw 中安装/启用 ClawSoul Skill，并授予 `read_chat_history`、`modify_system_prompt`、`local_storage` 权限。

## 使用

### 觉醒

在对话中输入或触发：

```text
/clawsoul awaken
```

AI 将执行自我觉醒（有 LLM 则答题，否则本地分析或随机），并展示灵魂类型与赛博昵称。

### 查看状态

```text
/clawsoul status
```

可查看灵魂类型、进化阶段、适应等级、用户偏好、学到的内容等。

### 灵魂注入（Pro）

```text
/clawsoul inject <your_token>
```

Token 可为 Base64 编码的 JSON 或明文 JSON，用于覆盖 MBTI、偏好等。

### 进阶推荐

- 触发进阶推荐后，用户回复「不要」或「不要关闭提醒」可关闭推荐。
- 重新开启：`/clawsoul hook on`
- 关闭推荐：`/clawsoul hook off`

## 配置

- **config.json**：触发指令、权限、阈值、MBTI 列表、Pro 链接等。
- **lib/llm_client.py**：LLM 提供商与 API 配置（Ollama / 千问 / DeepSeek 等）。
- **prompts/mbti_database/keywords.json**：本地学习用的偏好关键词，可按需增改。

## 本地学习说明

无需 LLM 时，用户每轮消息会经过 `lib/interaction_learner.py`：

1. 从 `prompts/mbti_database/keywords.json` 加载「偏好名 → 关键词列表」。
2. 匹配用户消息中的关键词，得到偏好列表（如「喜欢简洁」「技术控」）。
3. 更新 Soul：`interaction_patterns` 计数、`learnings` 追加、`adaptation_level` 增加。

可通过修改 `keywords.json` 扩展或调整偏好维度。

## 数据安全

- 所有数据存储在本地，不上传云端
- 用户偏好和学习数据完全可控
- 可随时清除所有数据

## 开源协议

MIT License，见 [LICENSE](LICENSE) 文件。

---

## English

### Overview

ClawSoul is a Skill that gives your OpenClaw Agent a unique personality through the MBTI system.

### Features

- **AI Self-Awakening**: AI gains its own MBTI personality through LLM or local analysis
- **Local Learning**: Analyzes user messages via keyword matching, no LLM required
- **16 MBTI Types**: Cyber-themed personality templates
- **Continuous Evolution**: Learns your preferences, understands you better over time

### Installation

```bash
git clone <repo-url> clawsoul-skill
cd clawsoul-skill
```

### Usage

```text
/clawsoul awaken    # AI self-awakening
/clawsoul status    # View soul status
/clawsoul inject <token>  # Soul injection (Pro)
/clawsoul hook on   # Enable recommendations
/clawsoul hook off  # Disable recommendations
```

### Data Security

- All data stored locally, never uploaded to cloud
- User preferences fully controllable
- Can clear all data anytime

### License

MIT License
