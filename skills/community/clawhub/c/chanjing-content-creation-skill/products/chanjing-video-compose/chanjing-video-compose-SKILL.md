---
name: chanjing-video-compose
description: Use Chanjing video synthesis APIs to create digital human videos from text or audio, with optional background upload, task polling, and explicit download when the user asks to save the result locally.
---

# Chanjing Video Compose

## L2 Product Skill

本文件是 **L2 产品层**主手册（**Agent 执行真值**）。

- **本文件（`chanjing-video-compose-SKILL.md`）**：业务逻辑、追问与异常语义；据此调度 [`scripts/cli_capabilities.py`](scripts/cli_capabilities.py) 与 [`scripts/`](scripts/) 下脚本。
- **顶层入口** [`../../SKILL.md`](../../SKILL.md)：仅负责路由到本目录，**不**承载本产品执行细则。
- **跨场景约定** [`../../orchestration/orchestration-contract.md`](../../orchestration/orchestration-contract.md)；L3 编排层说明见 [`../../orchestration/README.md`](../../orchestration/README.md)。

## When to Use This Skill

当用户要做这些事时使用本 Skill：

* 创建数字人视频合成任务
* 用文本驱动数字人出镜
* 用本地音频驱动数字人视频
* 查询公共数字人或定制数字人形象
* 轮询视频合成结果
* 在用户明确要求时下载最终视频到本地

如果需求更接近“上传一段真人视频做对口型驱动”，优先使用 `chanjing-avatar`，不要混用。

### `model` 参数

| 取值 | 说明 | 费用 |
|------|------|------|
| **0**（默认） | 基础版：蝉镜 lip-sync 模型 | 1 蝉豆/秒 |
| **1** | 高质版：蝉镜 lip-sync Pro 模型 | 2 蝉豆/秒 |
| **2** | **卡通形象专用**：训练素材**必须为卡通形象**，否则效果与合规风险由使用方承担 | 3 蝉豆/秒 |

CLI 示例：`create_task.py ... --model 2`。

## Preconditions

凭证由顶层入口统一校验；本 Skill 不重复执行凭证校验步骤。

本 Skill 共用：

* `skills/chanjing-content-creation-skill/.env`（`CHANJING_APP_ID`、`CHANJING_SECRET_KEY`）
* `https://open-api.chanjing.cc`

## Standard Workflow

统一按“每步 = 脚本名 + 输入 + 输出 + 下一步 + 失败分支”执行：

| Step | 脚本名 | 输入 | 输出 | 下一步 | 失败分支 |
|---|---|---|---|---|---|
| 1 | `list_tag_dict.py`（推荐） | `--business-type 1 --json`（可选） | 标签字典 | Step 2 | 查询失败：记录后走 Step 2 的无标签模式 |
| 2 | `list_figures.py` | `--source common|customised`，推荐 `--fetch-all --page-size 80 --json` | 全量候选人物列表 | Step 3 | 失败：`upstream_error`，提示重试 |
| 3 | 无脚本（筛选决策） | 选题、人设、画幅、音色约束 | `person_id`、`figure_type`、可选 `audio_man_id` | Step 4 | 候选不足：`need_param` 或换筛选条件重走 Step 2 |
| 4 | `upload_file.py`（按需） | 本地音频/背景素材 | `file_id` | Step 5 | 上传失败：修正文件后重试 Step 4 |
| 5 | `create_task.py` | `person_id` + 文本或音频参数 + 字幕策略 | `video_id` | Step 6 | `10400`→`auth_required`；`40000`→`need_param`；`50000`→`upstream_error` |
| 6 | `poll_task.py` | `video_id` | `video_url` | Step 7 | 超时/失败：`timeout` 或 `upstream_error` |
| 7 | `download_result.py`（仅显式下载） | `video_url`、`--output`（可选） | 本地文件路径 | 结束 | 下载失败：返回 `video_url` + 错误信息 |

### Workflow Output Semantics

本 Skill 输出语义对齐 [`../../orchestration/orchestration-contract.md`](../../orchestration/orchestration-contract.md)：

- `ok`：成功返回 `video_url` 或本地路径
- `need_param`：缺少必要参数（如 `person_id` 或硬校验失败）
- `auth_required`：凭据不可用（典型 `10400`）
- `upstream_error`：上游接口失败（典型 `50000`）
- `timeout`：轮询超时

## Covered APIs

本 Skill 当前覆盖：

* `GET /open/v1/list_common_dp`
* `GET /open/v1/common/tag_list`
* `POST /open/v1/list_customised_person`
* `POST /open/v1/create_video`
* `GET /open/v1/video`
* `GET /open/v1/common/create_upload_url`
* `GET /open/v1/common/file_detail`

## Scripts

脚本目录：

* `skills/chanjing-content-creation-skill/products/chanjing-video-compose/scripts/`

| 脚本 | 说明 |
|------|------|
| `_auth.py` | 读取凭证、获取或刷新 `access_token` |
| `list_tag_dict.py` | `GET /open/v1/common/tag_list`：业务大类（`name`/`business_type`/`weight`/`update_time`/`tag_list`）与子标签（`id`/`parent_id`/`level`/`weight` 等）；`--business-type 1` 常见为数字人；`--json` 完整输出 |
| `list_figures.py` | 按 `--source common|customised` 列出数字人；公共库可选 **`--tag-ids`**（AND）、**`--common-dp-source`**；**`--fetch-all`** 拉全量至当前条件下的 `total_count`；或 `--max-pages` 多页合并；建议 `--json` 与较大 `--page-size` |
| `upload_file.py` | 上传音频或背景素材，轮询到文件可用后输出 `file_id` |
| `create_task.py` | 创建视频合成任务；使用公共数字人时可补充 `--figure-type ...`，字幕支持 `--subtitle show|hide` 以及完整字幕配置参数 |
| `poll_task.py` | 轮询视频详情直到完成，默认输出 `video_url` |
| `download_result.py` | 下载最终视频到 `outputs/video-compose/` |

## Usage Examples

示例 1：公共数字人文本驱动

```bash
# 1. 先拉全量公共数字人，再在完整列表上做全局匹配选型（勿只用第一页）
python skills/chanjing-content-creation-skill/products/chanjing-video-compose/scripts/list_figures.py --source common --fetch-all --page-size 80 --json

# 2. 用公共数字人创建文本驱动视频
VIDEO_ID=$(python skills/chanjing-content-creation-skill/products/chanjing-video-compose/scripts/create_task.py \
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
python skills/chanjing-content-creation-skill/products/chanjing-video-compose/scripts/poll_task.py --id "$VIDEO_ID"
```

示例 2：定制数字人上传本地音频驱动

```bash
python skills/chanjing-content-creation-skill/products/chanjing-video-compose/scripts/list_figures.py --source customised

AUDIO_FILE_ID=$(python skills/chanjing-content-creation-skill/products/chanjing-video-compose/scripts/upload_file.py \
  --service make_video_audio \
  --file ./input.wav)

VIDEO_ID=$(python skills/chanjing-content-creation-skill/products/chanjing-video-compose/scripts/create_task.py \
  --person-id "C-ef91f3a6db3144ffb5d6c581ff13c7ec" \
  --subtitle "hide" \
  --audio-file-id "$AUDIO_FILE_ID")

python skills/chanjing-content-creation-skill/products/chanjing-video-compose/scripts/poll_task.py --id "$VIDEO_ID"
```

示例 3：显式下载最终视频

```bash
python skills/chanjing-content-creation-skill/products/chanjing-video-compose/scripts/download_result.py \
  --url "https://example.com/output.mp4"
```

## Download Rule

下载是显式动作，不是默认动作：

* `poll_task.py` 成功后应先返回 `video_url`
* 不要自动下载结果文件
* 只有当用户明确表达“下载到本地”“保存到 outputs”“帮我落盘”时，才执行 `download_result.py`

## Figure Selection Rule

选择数字人时遵循这条规则：

* 如果用户要用平台已有人物库，先走公共数字人：`list_figures.py --source common --fetch-all --page-size 80 --json`，在**全量列表**上全局匹配后再写 `person_id` / `figure_type`
* 如果用户要用自己训练或上传生成的人物，先走定制数字人：`list_figures.py --source customised`
* 使用公共数字人创建视频时，可按所选形态传 `--figure-type <type>`
* 使用定制数字人时，不需要 `figure_type`

## Subtitle Rule

字幕遵循这条规则：

* 不要默认假设用户要字幕或不要字幕
* 创建任务前，必须先明确询问用户选择：`show` 或 `hide`
* 若由 **`chanjing-one-click-video-creation`** 的 **`run_render.py`** 调用 `create_task.py`，以当次 **`workflow.json` 根级 `subtitle_required`** 为准（**默认 false** → `--subtitle hide`；**true** → `show` 及推荐样式），**无需**为该一键成片路径再单独追问字幕开关，除非用户在需求里明确要求改字幕策略
* 用户选择保留字幕时，调用 `create_task.py --subtitle show`
* 若用户未指定字幕位置或样式，直接使用默认字幕参数（清晰橙字方案）：1080p 为 `x=31 y=1521 width=1000 height=200 font_size=64 color=#FF8A00 stroke_color=#1F1F1F stroke_width=3 asr_type=0`；4K 画布为 `x=80 y=2840 width=2000 height=1000 font_size=150 color=#FF8A00 stroke_color=#1F1F1F stroke_width=5 asr_type=0`
* 用户选择隐藏字幕时，调用 `create_task.py --subtitle hide` 或兼容旧用法 `--hide-subtitle`
* 若用户要求调整字幕位置或样式，可继续传 `--subtitle-x` / `--subtitle-y` / `--subtitle-width` / `--subtitle-height` / `--subtitle-font-size` / `--subtitle-color` / `--subtitle-stroke-color` / `--subtitle-stroke-width` / `--subtitle-font-id` / `--subtitle-asr-type`
* 坐标基于左上角原点；字幕区域不能超出 `screen_width` / `screen_height`
* 如果用户只说“要字幕”但没指定位置，不必再追问具体数值；除非用户明确要调位置，否则直接走默认值

## Output Convention

默认本地输出目录：

* `outputs/video-compose/`

## Additional Resources

更多接口细节见：

* `skills/chanjing-content-creation-skill/products/chanjing-video-compose/reference.md`
* `skills/chanjing-content-creation-skill/products/chanjing-video-compose/examples.md`
