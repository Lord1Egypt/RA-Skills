# AI 音频内容审核 Skill

基于 SenseAudio ASR 的 Claude Skill，自动识别音频/视频中的语音内容，进行敏感词检测，生成结构化审核报告。深度语义审核由 Claude 直接完成。

## 核心功能

- **语音识别** — SenseAudio ASR 将音频转文字
- **敏感词扫描** — 内置 6 大类敏感词库 + 支持自定义关键词
- **深度语义审核** — Claude 直接分析转写文本，检测隐晦违规、擦边、虚假宣传等
- **情感分析** — 标注异常情绪片段
- **说话人分离** — 定位具体说话人的违规内容
- **批量审核** — 支持整个目录的音视频文件批量处理
- **结构化报告** — JSON + 可读文本双格式输出

## 项目结构

```
.
├── SKILL.md              # Skill 描述（Claude 读取）
├── scripts/
│   └── audio_audit.py    # ASR + 敏感词扫描脚本
├── outputs/              # 输出目录
├── README.md
└── USAGE.md              # 详细使用指南
```

## 环境要求

- Python 3.10+
- 依赖：`requests`
- 系统依赖：`ffmpeg`（视频音频提取）
- `SENSEAUDIO_API_KEY` — [SenseAudio 官网](https://senseaudio.cn) 获取（唯一需要的密钥）

## 适用场景

- 短视频/直播平台内容审核
- 播客/音频节目合规检查
- 企业内部会议内容审计
- 教育内容质量把控

## License

MIT

## Author

QWERTY0205
