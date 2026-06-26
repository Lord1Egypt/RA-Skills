# 火山引擎视频点播 VOD 配置

# --- 执行模式 ---
# 留空自动检测（apig > cloud > local），或显式指定:
#   apig  - SkillHub 网关（需 ARK_SKILL_API_BASE + ARK_SKILL_API_KEY）
#   cloud - 直连火山引擎 OpenAPI（需 VOLC_ACCESS_KEY_* + VOLC_SPACE_NAME + ASR_*）
#   local - 完全本地执行（Qwen-ASR / Demucs / ffmpeg），无需任何云端环境变量和 VOD 空间

EXECUTION_MODE=

# --- SkillHub / APIG（勿写入本文件）---
# `ARK_SKILL_API_BASE`、`ARK_SKILL_API_KEY` 由容器或宿主在运行时注入进程环境，
# 脚本与 Python 通过 `os.getenv` / 环境变量读取，无需也不宜写入 `.env`。
# 本地调试可自行 `export ARK_SKILL_API_BASE=...`、`export ARK_SKILL_API_KEY=...`。

# 火山引擎 Access Key ID

VOLC_ACCESS_KEY_ID=

# 火山引擎 Access Key Secret

VOLC_ACCESS_KEY_SECRET=

# 点播空间名称

VOLC_SPACE_NAME=

# 导出时是否跳过字幕压制（默认跳过；0/false/no 表示启用字幕压制）

VOD_EXPORT_SKIP_SUBTITLE=1

# 审核页启动时是否自动打开浏览器（默认不打开；1/true/yes 表示打开）

TALKING_VIDEO_AUTO_EDIT_REVIEW_AUTO_OPEN=0

# （可选）产物工程根。未设置时由脚本从 SKILL_DIR 沿父目录固定层级推断；任意自定义目录树请显式填写。
# VOICEOVER_EDITING_PROJECT_ROOT=

# 豆包语音转写 API Key

ASR_API_KEY=

# 豆包语音转写 API Base URL

ASR_BASE_URL=https://openspeech.bytedance.com/api/v3/auc/bigmodel

# 是否进行导出视频剪辑：1 进行（默认），0 不进行。仅当有字幕或音频静音时生效；mute 段会从输出中移除，主时间轴从 0 起无缝拼接

TALKING_VIDEO_AUTO_EDIT_VIDEO_CUT=1
