# Fun-ASR Skill 使用规范

## 工作流程（2026-04-09 更新）

当用户涉及抖音视频音频处理时，按以下规范执行：

### 场景 1：获取链接 + ASR 识别
**触发条件**：用户明确要求"获取抖音视频音频链接并识别/转写"
**执行动作**：
1. 使用 tikhub-douyin-media-links skill 获取音频链接
2. 下载音频文件
3. 使用 fun-asr skill 进行语音识别
4. 输出转写结果

### 场景 2：仅获取链接
**触发条件**：用户仅要求"获取抖音视频音频链接"，未提及识别/转写
**执行动作**：
1. 仅使用 tikhub-douyin-media-links skill 获取音频链接
2. 输出链接
3. ❌ 不进行 ASR 识别

### 关键原则
- **不自动执行**：除非用户明确要求，否则不自动进行 ASR 转写
- **分步确认**：获取链接后可询问用户是否需要进一步识别

## 技术修复记录（2026-04-09）

修复了 fun-asr skill 脚本的问题：

**原问题**：
- 使用实时流式识别方式，一次性发送整个音频文件导致 WebSocket 超时
- 未处理双声道音频（API 要求单声道）

**修复方案**：
- 改用非流式调用 `recognition.call(file_path)`，更适合本地文件
- 使用 FFmpeg 预处理音频：`pcm_s16le`、16kHz、单声道
- 正确处理返回的列表结构，拼接所有句子文本

**文件修改**：
- `/root/.openclaw/workspace/skills/fun-asr-file/scripts/cli.py`

## 音频预处理命令
```bash
ffmpeg -i input.mp3 -c:a pcm_s16le -ar 16000 -ac 1 output.wav -y
```

## 依赖
- dashscope SDK
- FFmpeg（用于音频格式转换）
