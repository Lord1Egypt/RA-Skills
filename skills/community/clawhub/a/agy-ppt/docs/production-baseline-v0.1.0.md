# agy-ppt v0.1.0 Production Baseline

本文件是 v0.1.0 baseline reconciliation audit 的產出，記錄 v0.1.0 release **實際**
保證的 production behavior，以及哪些歷史 claim 屬於 prompt-level 行為、
project-specific artifact，或純粹的 historical live evidence，而不是可重用的
deterministic subsystem。

本文件只描述 public repository（`https://github.com/sujunmin/agy-ppt`，
release `v0.1.0`，commit `3a2c83964890fe8773f479e6e406656bffcbdf29`）中可以被
程式碼、schema、test 或 doc 直接證實的內容。任何無法在 repository 中找到對應
implementation 的能力，本文件都不會宣稱為「guaranteed」。

## 1. Guaranteed Production Features（有 deterministic implementation）

以下能力在 `skills/agy-ppt/` 中有 reusable 的程式碼／schema／test，任何新專案都
可以直接重用，不需要重新實作：

| 能力 | 實作位置 | 說明 |
| --- | --- | --- |
| AGY sole-orchestrator ownership | `SKILL.md`、`docs/agent-routing.md`、`docs/architecture-and-design-rationale.md` | `AGY -> worker -> AGY`，禁止 worker chaining |
| Kiro V3 `ppt-engineer` engineering worker | `scripts/kiro_acp_bridge.py` | 歷史／替代 ACP engineering worker，agent-scope 為 turn-long runtime invariant |
| Codex Production Engineering Worker | repository governance | 明確指派後可執行 production engineering；AGY 仍保有 semantic authority |
| Codex Slide Image Worker | `scripts/codex_image_adapter.py` | 透過訂閱 session 呼叫內建 `image_gen`，backend 固定 `codex_builtin_imagegen` |
| Deterministic Project State | `scripts/project_state.py`、`scripts/validate_project.py`、`schemas/project_state.schema.json` | deck/slide state machine、generation 計數器、attempt 歷史 |
| Generic-failure retry / block 政策 | `scripts/project_state.py`（`consecutive_failure_streak` / `may_retry_immediately` / `block_after_repeated_failure`） | 同一頁連續兩次 `IMAGE_GENERATION_FAILED` 即 block，不無限重試 |
| Operator-confirmed quota blocker | `scripts/project_state.py`（`block_for_operator_confirmed_quota`） | 與 worker error_code provenance 分離記錄 |
| Resume / idempotency | `scripts/project_state.py`（`recover_interrupted`） | 沒有 completed result + 已驗證 artifact 就不視為成功 |
| External `codex-ppt` dependency resolver | `scripts/codex_ppt_dependency.py` | 固定 upstream URL、`main` HEAD、外部快取、offline 重用、deterministic 失敗 |
| No production API-key fallback | `scripts/codex_image_adapter.py`（`sanitize_env`） | 子行程環境移除 API-key 類變數，內建工具不可用時交回 AGY |
| Deterministic 測試套件 | `skills/agy-ppt/tests/recovery/`、`tests/test_codex_ppt_dependency.py`、`tests/test_project_state.py` 等 | 不消耗 AI 訂閱額度，不呼叫真實 Codex/Kiro |

## 2. Historical Validation Only（真實 live run 曾成功，但沒有 generic reusable subsystem）

以下能力在歷史使用中（包含在真實簡報專案上）曾經由 AGY 成功執行，但目前 public
repository 沒有一個獨立、deterministic、可重用的 subsystem 去保證或強制執行它：

- **AGY 對簡報內容進行「事實」與版式檢查**（`SKILL.md` 第 337 行：
  「AGY 檢查文字、事實、版式、required assets、風格一致性」）。這是
  `AGY_PROMPT_ORCHESTRATION_BEHAVIOR`：AGY 被要求在檢查清單中核對事實，但這是
  prompt-level 指示，不是一段可被單獨呼叫、單獨測試的程式碼。
- **speaker notes 與投影片對應正確性檢查**（`docs/project-assembly-and-reporting.md`：
  「speaker notes 對應正確」）。同樣是 AGY 執行的人工檢查清單項目，沒有對應的
  deterministic validator。

歷史上 AGY 曾在某次真實專案中，對照原始來源文件核對簡報內容（例如數字、模態語言、
權責敘述是否忠實反映來源），並產出過像「clause matrix」、「coverage map」、
「source inventory」、「traceability」這類分析產物。**這些是那次專案的
project-specific output，不是 agy-ppt 這個 skill 本身附帶的功能**。它們：

- 不存在於本 repository 的任何版本（`git log --oneline --all` 只有 1 個
  commit，即上游 fork 時的初始 commit；本地開發過程中新增的所有 agy-ppt
  檔案在 v0.1.0 之前皆未被 commit 過，因此也沒有任何「曾經被刪除」的痕跡）
- 不存在於目前的 `skills/agy-ppt/` 樹（scripts、schemas、prompts、references、
  docs、tests 逐一搜尋 `traceability`、`clause`、`coverage`、`inventory`、
  `source_map`、`provenance`、`citation` 等概念，皆無命中，除了兩處與此無關的
  `thread_id`/worker-error-code provenance 註解）
- 因此不是「standalone migration 時意外漏掉的 public production file」，而是
  一開始就不屬於 agy-ppt skill 原始碼的內容

## 3. Project-Specific Artifacts（不屬於 public source repository）

以下不是 agy-ppt 的功能，而是某次具體專案執行過程中產生的一次性文件，因此明確
標示為 **NOT PART OF PUBLIC SOURCE REPOSITORY**：

- Source inventory（某次專案的來源清單）
- Contract clause matrix（某次契約逐條對照表）
- Contract coverage map（某次契約覆蓋範圍圖）
- Source traceability table（某次專案的來源追溯表）
- Numeric fidelity spot audit（某次專案的數字覆核記錄）
- Modal/responsibility language fidelity spot audit（某次專案的用語覆核記錄）
- Speaker notes traceability report（某次專案的備稿追溯報告）

這些文件本質上是「AGY 在某個具體專案 workspace 中產生的 deliverable」，屬於該
專案的 output，而不是 agy-ppt skill 本身的 reusable 程式碼或 schema。它們理應
留在該專案自己的 workspace（`~/projects/<project-name>/` 這類 external project
workspace），不應該、也從未被放進 agy-ppt 這個 skill 的原始碼樹。

## 4. Not Currently Guaranteed（尚無 implementation，也未在 v0.1.0 宣稱）

以下能力目前**沒有** deterministic implementation，v0.1.0 的 README／
CHANGELOG／Release Notes 也刻意沒有宣稱它們是 production feature：

- **Source traceability** 作為 reusable production feature：不存在。目前只有
  AGY 的 prompt-level「檢查事實」指示（見上方第 2 節），沒有任何程式碼把「簡報
  某個句子」與「來源文件某個段落」建立可查詢、可驗證的對應關係。
- **Source-grounded QA** 作為 reusable production feature：不存在。`content QA
  / visual QA` 是 AGY 擁有的職責（`SKILL.md` 第 49 行），但這只是「AGY 負責做
  QA」的職責宣告，不是一個獨立的、可重用的、對照來源文件驗證內容真實性的
  deterministic 子系統。

若未來要把這兩項變成 reusable production feature，需要另外設計、實作、測試，
屬於未來 Phase 的工作範圍，不在 v0.1.0 baseline 之內。

## 5. Relationship to Frozen Architecture

本文件不改變、也不需要改變任何既有 frozen 決策：

```text
AGY   = Sole Orchestrator / Single Source of Truth
Kiro  = Alternative Engineering Worker Only
Codex Production Engineering Worker = Explicitly Assigned Engineering Only
Codex Slide Image Worker = Slide Image Only
```

```text
AGY -> Kiro  -> AGY
AGY -> Codex -> AGY
```

Retry / block / resume / operator-blocker semantics（Phase 10.2、10.3）維持
既有規則不變；本文件純粹是「盤點目前 repository 實際保證什麼」的說明文件，不是
功能變更。
