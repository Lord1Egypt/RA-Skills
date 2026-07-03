---
name: edge-tts-zh
description: 中文语音合成（Text-to-Speech），使用Microsoft Edge TTS引擎，无需API key，完全免费。内置中文最佳声音列表（男声/女声/不同风格）。适用于：(1)将文字转为语音消息 (2)新闻/文章朗读 (3)语音通知和提醒 (4)播客/视频配音。支持语速/音调调节和字幕生成。
---

# 中文语音合成 (edge-tts)

使用 Microsoft Edge TTS 引擎生成高质量中文语音，完全免费。

## 快速使用

```bash
# 基础用法 - 默认男声
python3 {baseDir}/scripts/speak.py "你好，今天天气怎么样？"

# 指定声音
python3 {baseDir}/scripts/speak.py "今日新闻简报" --voice xiaoxiao

# 调整语速
python3 {baseDir}/scripts/speak.py "慢速朗读" --rate -20%
python3 {baseDir}/scripts/speak.py "快速朗读" --rate +30%

# 保存到文件
python3 {baseDir}/scripts/speak.py "保存这段话" --output speech.mp3

# 从文件读取文本
python3 {baseDir}/scripts/speak.py --file article.txt --voice xiaoxiao
```

## 中文声音列表

### 推荐声音

| 简称 | 全名 | 性别 | 风格 |
|------|------|------|------|
| yunxi | zh-CN-YunxiNeural | 男 | 自然、年轻 **（推荐）** |
| yunyang | zh-CN-YunyangNeural | 男 | 新闻播报 |
| yunjian | zh-CN-YunjianNeural | 男 | 阳刚、有力 |
| xiaoxiao | zh-CN-XiaoxiaoNeural | 女 | 温暖、活泼 |
| xiaoyi | zh-CN-XiaoyiNeural | 女 | 知性、优雅 |
| xiaomeng | zh-CN-XiaomengNeural | 女 | 可爱、甜美 |

### 其他方言/地区

| 简称 | 全名 | 地区 |
|------|------|------|
| tw-male | zh-TW-YunJheNeural | 台湾男声 |
| tw-female | zh-TW-HsiaoChenNeural | 台湾女声 |
| hk-male | zh-HK-WanLungNeural | 粤语男声 |
| hk-female | zh-HK-HiuGaaiNeural | 粤语女声 |

## 参数说明

- `--voice NAME` — 声音简称或完整名称（默认: yunxi）
- `--rate RATE` — 语速调整，如 `+20%` 或 `-10%`（默认: +10%）
- `--pitch PITCH` — 音调调整，如 `+5Hz` 或 `-2st`
- `--output FILE` — 输出文件路径（默认: /tmp/tts-output.mp3）
- `--file FILE` — 从文件读取文本
- `--format FORMAT` — 输出格式: mp3, ogg（默认: mp3）
- `--list` — 列出所有可用中文声音

## 安装

脚本自动检测 edge-tts，未安装时提示：
```bash
pip install edge-tts
```
