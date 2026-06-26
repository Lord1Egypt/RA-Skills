# aim-digital-human-video

数字人视频生成 Skill —— 基于一张人物图片和音频（或文案），自动生成数字人说话视频，返回公开可访问的视频链接。

## 功能

- 输入人物图片 + 音频/文案，自动生成数字人说话视频
- 支持三种音频来源：现成音频文件、文案+克隆语音、文案+预设语音
- 自动调用 TTS 服务将文案转为语音
- 智能轮询策略，根据音频时长预估生成时间，动态调整检查频率
- 任务状态持久化，轮询超时后下次运行自动回查

## 前置条件

### 1. 密钥配置

使用前需要获取 `aim-secret-key`：

1. 前往 [https://tools.mentarc.cn/aim-skills/](https://tools.mentarc.cn/aim-skills/) 注册账号
2. 获取你的 `aim-secret-key`
3. 复制配置模板并填入密钥：

```bash
cp .env.example .env
```

编辑 `.env`，将密钥填入：

```
aim-secret-key=你的密钥
```

### 2. Python 依赖

```bash
pip install requests
```

### 3. 可选依赖

- [ffprobe](https://ffmpeg.org/)（用于获取音频时长，缺失时使用保守默认值）

## 使用方式

### 用现成音频

```bash
python3 scripts/gen_digital_human.py \
  --image-path /path/to/image.png \
  --audio-path /path/to/audio.mp3 \
  --task-name "我的数字人视频"
```

### 用文案（默认中文女声）

```bash
python3 scripts/gen_digital_human.py \
  --image-path /path/to/image.png \
  --text "你好，欢迎来到我们的频道" \
  --task-name "欢迎视频"
```

### 用文案 + 克隆语音

```bash
python3 scripts/gen_digital_human.py \
  --image-path /path/to/image.png \
  --text "你好，欢迎来到我们的频道" \
  --voice-sample /path/to/voice_sample.wav \
  --voice-sample-text "这段话是语音样本对应的原文" \
  --task-name "克隆语音视频"
```

### 用文案 + 预设语音

```bash
python3 scripts/gen_digital_human.py \
  --image-path /path/to/image.png \
  --text "Hello, welcome to our channel" \
  --voice-preset "英文女" \
  --task-name "英文视频"
```

预设语音可选：`中文女`（默认）、`中文男`、`英文男`、`英文女`

## 参数说明

| 参数 | 必填 | 说明 |
|------|------|------|
| `--image-path` | 是 | 人物图片本地路径 |
| `--audio-path` | 三选一 | 现成音频文件路径 |
| `--text` | 三选一 | 要说的文案（需配合语音选项） |
| `--voice-sample` | 否 | 克隆语音样本路径（5-10秒） |
| `--voice-sample-text` | 否 | 语音样本对应的文字 |
| `--voice-preset` | 否 | 预设语音：中文男/中文女/英文男/英文女 |
| `--task-name` | 否 | 任务名称（默认 `digital-human`） |
| `--quality` | 否 | 视频质量：`high` / `normal` |
| `--poll-timeout` | 否 | 轮询超时秒数（默认 3600） |

音频来源三选一：`--audio-path`（现成音频）、`--text`（文案+语音合成）、必须提供其中一种。

## 输出示例

```json
{
  "success": true,
  "taskName": "欢迎视频",
  "uuid": "dh_a1b2c3d4e5f6",
  "videoUrl": "https://tos-xxx.volces.com/xxx/video.mp4",
  "totalSeconds": 180,
  "audioDuration": 4.8,
  "estimatedRange": "150~270s"
}
```

核心字段：`videoUrl`（TOS 公开 URL，可直接访问或分享）。

## 智能轮询策略

根据音频时长预估视频生成时间（经验值：音频时长 × 25~50 + 30s 开销）：

| 阶段 | 时间范围 | 轮询间隔 |
|------|----------|----------|
| 阶段1 | 0 ~ 预估70% | 每 15s |
| 阶段2 | 预估70% ~ 预估最大值 | 每 5s |
| 阶段3 | 超过预估值 | 每 3s |

## 任务状态管理

脚本在 skill 目录下维护 `.task-history.jsonl`，自动处理轮询超时但上游任务仍在运行的情况：

- 提交成功 → 标记 `pending`
- 轮询到视频就绪 → 标记 `ready`
- 超过 24h 仍 404 → 标记 `expired`
- 本次轮询超时 → 保持 `pending`，下次运行自动回查

查看任务状态：

```bash
python3 scripts/gen_digital_human.py --list-tasks
```

## 文件结构

```
aim-digital-human-video/
├── .env.example              # 密钥配置模板
├── .env                      # 密钥配置（需自行创建，已 gitignore）
├── SKILL.md                  # Skill 详细文档
├── scripts/
│   └── gen_digital_human.py  # 主脚本：TTS → 提交 → 轮询 → 状态落盘
├── .task-history.jsonl       # 运行时生成（已 gitignore）
```

## 注意事项

- 图片和音频文件会以 base64 编码提交到 AEP 网关，请确保文件大小合理
- 单次轮询默认超时 60 分钟，超时不等于失败，任务会保留为 pending 状态
- 请勿将 `.env` 中的密钥提交到代码仓库
