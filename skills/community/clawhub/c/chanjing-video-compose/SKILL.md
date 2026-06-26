---
name: chanjing-video-compose
description: "Use Chanjing video synthesis APIs to create digital human videos from text or audio, with optional background upload, task polling, and explicit download when the user asks to save the result locally. Primary credential: credentials.json (app_id/secret_key; access_token persisted on disk—do not commit; user accepts file-based secrets). Same credentials file as chanjing-credentials-guard. Not OpenClaw primaryEnv. Default path in metadata.openclaw.credentialModel. Optional env: CHANJING_API_BASE, CHANJING_CONFIG_DIR. May invoke open_login_page.py when AK/SK missing. create_task.py optional --callback may cause the API to POST task result payloads to a user-supplied URL. This skill's scripts do not require ffmpeg/ffprobe."
author: chan-skills
binaries: []
env:
  - CHANJING_CONFIG_DIR
  - CHANJING_API_BASE
category: 媒体处理
tags:
  - 视频合成
  - 数字人
  - ChanjingAPI
  - 蝉镜
sibling_skills:
  - chanjing-credentials-guard
credential_hint: "~/.chanjing/credentials.json（可用 CHANJING_CONFIG_DIR 覆盖目录）"
metadata:
  openclaw:
    homepage: https://doc.chanjing.cc
    credentialModel:
      type: credentials_json
      defaultPath: "~/.chanjing/credentials.json"
      optionalEnv:
        - CHANJING_CONFIG_DIR
        - CHANJING_API_BASE
      apiBaseDefault: https://open-api.chanjing.cc
      primaryEnvIntentionallyOmitted: true
      persistAccessTokenOnDisk: true
      sensitiveFields:
        - app_id
        - secret_key
        - access_token
        - expire_in
      doNotCommitToVcs:
        - credentials.json
    agentPolicy:
      alwaysSkill: false
      modifiesOtherSkillsOrGlobalAgent: false
---

# Chanjing Video Compose

技能包标识：`chanjing-video-compose`。

## 功能说明

调用蝉镜**视频合成** Open API：列举公共/定制形象、上传素材、文本或音频驱动数字人、轮询任务；用户明确要求时用脚本下载成片。本 skill 脚本**不**依赖 ffmpeg/ffprobe（与一键成片编排不同）。机器可读凭据路径与敏感字段见篇首 **`metadata.openclaw.credentialModel`**。

## 运行依赖

- **python3** 与同仓库 `scripts/*.py`
- **无** ffmpeg/ffprobe 门控

## 环境变量

1. **CHANJING_CONFIG_DIR**（可选）：`credentials.json` 所在目录，默认 `~/.chanjing`
2. **CHANJING_API_BASE**（可选）：Open API 基址，默认 `https://open-api.chanjing.cc`

## 使用命令

- **ClawHub**（slug 以注册表为准）：`clawhub run chanjing-video-compose`
- **本仓库**：`python skills/chanjing-video-compose/scripts/create_task.py …`（见 **Standard Workflow**）

---

## 登记摘要（英文 · ClawHub / OpenClaw）

**Primary credential (not `primaryEnv`)**: `app_id` + `secret_key` in `~/.chanjing/credentials.json` (or `$CHANJING_CONFIG_DIR/credentials.json`); `access_token` / expiry **read/written** in the same file. **`primaryEnv` is omitted** on purpose (OpenClaw uses it for a single env-injected API key; this client uses **file-based dual keys**).

**Required vs optional**: **`CHANJING_API_BASE`** is **optional** (defaults to `https://open-api.chanjing.cc`). **`CHANJING_CONFIG_DIR`** is optional. **No `ffmpeg` / `ffprobe` gate** in this skill's `metadata`—orchestration-only use of this skill does not bundle local concat.

**Purpose alignment**: Chanjing **digital-human video compose** API client (list figures, upload assets, create/poll tasks, optional `download_result.py`). **Trust**: HTTPS to the API host and **URLs returned in responses** when saving media.

Chinese Q&A: **审阅四条对表** under **Preconditions** → **安全与凭据（登记摘要）**；与 **`credential_hint`**、**`metadata.openclaw.credentialModel`** 一致。

## When to Use This Skill

当用户要做这些事时使用本 Skill：

* 创建数字人视频合成任务
* 用文本驱动数字人出镜
* 用本地音频驱动数字人视频
* 查询公共数字人或定制数字人形象
* 轮询视频合成结果
* 在用户明确要求时下载最终视频到本地

如果需求更接近“上传一段真人视频做对口型驱动”，优先使用 `chanjing-avatar`，不要混用。

## Preconditions

执行本 Skill 前，必须先通过 `chanjing-credentials-guard` 完成 AK/SK 与 Token 校验。

本 Skill 与 guard 共用：

* `~/.chanjing/credentials.json`
* `https://open-api.chanjing.cc`

无凭证时，脚本会自动打开蝉镜登录页，并提示配置命令。

### 审阅四条对表（Purpose / 主凭据 / 指令范围 / 持久化）

以下为对「Purpose & Capability / Instruction Scope / Credentials / Persistence」类评审话术的**直接对表说明**；与代码、篇首英文登记摘要、**`description` frontmatter** 一致。

| # | 关切 | 说明 |
|---|------|------|
| **1** | **名称/能力与实现一致？主凭据是否写进登记？** | **一致**。本 skill 为蝉镜 **数字人视频合成** API 客户端（形象列表、上传、创建/轮询任务、用户明确要求时 **`download_result.py`**）。**`CHANJING_API_BASE` 不是必填**（有默认基址）。**主凭据**为 **`credentials.json`** 内 **`app_id` / `secret_key`** 及刷新后的 **`access_token`**；已在 **`description`**、**`credential_hint`**、**`metadata.openclaw.credentialModel`**、篇首英文摘要、下表 **安全与凭据** 写明。**不**声明 **`primaryEnv`**（双字段文件凭据，与单一 env Key 模型不符）。本 skill **不**将 **`ffmpeg`/`ffprobe`** 写入 `metadata.requires.bins`（与 **一键成片** 不同）。 |
| **2** | **运行时指令范围与敏感数据、任意 URL** | **符合声明目的**。脚本 **读写** **`CHANJING_CONFIG_DIR/credentials.json`**；缺凭证时可能 **浏览器** 或 **`open_login_page.py`**；向 Open API **上传/下载**；用户明确要求落盘时 **`download_result.py`** 会请求 **接口返回的媒体 URL**——请自行判断是否信任 API 主机与链接。若使用 **`create_task.py --callback <URL>`**，蝉镜服务端可能向该 URL **推送任务结果**——仅使用你信任且可接收回调的端点。 |
| **3** | **环境变量适合客户端，主凭据在文件** | **`CHANJING_CONFIG_DIR` / `CHANJING_API_BASE`** 为可选配置。**主凭据非**单一注入式 env Key：**`app_id` / `secret_key`** 经 **guard** 等写入 **`credentials.json`**（路径见 **`metadata.openclaw.credentialModel`**）；**`access_token` 持久化到磁盘**，属敏感；勿提交版本库、勿在对话中回显完整密钥。 |
| **4** | **持久化与特权** | 凭据与 token 写入约定 **配置文件**；可能 **交互式登录**。**`always: false`**（默认）；**不**修改其它 skill 或全局 Agent 配置。 |

### 安全与凭据（登记摘要）

与 **审阅四条对表**、篇首英文登记摘要、`description` 一致。

| 维度 | 说明 |
|------|------|
| **主凭据** | `app_id`、`secret_key` 存于 **`credentials.json`**（默认 `~/.chanjing/`，**`CHANJING_CONFIG_DIR`** 可改目录）。经 **`chanjing-credentials-guard`** 配置。非 OpenClaw **`primaryEnv`** 模型（非单一环境变量 API Key）。 |
| **Token** | 脚本将 **`access_token`** / **`expire_in`** 写回同一文件；与 **`chanjing-credentials-guard`** 及其它蝉镜子技能**共用**该文件（磁盘持久化、跨技能状态）。 |
| **回调（可选）** | **`create_task.py --callback`**：若提供，API 可能向用户 URL 发送任务相关负载；属**出站到你方端点**的信任边界，请自行评估。 |
| **环境变量** | **`CHANJING_API_BASE`**、**`CHANJING_CONFIG_DIR`** 可选。 |
| **网络与浏览器** | HTTPS **`https://open-api.chanjing.cc`**；无凭证时可能 **`webbrowser.open`** 或通过 guard 打开登录页。 |
| **下载与信任** | 仅在用户明确要求落盘时调用 **`download_result.py`**，请求接口返回的媒体 URL；请信任蝉镜 API 与其返回链接。 |
| **持久化** | **`always: false`**（默认）；不修改其它 skill 或全局 Agent 配置。 |

## Standard Workflow

1. 先让用户明确选择数字人来源：`common`（公共数字人）或 `customised`（定制数字人）
2. 调用 `list_figures.py --source <common|customised>`（建议 `--json`，公共源可加大 `--page-size` 或翻页）获取可用形象；**在候选内对比** `name`、各 `figure` 的 `type` 与分辨率、`audio_man_id`、`audio_name`（若有）与任务人设后再选定 `person.id`。**禁止**未比较就默认列表最前几项。
3. 如果选择公共数字人，还要再确认 `figure_type`（与所选 `figures[].type` 一致），例如 `sit_body` / `whole_body` / `circle_view`。无用户特殊要求时，**默认优先年轻、有活力的形象**（名称/`audio_name` 偏青年、学生、元气等）；题材需要成熟或中老年气质时再改选。
4. 若使用文本驱动，确定 `audio_man_id`
5. 在创建任务前，必须明确询问用户字幕偏好：`show`（保留字幕）或 `hide`（隐藏字幕）
6. 如果用户选择 `show` 但没有提出自定义样式或位置需求，直接使用官方文档推荐默认值；只有在用户明确想调整字幕位置或样式时，才继续追问 `subtitle_config` 参数
7. 若用户要定制字幕位置，说明坐标以左上角为原点，再补充 `subtitle_config` 相关参数
8. 若使用本地音频或背景图，先调用 `upload_file.py` 获取 `file_id`
9. 调用 `create_task.py` 创建视频合成任务，得到 `video_id`
10. 调用 `poll_task.py` 轮询直到成功，得到 `video_url`
11. 只有在用户明确要求保存到本地时，才调用 `download_result.py`

## Covered APIs

本 Skill 当前覆盖：

* `GET /open/v1/list_common_dp`
* `POST /open/v1/list_customised_person`
* `POST /open/v1/create_video`
* `GET /open/v1/video`
* `GET /open/v1/common/create_upload_url`
* `GET /open/v1/common/file_detail`

## Scripts

脚本目录：

* `skills/chanjing-video-compose/scripts/`

| 脚本 | 说明 |
|------|------|
| `_auth.py` | 读取凭证、获取或刷新 `access_token` |
| `list_figures.py` | 按 `--source common|customised` 列出数字人形象，输出 `person.id` / `figure_type` / `audio_man_id` / 预览信息 |
| `upload_file.py` | 上传音频或背景素材，轮询到文件可用后输出 `file_id` |
| `create_task.py` | 创建视频合成任务；使用公共数字人时可补充 `--figure-type ...`，字幕支持 `--subtitle show|hide` 以及完整字幕配置参数；可选 **`--callback`**（服务端可能向该 URL 推送结果） |
| `poll_task.py` | 轮询视频详情直到完成，默认输出 `video_url` |
| `download_result.py` | 下载最终视频到 `outputs/video-compose/` |

## Usage Examples

示例 1：公共数字人文本驱动

```bash
# 1. 先列公共数字人
python skills/chanjing-video-compose/scripts/list_figures.py --source common

# 2. 用公共数字人创建文本驱动视频
VIDEO_ID=$(python skills/chanjing-video-compose/scripts/create_task.py \
  --person-id "C-ef91f3a6db3144ffb5d6c581ff13c7ec" \
  --figure-type "sit_body" \
  --audio-man "C-0ae461135d8a4eb2b59c853162ea9848" \
  --subtitle "show" \
  --subtitle-x 31 \
  --subtitle-y 1521 \
  --subtitle-width 1000 \
  --subtitle-height 200 \
  --subtitle-font-size 64 \
  --subtitle-stroke-width 7 \
  --text "你好，这是一个蝉镜视频合成测试。")

# 3. 轮询到完成，拿到 video_url
python skills/chanjing-video-compose/scripts/poll_task.py --id "$VIDEO_ID"
```

示例 2：定制数字人上传本地音频驱动

```bash
python skills/chanjing-video-compose/scripts/list_figures.py --source customised

AUDIO_FILE_ID=$(python skills/chanjing-video-compose/scripts/upload_file.py \
  --service make_video_audio \
  --file ./input.wav)

VIDEO_ID=$(python skills/chanjing-video-compose/scripts/create_task.py \
  --person-id "C-ef91f3a6db3144ffb5d6c581ff13c7ec" \
  --subtitle "hide" \
  --audio-file-id "$AUDIO_FILE_ID")

python skills/chanjing-video-compose/scripts/poll_task.py --id "$VIDEO_ID"
```

示例 3：显式下载最终视频

```bash
python skills/chanjing-video-compose/scripts/download_result.py \
  --url "https://example.com/output.mp4"
```

## Download Rule

下载是显式动作，不是默认动作：

* `poll_task.py` 成功后应先返回 `video_url`
* 不要自动下载结果文件
* 只有当用户明确表达“下载到本地”“保存到 outputs”“帮我落盘”时，才执行 `download_result.py`

## Figure Selection Rule

选择数字人时遵循这条规则：

* 如果用户要用平台已有人物库，先走公共数字人：`list_figures.py --source common`
* 如果用户要用自己训练或上传生成的人物，先走定制数字人：`list_figures.py --source customised`
* 使用公共数字人创建视频时，可按所选形态传 `--figure-type <type>`
* 使用定制数字人时，不需要 `figure_type`

## Subtitle Rule

字幕遵循这条规则：

* 不要默认假设用户要字幕或不要字幕
* 创建任务前，必须先明确询问用户选择：`show` 或 `hide`
* 若由 **`chanjing-one-click-video-creation`** 的 **`run_render.py`** 调用 `create_task.py`，以当次 **`workflow.json` 根级 `subtitle_required`** 为准（**默认 false** → `--subtitle hide`；**true** → `show` 及推荐样式），**无需**为该一键成片路径再单独追问字幕开关，除非用户在需求里明确要求改字幕策略
* 用户选择保留字幕时，调用 `create_task.py --subtitle show`
* 若用户未指定字幕位置或样式，直接使用官方推荐默认值；`create_task.py` 在未传 `--subtitle-color` 时默认白字 `color=#FFFFFF`：1080p 为 `x=31 y=1521 width=1000 height=200 font_size=64 stroke_width=7 asr_type=0`；4K 画布为 `x=80 y=2840 width=2000 height=1000 font_size=150 stroke_width=7 asr_type=0`（两组均含 `color=#FFFFFF`）
* 用户选择隐藏字幕时，调用 `create_task.py --subtitle hide` 或兼容旧用法 `--hide-subtitle`
* 若用户要求调整字幕位置或样式，可继续传 `--subtitle-x` / `--subtitle-y` / `--subtitle-width` / `--subtitle-height` / `--subtitle-font-size` / `--subtitle-color` / `--subtitle-stroke-color` / `--subtitle-stroke-width` / `--subtitle-font-id` / `--subtitle-asr-type`
* 坐标基于左上角原点；字幕区域不能超出 `screen_width` / `screen_height`
* 如果用户只说“要字幕”但没指定位置，不必再追问具体数值；除非用户明确要调位置，否则直接走默认值

## Output Convention

默认本地输出目录：

* `outputs/video-compose/`

## Additional Resources

更多接口细节见：

* `skills/chanjing-video-compose/reference.md`
* `skills/chanjing-video-compose/examples.md`
