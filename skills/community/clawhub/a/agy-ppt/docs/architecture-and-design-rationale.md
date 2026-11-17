# 架構與設計思維

## 目前架構狀態

- Phase 12：FROZEN
- Phase 13：FROZEN
- Phase 14：ENFORCED
- Phase 15：COMPLETE / MERGED / BASELINE FROZEN
- Phase 16：**COMPLETE / MERGED / BASELINE FROZEN**
- Phase 17：**COMPLETE / MERGED / BASELINE FROZEN**
- Phase 18：**DEFINED / NOT STARTED**

Phase 16 的產品、證據綁定、Human Editorial Quality、子階段與非目標定義見
[Phase 16 — Grounded Presentation Planning, Evidence Binding & Human Editorial Quality](phase16-grounded-presentation-and-editorial-quality.md)。
Phase 16.1–16.5 均已合併並完成 deterministic integrated qualification；此 baseline 已凍結。

Phase 17 的 presentation strategy、narrative、visual communication、delivery 與 effectiveness
QA 架構見 [Phase 17 — Presentation Intelligence & Delivery Quality](phase17-presentation-intelligence-and-delivery-quality.md)。
Phase 17.1–17.5 均為 **COMPLETE / MERGED / BASELINE FROZEN**，並已通過 14-scenario
deterministic integrated qualification；此 baseline 不修改 Phase 12–16 frozen runtime，也不增加
預設使用者核准階段。

Phase 18 的 delivery fidelity、portability、selective editability、font/client-environment qualification
與 round-trip QA 架構見 [Phase 18 — Delivery Fidelity, Portability & Intelligent Editability](phase18-delivery-fidelity-portability-and-intelligent-editability.md)。
Phase 18.1–18.5 均為 **NOT STARTED**；此 architecture definition 不修改 Phase 12–17 frozen
semantics、不加入 runtime dependency，也不啟動 Phase 19。

## 1. 為什麼不是三個 CLI 平級

本系統採用「單一控制者 + 專業 worker」模式，而不是三個平級 Agent。

平級 Agent 最大的問題是 workflow state 與 intent 容易分裂：

- AGY 認為正在做 QA。
- Kiro 認為應該先重構組裝程式。
- Codex 認為文案不夠好而自行重寫。

因此整套系統只允許 AGY 持有完整簡報上下文與下一步決策權。

核心模式：

```text
AGY -> worker -> AGY
```

## 2. AGY 的角色：簡報導演與控制平面

AGY 處理 semantic/presentation decision：

- 讀資料
- 決定故事線
- 決定每頁角色
- 寫／調整文案（文字完整性優先，不設固定字數上限）
- 決定視覺語言與高密度分區版型（雙欄、2x2、2x3、卡片、流程、Checklist 等）
- 建立 slide job
- 管理 required assets
- content QA
- visual QA（以可讀性、正確性與留白判定 `qa_passed`，不以字數多寡為由失敗；排版不佳優先 `regenerate`）
- approval gate
- project state
- 判斷要不要重生
- 判斷是否需要工程修復

AGY 的責任是「決定系統應該做什麼」。
Phase 8A 實測已驗證目前系統至少能穩定處理約 79～239 字／頁的高密度繁體中文內容（已驗證成功範圍，非系統硬性上限）。

## 3. Production engineering worker：Codex 或 Kiro

所有 executable implementation 都必須由 AGY 明確指派的 Production Engineering Worker 執行；可由 Codex 或 Kiro 擔任。

這包括 Python scripts、ACP bridge、CLI adapters、schema、tests、dependency、build、filesystem logic、PPTX assembly logic 等。

重要原則：

```text
正常簡報執行 != Skill 開發
```

如果現有工具正常，Kiro 完全不需要出現在一次普通的 PPT 生成流程裡。

只有在「需要改系統」時才叫明確指派的工程 worker。Kiro availability 不再是必要前提。

## 4. Codex Slide Image Worker 的角色：視覺 renderer

Codex 的價值集中在圖片生成／編修。

如果讓 Codex 同時規劃大綱、改文案、寫程式、管理 state，就會浪費上下文與增加角色衝突。

因此 Codex 收到的 job 應該盡量完整、封閉、單頁化：

```text
slide_job.json
  -> Codex $imagegen
  -> slide_XX.png
  -> renderer QA note
  -> AGY
```

Codex 的正式派工鏈由 `scripts/codex_image_adapter.py` 實作：

```text
AGY
  -> codex_image_adapter.py
  -> codex exec --json          (ChatGPT/Codex 訂閱 session，prompt 走 stdin)
  -> $imagegen -> built-in image_gen
  -> $CODEX_HOME/generated_images/<thread_id>/<artifact>.png
  -> 驗證 + copy 進 workspace output_path
  -> structured result
  -> AGY
```

Adapter 只包裝 AGY 給的 authoritative slide prompt，不改寫簡報內容；Codex 不得
呼叫 Kiro、不得寫 code、不得組 PPTX、不得決定下一個 phase。built-in `image_gen`
不接受 output-path 參數，所以 adapter 用「明確 `ARTIFACT_PATH` 優先、thread 範圍
before/after diff 為 fallback」找出 turn 產物，而不是依賴脆弱的「取最新檔案」。細節見
`docs/codex-image-runtime.md`。

## 5. 為什麼保留上游 scripts

原始 `codex-ppt-skill` 已經有成熟的：

- outline/sample gate
- slide job preparation
- dispatch/state/result recording
- speaker notes
- image-based PPTX assembly
- style references

沒有必要為了換 orchestrator 就重寫 deterministic machinery。

本 fork 的主要改動是 ownership/routing，不是 PPT engine replacement。

## 6. 為什麼完整 Skill 只安裝給 AGY

完整 workflow 只應該存在 AGY。

Codex Production Engineering Worker 與 Codex Slide Image Worker 是兩個分離角色；Kiro custom agent 仍可作為替代工程 worker。

這能避免多份 workflow definition 漂移。

## 7. OAuth-only 的理由

三個 CLI 都使用各自訂閱方案登入，所以 Skill 不應變成 credential broker。

每個 vendor CLI 自己儲存登入狀態：

```text
AGY session != Kiro session != Codex session
```

Skill 不讀 token、不複製 token、不把 token 放進 JSON job，也不自動轉 API key。

## 8. 為什麼禁止 silent API fallback

「訂閱額度」與「API 計費」是兩個不同成本模型。

如果 Codex built-in image generation 不可用，最安全的預設不是偷偷改走 `OPENAI_API_KEY`，而是回報 blocker，讓 AGY／使用者決定。

因此：

```text
built-in image_gen unavailable
  -> IMAGE_BACKEND_UNAVAILABLE
```

而不是自動付費 fallback。

## 9. 狀態模型

AGY 應擁有唯一的 global project state。

每個 worker 回傳的只是區域性結果：

```text
Kiro  -> engineering_result
Codex -> render_result
```

AGY 再決定是否更新：

- slide status
- phase
- approval status
- retry count
- assembly readiness

這套 AGY-owned deterministic state 由 `scripts/project_state.py` 實作，落在
`<workspace>/project_state.json`，是「單一控制者」原則的程式化落實：deck phase 機、
slide state 機、generation counter、attempt history、resume/recovery、idempotency、
worker-result validation 都是 deterministic infrastructure，程式不做任何簡報決策。
它以 `job_path` / `image_path` 引用 upstream 既有 `prompts/slide_XX.json` 與
`origin_image/slide_XX.png`，不重造 upstream 的 prompt/image 資料。詳見
`docs/runtime-state-and-routing.md`。

## 10. 失敗處理

### Codex 不可用

```text
IMAGE_BACKEND_UNAVAILABLE
```

AGY 停在 image phase，不自動換 backend。

`codex_image_adapter.py` 另外區分這些 renderer 失敗（都不 fallback 付費 API）：

```text
CODEX_CLI_UNAVAILABLE        codex 可執行檔不存在 / 無法啟動
CODEX_AUTH_UNAVAILABLE       codex session 未登入 / 失效
IMAGE_GENERATION_FAILED      codex turn 非正常結束
IMAGE_ARTIFACT_NOT_FOUND     turn 沒有產出可辨識的新圖
IMAGE_ARTIFACT_AMBIGUOUS     turn 產出多個有效候選圖，adapter 不猜，交回 AGY 選
IMAGE_OUTPUT_INVALID         產物不是有效 bitmap / 0 bytes
IMAGE_OUTPUT_PATH_CONFLICT   output 已存在且非 regenerate
CODEX_TIMEOUT                render / probe 逾時
```

這些都交回 AGY 決策，adapter 不自行重試、不換 backend、不推進 workflow。

### Kiro 不可用

```text
ENGINEERING_WORKER_UNAVAILABLE
```

AGY 保留工程需求與 acceptance criteria，不自行改 code。

### Kiro 可連線但 agent 無法確認

```text
ENGINEERING_AGENT_UNAVAILABLE
```

ACP session 建立成功、但無法確認已切換到 `ppt-engineer` 時，不送出 coding task。

理由：引擎預設 agent（例如 `vibe`）沒有 `ppt-engineer` 的角色邊界與權限政策。
用它執行 AGY 的工程任務，等於放棄整個 ownership 模型。

V3 的 `session/set_mode` 即使 modeId 不存在也回傳空結果，所以「呼叫成功」不等於
「切換成功」。必須以引擎回報的 active agent 為準。

### Turn 中 agent 漂移

```text
ENGINEERING_AGENT_SCOPE_LOST
```

`ppt-engineer` 不只是 dispatch 前的一次檢查，而是整個 engineering turn 的 runtime
invariant。`session/prompt` 送出後到 `end_turn` 之前，只要 active agent 改變，該 turn
的輸出就不再是 `ppt-engineer` 的輸出，必須整個作廢。

處理方式固定為：停止批准 permission、`session/cancel`、套用既有 grace period、
清理 process group、回報 scope loss。

刻意不做的事：不自動切回 `ppt-engineer` 續跑、不 silently restart、不把 turn 判定成
completed。自動修復會讓 AGY 收到一份「一半由別的 agent 產生」的結果，這比失敗更糟。

### 為什麼只支援 V3

V2 與 V3 的 agent 解析、權限模型與工具集不同。同時支援兩者會讓 AGY 無法確定拿到的是
哪一個 worker，也讓 safety 規則要維護兩套。因此 production runtime 收斂為單一路徑：
`kiro-cli --v3 acp --auth-method cli`。

沒有 V2 執行路徑，也沒有 fallback。舊 caller 送 `engine = "v2"` 時直接回
`UNSUPPORTED_KIRO_ENGINE`，而不是靜默改跑別的引擎。

這與 image backend 的原則一致：不做 silent fallback。

### Script 執行失敗

AGY 可以先讀錯誤訊息與定位問題；只要解法需要改 executable code，就交 Kiro。

## 11. 安全邊界

- AGY：完整 read + workflow decision；對既有 script 有 execute 權。
- Kiro：repository code write 權，但不得自行改簡報內容。
- Codex：slide job input + image output；不得寫 workflow code。
- OAuth token：完全不進 Skill state。

Bridge 層的具體邊界：

- 只支援 `kiro-cli --v3 acp --auth-method cli`，沒有 V2 路徑，也沒有 engine fallback。
- ACP client 不宣告 `fs` / `terminal` capability，Kiro 只能用自己的沙箱工具。
- 子行程環境移除 API-key 類變數，避免 silent API fallback；diagnostics 只記變數名稱。
- token 解析留在 kiro-cli 內部，Bridge 不 broker `_kiro/auth/getAccessToken`。
- `ppt-engineer.md` 定義 Agent 能力，`kiro_acp_bridge.py` 定義 runtime enforcement，
  衝突時採較嚴格者。
- 工程 Worker 不提供 Git 能力；dependency 變更預設需要額外授權。
- shell chaining / pipeline / substitution、`sudo`、destructive 命令一律拒絕。
- `codex` / `$imagegen` / `image_gen` 永久拒絕，並記錄 `policy_violations`。

Bridge 只負責：啟動 V3 ACP、OAuth CLI auth、建立 session、scope 並驗證
`ppt-engineer`、派發單一 engineering turn、streaming、permission enforcement、
timeout / cancel、process cleanup、structured result、控制權回 AGY。

Bridge 不負責：簡報規劃、文案、頁面策略、visual direction、Codex image generation、
Git 版本控制、PR / CHANGELOG workflow、API credential management、自行推進 deck workflow。

## 12. Anti-patterns

禁止：

- AGY 自己寫程式只因為修改很小。
- Kiro 做完 code 後自己繼續跑簡報。
- Codex 自行重寫文案。
- Codex 自行切換圖片 API。
- 三個 CLI 都各自儲存完整 project state。
- 把 API key 當成 OAuth session 的 fallback。

## 13. 未來擴充

這個架構故意讓 worker 可替換：

```text
AGY orchestrator
  + coding worker interface
  + image renderer interface
```

未來可以替換 Kiro 或 Codex，而不重寫 AGY 的 presentation workflow。

真正需要長期穩定的不是某個 model，而是：

- ownership
- job contract
- state contract
- failure contract
- approval contract

## 14. Freeze 狀態

| 元件 | 狀態 |
| --- | --- |
| `scripts/kiro_acp_bridge.py`（Kiro ACP Bridge） | **Production Baseline / Frozen** |
| `scripts/codex_image_adapter.py`（Codex Image Adapter，含 Phase 5.1 ambiguity fix） | **Production Baseline / Frozen** |

Freeze 意義：除非出現實際 integration blocker / bug，否則後續 Phase 不得順手 refactor
這兩個元件。Phase 6 的 AGY-owned deterministic state 系統（`scripts/project_state.py`、
`scripts/validate_project.py`、`schemas/*.json`）是新增的獨立 infrastructure，未修改
上述任一 frozen 元件（除本次明確要求的 Codex Phase 5.1 ambiguity 修正）。
