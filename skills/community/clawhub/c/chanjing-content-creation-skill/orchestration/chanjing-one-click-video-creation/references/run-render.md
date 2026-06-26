# 自动化编排（`run_render.py`）

**依赖**：可选 **`CHAN_SKILLS_DIR`**（见 [`../../../references/top-level-runtime-contract.md`](../../../references/top-level-runtime-contract.md)）；`chanjing-tts` / `chanjing-video-compose` / `chanjing-ai-creation`。凭证由顶层入口统一保证。

**职责**：① TTS+`audio_task_state`；批合并与单批字数上限见 **`render-rules.md` §3·C.4**（`TTS_BATCH_MAX`）② 切段（**`render-rules.md` §3·C.5**）③ **有 AI 镜时先完成首条数字人并 `ffprobe`（含 `rotate`）→ 再按映射提交文生 `aspect_ratio`/`clarity`**（见 **`render-rules.md` §3·C.6**、`debug.ai_video_submit_params`）④ 与其余 DH/AI 并行 poll ⑤ AI 轨对齐该参照 `ffprobe` ⑥ ffmpeg concat ⑦ 多段文生在 `ref_prompt` 后追加英文分层；总长由 **`AI_VIDEO_PROMPT_MAX_CHARS`** 约束

**不做**：不产 plan/script/storyboard；不自动非当代/当代；不用 `list_tasks.py` 当代次（**`render-rules.md` §4 表项 8**）

**手工编排**：仍须满足 **`render-rules.md` §3、§4** 与本节 MVP；**`render-rules.md` §3** 中细化（如 `silencedetect`、`minterpolate`、参照轨码率、同套切段音频换形象、TTS 批间静音等）**全部保留**。

## 输入 MVP

| 字段 | 必填 | 说明 |
|------|------|------|
| `full_script` | 是 | 与各镜 `voiceover` 按 `scene_id` 拼，`norm` 一致 |
| `scenes` | 是 | `scene_id`、`voiceover`、`use_avatar`；AI 镜 `ref_prompt`（**`storyboard-prompt.md`** / **`history-storyboard-prompt.md`**；[`ref-prompt-pointers.md`](ref-prompt-pointers.md)）；可选 `subtitle` |
| `audio_man` | 是 | 宜与所选数字人形象的 `audio_man_id` 一致 |
| `person_id`/`avatar_id` | 条件 | 有 DH 镜必填 |
| `figure_type` | 否 | 与当次 `list_figures.py` 所选形象行的 `figure_type` 一致（公共多形态时必填） |
| `subtitle_required` | 否 | 默认 false；为 true 时数字人镜烧录字幕（`--subtitle show`） |
| `speed`/`pitch` | 否 | 默认 1/1 |
| `ai_video_duration_sec` | 否 | 5 或 10，默认 10 |
| `model_code` | 否 | 默认 **`AI_VIDEO_MODEL`** 或 `Doubao-Seedance-1.0-pro`；creation_type=4；不传 `ref_img_url` |
| `max_retry_per_step` | 否 | 默认 1（完整请求体字段见 [`workflow-json-schema.md`](workflow-json-schema.md)） |

```bash
python scripts/run_render.py --input workflow.json --output-dir output/run1
```

（从仓库根执行时路径为 `skills/chanjing-one-click-video-creation/scripts/run_render.py`。）

未传 `--output-dir` 时，默认输出到 `skills/chanjing-content-creation-skill/output/<input_stem>-<timestamp>/`。  
**输出**：`final_one_click.mp4`；`workflow_result.json`；`work/`
