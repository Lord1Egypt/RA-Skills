---
name: AI 研报速读播客
description: 当用户说：- "把这篇研报转成音频"- "帮我听听这篇文章"- "生成播客版本"
category: 图像
triggers:
---

# AI 研报速读播客

将研报、长文、技术文档自动转化为可收听的播客音频。

## 触发条件

当用户说：
- "把这篇研报转成音频"
- "帮我听听这篇文章"
- "生成播客版本"
- "URL 转语音"
- "研报速读"

## 执行流程

### 1. 内容抓取与摘要

使用 `summarize` 技能：

```bash
summarize "<source>" --max-length 500 --output /tmp/summary.md
```

支持的输入源：
- HTTP/HTTPS URL
- 本地 PDF 文件
- 本地 Markdown/文本文件
- 直接粘贴的文本

### 2. 语音合成

使用 `sherpa-onnx-tts` 技能：

```bash
sherpa-onnx-tts \
  --input /tmp/summary.md \
  --output /tmp/podcast.mp3 \
  --voice zh_CN-female \
  --speed 1.0
```

可选参数：
- `--voice`: 音色选择
- `--speed`: 语速 (0.5-2.0)
- `--output-format`: mp3/wav

### 3. 推送通知（可选）

如果用户指定推送渠道：

```bash
# Feishu
message --target feishu --file /tmp/podcast.mp3 --text "AI 研报速读"

# 微信
message --target wechat --file /tmp/podcast.mp3
```

## 示例对话

**用户**: 帮我把这篇论文转成音频 https://arxiv.org/abs/2401.12345

**Agent**:
1. 抓取论文内容并生成摘要...
2. 将摘要转为语音播客...
3. 完成！音频文件：`/tmp/podcast_2401.12345.mp3` (时长 3:42)

**用户**: 每天早上 8 点自动推送最新的 AI 论文音频

**Agent**:
好的，已设置定时任务。每天 8:00 会自动：
1. 抓取 arXiv cs.AI 最新论文
2. 生成摘要并转音频
3. 推送到你的飞书

## 注意事项

- sherpa-onnx 需要首次下载语音模型（约 100MB）
- 离线模式，无需联网，隐私安全
- 建议摘要长度控制在 300-800 字，音频时长 2-5 分钟