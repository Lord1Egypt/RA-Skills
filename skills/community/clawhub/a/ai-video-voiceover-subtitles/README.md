# AI配音

「AI配音」是一个把视频文字稿一键生成多角色配音（WAV）和带时间轴 SRT 字幕的 Agent 技能：音色用账号已有角色或参考音频声音克隆，覆盖口播、电影解说、小说推文、带货、广告片和有声书，本地无需显卡。

- 文字稿 → 多角色配音 WAV + 带时间轴 SRT 字幕 + 逐句时间 JSON，一条命令
- 账号已有角色或参考音频声音克隆；语气标签、0.25–4 倍语速；已有音视频识别成字幕
- 6 个节奏预设（口播、解说、带货、数字人、广告片、有声书）；本地无需显卡

## 安装

把本文件夹 `miragea-video-voiceover/` 复制到 Agent 的 skills 目录（如 `~/.claude/skills/`、`~/.codex/skills/`）即可，也可以在技能市场一键安装。完整用法、写稿方法和 FAQ 见 [SKILL.md](./SKILL.md)。

需要 Python 3.9+ 和环境变量 `MIRAGEA_API_KEY`（在 https://miragea.ai/workspace/api 生成）；没有 Key 可先加 `--dry-run` 离线试跑。配音与字幕由 Miragea（https://miragea.ai）提供。
