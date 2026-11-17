# Agent Routing 規則

## 一句話版本

```text
AGY = 決定要做什麼
Codex Production Engineering Worker / Kiro = 寫程式讓系統做到
Codex Slide Image Worker = 把視覺做出來
```

## 決策樹

```text
收到任務
  |
  +-- 是簡報內容、故事線、版式策略、文案、QA？ -> AGY
  |
  +-- 是否需要寫/改/debug/test executable code？ -> Kiro
  |
  +-- 是否要生成或編修投影片圖片？ -> Codex
  |
  +-- 是否只是執行已存在且已驗證 script？ -> AGY 可以執行
```

## Production engineering worker routing 關鍵字

遇到以下內容通常代表 production engineering worker（可由明確指派的 Codex 或 Kiro 執行）：

- implement
- fix bug
- refactor
- modify script
- add validator
- adapter
- ACP client
- CLI integration
- schema migration
- dependency
- test
- regression
- filesystem automation
- PPTX assembly logic

## Codex Slide Image Worker routing 關鍵字

- generate slide image
- edit slide image
- regenerate slide
- visual variation
- sample slide image

## 不可跨權

### AGY 不得

- 因為「只改一行」就自行修改 code。

### Production engineering worker 不得

- 自行調整已核准文案／大綱／視覺方向。
- 自行呼叫 Codex 接著把流程跑完。
- 執行 Git 版本控制操作。
- 未經授權變更 dependency / lockfile。
- 成為 semantic authority，或在架構歧義影響外部契約時自行選擇新政策。

### Codex Slide Image Worker 不得

- 改文案。
- 改 deck strategy。
- 寫 code。
- 組 PPT。
- 換 backend。

## 控制權

任何 worker 完成後：

```text
worker -> result -> AGY
```

## 正式 Routing Contract

```text
AGY = sole orchestrator / state owner
Kiro V3 `ppt-engineer` = engineering worker only
Codex CLI Slide Image Worker = slide-image worker only
```

正式且唯一允許的 routing：

```text
AGY -> worker -> AGY
```

嚴格禁止以下任何 routing（worker 之間不得互相呼叫或轉交流程）：

```text
AGY -> Kiro -> Codex   (禁止)
AGY -> Codex -> Kiro   (禁止)
Kiro -> Codex          (禁止)
Codex -> Kiro          (禁止)
```

原因：worker 只回傳結果，不持有簡報 context、不做下一步決策、也不可以把工作直接
轉交給另一個 worker。任何 worker 對話中出現「接下來我幫你叫 Codex/Kiro」都是違反
此 routing contract 的訊號，應由 AGY 介入而不是讓 worker 自行接續。

只有 AGY 可以決定下一步。

## 禁止 Worker Chain

永遠禁止 worker 互相直接交接：

```text
AGY -> Kiro -> Codex      (禁止)
AGY -> Codex -> Kiro      (禁止)
```

正式只能：

```text
AGY -> worker -> AGY
```

## State Ownership

project / slide workflow state 由 **AGY only** 擁有，記錄在
`<workspace>/project_state.json`（見 `docs/runtime-state-and-routing.md`）。

- Kiro 不得直接推進簡報 workflow state。
- Codex 不得直接推進簡報 workflow state。
- worker 只回 result；AGY 判斷後才透過 deterministic state tool 更新。
- Codex 回 `generated` **不等於** `qa_passed`；只有 AGY 能做 `generated -> qa_passed`。

## Codex 派工路徑

### Codex Runtime

圖片 worker 使用目前已登入的 Codex CLI ChatGPT/Codex 訂閱 session。

```text
AGY
  -> codex_image_adapter.py
  -> Codex CLI          codex exec --json --skip-git-repo-check   (prompt 走 stdin)
  -> 使用既有 ChatGPT/Codex 登入 session
  -> $imagegen
  -> built-in image_gen
  -> $CODEX_HOME/generated_images/<thread_id>/<artifact>.png
  -> 驗證 + copy 進 workspace output_path
  -> structured result
  -> AGY
```

- Adapter：`scripts/codex_image_adapter.py`
- Backend：`codex_builtin_imagegen`（built-in `image_gen` only）
- Operation 第一版：`generate` / `regenerate` / `probe`（`edit` 尚未支援）

禁止路徑：

```text
AGY -> Codex API     (付費 Images API / OPENAI_API_KEY)
Codex -> Kiro
```

派工指令：

```bash
python3 scripts/codex_image_adapter.py --input job.json
```

若 built-in `image_gen` 不可用，回 `IMAGE_BACKEND_UNAVAILABLE` 並把控制權交回 AGY，
**不**自動 fallback 到付費 API。細節見 `docs/codex-image-runtime.md`。

## Engineering worker dispatch

Production implementation is no longer blocked by Kiro availability. AGY may explicitly assign Codex as Production Engineering Worker, subject to AGENTS.md, committed architecture, frozen contracts, security, CI, and phase scope. Codex must return results to AGY and must request architecture clarification when ambiguity affects an externally observable contract.

## Kiro 派工路徑

### Kiro Runtime

唯一受支援：`Kiro CLI V3`。

```text
AGY
  -> kiro_acp_bridge.py
  -> Kiro CLI V3 ACP        kiro-cli --v3 acp --auth-method cli
  -> 使用既有 Kiro Pro CLI OAuth session
  -> session/new
  -> 發現 ppt-engineer       modes.availableModes
  -> session/set_mode        {modeId: "ppt-engineer"}
  -> 確認 agent scope        config_option_update / current_mode_update
  -> engineering task        session/prompt
  -> permission enforcement
  -> TurnEnd                 stopReason: end_turn
  -> AGY
```

- Agent：`ppt-engineer`
- Agent selection：`session/set_mode`
- Agent confirmation：`config_option_update` / `current_mode_update`
- V2：**不支援**，不得 fallback。舊 caller 送 `engine="v2"` 一律回 `UNSUPPORTED_KIRO_ENGINE`。

派工指令：

```bash
python3 scripts/kiro_acp_bridge.py --input job.json
```

### Agent Scope

dispatch 前必須同時成立：

```text
diagnostics.agent_requested = "ppt-engineer"
diagnostics.agent_resolved  = true
diagnostics.agent_scoped    = true
```

不成立時不送 coding task，回 `ENGINEERING_AGENT_UNAVAILABLE`。

`ppt-engineer` 同時是整個 engineering turn 的 runtime invariant。turn 中 active agent
發生 drift 時立即 cancel 並回：

```text
ENGINEERING_AGENT_SCOPE_LOST
```

不得自動切回、不得繼續批准 tool call、不得判定 completed。

不得默默用 `kiro_default` 或引擎預設 agent 執行 AGY 的 engineering task。

### Permission Boundary

`ppt-engineer.md` 定義 Agent 能力；`kiro_acp_bridge.py` 定義 runtime enforcement。
衝突時採較嚴格規則。

- 允許：專案讀取、repository root 內寫入、`python` / `python3` / `pytest`、
  `pip list` / `pip show` / `pip check`
- 目前工程 Worker **不提供 Git 能力**
- Dependency changes 預設需要額外授權（`allow_dependency_changes`）
- shell chaining / pipeline / substitution、`sudo`、destructive 命令、
  未授權 package execution 一律拒絕
- `codex` / `$imagegen` / `image_gen` 永久拒絕

超出 policy 一律 deny 並記錄到 `policy_violations`。

Codex / image generation 永遠不屬於 Kiro 的責任範圍。


## Freeze 狀態

| 元件 | 狀態 |
| --- | --- |
| `scripts/kiro_acp_bridge.py` | **Production Baseline / Frozen** |
| `scripts/codex_image_adapter.py`（含 Phase 5.1 ambiguity fix） | **Production Baseline / Frozen** |

除非出現實際 integration blocker / bug，否則後續 Phase 不得順手 refactor 這兩個元件。
AGY-owned deterministic state 系統見 `docs/runtime-state-and-routing.md`。
