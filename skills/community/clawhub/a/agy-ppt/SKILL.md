---
name: agy-ppt
description: 以 AGY 為唯一主控，Kiro 負責所有程式工程，Codex 僅透過 built-in $imagegen 產生或編修整頁簡報圖片的圖片式 PPT/PPTX 工作流程。
---
# AGY PPT Orchestrator

## 1. 目的

本 Skill 建立在 `codex-ppt-skill` 的成熟圖片式 PPT 流程之上，但重新定義 Agent ownership。

每張投影片以完整 16:9 圖片呈現，最後使用既有 deterministic script（例如 `scripts/assemble_ppt.py`）組裝為 `.pptx`。

本 Skill 的最高層規則是：

```text
AGY   = 唯一主控 / 簡報導演 / workflow source of truth
Kiro  = 工程師 / Skill 維護者 / 所有 executable code change owner
Codex = 圖片 renderer / editor only
既有 scripts = AGY 可以執行，但只有 Kiro 可以修改
```

任何上游檔案若與本檔案的 ownership、routing、backend 或 OAuth policy 衝突，以本檔案與 `docs/agent-routing.md` 為準。

## 2. 核心設計原則

### 2.1 單一控制者

工作流程永遠遵守：

```text
AGY -> worker -> AGY
```

Kiro 與 Codex 不得互相直接交接，也不得自行決定下一個 workflow phase。

### 2.2 AGY 負責「要做什麼」

AGY 擁有：

- 使用者需求理解
- 受眾與簡報目的
- 大綱、頁數、storyline
- `outline.md`（簡報說什麼的內容權威）
- 視覺方向與版式策略
- `deck_spec.json`（簡報如何呈現的視覺規格；其中的投影片文字只可衍生自核准大綱）
- slide jobs / state
- 每頁文案、資訊層級、圖片 prompt
- approval gates
- content QA / visual QA
- speaker notes
- 是否接受 worker 結果
- 是否重生圖片
- 是否進入組裝與完成階段

### 2.3 Kiro 負責「如何讓系統做到」

只要任務需要：

- 寫程式
- 改程式
- debug
- 新增功能
- 改 executable workflow logic
- Python / JS / TS / Shell / PowerShell
- CLI adapter / ACP adapter
- schema/tool contract 修改
- filesystem processing
- PPTX assembly implementation
- validator
- dependency/build 修復
- tests / fixtures / regression test

一律由 AGY 派給 Kiro。

AGY 可以執行已存在且已驗證的 script，但不得因為自己有能力就直接修改程式碼。

### 2.4 Codex 只負責圖片

Codex 可以：

- 生成一張樣張
- 生成指定的一張正式投影片圖片
- 編修／重生指定投影片圖片
- 回傳簡短 renderer QA note

Codex 不得：

- 改 `outline.md`
- 改 `deck_spec.json`
- 改 slide job
- 重寫文案或事實
- 增減頁數
- 改整份簡報策略
- 寫或改程式
- 組裝 PPTX
- 自行換 image backend
- 使用 Pillow / SVG / HTML / CSS / Canvas / python-pptx / PptxGenJS 假裝成 AI 生圖

## 3. OAuth-only 執行原則

本 workflow 假設三個 CLI 都已經用各自訂閱方案登入：

```text
AGY   -> Google AI Pro session
Kiro  -> Kiro Pro session
Codex -> ChatGPT Plus / Codex session
```

Skill 不管理、不複製、不讀取、不轉傳 OAuth access token / refresh token。

預設不要求：

- `GEMINI_API_KEY`
- `KIRO_API_KEY`
- `OPENAI_API_KEY`
- `CODEX_API_KEY`

## 4. 固定圖片後端

正常路徑固定為：

```text
AGY
  -> phase18_codex_worker.py（Hybrid/Clean Plate job；驗證並傳遞 Reserved Editable Zones）
  -> codex_image_adapter.py（frozen image transport）
  -> Codex CLI          codex exec --json --skip-git-repo-check   (prompt 走 stdin)
  -> $imagegen
  -> built-in image_gen
  -> $CODEX_HOME/generated_images/<thread_id>/<artifact>.png
  -> 驗證 + copy 進 workspace output_path
  -> AGY QA
```

Codex 圖片派工由 `scripts/codex_image_adapter.py` 實作，backend 固定為
`codex_builtin_imagegen`，operation 第一版支援 `generate` / `regenerate` / `probe`。

不得自動改用上游的 `scripts/image_gen.py`、第三方 API 或其他付費 image backend。
adapter 會從 Codex 子行程環境移除 API-key 類變數，避免 silent API fallback。

若 Codex 當前 session 沒有暴露 built-in `image_gen`，回報：

```text
IMAGE_BACKEND_UNAVAILABLE
```

並將控制權交回 AGY。其他 renderer 失敗（`CODEX_CLI_UNAVAILABLE`、
`CODEX_AUTH_UNAVAILABLE`、`IMAGE_GENERATION_FAILED`、`IMAGE_ARTIFACT_NOT_FOUND`、
`IMAGE_OUTPUT_INVALID`、`IMAGE_OUTPUT_PATH_CONFLICT`、`CODEX_TIMEOUT`）同樣交回 AGY，
不自動 fallback 付費 API。細節見 `docs/codex-image-runtime.md`。

Phase 18 Hybrid output 的 image job 必須經過 `scripts/phase18_codex_worker.py`。此 additive
wrapper 不改寫 frozen adapter；它會在 dispatch 前 fail-closed 驗證 Clean Plate manifest，把
Reserved Editable Zone 的 identity、座標、`CONTENT_FREE` exclusion、manifest SHA-256 與
`COMPOSITE_CONFLICT` 行為放入 Codex worker prompt，並在結果中保留 dispatch/job/thread/artifact
evidence。缺少或矛盾的 manifest 不得派工。普通非 Hybrid image job 仍可直接使用 frozen adapter。
Jev 不在此 runtime path。

Hybrid Sample 與 final deck 的視覺資格必須以 `presentation_visual_qualification.py` 綁定 exact
artifact：至少記錄 Raw Plate、實際 Hybrid Preview、以及實際 PowerPoint client render 的 SHA-256
與 environment，並比較 Plate → Hybrid 與 Hybrid → client，定位品質損失發生在哪一層。Raw Plate
不得冒充使用者核准的 Sample；使用者看到並核准的必須是 Hybrid Preview。Semantic/content difference
永遠不能以 pixel drift 合理化，approved Sample hierarchy／composition 的 material degradation 也必須
阻擋。Automated checks 與 Jev 最多只能產生 `REVIEW_REQUIRED`／`BLOCK`；只有使用者檢視同一個 final
PPTX artifact 後，才能把 `HUMAN_PRESENTATION_QUALITY` 設為 `PASS`。

## 5. Kiro 呼叫原則

Kiro custom agent 名稱：

```text
ppt-engineer
```

放在：

```text
<repo>/.kiro/agents/ppt-engineer.md
```

### 5.1 Kiro Runtime

唯一受支援：

```text
Kiro CLI V3
```

正式啟動：

```bash
kiro-cli --v3 acp --auth-method cli
```

ACP over stdin/stdout，使用 JSON-RPC 2.0。

- Agent：`ppt-engineer`
- Agent selection：`session/set_mode`
- Agent confirmation：`config_option_update` / `current_mode_update`
- V2：**不支援**，不得 fallback

V3 的 `acp` 子指令不接受 `--agent`，因此 `ppt-engineer` 必須在 ACP session 內切換。

`--auth-method cli` 讓 kiro-cli 自己解析 access token。省略時 V3 引擎會要求 ACP client
代為提供 token，這是本 Skill 禁止的行為。

舊 caller 若仍送出 `engine = "v2"`，一律回報並拒絕執行：

```text
UNSUPPORTED_KIRO_ENGINE
```

### 5.2 正式流程

```text
AGY
  -> kiro_acp_bridge.py
  -> Kiro CLI V3 ACP
  -> 使用既有 Kiro Pro CLI OAuth session
  -> session/new
  -> 發現 ppt-engineer
  -> session/set_mode
  -> 確認 agent scope
  -> engineering task
  -> permission enforcement
  -> TurnEnd
  -> AGY
```

派工使用：

```bash
python3 scripts/kiro_acp_bridge.py --input job.json
```

AGY 送出的工程任務至少包含：

- repository root
- 問題或需求
- 可修改範圍
- acceptance criteria
- 要跑的 tests/checks
- 禁止自行改簡報內容與視覺策略
- 完成後必須回 AGY

### 5.3 Agent selection 與 scope

`session/set_mode` 請求：

```json
{"method": "session/set_mode", "params": {"sessionId": "...", "modeId": "ppt-engineer"}}
```

`session/set_mode` 即使 `modeId` 不存在也會回傳空結果，所以不得把 response 當成成功證據。
唯一確認來源是引擎回報的 active agent：`session/update` 的 `config_option_update`
（`configOptions[id="mode"].currentValue`），或標準 `current_mode_update`。

dispatch 前必須滿足：

```text
diagnostics.agent_requested = "ppt-engineer"
diagnostics.agent_resolved  = true
diagnostics.agent_scoped    = true
```

不成立時不得送出 coding task，回報：

```text
ENGINEERING_AGENT_UNAVAILABLE
```

不得默默使用 `kiro_default` 或任何引擎預設 agent 執行 AGY 的 engineering task。

### 5.4 Agent scope 是 turn-long invariant

`ppt-engineer` 必須是整個 engineering turn 的 runtime invariant。

從 `session/prompt` 送出，到 `stopReason = end_turn` 之前，只要任何 ACP event 顯示
active agent 已不是 `ppt-engineer`，即視為 agent scope loss：

1. 記錄 diagnostics
2. timeline 加入 `agent_scope_lost`
3. 停止批准新的 permission request
4. `session/cancel`
5. 套用既有 cancel grace period
6. 清理 child process group
7. 回報 `ENGINEERING_AGENT_SCOPE_LOST`

不得自動切回 `ppt-engineer` 後繼續、不得繼續批准 tool call、不得判定 completed、
不得 silently restart。

### 5.5 失敗回報

```text
ENGINEERING_WORKER_UNAVAILABLE   Kiro 無法啟動或 ACP handshake 失敗
ENGINEERING_AGENT_UNAVAILABLE    worker 可連線但 agent scope 無法確認
ENGINEERING_AGENT_SCOPE_LOST     turn 中 active agent 漂移
UNSUPPORTED_KIRO_ENGINE          caller 要求非 V3 engine
```

都不得偷偷切 API key，也不得由 AGY 接手寫 code。

### 5.6 Permission boundary

`.kiro/agents/ppt-engineer.md` 定義 Agent 能力。
`scripts/kiro_acp_bridge.py` 定義 runtime enforcement。
兩者衝突時採**較嚴格者**。

允許：

- 讀取專案檔案
- 寫入 repository root 內的檔案
- `python` / `python3` / `pytest`（含 `-m unittest`、既有 script）
- `pip list` / `pip show` / `pip check`

拒絕並記錄到 `policy_violations`：

- 版本控制（本工程 Worker 不提供 Git 能力）
- shell chaining / pipeline / command substitution（`&&`、`||`、`;`、backtick、`$()`）
- `sudo`、destructive filesystem 命令、未授權 package execution
- repository root 之外的寫入
- dependency / lockfile 變更（預設需額外授權）
- `codex`、`$imagegen`、`image_gen`（永久拒絕）

Dependency 變更預設關閉：

```json
{"allow_dependency_changes": false}
```

未取得 explicit opt-in 時 reject，並記錄：

```text
dependency_change_requires_explicit_authorization
```

`true` 只代表通過 dependency gate，仍必須通過 shell parser、command safety、
workspace policy 與 permission mode。

Kiro 永遠不得自行呼叫 Codex。

## 6. 正常簡報流程

1. AGY 讀取來源資料。
2. AGY 決定 audience、objective、page count、storyline。
3. AGY 在內部保存完整大綱，只向使用者提交自然語言的大綱內容；使用者核准前不得進入 style、sample 或整套生圖。
4. 大綱核准後，AGY 提出視覺方向與 required assets；使用者核准風格前不得生樣張或整套簡報。
5. 大綱與風格均核准後，AGY 選定第一張適合的非封面內容頁（或使用者指定頁），建立單一 sample slide job。
6. AGY 派 Codex 走正式單頁生成路徑，**只生成 1 張**真實樣張。
7. AGY QA 後必須讓使用者核准樣張；未核准時只能修改並重生單張樣張。
8. 只有 `outline`、`style`、`sample` 三個 gate 均為目前 deck revision 的 `approved`，AGY 才使用既有 upstream scripts 初始化其餘 jobs。
9. AGY 逐頁派 Codex 產圖。
10. 每個 Codex worker 完成後都回 AGY。
11. AGY 檢查文字、事實、版式、required assets、風格一致性。
12. 不合格的頁面由 AGY 下達精準修正 job，再交 Codex。
13. AGY 產生 `speech.md`。
14. AGY 執行既有 `assemble_ppt.py`。
15. AGY 驗證最終 `.pptx`、頁數與 notes。
16. AGY 回報產物。

預設互動流程固定依序確認大綱、視覺方向與一張真實樣張，再完成整份簡報。內部狀態為：

```text
REQUEST -> OUTLINE_PENDING_APPROVAL -> STYLE_PENDING_APPROVAL
        -> SAMPLE_PENDING_APPROVAL -> FULL GENERATION
```

大綱異動會撤銷大綱核准並使 style/sample gate 回到 pending；風格異動會撤銷
style 核准並使 sample gate 回到 pending；樣張異動後 sample 維持 pending，直到使用者
再次核准。既有明確 non-interactive mode 若有自己的已承諾行為則維持不變；不得新增
臨時 bypass 來跳過預設 gate。`scripts/presentation_workflow.py` 只讓 AGY 寫入核准狀態，
generator callback 不會取得 Project State，也無權推進 gate。

### 6.1 內容修訂與風格修訂

`outline.md` 只擁有 **WHAT**：頁序、目的、標題、敘事、核心訊息、實例與事實。
`deck_spec.json` 只擁有 **HOW**：視覺方向、色彩、字體、留白、版式、影像處理、
圖像比例、元件風格與資訊密度的視覺呈現。deck spec 中為 renderer 準備的標題或重點是
核准大綱的衍生輸入，不得反過來改寫大綱。

AGY 先把回饋判定為結構化修訂意圖，再呼叫 workflow；workflow 本身不猜自然語言：

- **純風格**：例如更高級、少一點制式企業感、金融雜誌風、淺色背景、大照片、
  視覺上少字、高留白、換色彩／字體／卡片／構圖。只更新 HOW，保留目前大綱 revision
  與大綱核准；撤銷風格與樣張核准，重新確認風格後只生一張新樣張。
- **內容**：例如換頁序、刪頁、換實例、換受眾／論點／標題含義／主題／story arc。
  更新 WHAT，撤銷大綱及相依核准，回到大綱確認。
- **混合**：同一則回饋同時含內容與風格變更，一律走內容修訂路徑。

純風格修訂不得帶入或覆寫 outline payload。若版面需要更短的顯示文案，該文案只能是
render 階段的衍生資料，不得成為新的大綱內容。

### 6.2 使用者訊息

正常對話使用簡短自然語言：先請使用者確認大綱；風格階段只摘要視覺方向、色彩、
字體、影像與密度；樣張階段提供一張真實樣張並請使用者確認；完成時優先提供 PPTX
與必要預覽。除非使用者要求技術細節、進入除錯模式或錯誤診斷確實需要，對話不得顯示
gate 編號、內部狀態常數、內部檔名／路徑或 worker dispatch 細節；尤其不得把
`outline.md`、`deck_spec.json`、`project_state.json`、`slide_jobs.json` 當成一般使用者
產物或在大綱建立／修訂訊息中提及。這些內部檔案仍須正常保存與運作。只有使用者明確
要求專案內部資訊、開發／除錯模式明確需要，或真實錯誤診斷需要具體檔案時才能揭露；
最終交付則可明確命名 PPTX 等對使用者有意義的產物。

樣張回覆不附帶冗長的自製 Visual QA 報告；只有實際警示才簡短揭露。QA 說法必須符合
真正執行的檢查，不得使用「逐字完全無錯」、「完全無擁擠」或「百分之百正確」等
超出證據的絕對保證。

### 6.3 文字密度與 Visual QA 原則

1. **不設定固定字數上限**：AGY 不得單純因為文字超過某個固定字數，就強制拆頁、刪除文字、縮寫內容、改寫權威文案（authoritative text）或遺漏條件說明。文字內容完整性永遠優先。
2. **實績驗證範圍**：Phase 8A 實測已驗證目前系統至少能穩定處理約 79～239 字／頁的高密度繁體中文內容（此為已驗證成功範圍，而非系統硬性上限）。不建立硬性 240 / 300 字門檻，更高文字量依實際 Visual QA 判斷。
3. **以 Visual QA 決定是否需要拆頁**：只要生成後的圖片符合：
   - authoritative text 完整且文字完全正確
   - 字級清楚可讀、無裁切、無重疊
   - 換行合理、層級清楚
   - 版面仍具備合理留白與可接受的整體閱讀負荷
   即可判定 `qa_passed`。不得僅因為「文字很多」本身判定失敗。
4. **高文字量優先調整版型**：若單頁文字量較高，AGY 應在 prompt 與版面策略上優先考慮雙欄、2×2、2×3、多區塊卡片、比較矩陣、Checklist、流程、階梯、Framework 等分區架構，避免預設使用容易擁擠的單欄長條列。
5. **Regenerate 優先於拆頁**：若內容完整但第一版排版太擠、字級過小、間距不足或閱讀動線不佳，先由 AGY 判定 `generated -> qa_failed -> ready -> regenerate`，要求 Codex 採用更適合高資訊密度的版型。只有當 AGY 判斷「在維持完整文字與可讀性的前提下，單頁確實無法合理容納」時，才允許拆頁。

## 7. 工程例外流程

正常簡報製作不需要每次經過 Kiro。

只有出現工程需求時：

```text
AGY 發現 coding/tooling 問題
  ↓
定義工程需求與 acceptance criteria
  ↓
Kiro 修改 / debug / test
  ↓
Kiro 回報
  ↓
AGY 驗收
  ↓
AGY 回到原本簡報流程
```

## 8. 既有指令碼規則

AGY 可以執行已存在的：

- `scripts/assemble_ppt.py`
- `scripts/prepare_slide_prompts.py`
- `scripts/phase18_codex_worker.py`（Phase 18 Hybrid/Clean Plate image job）
- `scripts/kiro_acp_bridge.py`
- state / dispatch / result scripts
- runtime bootstrap / validation helpers

若上述 script 需要新增、修改、修復或測試，必須交給 Kiro。

## 9. 狀態 ownership

全域 workflow state 只能由 AGY 決定。

Codex 只能回 renderer result。

Kiro 只能回 engineering result。

Worker 不得把自己的區域性狀態當成整份簡報的真實狀態。

AGY 專用的 deterministic project state 記錄在 `<workspace>/project_state.json`，
由 `scripts/project_state.py` / `scripts/validate_project.py` 操作：

- deck phase 機：`intake -> outline -> style -> sample -> slide_generation ->
  visual_qa -> assembly -> complete`，任何 phase 可 `-> blocked`。
- slide state 機：`planned -> ready -> generating -> generated ->
  qa_passed/qa_failed -> assembled`，`generation_failed` 可退回 `ready` 重生。
- `controller` 永遠 `agy`；`sequential_only` 永遠 `true`（第一版）。
- Codex 回 `generated` **不等於** `qa_passed`；只有 AGY 能做 `generated -> qa_passed`。
- worker result 不得寫 project phase；generation counter、attempt history、
  resume/recovery、idempotency、corrupt-state 保護、path safety 皆為 deterministic。
- 禁止 worker chain（`AGY -> Kiro -> Codex`、`AGY -> Codex -> Kiro`）。

詳見 `docs/runtime-state-and-routing.md`。

Schema：`schemas/project_state.schema.json`、`schemas/slide_job.schema.json`、
`schemas/worker_result.schema.json`。

## 9.1 Freeze 狀態

| 元件 | 狀態 |
| --- | --- |
| `scripts/kiro_acp_bridge.py`（Kiro ACP Bridge） | **Production Baseline / Frozen** |
| `scripts/codex_image_adapter.py`（Codex Image Adapter，含 Phase 5.1 ambiguity fix） | **Production Baseline / Frozen** |

Freeze 意義：除非出現實際 integration blocker / bug，否則後續 Phase 不得順手 refactor。

## 9.2 Source Grounding & Traceability（optional，source-driven 專案適用）

`scripts/source_grounding.py` 提供一組獨立於 `project_state.py` 的 sidecar
artifact（`source_inventory.json`、`claim_traceability.json`、
`source_coverage.json`、`source_grounded_qa.json`），供有 source document 的
專案（例如需要對照契約、報告等原始文件產出簡報）記錄 source unit、claim 對應、
coverage accounting 與最終 grounded QA report。

- **Optional capability**：純創意、無 source 的簡報完全不受影響，不需要建立
  任何這裡描述的 artifact。單一判斷方式：
  `source_grounding_enabled(workspace)`——只有 `source_inventory.json` 存在
  且 `enabled: true` 才算啟用。使用者只提供 logo／參考圖／風格樣張時
  **不算** factual source，不得因此啟用。
- **兩層分離**：AGY 負責 semantic judgement（source 切分、claim 對應、claim 是否
  被 source 支持、coverage priority 與 omission 理由、數字/模態語意、最終
  Content QA outcome）；Python validator 只負責 schema 形狀、ID 完整性、參照
  存在性、coverage accounting 與 unresolved-claim 偵測，**永遠不會自己判斷一個
  claim 是否為真**，也不做 OCR、不解析契約語意。
- **與既有 Visual QA 完全分離**：不改寫、不覆蓋 `generated -> qa_passed/qa_failed`
  的既有語意。Content QA（source grounding）與 Visual QA 是兩個獨立 gate。

### 9.2.1 Source-driven 分支（接在第 6 節正常流程之上）

當 `source_grounding_enabled(workspace)` 為 true 時，AGY 在既有流程中額外負責：

| 既有流程階段 | 額外的 source-grounding 動作 |
| --- | --- |
| 1（讀取來源資料） | 建立 `source_inventory.json`（`enabled: true`）、記錄 `source_digest`、把 source 切成 source units 並標 priority |
| 3（確認 `outline.md`） | 規劃每個 source unit 的 coverage 意圖（進 slide / 只進 speaker notes / 明確不放並附理由） |
| 9–10（逐頁產圖並收回結果） | 為每頁登錄 claims（`claim_id`、`source_unit_ids`） |
| 11（AGY 檢查文字、事實、版式…） | Content QA：為每個 claim 給出 `support_status`，記錄 numeric/modal evidence，完成 coverage accounting |
| 13（產生 `speech.md`） | 只進 speaker notes 的 source-dependent claim 也要有 claim 與 `speaker_notes_only` coverage |
| **14 之前（執行 `assemble_ppt.py` 前）** | **必須**先跑 deterministic gate：`python3 scripts/validate_source_grounding.py <workspace>`。exit code 非 0 時**不得**呼叫 `assemble_ppt.py`，改為修復 grounding/Content QA 後重新驗證 |
| 16（回報產物） | 產生／更新 `source_grounded_qa.json`，含 AGY 的 `agy_qa_outcome` |

Gate 失敗是 **grounding precondition failure，不是 assembly failure**
（`assemble_ppt.py` 根本沒被呼叫），不得記錄成 Phase 9 assembly recovery；
也不會讓專案進入 `blocked`——它是可恢復的 AGY workflow issue。

詳見 `docs/source-grounding.md`。Schema：`schemas/source_inventory.schema.json`、
`schemas/claim_traceability.schema.json`、`schemas/source_coverage.schema.json`、
`schemas/source_grounded_qa.schema.json`。

## 9.3 Source Ingestion（optional，本機來源檔案適用）

當 source-driven 專案的來源是**本機**的 PDF（具可擷取文字層）、Markdown、純文字、
DOCX 或靜態 HTML 檔時，第 1 階段（讀取來源資料）可以先用
`scripts/ingest_source.py` 做 deterministic 擷取，再由 AGY 進行 semantic
segmentation：

```text
local source
  → scripts/ingest_source.py（deterministic extraction）
  → AGY semantic segmentation
  → source_inventory.json 的 source units
  → 9.2 的 grounding workflow
```

```bash
python3 scripts/ingest_source.py \
    --source <file> --source-id <src_id> --output <extraction.json>
```

- **Extraction 不等於 semantic understanding**：ingestion 只產出 blocks 與
  locator（PDF 1-based 頁碼、Markdown heading 層級與行號、純文字行號範圍、
  DOCX heading 層級與結構性元素／表格序號）。
  **它不決定** 什麼重要、priority、claim 語意或 coverage。
- **Block 不是 source unit**：AGY 決定要把哪些 block 升級成 Phase 12 source unit，
  ingestion 不會自動升級，也不會寫出任何 Phase 12 artifact。
- **PDF 需要文字層**：掃描／純影像 PDF 會以 `SOURCE_TEXT_UNAVAILABLE` 明確失敗，
  **沒有 OCR fallback**。
- **DOCX 是結構性擷取**：擷取 heading 層級、段落與表格，並保留文件順序。DOCX 是
  flow-based OOXML，**沒有可靠的 rendered 頁碼**，因此不提供也不虛構頁碼 locator；
  headers/footers/footnotes/comments 與內嵌圖片文字皆不擷取。
- **HTML 是本機靜態擷取**：只讀本機 `.html`／`.htm`，擷取 heading、段落、清單與表格
  並保留 DOM 順序。**不執行 JavaScript、不使用 browser、不套用 CSS、不下載任何遠端
  或本機參照資源、不追蹤超連結、不抓取 iframe**；`script`／`style`／`noscript`／
  註解／JSON-LD 皆排除。網路活動為 zero。
- 遠端來源需另外經由 9.4 的 acquisition 層明確取得；web crawling、browser rendering
  與 OCR 目前不支援。
- `source_digest` 直接沿用 Phase 12 的 `compute_source_digest()`，全專案只有一個
  canonical fingerprint 定義。

詳見 `docs/source-ingestion.md`。

## 9.4 Remote Source Acquisition（optional，明確指定的公開 URL 適用）

若來源不在本機，而是一個**明確指定的公開 URL**，可先用
`scripts/acquire_source.py` 取得成本機 payload，再交給 9.3 的 ingestion：

```text
明確指定的公開 URL
  → scripts/acquire_source.py（bounded acquisition）
  → repository 外部的本機 payload
  → Phase 13 ingestion
  → AGY semantic segmentation
  → source_inventory.json 的 source units
  → 9.2 的 grounding workflow
```

```bash
python3 scripts/acquire_source.py \
    --url https://example.org/source.pdf \
    --source-id <src_id> --output-dir <workspace> --ingest
```

- **Acquisition 不等於 extraction**：本層只負責取得位元組，不解析、不判斷格式、
  不做語意判斷。`Content-Type` 只是 metadata，格式判定仍由既有 detection 決定。
- **只支援公開未認證來源**：只允許 `http`/`https`，拒絕 URL 內嵌帳密，不使用 cookie、
  `.netrc`、雲端憑證或任何 token。**沒有** browser、**沒有** JavaScript、
  **沒有** crawler，也不會遞迴抓取 asset／iframe／連結。
- **SSRF 護欄**：拒絕 `localhost` 與解析到 loopback／private／link-local／reserved
  的目的位址，**每一個 redirect 跳點都重新驗證**，redirect 上限 5，response 上限
  25 MiB，TLS 正常驗證。**這不是 hardened SSRF sandbox**，仍有 DNS-rebinding 殘餘
  風險，詳見 `docs/source-acquisition.md`。
- **Payload 落在 repository 之外**：由呼叫者指定 output directory，不建立隱性永久快取。
- `source_digest` 仍是 Phase 12 的 `compute_source_digest()`，對取得的原始位元組計算；
  `retrieved_at` 只供稽核，不影響任何 ID。

詳見 `docs/source-acquisition.md`。

## 9.5 Presentation Intelligence & Delivery Quality

每次簡報規劃都應在既有核准流程內套用 Phase 17，而不是新增使用者 gate：

1. 從使用者明確提供的 audience、purpose、desired outcome、context、duration 與 constraints
   建立內部 Presentation Brief；只可做非敏感、顯而易見的 context inference，不得建立
   psychographic profile 或推定敏感特徵。未提供 duration 時不得虛構精確時長。
2. 在向使用者顯示大綱前，先套用 Phase 16 claim-origin 與 evidence boundary。沒有來源或
   使用者明確提供的事實時，不得把情境稱為「真實案例」，也不得虛構比例、金額、日期、
   成效、法規／合約必要性、服務時限、公司承諾或引用；教學用情境必須誠實標為示意／假設，
   AGY synthesis 不得冒充 grounded fact。No-source 簡報只能把使用者明確提供的 material fact
   當成 USER_PROVIDED；其餘內容必須是明確的建議、框架、問題或示意，不得以肯定句包裝成
   已驗證事實。送出大綱前必須掃描所有數字、日期、百分比、比較級、法規字眼與營運承諾：
   沒有可用 provenance 就刪除、改成不帶事實主張的表達，或向使用者詢問；不得以「常識」補值。
3. 在大綱核准前，以 `phase17_narrative.py` 的概念安排 deck thesis、narrative role、slide
   intent、takeaway、job-to-be-done、opening、closing 與 transitions。Narrative role 與 Phase 16
   visual role 必須分離。接著必須以 `presentation_content_quality.py` 對準備呈現給使用者的實際
   title/key points 做 content-quality preflight：辨認只有主題標籤而沒有觀點的 headline、重複且
   空泛的 schema-fill copy、mode-aware density、重複標題，以及 narrative role 與實際文案錯位。
   Label-only finding 不是全域禁令；cover、legal、technical、report 等情境由 AGY 依 audience 與
   purpose 判斷。任何 assertion 仍必須先通過 Phase 16 evidence/provenance boundary；preflight 不得
   自己認定 support，也不得自動改寫內容。
4. 用 `phase17_visual_communication.py` 選擇最簡單且能服務 takeaway 的 information form，並記錄
   hierarchy 與 image purpose；不得改寫 Phase 16 evidence 或要求 renderer 判斷 evidence support。
5. 用 `phase17_delivery.py` 依 narrative weight 規劃 Notes、transitions、rehearsal cues 與時間。
   Timing 是保守估計，不是保證；內容明顯超時時不得宣稱符合時限。
6. 完成前以 `phase17_effectiveness.py` 整合 narrative、visual、delivery findings 與 Phase 16
   evidence/editorial report。不得產生總分、engagement probability、persuasion score 或
   AI-generated score。

在每次把 outline、style、sample 說明或 final summary 顯示給使用者前，先做一次 bounded Human
Editorial review：減少 slogan、抽象商業術語與過度銷售式修辭（例如連續使用「打造、賦能、
共贏、金礦、護城河、高價值」），改為可口述、具體、克制的簡報語言。這些詞不是 blacklist；
重點是避免重複、空泛與機械感，且 editorial rewrite 絕不可改變 claim meaning。

一般使用者仍只看到「大綱 → 風格 → 一張真實樣張 → 完整簡報」。不得預設顯示 enum、ID、
QA constant、timing model、internal report、中間產物 filename 或 absolute path。樣張核准時應直接
顯示／附上圖片並自然稱為「第 N 頁樣張」，不得把 `slide_02.png` 等內部名稱當作一般交付物；
最終交付時才可有意義地命名實際 PPTX。Notes wording、transition 與 timing annotation 等
non-semantic cleanup 可安全調整；新增／移除／重排頁面、改 takeaway／recommendation／fact／thesis
必須走既有 content revision 並重新核准大綱；substantive HOW change 依既有規則重開 style/sample。

Phase 17 的 typed findings 是給 AGY 的 review input；AGY 仍是唯一 semantic authority。任何
外部 semantic classifier 都只能提供 narrow、confidence-gated finding，不得自動改動 evidence、
approval state 或最終 readiness policy，也不得出現在 deterministic CI 的必跑路徑。

在 outline 顯示前若 content-quality preflight 回報 `REVIEW_REQUIRED` 或 `BLOCK`，AGY 應先依原始
request、audience、narrative intent 與 evidence 修整內容，再重新執行 deterministic preflight。
Outline 核准後才發現需要改 headline、takeaway、claim 或 key point 時，屬 substantive WHAT change，
必須走既有 content revision／outline reapproval；不得由 slide worker 靜默升級標題、補事實或重寫
claim。`prepare_slide_prompts.py` 會再次明示 worker 只能保留已核准內容的語意，不能把 topic label
自行變成 factual assertion。

## 10. 必讀檔案

- `docs/architecture-and-design-rationale.md`
- `docs/agent-routing.md`
- `docs/oauth-subscription-runtime.md`
- `docs/codex-image-runtime.md`
- `docs/runtime-state-and-routing.md`
- `docs/workflow-gates-and-progress.md`
- `docs/outline-style-and-sample.md`
- `docs/slide-generation-and-subagents.md`
- `docs/project-assembly-and-reporting.md`
- `docs/source-grounding.md`（optional，僅適用於有 source document 的 source-driven 專案）
- `docs/source-ingestion.md`（optional，僅適用於需要擷取本機 PDF/Markdown/純文字/DOCX/HTML 來源的專案）
- `docs/source-acquisition.md`（optional，僅適用於需要取得明確指定的公開 URL 來源的專案）
- `docs/production-baseline-phase13.md`（Phase 13 production capability 摘要）
- `docs/phase16-grounded-presentation-and-editorial-quality.md`（Phase 16 frozen evidence/editorial baseline）
- `docs/phase17-presentation-intelligence-and-delivery-quality.md`（Phase 17 frozen strategy/delivery baseline）
