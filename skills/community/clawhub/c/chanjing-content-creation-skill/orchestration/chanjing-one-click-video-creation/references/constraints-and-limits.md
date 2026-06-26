# 硬性约束与产品限制

## 硬性约束

表在 **`templates/render-rules.md` §4**；与 `ref_prompt` 交叉见 **`storyboard-prompt.md`** / **`history-storyboard-prompt.md`**（[`ref-prompt-pointers.md`](ref-prompt-pointers.md) 指针）。本节为锚点。

## 限制

- 本地 mp4；不上传  
- AI 单段常 5–10s；长口播多段  
- 成片时长=TTS 总轨；可与 `duration_sec` 不符  
- **TTS**：整轨优先、超长少批合并；单批上限与合并策略（含 `TTS_BATCH_MAX`）以 **`render-rules.md` §3·C.4** 为准  
- 文生失败可能为平台/模型；试增 `max_retry_per_step`、短 `ref_prompt`、拆镜；查 `workflow_result.json`
