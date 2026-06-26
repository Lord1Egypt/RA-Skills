# Edge TTS 中文转语音

将中文文章转换为语音音频（仅限中文）。

## 使用方法

### 方式1：直接输入文本
```bash
python3 edge_tts_chinese.py --text "你的中文文章内容"
```

### 方式2：从文件读取
```bash
python3 edge_tts_chinese.py --file 文章.txt
```

### 方式3：交互式输入
```bash
python3 edge_tts_chinese.py
# 然后粘贴文章内容，按 Ctrl+D 结束
```

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--text`, `-t` | 直接输入文章内容 | - |
| `--file`, `-f` | 从文件读取文章 | - |
| `--voice`, `-v` | 语音名称 | zh-CN-XiaoxiaoNeural |
| `--output`, `-o` | 输出文件路径 | /tmp/edge_tts_chinese.mp3 |

## 可用语音

| 语音 | 说明 |
|------|------|
| zh-CN-XiaoxiaoNeural | 中文女声（默认） |
| zh-CN-YunxiNeural | 中文男声 |
| zh-CN-XiaoyiNeural | 中文女声（年轻） |
| zh-CN-YunyangNeural | 中文男声（新闻） |

## 使用场景

- 随时需要将中文文章转为语音时使用
- 例如：新闻朗读、故事讲述、通知播报等

## 技术说明

- 使用 edge-tts（微软Edge浏览器语音合成）
- 支持长文本（5000+字符测试通过）
- 输出格式：MP3
