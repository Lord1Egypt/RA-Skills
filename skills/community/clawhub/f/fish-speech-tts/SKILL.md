---
name: fish-speech-tts
version: 2.0.0
description: "Fish Speech AI 配音工具 — 声音克隆 + 情绪分析 + 多段合成。用于短剧/AI剧配音制作，支持参考音频克隆音色、智能情绪识别、批量台词生成、音色库管理。"
---

# Fish Speech TTS 技能 v2.0.0

本地 AI 语音合成系统，支持**声音克隆**、**情绪分析**、**多段合成**、**音色库管理**。

## 🎯 核心功能

1. **声音克隆** — 用参考音频的音色朗读任意文本
2. **情绪分析** — 自动识别台词情绪（开心/悲伤/愤怒/惊讶/温柔/讽刺/恐惧）
3. **多段合成** — 长文本自动分割 + 情绪分段 + 停顿控制
4. **音色库管理** — 注册/管理多个角色音色，支持搜索和筛选
5. **批量配音** — 从 JSON 脚本批量生成配音

## 📦 前置条件

### 1. Fish Speech API 必须运行

```bash
cd E:\fish-speech
.venv\Scripts\activate
python tools/api_server.py \
  --llama-checkpoint-path checkpoints/s2-pro \
  --decoder-checkpoint-path checkpoints/s2-pro/codec.pth \
  --device cuda --half --listen 127.0.0.1:18791
```

### 2. 依赖安装

```bash
# Fish Speech 环境
cd E:\fish-speech
.venv\Scripts\activate
pip install -e .

# 额外依赖（音频后处理）
pip install pydub
```

**注意**: pydub 需要 FFmpeg，Windows 用户需手动安装 FFmpeg 并添加到 PATH。

## 🚀 快速开始

### 场景 1: 简单配音（无情绪分析）

```bash
E:/fish-speech/.venv/Scripts/python.exe \
  H:/OpenClaw/.openclaw/agents/moviemaster/workspace/skills/fish-speech-tts/main.py \
  tts --text "你好，世界！" \
  --output "E:/fish-speech/output/hello.mp3"
```

### 场景 2: 声音克隆

```bash
E:/fish-speech/.venv/Scripts/python.exe \
  H:/OpenClaw/.openclaw/agents/moviemaster/workspace/skills/fish-speech-tts/main.py \
  tts --text "顾栖上台缺了这件首饰，狂热粉丝能掀翻整栋场馆！" \
  --ref "D:/Project/二十四节气/配音修改/momo参考音.mp3" \
  --output "E:/fish-speech/output/momo_首饰台词.mp3"
```

### 场景 3: 智能配音（带情绪分析）

```bash
E:/fish-speech/.venv/Scripts/python.exe \
  H:/OpenClaw/.openclaw/agents/moviemaster/workspace/skills/fish-speech-tts/main.py \
  smart-tts --text "太好了！我们成功了！哈哈，真是太开心了！" \
  --ref "D:/Project/二十四节气/配音修改/momo参考音.mp3" \
  --output "E:/fish-speech/output/happy_scene.mp3" \
  --verbose
```

**输出示例**:
```
文本已分割为 3 段

处理第 1/3 段: 太好了！...
  ✅ 生成成功: output/temp_seg_000.mp3 (45.2 KB)

处理第 2/3 段: 我们成功了！...
  ✅ 生成成功: output/temp_seg_001.mp3 (48.1 KB)

处理第 3/3 段: 哈哈，真是太开心了！...
  ✅ 生成成功: output/temp_seg_002.mp3 (52.3 KB)

=== 情绪分析结果 ===
  段 1: happy (1200ms)
    文本: 太好了！
  段 2: happy (1500ms)
    文本: 我们成功了！
  段 3: happy (1800ms)
    文本: 哈哈，真是太开心了！

合成完成: 3/3 段成功
✅ 完整音频已生成: E:/fish-speech/output/happy_scene.mp3
```

### 场景 4: 分析台词情绪

```bash
E:/fish-speech/.venv/Scripts/python.exe \
  H:/OpenClaw/.openclaw/agents/moviemaster/workspace/skills/fish-speech-tts/main.py \
  analyze --text "对不起，我真的很难过……"
```

**输出**:
```
文本: 对不起，我真的很难过……
情绪: sad (强度: 0.67)
节奏: slow
停顿: 0.6s
重音: 真的

Fish Speech 参数:
  temperature: 0.60
  top_p: 0.75
  repetition_penalty: 1.10
  chunk_length: 150
```

### 场景 5: 音色库管理

#### 添加音色

```bash
E:/fish-speech/.venv/Scripts/python.exe \
  H:/OpenClaw/.openclaw/agents/moviemaster/workspace/skills/fish-speech-tts/main.py \
  voice add \
  --id "momo_happy" \
  --name "MOMO-开心" \
  --audio "D:/Project/二十四节气/配音修改/momo参考音.mp3" \
  --description "MOMO 角色开心状态" \
  --gender "female" \
  --language "zh" \
  --emotion "happy" "excited" \
  --register
```

#### 列出所有音色

```bash
E:/fish-speech/.venv/Scripts/python.exe \
  H:/OpenClaw/.openclaw/agents/moviemaster/workspace/skills/fish-speech-tts/main.py \
  voice list
```

#### 按情绪筛选

```bash
E:/fish-speech/.venv/Scripts/python.exe \
  H:/OpenClaw/.openclaw/agents/moviemaster/workspace/skills/fish-speech-tts/main.py \
  voice list --emotion "happy"
```

#### 同步本地库与 API

```bash
E:/fish-speech/.venv/Scripts/python.exe \
  H:/OpenClaw/.openclaw/agents/moviemaster/workspace/skills/fish-speech-tts/main.py \
  voice sync
```

### 场景 6: 批量配音

创建脚本文件 `scene1.json`:

```json
[
  {
    "text": "你好，好久不见！",
    "voice_id": "momo_happy",
    "output": "scene1_line001.mp3"
  },
  {
    "text": "最近怎么样？",
    "voice_id": "momo_neutral",
    "output": "scene1_line002.mp3"
  },
  {
    "text": "对不起，我真的很想你……",
    "voice_id": "momo_sad",
    "emotion": "sad",
    "output": "scene1_line003.mp3"
  }
]
```

运行批量配音:

```bash
E:/fish-speech/.venv/Scripts/python.exe \
  H:/OpenClaw/.openclaw/agents/moviemaster/workspace/skills/fish-speech-tts/main.py \
  batch --script "scene1.json" --output-dir "E:/fish-speech/output/scene1/"
```

## 🧠 情绪分析引擎

### 支持的情绪类型

| 情绪 | 关键词示例 | 参数特征 |
|------|-----------|---------|
| **happy** | 哈哈、太好了、真棒、开心 | temperature: 0.8, top_p: 0.85 |
| **sad** | 呜呜、难过、伤心、对不起 | temperature: 0.6, top_p: 0.75 |
| **angry** | 混蛋、气死、烦死、滚 | temperature: 0.85, top_p: 0.9 |
| **surprised** | 什么、怎么可能、天哪 | temperature: 0.85, top_p: 0.9 |
| **tender** | 亲爱的、宝贝、我爱你 | temperature: 0.65, top_p: 0.7 |
| **sarcastic** | 呵呵、是啊、你可真行 | temperature: 0.75, top_p: 0.8 |
| **fearful** | 害怕、恐惧、不要、救命 | temperature: 0.7, top_p: 0.75 |
| **neutral** | （默认） | temperature: 0.7, top_p: 0.8 |

### 情绪识别规则

1. **关键词匹配** — 基于预设情绪关键词库
2. **标点符号影响** — 感叹号增强情绪、问号表示疑惑、省略号表示犹豫
3. **上下文提示** — 可通过 `--emotion` 参数手动指定情绪（覆盖自动分析）

### 节奏控制

- **语速**: 基于情绪和句长自动判断（fast/normal/slow）
- **停顿**: 句末自动插入停顿（0.3-0.8 秒）
- **重音**: 识别"最+形容词"、"非常+形容词"等模式

## 📚 音色库管理

### 目录结构

```
voice_profiles/
├── voices.json          # 音色档案（JSON）
└── audio/               # 参考音频文件
    ├── momo_happy.mp3
    ├── momo_sad.mp3
    └── ...
```

### 音色档案字段

```json
{
  "id": "momo_happy",
  "name": "MOMO-开心",
  "description": "MOMO 角色开心状态",
  "gender": "female",
  "age_range": "20-30",
  "language": "zh",
  "emotion_tags": ["happy", "excited"],
  "ref_audio_path": "voice_profiles/audio/momo_happy.mp3",
  "ref_text": "参考音频对应的文本（可选）",
  "registered": true,
  "metadata": {}
}
```

### API 注册流程

1. **添加到本地库** — `voice add` 命令
2. **注册到 API** — `voice register` 命令（或 `--register` 参数）
3. **使用已注册音色** — `tts --voice-id momo_happy`

## 🎛️ 高级用法

### 自定义情绪参数

```bash
E:/fish-speech/.venv/Scripts/python.exe \
  H:/OpenClaw/.openclaw/agents/moviemaster/workspace/skills/fish-speech-tts/main.py \
  tts --text "你好" \
  --temperature 0.9 \
  --top-p 0.95 \
  --repetition-penalty 1.2 \
  --output "test.mp3"
```

### 控制停顿

```bash
E:/fish-speech/.venv/Scripts/python.exe \
  H:/OpenClaw/.openclaw/agents/moviemaster/workspace/skills/fish-speech-tts/main.py \
  smart-tts --text "第一句。第二句。第三句。" \
  --silence-ms 1000 \
  --output "with_long_pause.mp3"
```

### 禁用段落停顿

```bash
E:/fish-speech/.venv/Scripts/python.exe \
  H:/OpenClaw/.openclaw/agents/moviemaster/workspace/skills/fish-speech-tts/main.py \
  smart-tts --text "连续说话不要停顿" \
  --no-silence \
  --output "no_pause.mp3"
```

## 🐍 Python API 调用

### 简单合成

```python
from src.synthesizer import SimpleSynthesizer

synth = SimpleSynthesizer(api_base="http://127.0.0.1:18791")
synth.synthesize(
    text="你好世界",
    output_path="output/hello.mp3",
    ref_audio="reference.mp3"
)
```

### 智能合成（带情绪分析）

```python
from src.synthesizer import MultiSegmentSynthesizer

synth = MultiSegmentSynthesizer(
    api_base="http://127.0.0.1:18791",
    output_dir="output"
)

results = synth.synthesize_with_analysis(
    text="太好了！我们成功了！",
    output_path="output/happy.mp3",
    ref_audio="reference.mp3",
    context={"emotion_hint": "happy"},  # 可选：手动指定情绪
    add_silence=True,
    silence_duration_ms=500
)

for r in results:
    print(f"段 {r.segment_index}: {r.emotion} - {'成功' if r.success else '失败'}")
```

### 音色库管理

```python
from src.voice_library import VoiceLibrary

library = VoiceLibrary(library_dir="voice_profiles")

# 添加音色
profile = library.add_voice(
    voice_id="momo_happy",
    name="MOMO-开心",
    ref_audio_path="momo_ref.mp3",
    gender="female",
    emotion_tags=["happy", "excited"]
)

# 注册到 API
library.register_to_api("momo_happy")

# 列出所有音色
voices = library.list_voices()
for v in voices:
    print(f"{v.id}: {v.name} (已注册: {v.registered})")
```

### 台词分析

```python
from src.text_analyzer import TextAnalyzer

analyzer = TextAnalyzer()
result = analyzer.analyze("顾栖上台缺了这件首饰，狂热粉丝能掀翻整栋场馆！")

print(f"情绪: {result.emotion.emotion} (强度: {result.emotion.intensity})")
print(f"节奏: {result.rhythm.speed}")
print(f"Fish Speech 参数: {result.voice_params}")
```

## 📋 参考音频要求

- **时长**: 10~30 秒效果最佳
- **格式**: WAV / MP3 / FLAC
- **质量**: 清晰人声，无明显背景噪音
- **内容**: 建议包含目标情绪的朗读

## 🗂️ 关键目录

| 目录 | 用途 |
|------|------|
| `skills/fish-speech-tts/` | 技能根目录 |
| `skills/fish-speech-tts/main.py` | CLI 入口 |
| `skills/fish-speech-tts/src/` | 核心模块 |
| `skills/fish-speech-tts/voice_profiles/` | 音色库 |
| `skills/fish-speech-tts/output/` | 默认输出目录 |
| `E:/fish-speech/` | Fish Speech 仓库 |
| `E:/fish-speech/references/` | API 端参考音频 |

## ⚠️ 注意事项

1. **API 必须先启动** — 所有命令都依赖 Fish Speech API 运行
2. **pydub + FFmpeg** — 多段合成需要 pydub 和 FFmpeg
3. **中文/英文/日文效果最佳** — 支持 80+ 语言
4. **参考音频越清晰，克隆效果越好**
5. **每条台词大约 3~5 秒生成时间**（RTX 5090）
6. **情绪分析基于规则** — 复杂语境可能需要手动指定情绪

## 🔄 版本历史

### v2.0.0 (2026-06-25)

- ✅ 新增情绪分析引擎
- ✅ 新增多段合成器
- ✅ 新增音色库管理
- ✅ 新增批量配音功能
- ✅ 重写 CLI 入口（main.py）
- ✅ 修复 base64 编码 bug
- ✅ 完整文档和示例

### v1.0.0 (初始版本)

- ✅ 基础声音克隆
- ✅ 简单 TTS
- ✅ 批量配音（JSON 脚本）

## 📖 相关文档

- Fish Speech 官方文档: `E:/fish-speech/docs/`
- API 文档: `http://127.0.0.1:18791/docs`
- 技能开发指南: OpenClaw 文档

---

**维护者**: 电影大师 (moviemaster)  
**最后更新**: 2026-06-25
