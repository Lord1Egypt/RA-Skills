# Source Grounding & Traceability（Phase 12.1 + 12.2 + 12.3）

本文件描述 Phase 12 建立的 source-grounding sidecar 系統，以及它在 AGY
workflow 中的正式整合方式（Phase 12.3）。這是 **optional capability**：純創意、
無 source document 的簡報完全不受影響，也不需要建立任何本文件描述的 artifact。

## 1. 與 v0.1.0 baseline 的關係

`docs/production-baseline-v0.1.0.md` 是 immutable 的歷史 baseline 文件，記錄
v0.1.0 release 當時「source traceability」「source-grounded QA」尚未有 reusable
production 實作。本文件記錄的是 v0.1.0 **之後** 新增的能力，不會、也不應該回頭
修改 v0.1.0 baseline 文件本身。

## 2. 核心設計原則：兩層分離

Source grounding 拆成兩層，**不得混淆**：

### Layer A — Semantic Evidence Creation（AGY 擁有）

AGY 負責：

- 理解 source document
- 定義 source units（要拆成哪些段落/頁面/條款）
- 判斷某個 slide claim 對應哪個/哪些 source unit
- 判斷該 claim 是否真的被 source 支持（`support_status`）
- 判斷 source unit 的 coverage priority（`HIGH` / `MEDIUM` / `LOW`）
- 判斷數字、模態語言（must/may/shall...）、權責歸屬的語意
- 產生 traceability evidence 並持久化

### Layer B — Deterministic Contract Validation（`scripts/source_grounding.py`）

Python 負責：

- schema 形狀驗證
- ID 唯一性、可推導性（`unit_id` 必須能從 `source_id` + `locator` 重新算出來）
- 參照完整性（`claim_traceability.json` 裡的 `source_unit_ids` 必須真的存在於
  `source_inventory.json`；`slide_id` 必須真的存在於 `project_state.json`）
- HIGH priority source unit 的 coverage accounting 完整性（不能默默消失）
- 合法 status 值檢查
- resume-safe 的 atomic 持久化

**Python 永遠不會**：

- 自己判斷一個 claim 是否為真
- 自己理解契約/文件的語意
- 取代 AGY 的 Content QA 或 source understanding
- 取代既有的 Visual QA（`generated -> qa_passed/qa_failed`）

## 3. 四個 sidecar Artifact

全部存在 workspace 根目錄，與 `project_state.json` 同層（`prompts/slide_XX.json`
的相同 pattern：additive，不複製、不取代）：

| 檔案 | Schema | 目的 |
| --- | --- | --- |
| `source_inventory.json` | `schemas/source_inventory.schema.json` | 把 source document 拆成穩定的 source units |
| `claim_traceability.json` | `schemas/claim_traceability.schema.json` | 記錄每個 slide claim 對應哪些 source unit，以及 AGY 的支持判斷 |
| `source_coverage.json` | `schemas/source_coverage.schema.json` | 每個 source unit 的 deterministic accounting |
| `source_grounded_qa.json` | `schemas/source_grounded_qa.schema.json` | 最終報告，明確拆成 `deterministic_findings` 與 `semantic_findings` 兩個區塊 |

## 4. Optional Capability

`source_inventory.json` 不存在，或存在但 `enabled: false`，代表這個專案**沒有**
啟用 source grounding：

```python
from source_grounding import source_grounding_enabled
source_grounding_enabled(workspace_root)  # False when file absent or enabled=false
```

在這個狀態下：

- 不需要 `claim_traceability.json` / `source_coverage.json` /
  `source_grounded_qa.json`
- `assembly_precondition_errors()` 一律回傳空陣列（不 block 組裝）
- `project_state.py` 完全不知道、也不需要知道這個模組存在

## 5. Stable IDs

| ID | 格式 | 推導方式 |
| --- | --- | --- |
| `source_id` | `src_<caller-supplied-slug>` | AGY 提供，人類可讀，不含絕對路徑 |
| `unit_id` | `su:<source_id>:<12-hex>` | `compute_unit_id(source_id, locator)`：對 `(source_id, canonical_json(locator))` 取 sha256 前 12 hex，deterministic、resume-safe，重新計算永遠得到相同值 |
| `claim_id` | `cl:<slide_id>:<NN>` | `make_claim_id(slide_id, sequence)`，deterministic |

沒有任何 ID 使用 random UUID 作為唯一身分，也沒有任何 ID 包含 OS 絕對路徑。

Phase 15.5 OCR 接地轉譯沿用本節 frozen locator union：PDF page 使用 `start/end`，standalone single image 使用既有 `generic` kind 的 deterministic label `image:1-of-1`。轉譯只建立可供 AGY promotion 的 additive evidence envelope，不改變本模組的 locator schema 或 semantic authority。

## 6. Source Locator Contract

`locator` 是一個可擴充的 tagged union，**不綁死 OS 絕對檔案路徑**：

```json
{"kind": "page", "start": 12, "end": 12}
{"kind": "section", "label": "Termination"}
{"kind": "line_range", "start": 40, "end": 55}
{"kind": "generic", "label": "Appendix B"}
```

Phase 12.1/12.2 只定義 contract，不內建 PDF/DOCX/Markdown parser；未來若要自動
從真實文件產生這些 locator，屬於後續 Phase 的工作。

## 7. Source Privacy

- `source_digest` 只存 sha256 hex digest（`compute_source_digest()`），**永遠
  不存來源文件的原文**。
- `source_changed(source_id, current_digest)` 用來偵測來源是否已更動；偵測到
  改變後是否要作廢舊的 traceability evidence，是呼叫端（AGY/未來的 workflow
  整合）的明確決策，本模組只提供 `SourceChanged` 這個 error class 供呼叫端使用，
  不會自動、悄悄地沿用過期 evidence。
- Metadata 中任何 credential-shaped key（`api_key`、`access_token` 等）會被
  `validate_source_inventory()` / `validate_claim_traceability()` /
  `validate_source_coverage()` / `validate_source_grounded_qa()` 拒絕，與
  `project_state.py` 的 `_reject_credentials` 精神一致（各自獨立實作，未共用
  import，避免 sidecar 與 frozen 核心互相耦合）。

## 8. 錯誤代碼

```text
SOURCE_INVENTORY_INVALID
TRACEABILITY_INVALID
SOURCE_REFERENCE_MISSING
SOURCE_COVERAGE_INCOMPLETE
GROUNDED_QA_INCOMPLETE
SOURCE_CHANGED
```

這些是獨立的 error 家族，**與** `IMAGE_GENERATION_FAILED`、
`IMAGE_BACKEND_UNAVAILABLE` 等 worker/image error **完全分離**；不共用同一個
retry/block policy。Phase 10.2/10.3 的「連續兩次相同 image failure 即 block」
語意不因本模組而改變。

## 9. Assembly Gate（deterministic precondition，已整合進 AGY workflow）

`evaluate_assembly_gate(workspace_root, known_slide_ids, *, current_source_digests=None,
require_grounded_qa=True)` 是**唯一**的 deterministic grounding gate 實作。
`assembly_precondition_errors()` 是回傳 `list[str]` 的薄包裝，
`scripts/validate_source_grounding.py` 是薄 CLI adapter——三者共用同一份 logic，
不存在第二套 validation。

Gate 行為：

- source grounding 未啟用 → 立刻 `ready=True`（不 block，不要求任何 artifact）
- 已啟用時，依序檢查：
  1. 三個 artifact 可載入且 schema 有效
  2. 沒有 dangling `source_unit_id` / `slide_id`
  3. coverage accounting 完整、未重複膨脹
  4. 沒有 HIGH priority unit 停留在 `unaccounted`
  5. 沒有 claim 停留在 `unsupported` / `pending_review`
  6. （若提供 `current_source_digests`）source digest 仍相符
  7. `source_grounded_qa.json` 存在、結構有效，且
     `semantic_findings.agy_qa_outcome` ∈ `("passed", "passed_with_notes")`

CLI 使用方式：

```bash
python3 skills/agy-ppt/scripts/validate_source_grounding.py <workspace>
python3 skills/agy-ppt/scripts/validate_source_grounding.py <workspace> \
    --source-digest src_agreement=<sha256hex>
python3 skills/agy-ppt/scripts/validate_source_grounding.py <workspace> --skip-grounded-qa
```

exit code：`0` = 未啟用或 gate 通過；`1` = grounding precondition 失敗；
`2` = `project_state.json` 無法讀取。

### 9.1 Grounding precondition failure ≠ assembly failure

**極重要的邊界**：gate 失敗時 `assemble_ppt.py` **根本沒有被呼叫**，所以這
不是 assembly failure，不得記錄成、也不得混入 Phase 9 的 assembly recovery
語意。正確流程是：

```text
precondition fails
→ 交回 AGY Content QA / grounding repair
→ 修好後重新驗證
→ 才呼叫 assemble_ppt.py
```

### 9.2 不新增 Project State blocker path

一般 grounding validation failure（缺 mapping、coverage gap、unsupported
claim、stale evidence）視為**可恢復的 AGY workflow issue**，不會讓
`project_state.json` 進入 `blocked`。本階段刻意不新增任何 Project State
blocker 路徑；`project_state.py` 完全未被修改。

## 10. Content QA vs Visual QA

- **Content QA**：claim support、source grounding、數字/模態語言 fidelity、
  coverage——由本模組的 artifact 承載 AGY 的判斷，deterministic validator 只
  驗證形狀與參照完整性。
- **Visual QA**：視覺品質、版式、渲染、圖片正確性——由
  `project_state.py` 既有的 `generated -> qa_passed/qa_failed` state machine
  處理，**完全不受本模組影響**。

`source_grounded_qa.json` 的 `semantic_findings.agy_qa_outcome` 是 Content QA
的持久化結果，與 slide 的 Visual QA 狀態是兩個獨立的欄位、獨立的檔案，永遠不會
互相覆寫。

## 11. Numeric / Modal Fidelity

`claim_traceability.json` 每個 claim 可以附帶：

```json
"numeric_evidence": {
  "source_value": "90 days",
  "slide_value": "90 天",
  "unit": "days",
  "comparison_status": "match"
}
```

```json
"modal_evidence": {
  "source_modality": "shall",
  "slide_modality": "must",
  "responsible_party": "Vendor",
  "comparison_status": "match"
}
```

`comparison_status` 的值（`match` / `mismatch` / `not_comparable`）由 AGY 提供
並持久化。Deterministic validator 只驗證這個欄位是否為合法列舉值，**不會**
自己解析或比較數字/法律語意——避免用脆弱的 regex 假裝理解整份文件。

## 12. Speaker Notes

`assemble_ppt.py` 既有、frozen 的 `speech.md` → PPTX notes 寫入機制未被修改。
若未來要讓 speaker-note claims 也進入 traceability，屬於 Phase 12.3 的最小
整合工作，不在本階段範圍。

## 13. Activation（如何判斷要不要啟用）

單一 deterministic 判斷方式：

```python
from source_grounding import source_grounding_enabled
source_grounding_enabled(workspace_root)
```

只有 `source_inventory.json` 存在**且** `enabled: true` 才算啟用。沒有第二套
activation authority，也沒有為了一個 boolean 去修改核心 Project State。

**Enabled（source-driven）**：簡報的事實／內容 authority 來自一份或多份明確的
source（契約、報告、PDF、DOCX、Markdown、文字文件、以 document unit 表示的
資料集）。

**Disabled（creative / no-source）**：純創意簡報、腦力激盪、視覺概念稿，或使用者
要求 AGY 在沒有 authoritative source 的情況下自行構思內容。

重要：使用者提供 **logo / 參考圖 / 風格樣張** 時，**不算** source-grounding 的
factual source——visual reference ≠ factual source，不要因此自動啟用。

## 14. Lifecycle（AGY workflow 各階段責任）

| 階段 | AGY（Layer A，semantic） | Deterministic（Layer B） |
| --- | --- | --- |
| **intake** | 判斷是否 source-driven；建立 `source_inventory.json`（`enabled: true`）；指定 stable `source_id`；用 `compute_source_digest()` 記錄 fingerprint；把 source 切成 source units（AGY 是 segmentation authority） | `validate_source_inventory()` 驗證形狀、ID 可推導性、locator、credential guard |
| **outline / coverage planning** | 依 source unit priority 規劃哪些要進 slide、哪些只進 speaker notes、哪些明確不放（含理由） | 尚無強制檢查；coverage artifact 可稍後建立 |
| **slide planning** | 為每頁規劃 claims，決定 slide-local claim 順序 | `make_claim_id()` 產生 deterministic claim_id |
| **slide generation** | 既有 Visual QA 流程完全不變 | 完全不介入（`project_state.py` 獨立運作） |
| **Content QA** | 判斷每個 claim 的 `support_status`、numeric/modal 語意、coverage 決策與 omission 理由、最終 `agy_qa_outcome` | `validate_claim_traceability()`、`validate_source_coverage()` 驗證形狀與參照 |
| **assembly precondition** | 檢視 deterministic findings，修復問題後重新驗證 | `evaluate_assembly_gate()`（見第 9 節） |
| **complete** | 產生／更新 `source_grounded_qa.json` 的 semantic findings | `validate_source_grounded_qa()`；`build_grounded_qa_report()` 計算 deterministic findings |

Coverage 不要求「每個 source unit 都必須變成一頁 slide」，而是要求
**每個 source unit 都必須被 accounted for**（`covered` /
`speaker_notes_only` / `intentionally_omitted`（需理由）/ `not_applicable` /
`unaccounted`）。HIGH priority unit 不得停留在 `unaccounted`。

## 15. Claim Lifecycle

```text
AGY 規劃 claim
→ make_claim_id(slide_id, sequence) 得到 deterministic claim_id
→ 綁定 slide_id
→ AGY 對應 source_unit_ids
→ AGY 給出 support_status（semantic judgement）
→ deterministic validation
→ Content QA 解決所有 unresolved claim
```

- **不從 slide image OCR 抽 claim**，也不新增任何 OCR dependency——AGY 本來就
  知道自己規劃／生成了什麼內容。
- `upsert_claim()` 對同一個 `(slide_id, sequence)` 是**整筆覆寫**，不會把舊的
  evidence（`evidence_note` / `numeric_evidence` / `modal_evidence`）殘留合併
  到語意上已經不同的新 claim 上。
- **Unresolved claim**：`support_status` 為 `unsupported` 或 `pending_review`
  的 claim 會讓 assembly gate 失敗。合法的 resolution 全部由 AGY 執行（刪除
  claim、修改 claim、補上額外 source mapping、改寫成非事實陳述、或覆核後確認
  支持）。deterministic code **只偵測未解決狀態並交回 AGY，永遠不自行修改
  claim**。
- `partially_supported` 視為**已解決**（它已經是一個明確的 AGY 決定，通常伴隨
  `evidence_note`）。

## 16. Resume

Resume（grounding 已啟用）流程：

```text
載入 artifacts
→ 驗證 schema / version
→ 用當前 source digest 比對（stale evidence 偵測）
→ 對照當前 slide 集合驗證參照
→ 保留既有 semantic decisions
→ 從未完成的步驟繼續
```

保證：

- stable ID 不重新產生（`unit_id` 由 `(source_id, locator)` 推導；`claim_id`
  由 `(slide_id, sequence)` 推導）
- AGY 的 semantic decisions 不被清除
- claim / coverage entry 不重複（upsert 語意）
- grounded QA report 不重複（單一檔案 atomic replace）

**Resume 後新增 slide**：既有 slide / claim ID 保持不變，新 slide 取得新的
`slide_id`（`project_state.py` 的 `add_slide()`，slides 以 dict key 儲存，沒有
renumber 邏輯），新 claims 只增加新 ID，不會讓整個 deck 的 traceability 失效。

## 17. Source Change

首次 intake 時用 `compute_source_digest()` 建立 fingerprint。Resume 時重新計算
當前 digest 並比對：

- `current == persisted` → 既有 grounding artifacts 可繼續使用
- `current != persisted` → `SOURCE_CHANGED`，assembly gate 失敗

被視為 stale 而需要 revalidation / regeneration 的 artifact：
`source_inventory`、`claim_traceability`、`source_coverage`、
`source_grounded_qa`。

實作上**不做 destructive delete**：偵測到變更只會讓 gate 失敗並交回 AGY，歷史
evidence 仍在磁碟上，由 AGY 明確決定要修哪些、重建哪些（更新一律走
temp → validate → atomic replace）。這不影響既有 Project State 的
generation counter。

## 18. Non-Source Behavior（mandatory regression 保證）

grounding 未啟用時：

- 不需要 `source_inventory.json` / `claim_traceability.json` /
  `source_coverage.json` / `source_grounded_qa.json` 中的任何一個
- `evaluate_assembly_gate()` 回傳 `enabled=False, ready=True`
- `validate_source_grounding.py` exit code `0`
- `project_state.py` 的 phase / slide state machine、Visual QA
  （`generated -> qa_passed/qa_failed`）完全不受影響

## 19. 尚未完成的部分（Phase 12.4）

- 尚未對真實（非合成測試用）source document 執行過 live 驗證。
- 尚未內建任何 PDF / DOCX / Markdown parser：`locator` 目前由 AGY 自行提供，
  自動從真實文件產生 locator 屬於後續工作。
- 尚未有 release（v0.2.0 等）；Phase 12.3 只存在於 main 開發分支。

這些留給 Phase 12.4（real source validation）與其後的 release preparation。
