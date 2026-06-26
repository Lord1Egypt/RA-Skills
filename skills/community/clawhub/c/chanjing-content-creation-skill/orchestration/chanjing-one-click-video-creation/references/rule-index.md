# 规则索引与真值优先级

## 速查

| 内容 | 位置 |
|------|------|
| 工作流、`duration_sec`、`null`/合并、选题校验 | [`workflow-orchestration.md`](workflow-orchestration.md) |
| 切段、奇偶镜、`scenes[]`、`scene_count`/`video_type`；**首镜 `voiceover` ≤20 字（硬）** | [`../templates/storyboard-prompt.md`](../templates/storyboard-prompt.md) 篇首「文本切段」；[`../templates/script-prompt.md`](../templates/script-prompt.md) 首镜口播；[`../templates/video-brief-plan.md`](../templates/video-brief-plan.md) |
| 渲染技术、状态、`partial`/success、硬约束 | [`../templates/render-rules.md`](../templates/render-rules.md) §1–§4；§7、§8 |
| **`ref_prompt` / 文生提示词** | [`../templates/storyboard-prompt.md`](../templates/storyboard-prompt.md) + [`../templates/history-storyboard-prompt.md`](../templates/history-storyboard-prompt.md)；[`ref-prompt-pointers.md`](ref-prompt-pointers.md) |
| 请求体字段与默认 | [`workflow-json-schema.md`](workflow-json-schema.md)「输入」 |
| `run_render.py`、子进程 CLI | [`run-render.md`](run-render.md) |
| 安全、凭据、Agent 策略、出站与副作用 | [`../manifest.yaml`](../manifest.yaml)；扩展叙述见 [`extended-runtime-notes.md`](extended-runtime-notes.md) |
| 环境变量逐项说明 | [`../../../references/top-level-runtime-contract.md`](../../../references/top-level-runtime-contract.md) |

## 冲突（真值优先级）

渲染实现以 **[`../templates/render-rules.md`](../templates/render-rules.md)** 为准；**`ref_prompt`** 条文以 **`storyboard-prompt.md`** / **`history-storyboard-prompt.md`** 为准（[`ref-prompt-pointers.md`](ref-prompt-pointers.md) 汇总指针）。`run_render.py` 只实现 [`run-render.md`](run-render.md) + **`render-rules.md`**，不增业务规则。执行：手工编排子 skill、仅 `run_render`、或混用。
