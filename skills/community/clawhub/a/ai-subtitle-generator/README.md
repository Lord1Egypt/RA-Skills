# 字幕生成

「字幕生成」是一个把本地视频或音频自动识别成带时间轴 SRT 字幕（也可导出 TXT 文字稿或 JSON）的 Agent 技能，用于视频自动加字幕、音频转字幕和音频转文字；给文字稿配音时也能同步出字幕，本地无需显卡。

- 本地视频 / 音频 → 带时间轴 SRT，或 TXT 文字稿、JSON 分段
- 提交前读取实时费率、文件大小和时长上限；任务可续查不重复提交
- 配音稿同步生成 SRT 和逐句时间轴；ffmpeg / 剪映直接加到视频

## 安装

把本文件夹 `ai-subtitle-generator/` 复制到 Agent 的 skills 目录（如 `~/.claude/skills/`、`~/.codex/skills/`）即可，也可以在技能市场一键安装。完整用法、写稿方法和 FAQ 见 [SKILL.md](./SKILL.md)。

需要 Python 3.9+ 和环境变量 `MIRAGEA_API_KEY`（在 https://miragea.ai/workspace/api 生成）；没有 Key 可先加 `--dry-run` 离线试跑。配音与字幕由 Miragea（https://miragea.ai）提供。
