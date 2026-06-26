## SSML 标记规范

SSML（Speech Synthesis Markup Language）用于精细控制语音合成效果。

### 基础结构

```xml
<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="zh-CN">
  <voice name="zh-CN-XiaoxiaoNeural">
    你好，欢迎收听本期节目。
  </voice>
</speak>
```

### 常用标记

#### 重音标注
```xml
<emphasis level="strong">关键词</emphasis>
<emphasis level="moderate">次要强调</emphasis>
<emphasis level="reduced">弱化内容</emphasis>
```

#### 停顿控制
```xml
<break time="300ms"/>   <!-- 短停顿（逗号级别）-->
<break time="600ms"/>   <!-- 中停顿（句号级别）-->
<break time="1000ms"/>  <!-- 长停顿（段落级别）-->
<break strength="weak"/>
<break strength="medium"/>
<break strength="strong"/>
```

#### 语速调节
```xml
<prosody rate="fast">快速内容</prosody>
<prosody rate="medium">正常内容</prosody>
<prosody rate="slow">慢速内容</prosody>
<prosody rate="1.2">120%语速</prosody>
<prosody rate="0.8">80%语速</prosody>
```

#### 音调变化
```xml
<prosody pitch="high">升调内容</prosody>
<prosody pitch="low">降调内容</prosody>
<prosody pitch="+10%">略微升高</prosody>
<prosody pitch="-10%">略微降低</prosody>
```

#### 音量控制
```xml
<prosody volume="loud">大声</prosody>
<prosody volume="soft">轻声</prosody>
<prosody volume="+6dB">增大6dB</prosody>
```

#### 组合使用
```xml
<prosody rate="fast" pitch="high" volume="loud">
  <emphasis level="strong">重要公告！</emphasis>
</prosody>
```

### 完整示例

```xml
<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="zh-CN">
  大家好，<break time="300ms"/>欢迎收听今天的节目。
  <break time="600ms"/>
  今天我们要聊的话题是<emphasis level="strong">人工智能</emphasis>。
  <break time="300ms"/>
  <prosody rate="slow">这是一个改变世界的技术。</prosody>
  <break time="1000ms"/>
  让我们开始吧！
</speak>
```

### ElevenLabs 情感控制

ElevenLabs 不使用标准 SSML，而是通过 stability 和 similarity_boost 参数控制：

```python
voice_settings = {
    "stability": 0.5,          # 0-1，越低越有情感起伏
    "similarity_boost": 0.75,  # 0-1，越高越接近原始音色
    "style": 0.5,              # 0-1，风格强度（v2模型）
    "use_speaker_boost": True
}
```

| 情感 | stability | similarity_boost |
|------|-----------|-----------------|
| calm | 0.8 | 0.75 |
| warm | 0.5 | 0.75 |
| energetic | 0.3 | 0.7 |
| professional | 0.7 | 0.8 |
