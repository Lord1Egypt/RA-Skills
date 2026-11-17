# Runtime State 與 Routing（Phase 6）

本文件定義 AGY 專用的 deterministic project state 系統，以及 AGY 對 engineering 與
slide-image workers 的正式 routing contract。

核心前提：**AGY 永遠是唯一 Orchestrator / Single Source of Decision。**
本階段不建立第二個 AI orchestrator。程式只做 deterministic infrastructure。

## 1. 程式負責 / 不負責

程式（`scripts/project_state.py`、`scripts/validate_project.py`）只做：

- project state / slide state
- schema validation
- 合法 state transition
- job preparation 對接
- worker result 記錄與驗證
- output/path validation
- resume / recovery
- idempotency
- reporting（deterministic summary）

程式**不得**做：簡報策略、大綱決策、文案修改、視覺 QA 判斷、是否重生的決策、
自動呼叫工程 worker、自動改頁數、自動改 slide content、自動推進 phase。以上全部屬於 AGY。

## 2. 與 upstream state 的關係（不重造）

upstream `codex-ppt` 既有：

- `prepare_slide_prompts.py` → `prompts/slide_XX.json`（完整 image prompt + input images）
  與 `slide_jobs.json`（subagent dispatch / record ledger）
- `slide_run_state.py`、`record_slide_*.py`（atomic write / filelock / sha256）

Phase 6 **不重造**上述資料，而是新增 AGY 控制平面：

| 需求 | 來源 |
| --- | --- |
| 完整 image prompt、input images | upstream `prompts/slide_XX.json` |
| subagent dispatch ledger | upstream `slide_jobs.json` |
| **deck phase 機、slide state 機** | **本階段 `project_state.json`** |
| **generation counter、attempt history** | **本階段** |
| **resume / recovery、idempotency** | **本階段** |
| **worker result validation** | **本階段** |

`project_state.json` 以 `job_path`（指向 `prompts/slide_XX.json`）與
`image_path`（指向 `origin_image/slide_XX.png`）**引用**既有產物，不複製 payload，
避免互不相容的平行格式。

## 3. Project State Model

檔案：`<workspace>/project_state.json`，schema：`schemas/project_state.schema.json`。

```json
{
  "schema_version": "1",
  "project_id": "ppt_demo",
  "controller": "agy",
  "phase": "slide_generation",
  "phase_before_block": null,
  "sequential_only": true,
  "outline": {"status": "approved"},
  "style":   {"status": "approved"},
  "sample":  {"status": "approved"},
  "deck_spec_path": "deck_spec.json",
  "slide_jobs_path": "slide_jobs.json",
  "history": [{"from": "sample", "to": "slide_generation", "at": "...", "note": null}],
  "slides": {
    "slide_01": {
      "status": "qa_passed",
      "generation": 1,
      "generating_attempt": null,
      "job_path": "prompts/slide_01.json",
      "image_path": "origin_image/slide_01.png",
      "aspect_ratio": "16:9",
      "blocker": null,
      "attempts": [
        {"generation": 1, "worker": "codex", "status": "completed",
         "operation": "generate", "backend": "codex_builtin_imagegen",
         "output_path": "origin_image/slide_01.png", "error_code": null,
         "idempotency_key": "slide_01:gen1:origin_image/slide_01.png",
         "at": "...", "diagnostics": {"auth": "chatgpt_cli_session",
         "api_fallback_used": false, "thread_id": "01a0..."}}
      ]
    }
  }
}
```

- `controller` 永遠是 `agy`（validation 強制）。
- `sequential_only` 永遠 `true`（第一版）。

## 4. Project Phases 與合法 transition

phase：`intake`、`outline`、`style`、`sample`、`slide_generation`、`visual_qa`、
`assembly`、`complete`、`blocked`。

合法 forward transition：

```text
intake            -> outline
outline           -> style
style             -> sample
sample            -> slide_generation
slide_generation  -> visual_qa
visual_qa         -> assembly | slide_generation   (QA 不過可退回重生)
assembly          -> complete
```

- 任何 phase 皆可 `-> blocked`；進入 blocked 時記錄 `phase_before_block`。
- 解除 blocker 時，**只有 AGY** 能明確指定 resume target，且必須是 `phase_before_block`
  本身或它的合法後繼；不得任意跳 phase。
- 程式不會因猜測而跳 phase；非法 transition 一律 `INVALID_STATE_TRANSITION`。

## 5. Slide State Model 與合法 transition

slide status：`planned`、`ready`、`generating`、`generated`、`qa_passed`、
`qa_failed`、`generation_failed`、`assembled`、`blocked`。

合法 transition：

```text
planned            -> ready
ready              -> generating
generating         -> generated | generation_failed
generated          -> qa_passed | qa_failed        (AGY-only 視覺判斷)
qa_failed          -> ready
generation_failed  -> ready
qa_passed          -> assembled
任何狀態            -> blocked（記 phase_before_block，之後由 AGY 明確 resume）
```

- `generated -> qa_passed` / `generated -> qa_failed` 是 **visual-QA judgement**，
  只有 `by="agy"` 能執行。worker 記錄結果只會產生 `generated` 或 `generation_failed`，
  永遠不會自動 `qa_passed`。程式不做視覺判斷。
- **Visual QA 判定準則**：
  1. 不設定固定字數上限，權威文案（authoritative text）完整性優先。
  2. Phase 8A 已實證系統至少可穩定處理 79～239 字／頁（已驗證成功範圍，非硬性門檻）。
  3. 只要文字精確無誤、字級清晰可讀、無裁切重疊、留白與閱讀動線合理，即判 `qa_passed`；不得僅因「字數多」判失敗。
  4. 排版過密或字級不佳時，優先採 `generated -> qa_failed -> ready -> regenerate` 調整版型；僅在確定單頁無法容納時才允許拆頁。

## 6. Generation Counter 與 Attempt History

- 每次真正呼叫 Codex（`begin_generation`）時 `generation += 1`；第一次 = 1。
- 每次 worker result 記入 `attempts[]`，保留歷次 metadata（不只留最後一筆）。
- 不儲存任何 OAuth credential；diagnostics 只保留 `auth` / `api_fallback_used` /
  `thread_id` / `artifact_discovery`，並經 credential-key 過濾。

## 7. Worker Result Contract

schema：`schemas/worker_result.schema.json`（Codex 與 Kiro 是不同 shape，`oneOf`）。

Codex result 至少驗證：`status`、`slide_id`、`operation`、`backend`、`output_path`
（completed 必填）、`diagnostics`、`error_code`（error 必填且屬已知集合）。
`api_fallback_used=true` 直接判 `WORKER_RESULT_INVALID`。

Kiro engineering result 用 bridge 既有 schema tag 驗證，另成一份 contract，不硬塞成
與 Codex 相同 schema。

**任何 worker 都不得寫 project phase**：result 若含 `phase` / `project_phase` 欄位，
一律 `WORKER_RESULT_INVALID`。

## 8. Resume / Recovery

系統可中斷後恢復：

- `generated` / `qa_passed` 等已完成 slide 不會被重生。
- 停在 `generating` 的 slide **不可**當成成功：
  - 該 generation 有 recorded `completed` attempt **且** artifact 確認存在 → `generated`
  - 否則 → `generation_failed`（由 AGY 決定 retry 或 blocked）
- 無法確認就標 `generation_failed`，永不把未知當成功。

## 9. Idempotency

同一 completed result 重複 record 不會：generation +1、重複加 history、重複改 state。
idempotency key 優先用 worker 明確 `run_id` / `attempt_id`，否則以
`slide_id + generation + output_path/error_code` 組成。Codex `thread_id` 只存進
diagnostics 供追溯，**不**當唯一 project attempt id。

## 10. Filesystem Safety

- 只操作 workspace 內檔案；path traversal / root 外寫入一律 reject。
- atomic write（temp file + `os.replace` + fsync）；state JSON 不會半寫壞。
- schema validation 失敗**不覆蓋**原 state。
- state file corrupt 時**不**自行重建空 state 蓋掉，回 `PROJECT_STATE_INVALID`。

## 11. Concurrency

第一版 **sequential only**。不加 worker pool / async queue / multiprocessing /
lock server。但 state model（per-slide attempts、generation counter）不阻止未來加入
parallel generation。

## 12. AGY Routing Contract

```text
內容 / 規劃 / QA        -> AGY 自己處理
Coding                  -> 明確指派 Codex Production Engineering Worker 或 kiro_acp_bridge.py -> 回 AGY（worker 不推進 deck phase）
一般 Image              -> codex_image_adapter.py -> 回 AGY（AGY QA 後才更新 slide state）
Phase 18 Hybrid Image   -> phase18_codex_worker.py -> frozen codex_image_adapter.py -> 回 AGY
Assembly                -> upstream assemble_ppt.py（正常不需 engineering worker；有 bug 才派 Codex 或 Kiro）
```

永遠只允許：

```text
AGY -> worker -> AGY
```

**禁止 worker chain**：

```text
AGY -> Kiro -> Codex      (禁止)
AGY -> Codex -> Kiro      (禁止)
```

Codex 回 `generated` 不等於 `qa_passed`；只有 AGY 能做 `generated -> qa_passed`。

Phase 18 wrapper 只負責 production safety：驗證並傳遞 Clean Plate / Reserved Editable Zone
contract，保留 live dispatch、Codex thread、worker result 與 artifact hash evidence。它不改文案、
不選證據、不做 semantic QA，也不推進 approval gate。Jev 是 Codex 的 development-time bounded
decision layer，**不在**此 product runtime chain。

## 13. 統一 Error Handling

程式對外使用穩定 error_code，且**不吞掉** worker error：

```text
ENGINEERING_WORKER_UNAVAILABLE
ENGINEERING_AGENT_UNAVAILABLE
ENGINEERING_AGENT_SCOPE_LOST
IMAGE_BACKEND_UNAVAILABLE
IMAGE_ARTIFACT_AMBIGUOUS
IMAGE_GENERATION_FAILED
IMAGE_OUTPUT_INVALID
PROJECT_STATE_INVALID
INVALID_STATE_TRANSITION
WORKER_RESULT_INVALID
```

## 14. Reporting

`ProjectState.summary()` / `validate_project.py --summary` 回 deterministic 進度：

```json
{"phase": "slide_generation", "slides_total": 10, "planned": 0, "ready": 3,
 "generating": 0, "generated": 2, "qa_passed": 5, "failed": 0, "blocked": 0}
```

summary 只呈現進度，**不**決定下一步。

## 15. Freeze 狀態

| 元件 | 狀態 |
| --- | --- |
| `scripts/kiro_acp_bridge.py`（Kiro ACP Bridge） | **Production Baseline / Frozen** |
| `scripts/codex_image_adapter.py`（Codex Image Adapter，含 Phase 5.1 ambiguity fix） | **Production Baseline / Frozen** |

Freeze 意義：除非出現實際 integration blocker / bug，否則後續 Phase 不得順手 refactor。
