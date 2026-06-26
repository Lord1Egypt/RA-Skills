# 顶层运行时契约（详细版）

> **触发条件**：当遇到凭据异常、环境变量缺失、二进制找不到、副作用超出预期或门控不生效时 Read 本文件。  
> 摘要已内嵌在根 `SKILL.md`，日常路由无需额外加载本文件。

---

## 凭据与本地持久化

| 项 | 说明 |
|----|------|
| 项目密钥 | `skills/chanjing-content-creation-skill/.env`（`CHANJING_APP_ID`、`CHANJING_SECRET_KEY`） |
| 凭据文件 | `skills/chanjing-content-creation-skill/.env`（仅 APP_ID/SECRET_KEY） |
| 读写行为 | 鉴权从 `.env` 读取 APP_ID/SECRET_KEY；token 不落盘，按需请求并在进程内短时复用；首次配置走 `chanjing-credentials-guard` |
| API 基址 | `${CHANJING_API_BASE:-https://open-api.chanjing.cc}` |
| 无效凭据 | guard 可能 `webbrowser.open` 引导登录/注册页 |

---

## 环境变量（完整表）

### 可选（通用）

| 变量 | 默认 | 说明 |
|------|------|------|
| `CHANJING_APP_ID` | — | 蝉镜应用标识（用于换取 access_token） |
| `CHANJING_SECRET_KEY` | — | 蝉镜秘钥（用于换取 access_token） |
| `CHANJING_ACCESS_TOKEN` | — | 进程级可选 token 输入（不持久化） |
| `CHANJING_TOKEN_EXPIRE_IN` | — | 进程级 token 过期时间（Unix 时间戳，不持久化） |
| `CHANJING_API_BASE` | `https://open-api.chanjing.cc` | 覆盖 Open API 地址 |
| `CHAN_SKILLS_DIR` | — | 一键成片脚本仓库根路径（当前实现读取） |

### 可选（一键成片编排私有）

| 变量 | 默认 | 说明 |
|------|------|------|
| `AI_VIDEO_PROMPT_MAX_CHARS` | `8000` | ref_prompt 总长上限 |
| `AI_VIDEO_MODEL` | `Doubao-Seedance-1.0-pro` | 文生视频 model_code 缺省 |
| `FIRST_DIGITAL_HUMAN_MAX_CHARS` | `20` | 首个数字人分镜 voiceover 字符上限 |

### 说明

当前实现直接读取 `CHANJING_API_BASE`、`CHANJING_APP_ID`、`CHANJING_SECRET_KEY`、`CHANJING_ACCESS_TOKEN`、`CHANJING_TOKEN_EXPIRE_IN`、`CHAN_SKILLS_DIR`、`AI_VIDEO_PROMPT_MAX_CHARS`、`AI_VIDEO_MODEL`、`FIRST_DIGITAL_HUMAN_MAX_CHARS`。其中 token 变量仅用于进程级输入与校验，不写入 `.env`。若后续重命名环境变量，应先更新代码读取逻辑，再同步本文档与 manifest。

---

## OpenClaw/Manifest 门控对齐

为保证“加载前门控”和“运行时行为”一致，本包采用以下对齐规则：

| 维度 | 根 `SKILL.md` frontmatter | `manifest.yaml` | 说明 |
|---|---|---|---|
| OS | `darwin`、`linux` | `darwin`、`linux` | 仅在受支持系统启用 |
| 必需二进制 | `python3` | `python3` | 所有脚本入口依赖 Python 运行时 |
| 条件二进制 | `ffmpeg` 或 `ffprobe` | `ffmpeg` 或 `ffprobe` | 主要用于 L3 成片链路 |
| 必需 env | 无强制 | 无强制 | 通过默认值兜底；凭据缺失时走 guard |

若后续新增依赖（新 CLI 或强制 env），必须同时更新：

1. 根 `SKILL.md` frontmatter 的 `metadata.openclaw.requires`
2. `manifest.yaml` 的 `metadata.openclaw.requires`
3. 本文件“环境变量/二进制依赖”章节
4. 根 `SKILL.md` 的 `Runtime Contract（摘要）`

---

## 外部二进制依赖

| 二进制 | 何时需要 | 用途 |
|--------|----------|------|
| `ffmpeg` | L3 成片/拼接链路（`run_render.py` 等） | 转码、拼接、封装音视频 |
| `ffprobe` | L3 成片/拼接链路 | 读取媒体分辨率、时长、旋转元数据 |
| `python3` | 所有 `scripts/` 入口 | 执行产品层与编排层 CLI |

仅调用 L2 产品层 API 脚本（如 `list_voices.py`、`create_task.py`、`poll_task.py`）时通常**不需要** `ffmpeg`/`ffprobe`，但仍需要 `python3`。

---

## 典型副作用（按类）

| 类型 | 说明 | 关联脚本 |
|------|------|----------|
| 出站 HTTPS | 蝉镜 Open API、CDN `video_url` / 素材下载 | 所有产品与编排脚本 |
| 本地写入 | `output/`、`work/`、凭据文件 | `download_result.py`、`run_render.py`、`chanjing_get_token.py` |
| 子进程 | `ffmpeg`/`ffprobe`；`subprocess` 调用同仓库 Python CLI | `run_render.py`、部分编排脚本 |
| 浏览器 | `webbrowser.open` 引导登录 | `chanjing-credentials-guard` |

---

## 持久性变更与用户可控性

| 类别 | 写入什么 | 典型位置 | 用户如何控制 |
|------|----------|----------|-------------|
| 凭据状态 | `.env` 中 `CHANJING_APP_ID`/`CHANJING_SECRET_KEY` | `skills/chanjing-content-creation-skill/.env` | 事后删除/迁移；**勿**提交版本库 |
| 成片工件 | `final_one_click.mp4`、`workflow_result.json`、`work/` | `run_render.py --output-dir` | 明确 `--output-dir`；任务结束后按需清理 |
| 下载类输出 | 合成结果落盘 | `output/<产品线>/` 或 `--output` | 在预期 cwd 执行，或始终传 `--output` |
| 临时文件 | TTS 合并、切段、上传缓存 | `work/` | 随 `output_dir` 一并管理 |

**边界保证**：本包脚本不应修改其它技能目录、`.cursor/rules`、全局编辑器/Agent 配置。仅操作凭据路径、`--output-dir` 指定目录、相对 cwd 的 `output/`。

---

## 变更同步清单

当修改任一 `products/*/scripts/` 或 `orchestration/*/scripts/` 的副作用行为时，必须同步核对：

- 根 `SKILL.md` 的 `Runtime Contract（摘要）`
- `manifest.yaml` 的 `runtime`、`permissions`、`metadata.openclaw.requires`
- 本文档对应章节（凭据、环境变量、二进制、副作用、持久化）
