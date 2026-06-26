---
name: classroom-note-translator
summary: 将英文课堂音视频转成中文可学习笔记，支持 Markdown 输出，并可同步到 Notion 或导入 Obsidian。
description: 接收课堂录音、讲座音频或视频文件（视频会先抽取音轨），调用 SenseAudio HTTP ASR API 进行英文转录，可选直出中文翻译；随后整理为结构化 Markdown 学习笔记，包含摘要、关键概念、术语表、时间轴与复习问题，生成到桌面，并支持导出到 Notion 或保存到 Obsidian vault。
homepage: https://senseaudio.cn/docs/speech_recognition/http_api
user-invocable: true
metadata: {"openclaw":{"emoji":"🎓","homepage":"https://senseaudio.cn/docs/speech_recognition/http_api","primaryEnv":"SENSEAUDIO_API_KEY","requires":{"bins":["python3"],"env":["SENSEAUDIO_API_KEY"]},"skillKey":"classroom-note-translator"}}
---

# 课堂听译笔记官

当用户希望把**英文课堂录音、讲座、组会、YouTube 学习音频/视频**整理成中文笔记时，使用这个 skill。
触发（更明确）：
- 用户明确提到“总结”课堂内容
- 用户明确提到“转译/翻译”课堂音视频内容
- 用户明确提到“做中英对照笔记”或“整理课堂笔记”
- 用户提供网页链接并希望从页面里的音视频提取后再做总结/转译
非触发：
- 仅做逐字转写、且不需要总结和中英对照时
适用场景：
- 国外课堂听讲太快，想保留英文原文并生成中文笔记
- 学术报告、课程录音、线上讲座需要整理成复习材料
- 希望得到 Markdown 文档，并进一步导入 Notion 或 Obsidian

## 你应该做什么

1. 收集或确认以下输入：
   - 输入来源（三选一）：音频路径 / 视频路径 / 页面链接（从页面提取媒体）
   - 课程标题或主题（可选）
   - 是否需要说话人分离
   - 是否需要句级或字级时间戳
   - 输出目录（必填，使用用户指定目录）
   - 是否导出到 Notion
   - 是否写入 Obsidian vault
2. 运行脚本：

```bash
python3 "{baseDir}/scripts/classroom_note_translator.py" \
  --audio "<AUDIO_PATH>" \
  # 或 --video "<VIDEO_PATH>" \
  # 或 --page-url "<PAGE_URL>" \
  --title "<TITLE_OR_TOPIC>" \
  --model sense-asr-pro \
  --language en \
  --target-language zh \
  --timestamps segment \
  --speaker-diarization \
  --summary-provider local \
  --output-dir "<USER_SPECIFIED_OUTPUT_DIR>"
```

3. 如果用户想导出到 Notion，则追加：

```bash
  --export-notion \
  --notion-parent-page-id "<NOTION_PAGE_ID>"
```

4. 如果用户想写入 Obsidian，则追加：

```bash
  --export-obsidian \
  --obsidian-vault "/absolute/path/to/your/vault" \
  --obsidian-folder "Lecture Notes"
```

## 输出内容

脚本每次都会同时生成：
- `*_transcript.json`：SenseAudio 原始响应
- `*_summary.md`：结构化中文学习总结（Markdown）
- `*_bilingual.txt`：英文原文 + 中文翻译拼接文本

Markdown 文档默认包含：
- 标题与元信息
- 中文摘要
- 关键要点
- 术语表
- 带时间轴的内容梳理
- 复习问题
- 英文原文摘录

## 参数选择建议

- 默认优先用 `sense-asr-pro`：适合课堂、会议、复杂语音环境。
- 若追求更低成本，可改为 `sense-asr`。
- 若只要快速粗转写，不需要翻译/时间戳/说话人分离，不建议用本 skill，改用轻量转写更合适。
- 对于长音频，先切片再分别处理；SenseAudio 官方文档建议单文件不超过 10MB。

## 环境变量

- `SENSEAUDIO_API_KEY`：必填，SenseAudio API Key
- `OPENAI_API_KEY`：可选，仅当 `--summary-provider openai-compatible` 时需要
- `OPENAI_BASE_URL`：可选，OpenAI 兼容接口地址
- `NOTION_TOKEN`：可选，导出到 Notion 时需要

## 本地依赖

- 若使用 `--video`，需本机安装 `ffmpeg`（用于抽取音轨）

## 注意事项

- SenseAudio 文档显示，`sense-asr` 与 `sense-asr-pro` 支持翻译、句级/字级时间戳、说话人分离与情感分析；HTTP 接口为 `POST https://api.senseaudio.cn/v1/audio/transcriptions`，采用 `multipart/form-data` 与 Bearer Token。
- 若使用 `--page-url`，脚本会先抓取页面 HTML，优先提取 `og:video/og:audio` 和 `<video>/<audio>/<source>` 的 `src`，下载后再处理；部分站点（需登录、DRM、动态脚本拼接媒体地址）可能提取失败。
- 若 Obsidian vault 不可写，则只生成 Markdown 文件，由用户自行导入。
- 若未配置 Notion token，则跳过 Notion 导出。
- 若用户没有给出标题，可由文件名自动生成。
