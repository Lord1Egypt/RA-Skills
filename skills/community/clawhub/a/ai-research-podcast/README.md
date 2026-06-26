# AI 研报速读播客

> 将研报/长文自动转化为可收听的播客音频

## 业务场景

**痛点**：
- 每天大量研报、长文、技术文档，根本看不过来
- 通勤、运动、做家务时想"听"内容学习
- 传统 TTS 依赖云端，隐私泄露风险
- 人工摘要费时费力，错过关键信息

**解决方案**：一键将任意研报/URL 转化为自然语音播客

## Skill 编排图谱

```
┌─────────────────────────────────────────────────────────────┐
│                    AI 研报速读播客                            │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────┐    ┌──────────────┐    ┌──────────────────┐   │
│  │ 输入源  │    │   处理引擎   │    │    输出通道      │   │
│  ├─────────┤    ├──────────────┤    ├──────────────────┤   │
│  │ • URL   │───▶│ 1.summarize  │───▶│ • 本地音频文件   │   │
│  │ • PDF   │    │   (内容抓取  │    │ • Feishu 推送   │   │
│  │ • 文本  │    │   + 摘要)    │    │ • 微信推送      │   │
│  └─────────┘    │              │    │ • 邮件发送      │   │
│                 │ 2.sherpa-    │    └──────────────────┘   │
│                 │   onnx-tts   │                           │
│                 │   (离线TTS)  │                           │
│                 └──────────────┘                           │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## 参与技能

| Skill | 作用 | 来源 |
|-------|------|------|
| **summarize** | 抓取 URL/PDF 内容并生成摘要 | 本地 skills/summarize |
| **sherpa-onnx-tts** | 离线语音合成，无需云端 API | steipete/clawdis |
| **message** | 推送音频到指定渠道 | OpenClaw 内置 |

## 使用示例

### 基础用法

```
用户: 帮我把这篇研报转成音频
URL: https://example.com/ai-trend-report-2026.pdf

Agent 执行:
1. summarize 抓取 PDF 并生成 500 字摘要
2. sherpa-onnx-tts 将摘要转为 MP3
3. 返回音频文件路径或直接推送
```

### 进阶用法

```
用户: 每天早上 8 点把 AI 领域最新论文转成音频推给我

Agent 执行:
1. 设置 cron 定时任务
2. 定时触发: arxiv 搜索 → summarize → tts → message 推送
```

### 完整工作流

```bash
# Step 1: 抓取并摘要
summarize https://arxiv.org/abs/2401.xxxxx --output report.md

# Step 2: 生成音频
sherpa-onnx-tts --input report.md --output podcast.mp3 --voice zh_CN-female

# Step 3: 推送 (可选)
message --target feishu --file podcast.mp3 --text "今日 AI 研报速读"
```

## 配置说明

### 依赖安装

```bash
# summarize CLI
npm install -g @openclaw/summarize-cli

# sherpa-onnx TTS
pip install sherpa-onnx
# 或使用预编译版本
brew install sherpa-onnx  # macOS
```

### 音色选择

| 音色 ID | 描述 |
|---------|------|
| `zh_CN-female` | 中文女声（默认） |
| `zh_CN-male` | 中文男声 |
| `en_US-female` | 英文女声 |
| `en_US-male` | 英文男声 |

## 输出格式

- **格式**: MP3 / WAV
- **码率**: 128kbps (可配置)
- **采样率**: 16000Hz
- **文件大小**: 约 1MB / 分钟

## 扩展场景

1. **技术博客速听**: 每日自动抓取指定博客并转音频
2. **会议纪要播报**: 会议记录 → 摘要 → 语音通知
3. **新闻简报**: 多源聚合 → 综合摘要 → 早间播客
4. **学习笔记复习**: 笔记 → TTS → 睡前复习

## 技术亮点

- **完全离线**: sherpa-onnx 无需联网，隐私安全
- **低成本**: 无 API 调用费用
- **可定制**: 支持自定义音色、语速、停顿
- **跨平台**: Linux / macOS / Windows 均可运行

---

**创建时间**: 2026-03-24
**版本**: v1.0.0
**作者**: OpenClaw Agent