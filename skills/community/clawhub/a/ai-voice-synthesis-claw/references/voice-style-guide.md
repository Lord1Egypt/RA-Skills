## 音色库与风格指南

### 内置音色映射

| 音色标识 | 描述 | 适用场景 |
|---------|------|---------|
| `warm-female` | 温柔细腻的女声 | 情感故事、生活类内容 |
| `professional-male` | 沉稳专业的男声 | 知识讲解、新闻资讯 |
| `professional-female` | 清晰干练的女声 | 知识讲解、教程内容 |
| `magnetic-male` | 磁性有力的男声 | 商业广告、产品介绍 |
| `young-energetic` | 活泼俏皮的年轻音色 | 娱乐内容、短视频 |
| `calm-narrator` | 平稳舒缓的旁白音色 | 纪录片、有声读物 |

### ElevenLabs 音色 ID 映射

```python
VOICE_MAP = {
    "warm-female": "21m00Tcm4TlvDq8ikWAM",       # Rachel
    "professional-male": "ErXwobaYiN019PkySvjV",   # Antoni
    "professional-female": "EXAVITQu4vr4xnSDxMaL", # Bella
    "magnetic-male": "VR6AewLTigWG4xSOukaG",       # Arnold
    "young-energetic": "pNInz6obpgDQGcFmaJgB",     # Adam
    "calm-narrator": "yoZ06aMxZJJ28mfd3POQ",       # Sam
}
```

### OpenAI TTS 音色映射

```python
OPENAI_VOICE_MAP = {
    "warm-female": "nova",
    "professional-male": "onyx",
    "professional-female": "shimmer",
    "magnetic-male": "echo",
    "young-energetic": "fable",
    "calm-narrator": "alloy",
}
```

### 语速规范

| 内容类型 | 推荐语速 | rate 参数 |
|---------|---------|----------|
| 知识讲解 | 200-220字/分 | `normal` |
| 故事叙述 | 180-200字/分 | `slow` |
| 广告配音 | 220-250字/分 | `fast` |
| 新闻播报 | 220-240字/分 | `fast` |
| 有声读物 | 180-200字/分 | `slow` |

### 停顿规则

| 停顿类型 | 时长 | 触发位置 |
|---------|------|---------|
| 逗号停顿 | 300ms | ，, |
| 句号停顿 | 600ms | 。.!? |
| 段落停顿 | 1000ms | 段落间空行 |
| 强调停顿 | 200ms | 关键词前后 |

### 情感风格

- **calm**：平稳、中性、适合信息传达
- **warm**：亲切、温暖、适合情感类内容
- **professional**：权威、严肃、适合商务场景
- **energetic**：充满活力、积极向上、适合娱乐内容
