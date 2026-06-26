# audio-analyze-skill-for-openclaw

高精度转录并分析音频/视频内容。[由 Evolink.ai 驱动](https://evolink.ai/?utm_source=github&utm_medium=skill&utm_campaign=audio-analyze)

🌐 English | [日本語](README.ja.md) | [简体中文](README.zh-CN.md) | [한국어](README.ko.md) | [Español](README.es.md) | [Français](README.fr.md) | [Deutsch](README.de.md) | [Türkçe](README.tr.md) | [Русский](README.ru.md)

## 这是什么？

使用 Gemini 3.1 Pro 自动转录和分析您的音频/视频文件。[获取免费的 API 密钥 →](https://evolink.ai/signup?utm_source=github&utm_medium=skill&utm_campaign=audio-analyze)

## 安装

### 通过 ClawHub 安装（推荐）

```bash
openclaw skills add https://github.com/EvoLinkAI/audio-analyze-skill-for-openclaw
```

### 手动安装

```bash
git clone https://github.com/EvoLinkAI/audio-analyze-skill-for-openclaw
cd audio-analyze-skill-for-openclaw
pip install -r requirements.txt
```

## 配置

| 变量 | 描述 | 默认值 |
| :--- | :--- | :--- |
| `EVOLINK_API_KEY` | EvoLink API 密钥 | （必填） |
| `EVOLINK_MODEL` | 转录模型 | gemini-3.1-pro-preview-customtools |

*有关详细的 API 配置和模型支持，请参阅 [EvoLink API 文档](https://docs.evolink.ai/en/api-manual/language-series/gemini-3.1-pro-preview-customtools/openai-sdk/openai-sdk-quickstart?utm_source=github&utm_medium=skill&utm_campaign=audio-analyze)。*

## 使用方法

### 基本用法

```bash
export EVOLINK_API_KEY="your-key-here"
./scripts/transcribe.sh audio.mp3
```

### 高级用法

```bash
./scripts/transcribe.sh audio.mp3 --diarize --lang ja
```

### 输出示例

* **摘要 (TL;DR)**：该音频是一段用于测试的样本音轨。
* **核心要点**：高保真音质，清晰的频率响应。
* **待办事项**：上传至生产环境进行最终测试。

## 可用模型

- **Gemini 系列** (OpenAI API — `/v1/chat/completions`)

## 文件结构

```
.
├── README.md
├── SKILL.md
├── _meta.json
├── scripts/
│   └── transcribe.sh
└── references/
    └── api-params.md
```

## 故障排除

- **参数列表过长 (Argument list too long)**：对于大型音频数据，请使用临时文件。
- **API 密钥错误 (API Key Error)**：请确保已导出 `EVOLINK_API_KEY`。

## 链接

- [ClawHub](https://clawhub.ai/EvoLinkAI/audio-analyze)
- [API 参考](https://docs.evolink.ai/en/api-manual/language-series/gemini-3.1-pro-preview-customtools/openai-sdk/openai-sdk-quickstart?utm_source=github&utm_medium=skill&utm_campaign=audio-analyze)
- [社区](https://discord.com/invite/5mGHfA24kn)
- [支持](mailto:support@evolink.ai)

## 许可证

MIT