---
name: aim-digital-human-video
description: 当用户想要用一张图片生成数字人说话视频时使用此 skill。用户需提供图片和音频（或文案+克隆语音/预设语音），skill 通过 AEP 提交 /video2，智能轮询 TOS URL 等待结果就绪后返回视频公开链接。
---

# 数字人视频生成 Skill

用户说"帮我用这张图片做个数字人"时，使用此 skill。

## 用户交互流程

1. 用户提供一张人物图片（本地路径）
2. 用户提供音频来源（三选一）：
   - **现成音频文件**：直接提供本地路径（`--audio-path`）
   - **文案 + 克隆语音**：提供要说的文字（`--text`）和一段语音样本（`--voice-sample`）以及样本对应的文字（`--voice-sample-text`）
   - **文案 + 预设语音**：提供要说的文字（`--text`），可选预设声音（`--voice-preset`，默认"中文女"，可选 "中文男"/"英文男"/"英文女"）
3. 可选：视频质量（`--quality high/normal`）

注意：动作描述 prompt 功能暂不主动暴露，除非用户主动要求。

## 技术流程

```
[TTS(可选)] → 读取文件转base64 → AEP提交/video2 → 智能轮询TOS URL → 返回视频链接
```

1. 如果用户提供的是文案而非音频，先调用 TTS（走 AEP 网关）生成音频
2. 读取图片和音频文件，转为 base64 编码
3. 通过 AEP 网关提交 `/video2`（传 base64，服务端自行存储，立即返回 TOS 公开 URL）
4. 用 ffprobe 获取音频时长，预估生成时间，智能调整轮询频率
5. 通过 HTTP HEAD 轮询 TOS URL，就绪后直接返回视频链接

skill 不接触任何内部存储（FFS），只需要 AEP 凭证即可运行。

## 智能轮询策略

根据音频时长预估视频生成时间（经验值：音频时长 × 25~50 + 30s 开销）：
- **阶段1**（0 ~ 预估70%）：每 15s 检查一次，节省请求
- **阶段2**（预估70% ~ 预估最大值）：每 5s 检查一次
- **阶段3**（超过预估值）：每 3s 检查一次

## 使用方式

### 用现成音频

```bash
python scripts/gen_digital_human.py \
  --image-path /path/to/image.png \
  --audio-path /path/to/audio.mp3 \
  --task-name "我的数字人视频"
```

### 用文案（默认中文女声）

```bash
python scripts/gen_digital_human.py \
  --image-path /path/to/image.png \
  --text "你好，欢迎来到我们的频道" \
  --task-name "欢迎视频"
```

### 用文案 + 克隆语音

```bash
python scripts/gen_digital_human.py \
  --image-path /path/to/image.png \
  --text "你好，欢迎来到我们的频道" \
  --voice-sample /path/to/voice_sample.wav \
  --voice-sample-text "这段话是语音样本对应的原文" \
  --task-name "克隆语音视频"
```

脚本输出 JSON，核心字段：`videoUrl`（TOS 公开 URL，可直接发送给用户）。

## 密钥配置

密钥只放一个地方：**本 skill 根目录下的 [.env](.env)**，键名 `aim-secret-key`。脚本不看环境变量、不读家目录、不跨 agent 复用——就这一个文件。

**agent 生成前先跑自检**：

```bash
python scripts/gen_digital_human.py --check-config
```

- `aim_secret_key_configured: true` → 继续生成流程
- `aim_secret_key_configured: false` → 引导用户：
  1. 去 https://tools.mentarc.cn/aim-skills/ 注册，拿到 aim-secret-key
  2. 用户把密钥粘进对话框
  3. agent 把 `.env` 里的 `aim-secret-key=` 后面填上用户给的密钥（**用户不自己改文件**）
  4. 重跑自检确认


### 其他（可选）
- `AEP_BASE_URL`：AEP 网关地址（默认 `https://aep.focusaim.com`）
- `TTS_AEP_SERVICE_ID`：TTS 服务标识（默认 `speech_generation_service_pre`）

## 任务状态表（pending/ready/expired）

主脚本在 skill 目录下维护 `.task-history.jsonl`（已 gitignore，不会随 skill 分享），自动处理**单次轮询 60 分钟超时但上游任务仍可能在跑**的情形：

- 每次运行脚本，**提交新任务前**会先回扫所有 pending 任务，对它们的 TOS URL 做一次 HEAD
  - 200 → 标记 `ready`，显示在屏幕上
  - 仍 404 且距提交 ≥ 24h → 标记 `expired`（真的失败了）
  - 仍 404 且不到 24h → 继续保持 `pending`
- 提交成功立刻写 `pending`；本次轮询成功转 `ready`；本次轮询 60 分钟超时不改状态，留给下次运行回扫
- 只想看状态不提交新任务：`python scripts/gen_digital_human.py --list-tasks`

## 文件说明

- `scripts/gen_digital_human.py`：主脚本，完成 TTS→提交→轮询→状态落盘 全流程
- `.task-history.jsonl`（运行时生成）：任务状态表

## 规则

- 始终调用 `/video2`（结果上传 TOS，返回公开 URL）
- 如果用户只给了文案没给音频也没指定语音类型，默认使用"中文女"预设语音
- 动作描述（prompt）功能暂不主动向用户暴露
- 单次轮询超时默认 60 分钟；超时不等于失败，由任务状态表接管后续确认
