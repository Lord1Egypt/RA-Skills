---
name: feishu-voice-bubble
description: 教飞书agent如何发送语音气泡消息。需要先将文字转语音（MP3），再转为opus格式，最后通过飞书消息工具发送。
user-invocable: true
metadata:
  trigger_words:
    - 发语音气泡
    - 发送语音消息
    - 语音气泡
    - 发送语音
    - voice bubble
    - 语音
---

# Skill: 飞书语音气泡发送

**Trigger Words (触发词):**
- 发语音气泡
- 发送语音消息
- 语音气泡
- 发送语音
- voice bubble
- 语音

---

## 前置条件

### 环境要求

此技能依赖 `edge-tts` 和 `ffmpeg`，技能目录下已提供 `setup.sh` 自动安装脚本。

**OpenClaw 安装此技能时，请执行以下命令完成依赖安装：**

```bash
bash setup.sh
```

脚本会自动完成：
- 通过 `pip` 安装 `edge-tts`
- 通过系统包管理器（apt-get / brew / yum）安装 `ffmpeg`（版本 4.4.2+）

> 如果自动安装失败，请手动安装：
> - edge-tts：`pip3 install edge-tts`
> - ffmpeg：参考 https://ffmpeg.org/download.html

### 需要的工具
1. `tts` - 文字转语音（生成MP3）
2. `exec` - 用ffmpeg转换格式
3. `feishu_im_bot_image` 或 `message` - 发送.opus文件

---

## 初始化引导（首次安装后执行）

`setup.sh` 执行完毕后，**立即**向用户发送以下欢迎消息，并引导完成音色初始设置：

> 🎙️ feishu-voice-bubble 已安装完成！
> 我支持 14 种中文音色，现在为你逐一播放试音，听完告诉我你喜欢哪个就好。

然后按照下方「音色切换流程」逐一发送试音气泡。

---

## 音色管理

### 读取当前音色

每次发送语音前，先读取当前音色设置：

```python
voice = ctx.state.get("tts_voice", "zh-CN-XiaoxiaoNeural")  # 默认音色
```

### 音色切换触发词

当用户说出以下类似内容时，进入音色切换流程：
- "换个声音"、"切换音色"、"换个音色"、"我想换声音"
- "有哪些声音可以选"、"给我听听其他声音"
- "change voice"、"switch voice"

### 音色切换流程

**第一步**：发送文字说明当前音色，并告知即将逐一试音：

> 当前音色：**{当前音色名}**
> 共有 14 种中文音色，我来逐一播放，听完告诉我你想选哪个 👇

**第二步**：按顺序逐一发送每个音色的试音语音气泡，每条气泡前先发一条文字标注编号和音色信息：

| # | 音色名 | 性别 | 风格 | 特点 | 试音文本 |
|---|---|---|---|---|---|
| 1 | `zh-CN-XiaoxiaoNeural` | 女 | 新闻/小说 | 温暖 | 你好，我是晓晓，很高兴认识你。 |
| 2 | `zh-CN-XiaoyiNeural` | 女 | 动画/小说 | 活泼 | 你好，我是晓伊，超级开心见到你！ |
| 3 | `zh-CN-YunjianNeural` | 男 | 体育/小说 | 激情 | 你好，我是云健，让我们一起加油！ |
| 4 | `zh-CN-YunxiNeural` | 男 | 小说 | 阳光活泼 | 你好，我是云希，今天也是元气满满的一天！ |
| 5 | `zh-CN-YunxiaNeural` | 男 | 动画/小说 | 可爱 | 你好，我是云夏，嘿嘿，好高兴认识你哦。 |
| 6 | `zh-CN-YunyangNeural` | 男 | 新闻 | 专业可靠 | 您好，我是云扬，为您提供专业播报服务。 |
| 7 | `zh-CN-liaoning-XiaobeiNeural` | 女 | 方言 | 东北话 | 你好，我是晓北，老铁没毛病，双击666！ |
| 8 | `zh-CN-shaanxi-XiaoniNeural` | 女 | 方言 | 陕西话 | 你好，我是晓妮，额是陕西人，可高兴了！ |
| 9 | `zh-HK-HiuGaaiNeural` | 女 | 粤语 | 友好 | 你好，我係曉佳，好高興認識你！ |
| 10 | `zh-HK-HiuMaanNeural` | 女 | 粤语 | 友好 | 你好，我係曉曼，希望我哋可以做朋友！ |
| 11 | `zh-HK-WanLungNeural` | 男 | 粤语 | 友好 | 你好，我係雲龍，隨時為你服務！ |
| 12 | `zh-TW-HsiaoChenNeural` | 女 | 台湾普通话 | 友好 | 你好，我是曉臻，很開心認識你喔！ |
| 13 | `zh-TW-HsiaoYuNeural` | 女 | 台湾普通话 | 友好 | 你好，我是曉雨，希望我們可以成為好朋友！ |
| 14 | `zh-TW-YunJheNeural` | 男 | 台湾普通话 | 友好 | 你好，我是雲哲，很榮幸為你服務！ |

每条试音的发送格式（文字 + 语音气泡）：

```
[文字消息] 🔊 #3 云健 · 男声 · 激情风格
[语音气泡] 用 zh-CN-YunjianNeural 生成的 opus 文件
```

**第三步**：全部播放完毕后，发送：

> 14 种音色已全部播放完毕 🎉
> 请告诉我你想选哪个？可以说编号（如"选3"）或音色名（如"云希"）。

**第四步**：用户确认后，写入 `ctx.state` 并回复确认：

```python
ctx.state.set("tts_voice", "zh-CN-YunxiNeural")  # 替换为用户选择的音色
```

> ✅ 已切换为 **云希**（zh-CN-YunxiNeural），后续语音气泡将使用此音色。

---

## ⚠️ 重要行为约束

**禁止在生成 MP3 后直接将 MP3 文件发送到飞书聊天窗口。**

MP3 是中间产物，仅用于 ffmpeg 转换，不应作为最终消息发出。正确流程必须是：

```
生成 MP3 → 转换为 opus → 发送 opus（语音气泡）
```

**唯一例外**：用户明确要求发送 MP3 文件（如"把这个音频文件发给我"）时，才可直接发送 MP3。

---

## 完整操作步骤

### Step 1: 文字转语音 (MP3)

先读取用户设置的音色（若未设置则用默认值）：

```python
voice = ctx.state.get("tts_voice", "zh-CN-XiaoxiaoNeural")
```

使用 `tts` 工具生成MP3文件：

```json
{
  "channel": "feishu",
  "text": "要转成语音的文字内容",
  "voice": "<voice>"
}
```

> ⚠️ 注意：tts工具会返回音频文件路径，保存到 `/tmp/openclaw/` 目录下

### Step 2: 转换为 Opus 格式

使用 `exec` 运行 ffmpeg 命令转换格式：

```bash
ffmpeg -y -i /tmp/openclaw/xxx.mp3 -c:a libopus -b:a 32k -ar 48000 -ac 1 /tmp/openclaw/xxx.opus
```

参数说明：
- `-y` - 覆盖已存在的文件
- `-i input.mp3` - 输入文件
- `-c:a libopus` - 使用opus编码
- `-b:a 32k` - 音频比特率
- `-ar 48000` - 采样率
- `-ac 1` - 单声道
- `output.opus` - 输出文件

### Step 3: 发送语音气泡

使用 `feishu_im_bot_image` 工具发送 .opus 文件：

```json
{
  "message_id": "om_xxx",
  "file_key": "file_xxx",
  "type": "file"
}
```

或者使用 `message` 工具：

```json
{
  "action": "send",
  "filePath": "/tmp/openclaw/xxx.opus"
}
```

---

## 完整示例流程

```python
# 1. 调用tts生成语音
tts(text="你好，这是我的第一条语音消息！")

# 2. 假设返回的文件是 /tmp/openclaw/voice_123.mp3
# 用ffmpeg转换
exec(command="ffmpeg -y -i /tmp/openclaw/voice_123.mp3 -c:a libopus -b:a 32k -ar 48000 -ac 1 /tmp/openclaw/voice_123.opus")

# 3. 发送 opus 文件
feishu_im_bot_image(message_id="om_xxx", file_key="file_xxx", type="file")
```

---

## 常见问题

### Q1: 为什么不能直接发MP3？
A: 飞书语音气泡只支持opus格式，MP3发出去只是附件而非语音消息。

### Q2: ffmpeg找不到怎么办？
A: 确保ffmpeg已安装且在系统PATH中。如果是在OpenClaw环境中，应该已经预装了。

### Q3: 语音没有声音怎么办？
A: 检查opus文件是否正确生成，可以用 `ffprobe` 查看音频信息确认。

### Q4: 发送失败怎么办？
A: 确保message_id和file_key正确，且bot有发送文件的权限。

---

## 进阶技巧

1. **批量处理**: 如果需要发多条语音，可以循环执行tts+ffmpeg转换
2. **音色切换**: 用户可随时通过自然语言要求切换音色，参见「音色管理」章节
3. **文件名随机**: 使用时间戳或UUID避免文件名冲突

---

## 相关文件

- TOOLS.md - 基础环境配置
- 此技能依赖 tts, exec, feishu_im_bot_image 工具
