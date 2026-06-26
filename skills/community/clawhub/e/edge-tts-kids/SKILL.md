---
name: edge-tts-kids
description: |
  Edge TTS 中文定制版 - 包含儿童配音预设。生成后自动发送到对话，无需翻文件。
  触发词：配音、TTS、文生音、语音、配音生成、儿童配音
---

# Edge TTS 中文定制版

Edge TTS 的中文优化版本，包含预设音色和儿童配音，生成后自动发送到对话。

## ⚠️ 核心规则

**生成的配音文件必须直接发送到对话！**

```javascript
// 生成后立即发送
message({ action: "send", path: "生成的音频文件.mp3" })
```

不要让用户翻文件夹！

## 预设音色

### 成人音色

| 预设名 | Voice | Pitch | Rate | 适用场景 |
|--------|-------|-------|------|---------|
| **曼波** | zh-CN-XiaoyiNeural | +8% | default | 活泼、有活力的内容 |
| **晓伊** | zh-CN-XiaoyiNeural | default | +30% | 快节奏内容、新闻 |
| **晓晓** | zh-CN-XiaoxiaoNeural | default | default | 自然、通用 |
| **云扬** | zh-CN-YunyangNeural | default | +10% | 旁白、纪录片 |

### 儿童配音

| 预设名 | Voice | Pitch | Rate | 适用场景 |
|--------|-------|-------|------|---------|
| **小糖豆** | zh-CN-XiaoyiNeural | +15% | -5% | 活泼童趣、动画解说、儿童故事 |
| **棉花糖** | zh-CN-XiaoxiaoNeural | +5% | -10% | 温柔故事、睡前故事、绘本 |
| **小萌萌** | zh-CN-XiaoxiaoNeural | +10% | -5% | 亲切安抚、教育内容、儿歌 |

> ⚠️ **注意**：zh-CN-XiaohanNeural（晓涵）音色暂时不可用，已改用晓晓替代。

## 使用方式

### 方式一：内置 tts 工具（推荐）

```javascript
// 简单调用（默认音色）
tts("你的文本")

// 指定音色
tts("你的文本", { voice: "zh-CN-XiaoyiNeural", pitch: "+15%", rate: "-5%" })
```

### 方式二：edge-tts 技能脚本

```bash
cd ~/.openclaw/workspace/skills/edge-tts/scripts

# 小糖豆风格
node tts-converter.js "小朋友们好！" --voice zh-CN-XiaoyiNeural --pitch +15% --rate -5% --output output.mp3

# 棉花糖风格
node tts-converter.js "从前有一只小兔子..." --voice zh-CN-XiaoxiaoNeural --pitch +5% --rate -10% --output output.mp3

# 小萌萌风格
node tts-converter.js "宝宝真棒！" --voice zh-CN-XiaoxiaoNeural --pitch +10% --rate -5% --output output.mp3
```

## 完整工作流

1. **识别意图**：用户请求配音/TTS
2. **选择预设**：根据内容类型选择合适的音色
3. **生成音频**：调用 tts 工具或脚本
4. **发送到对话**：⚠️ 必须使用 `message` 工具发送，不要让用户翻文件夹

## 依赖

此技能依赖 `edge-tts` 技能的脚本文件：
- 路径：`~/.openclaw/workspace/skills/edge-tts/scripts/`
- 需要 `node-edge-tts` npm 包

## 技术说明

- 使用 Microsoft Edge 神经语音服务
- 无需 API Key（免费）
- 输出 MP3 格式
- 需要网络连接
