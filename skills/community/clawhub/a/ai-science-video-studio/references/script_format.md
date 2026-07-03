# Script Format Specification (script.json)

## Overview

The `script.json` file defines the complete video structure. Every AI science video
follows a 5-paragraph format: intro + 3 content sections + outro.

## Schema

```json
{
  "title": "视频标题",
  "topic": "视频主题简述",
  "total_duration": 104,
  "resolution": "1280x720",
  "fps": 24,
  "segments": {
    "intro": {
      "type": "digital_human",
      "engine": "google_flow",
      "duration": 10,
      "narration": "开场旁白文本（约50-60字）",
      "flow_prompt": "Google Flow 英文或中文提示词，描述数字人场景和表情",
      "notes": "开场说明"
    },
    "content_1": {
      "type": "slides",
      "engine": "pillow",
      "duration": 30,
      "narration": "第一段正文旁白文本",
      "slides_content": [
        "幻灯片第一行内容",
        "幻灯片第二行内容"
      ],
      "notes": "本段说明"
    },
    "content_2": {
      "type": "slides",
      "engine": "pillow",
      "duration": 25,
      "narration": "第二段正文旁白文本",
      "slides_content": ["..."],
      "notes": "..."
    },
    "content_3": {
      "type": "slides",
      "engine": "pillow",
      "duration": 29,
      "narration": "第三段正文旁白文本",
      "slides_content": ["..."],
      "notes": "..."
    },
    "outro": {
      "type": "digital_human",
      "engine": "google_flow",
      "duration": 10,
      "narration": "结尾旁白文本",
      "flow_prompt": "Google Flow 提示词",
      "notes": "结尾说明"
    }
  }
}
```

## Field Descriptions

### Top-Level

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| title | string | Yes | Video title (used for file naming) |
| topic | string | Yes | Brief topic description |
| total_duration | number | Yes | Sum of all segment durations |
| resolution | string | Yes | Video resolution, default "1280x720" |
| fps | number | Yes | Frame rate, default 24 |

### Segment Object

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| type | "digital_human" or "slides" | Yes | Segment type |
| engine | "google_flow", "sadtalker", or "pillow" | Yes | Generation engine |
| duration | number | Yes | Target video duration in seconds |
| narration | string | Yes | Narration/voiceover text |
| flow_prompt | string | Only for "digital_human" | Google Flow generation prompt |
| slides_content | string[] | Only for "slides" | Lines of content for slide rendering |
| notes | string | No | Internal production notes |

## Duration Guidelines

- Intro: 8-12 seconds (one concise opening statement)
- Content segments: 25-35 seconds each (~60-90 Chinese characters narration)
- Outro: 8-12 seconds (summary + call to action)
- Total: 90-120 seconds for standard explainer video

## Narration Writing Rules

1. Each segment narration should be ≤15 seconds worth of speech
2. For Chinese: approximately 4-5 characters per second → ~60 chars per 15s
3. Avoid words that TTS engines commonly mispronounce:
   - Compound technical terms: add commas between parts
   - Multi-phoneme characters: test with edge-tts first if unsure
4. Keep sentences short and natural — what sounds natural when spoken aloud

## Example: "What is Claude Code"

```json
{
  "title": "什么是Claude Code",
  "topic": "Anthropic推出的AI编程工具Claude Code介绍",
  "total_duration": 104,
  "resolution": "1280x720",
  "fps": 24,
  "segments": {
    "intro": {
      "type": "digital_human",
      "engine": "google_flow",
      "duration": 10,
      "narration": "大家好，我是才林。今天我们来聊聊Anthropic推出的AI编程工具——Claude Code。",
      "flow_prompt": "Chinese female tech presenter introducing Claude Code, warm professional smile, modern office background, speaking directly to camera",
      "notes": "开场自我介绍+点题"
    },
    "content_1": {
      "type": "slides",
      "engine": "pillow",
      "duration": 30,
      "narration": "Claude Code 是一个基于命令行的AI编程助手，它可以直接在你的终端中运行。你只需要输入普通的中文描述，它就能帮你写代码、调试、重构，甚至部署应用。",
      "slides_content": [
        "$ claude-code init my-project",
        "> 正在初始化项目...",
        "> 已创建 package.json",
        "> 项目初始化完成！",
        "",
        "# 用中文描述你的需求",
        "# Claude Code 自动生成代码"
      ],
      "notes": "介绍基本概念和使用方式"
    }
  }
}
```

## Script Validation Checklist

Before proceeding to generation, verify:
- [ ] All 5 segments are defined (intro, 3× content, outro)
- [ ] Each narration matches its target duration (~4-5 chars/second for Chinese)
- [ ] `total_duration` equals sum of all segment durations
- [ ] intro and outro have valid `flow_prompt` values
- [ ] content segments have meaningful `slides_content` arrays
- [ ] No markdown formatting in narration text (it will be spoken by TTS)
