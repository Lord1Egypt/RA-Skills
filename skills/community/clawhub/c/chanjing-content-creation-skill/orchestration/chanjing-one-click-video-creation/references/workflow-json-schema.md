# 工作流 JSON：输入与输出

## 输入（请求体）

**norm**：去 `\r`、首尾空白；空→空串；与 **`run_render.py`** 一致。口播：先 `full_script`，再 `script`→`copy_text`→`input_script`→`content` 首个非空。无 `topic`：首句代选题（40 字内遇句末标点截，否则 24 字）。`null`/合并见 [`workflow-orchestration.md`](workflow-orchestration.md)。

| 字段 | 必填 | 说明 |
|------|------|------|
| `topic` | 条件 | 无则见首句规则；建议 ≥5 字 |
| `industry`/`platform`/`style` | 否 | `industry` 空；platform/style：`DEFAULT_*` 或 `douyin`/`观点型口播` |
| `duration_sec` | 否 | `DEFAULT_DURATION` 或 60；策划参考 |
| `use_avatar` | 否 | 默认 true |
| `avatar_id`/`voice_id` | 否 | 空；**不得**用环境变量兜底音色或数字人；须在 `workflow.json` 写明 `audio_man`/`person_id`（及有 DH 镜时的 `figure_type`），由 Agent 按当次任务调用 `list_voices.py` 与 `list_figures.py`（来源与 **`video_plan`** / 用户指定一致）**对比 `name`、形态、画幅、`audio_name` 等后**选型；**禁止**未比较即取列表最前几条；**默认偏好年轻数字人**（见 [`workflow-orchestration.md`](workflow-orchestration.md)） |
| `subtitle_required` | 否 | 默认 false（数字人成片不烧录字幕；`run_render` 传 `hide`） |
| `cover_required` | 否 | 默认 true |
| `strict_validation`/`allow_auto_expand_topic`/`max_retry_per_step` | 否 | true/false/1 |
| `full_script` | 否 | 默认空 |
| `script_title`/`script_hook`/`script_closing_line` | 否 | 默认空（旧字段 `script_cta` 仅兼容历史数据） |
| `script`/… | 否 | 见上文口播顺序 |

仅渲染时的 MVP 字段表见 [`run-render.md`](run-render.md)。

## 输出 JSON

| 键 | 含义 |
|----|------|
| `status` | success / partial / failed |
| `video_plan` | Plan |
| `script_result` | title、hook、full_script、closing_line（旧键 `cta` 仅兼容历史数据） |
| `storyboard_result.scenes[]` | scene_id、duration_sec、voiceover、subtitle、visual_prompt、use_avatar |
| `render_result` | video_file、scene_video_urls、render_path、degrade_log |
| 其它 | error、debug… |

**渲染无降级**：任一步失败即中断，不自动改为仅 DH 或仅 AI 成片。**partial**：未成 success（如 `run_render` 异常仍写 `workflow_result.json`）；**不**表示允许上述降级，**不**免 **`storyboard-prompt.md`·D.1b** 类质检。成功 `degrade_log`=`[]`；失败尽量保留已产出文案与分镜。
