# `workflow.json` 与 `run_render.py` 的通用契约

本文档与**选题、行业、口播内容无关**：仅说明确定性渲染脚本**实际读取**的字段。  
实现真源：`scripts/run_render.py`（若与本文冲突以代码为准）。

---

## 两层分工（通用）

| 层级 | 含义 | `run_render` 是否读取 |
|------|------|----------------------|
| **内容 / 策划** | `topic`、`video_plan`、各镜文案创意、提示词语言等 | **否**（仅落盘供人读或宿主追溯；可任意扩展子字段） |
| **渲染契约** | 下文「根级」「分镜」表内字段 | **是**（缺必填或违反校验则退出） |

Agent 应：**先在模板中完成内容层**，再保证 **渲染契约字段** 与 `list_voices.py` / `list_figures.py` 返回值一致。

---

## 根级字段

| 字段 | 必需 | 说明 |
|------|------|------|
| `full_script` | 是* | 整段口播；可与 `script` / `copy_text` / `input_script` / `content` 择一（按顺序取首个非空） |
| `scenes` | 是 | 非空数组；见下表 |
| `audio_man` | 是 | TTS 音色 id；宜与所选数字人 `audio_man_id` 一致 |
| `person_id` 或 `avatar_id` | 条件 | 任一镜 `use_avatar: true` 时必填 |
| `figure_type` | 条件 | 有数字人镜时建议与 `list_figures.py` 中 `figures[].type` 一致；缺省行为以脚本为准 |
| `speed` | 否 | 默认 `1` |
| `pitch` | 否 | 默认 `1` |
| `max_retry_per_step` | 否 | 默认 `1` |
| `ai_video_duration_sec` | 否 | 文生视频单段秒数，仅 `5` 或 `10` 有效，否则回退 `10` |
| `model_code` | 否 | 文生模型；缺省可用环境变量 `AI_VIDEO_MODEL`，再缺省为 `Doubao-Seedance-1.0-pro` |
| `subtitle_required` | 否 | 真值：数字人任务 `--subtitle show`，否则 `hide` |
| `subtitle_color` | 否 | 非空则传给 `create_task.py` |
| `subtitle_stroke_color` | 否 | 同上 |
| `subtitle_stroke_width` | 否 | 同上（整数） |

\* `full_script` 与备选键互斥兜底，见上。

**内容层常用但渲染忽略**：`topic`、`video_plan`（任意结构）、`subtitle_note` 等——可保留在 JSON 中，**不得**替代上表必填项。

---

## 分镜 `scenes[]` 每条

| 字段 | 必需 | 说明 |
|------|------|------|
| `scene_id` | 是 | 用于排序；整数 |
| `voiceover` | 是 | 该镜口播；全镜拼接经 norm 后须与 `full_script` 一致 |
| `use_avatar` | 是 | `true`：数字人镜；`false`：AI 镜 |
| `ref_prompt` | 条件 | `use_avatar: false` 时必填（非空字符串） |
| `subtitle` | 否 | 与其它字段一并供下游/字幕对齐使用（以 `run_render` 与 TTS 为准） |

**首个数字人分镜**（`scene_id` 升序下第一条 `use_avatar: true`）：`voiceover` 长度默认 ≤ `FIRST_DIGITAL_HUMAN_MAX_CHARS`（默认 20，含标点）。
**AI 分镜硬约束**：必须至少存在 1 条 `use_avatar: false`。开启数字人时，镜头类型需符合分镜模板奇偶混剪规则（首镜/末镜/中间奇数镜为数字人，中间偶数镜为 AI）。

---

## 校验失败（通用）

- 缺 `full_script` 与有效 `scenes[]`
- `voiceover` 拼接与 `full_script` norm 不一致
- 缺 `audio_man`；有数字人镜却缺 `person_id`/`avatar_id`
- 缺 AI 镜（不存在 `use_avatar: false`）
- 开启数字人时未满足奇偶混剪规则
- AI 镜缺 `ref_prompt`
- 首数字人分镜超长


