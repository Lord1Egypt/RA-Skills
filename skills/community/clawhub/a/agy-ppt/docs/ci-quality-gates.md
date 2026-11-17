# GitHub Actions CI Quality Gates & Release Safety

本文件說明 `agy-ppt` 的持續整合（Continuous Integration, CI）、品質檢驗門檻（Quality Gates）與發布就緒（Release Readiness）安全機制。

---

## 1. 核心原則與責任分離

本專案將驗證工作嚴格區分為三個不同執行等級（Execution Classes）：

```text
                           Pull Request
                                │
                  ┌─────────────┴─────────────┐
                  ▼                           ▼
         Core Deterministic CI          Quality Gates
             (ci.yml)                   (quality.yml)
                  │                           │
                  └─────────────┬─────────────┘
                                ▼
                              PASS
                                │
                              Merge
                                │
                  ┌─────────────┴─────────────┐
                  ▼                           ▼
          Release Readiness             Live Validation
        (release-readiness.yml)       (live-validation.yml)
             manual only                manual / scheduled
```

### 三種驗證等級

| 等級 | 工作流程 | 觸發條件 | 執行特性 | 是否阻擋 PR |
| --- | --- | --- | --- | --- |
| **A. PR Required Candidates** | `ci.yml`, `quality.yml` | PR（針對 `main`）、Push（`main`）、手動 | 確定性（deterministic）、離線（offline）、可重複驗證 | **是**（PR 必要門檻） |
| **B. Release Readiness** | `release-readiness.yml` | 手動 `workflow_dispatch` | 無快取純淨環境（clean-room）、宣告相依性重現、源碼封存稽核 | **否**（僅發布前手動驗證） |
| **C. Live Validation** | `live-validation.yml` | 手動 `workflow_dispatch`、每週排程 | 外部網路連線、單一穩定公開來源（RFC 2119） | **否**（非阻擋性） |

---

## 2. 關鍵語意邊界（Semantic Boundary）

> [!IMPORTANT]
> **GitHub Actions 驗證確定性工程契約，不可取代 AGY 語意審查。**

GitHub Actions 具備自動驗證程式碼語法、schema 結構相容性、單元測試、故障復原情境與靜態檔案規範的能力。然而：
- **AGY semantic claim / source support 判斷**：無法簡化為 CI。
- **Claim 與來源文本之真實對應語意**：無法由 CI 證明。
- **CI 的成功**：代表程式碼與契約符合確定性工程規格，**不等於**對任何外部世界事實真偽的背書。

---

## 3. 工作流程架構

### 3.1 Core Deterministic CI (`.github/workflows/ci.yml`)

負責所有確定性工程與測試門檻驗證：
- **相依性安裝驗證** (`install-check`)：驗證從 `skills/agy-ppt/requirements.txt` 全新安裝相依套件，並檢查 `python-pptx`, `Pillow`, `openai`, `filelock`, `pypdf`, `python-docx`, `lxml` 核心模組正確匯入。
- **確定性測試套件** (`deterministic-tests`)：
  - Phase 13 遠端來源取得測試 (`test_source_acquisition.py`)
  - Phase 13 來源擷取測試 (`test_source_ingestion.py`，包含 HTML 網路安全與格式迴歸)
  - Phase 12 來源接地與工作流程測試 (`test_source_grounding.py`, `test_source_grounding_workflow.py`)
  - 完整單元測試探索 (`python3 -m unittest discover`)
- **解析器與復原測試** (`resolver-recovery`)：
  - Codex PPT 外部相依性解析器測試 (`test_codex_ppt_dependency.py`)
  - Phase 9 確定性故障復原情境測試 (`run_recovery_tests.py`)
- **穩定聚合檢查** (`deterministic`)：作為未來分支保護（Branch Protection）的單一穩定檢查名稱（Aggregator），依賴上述所有測試任務。

### 3.2 Quality Gates (`.github/workflows/quality.yml`)

負責程式庫衛生、文件雙語對齊與凍結契約保護：
- **README 雙語檢驗** (`readme-bilingual`)：
  - 驗證繁體中文 `README.md` 與英文 `README_en.md` 皆存在且相互連結。
  - 驗證所有儲存庫相對連結（local relative links）皆指向有效檔案與標題錨點（0 broken links）。
  - 驗證 20 個關鍵架構、安裝、測試、安全與限制主題在兩份 README 中具備語意對等性。
- **儲存庫衛生與憑證檢驗** (`hygiene-and-security`)：
  - 嚴格禁止追蹤 `.env`, `.venv/`, `__pycache__/`, `*.pyc`, `*.part` 等雜物。
  - 嚴格禁止追蹤執行階段產物（如產出的 `.pptx`, 投影片圖片 `slide_*.png`, 擷取 payload `src_*.txt`）。
  - 私有路徑防護：禁止本機絕對路徑（如 `/Users/<user>`, `/home/<user>`, `C:\Users\<user>`）洩漏至生產程式碼或說明文件（測試夾具使用明確白名單）。
  - 憑證防護：檢測私密金鑰標頭（Private Key headers）與常見金鑰字串。
- **凍結契約防護** (`frozen-contract-guard`)：
  - 監控已凍結之 Phase 12 與 Phase 13 生產契約路徑。
  - 若有修改且未附帶維護者核准標籤，立即失敗。
- **穩定聚合檢查** (`repository`)：作為品質與衛生門檻的單一穩定檢查名稱。

### 3.3 Release Readiness Clean-Room Audit (`.github/workflows/release-readiness.yml`)

模擬公開使用者在全新隔離環境中取得儲存庫的完整驗證流程：
- 僅支援手動觸發（`workflow_dispatch`），不自動在 PR 執行。
- **無快取純淨環境**：停用 pip 快取，以驗證宣告相依性之獨立安裝可靠度。
- **全套門檻複查**：依序執行 Phase 12、Phase 13、完整單元測試、解析器、復原測試、雙語對齊與衛生檢查。
- **源碼封存稽核**：透過 `git archive` 產生乾淨源碼封裝，驗證必要檔案齊全且不含任何違禁產物。
- **發布摘要產出**：於 GitHub Actions Job Summary 呈現完整檢驗矩陣。
- **不自動發布**：此工作流程純為驗證，不建立 Git tag、不發布 GitHub Release。

### 3.4 Live Validation (`.github/workflows/live-validation.yml`)

針對公開遠端來源取得機制進行有界限的實體驗證：
- 觸發條件：手動觸發或每週定期排程（週一 03:23 UTC，非整點時間以分散負載）。
- **單一有界來源**：僅取得 RFC 2119（`https://www.rfc-editor.org/rfc/rfc2119.txt`），比對已釘選之 SHA-256 雜湊值（`3c2ceb7bfc84cd34720f4a5271338ab9d8280d34bdd1eb250c64306202f2ed8b`）。
- **非阻擋性**：外部網路或目標伺服器暫時無法連線時，標記為環境受阻（`LIVE_REMOTE_VALIDATION_BLOCKED`），不視為專案程式碼缺陷，亦不阻擋一般 PR 合併。
- **無爬蟲行為**：不遞迴爬取、不執行瀏覽器、不存取多重網站。

---

## 4. 凍結契約保護政策（Frozen Contract Policy）

Phase 12（Source Grounding & Project State）與 Phase 13（Source Ingestion & Acquisition）已正式完工並凍結（FROZEN）。

### 受保護之生產表面（Designated Frozen Surfaces）

```text
Phase 12:
  skills/agy-ppt/scripts/source_grounding.py
  skills/agy-ppt/scripts/validate_source_grounding.py
  skills/agy-ppt/schemas/source_inventory.schema.json
  skills/agy-ppt/schemas/claim_traceability.schema.json
  skills/agy-ppt/schemas/source_coverage.schema.json
  skills/agy-ppt/schemas/source_grounded_qa.schema.json
  skills/agy-ppt/schemas/project_state.schema.json
  skills/agy-ppt/scripts/project_state.py
  skills/agy-ppt/scripts/assemble_ppt.py
  skills/agy-ppt/scripts/codex_image_adapter.py
  skills/agy-ppt/scripts/kiro_acp_bridge.py

Phase 13:
  skills/agy-ppt/scripts/source_ingestion.py
  skills/agy-ppt/scripts/source_acquisition.py
```

### 維護者核准機制

若未來因重大修復需要變更上述凍結檔案，必須依循以下流程：
1. PR 提交時，CI 的 `frozen-contract-guard` 將偵測到凍結檔案變更並發出錯誤：
   ```text
   FROZEN PRODUCTION CONTRACT MODIFIED
   ```
2. 儲存庫維護者審查該變更合理性後，於 GitHub PR 加上標籤：
   ```text
   frozen-contract-change-approved
   ```
3. 具備該標籤之 PR 重新觸發後，守門腳本將記錄核准日誌並通過。
4. 所有既有的單元測試、迴歸測試與品質檢驗依然必須全部通過。

---

## 5. 安全與最小權限規範（Supply-Chain Security）

- **權限最小化**：所有 PR 驗證工作流程皆宣告 `permissions: contents: read`，無任何寫入權限。
- **禁止 `pull_request_target`**：PR 程式碼驗證僅使用標準 `pull_request` 觸發，防止不可信 PR 程式碼取得具權限之 Token。
- **官方 Action 釘選**：第三方 Action 一律使用不可變之 Commit SHA 釘選，並附帶版本標籤註解：
  - `actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683` (# v4.2.2)
  - `actions/setup-python@42375524e23c412d93fb67b49958b491fce71c38` (# v5.4.0)
- **零機密需求**：確定性 CI 與品質檢驗完全不需要任何儲存庫 Secret 或生產 API Key。

---

## 6. 主分支保護與必要 CI 強制執行（Main Branch Protection）

`main` 分支透過 GitHub Repository Ruleset（`main-protection`，ID: `22388938`）強制保護，狀態為 **ACTIVE**：

- **必須透過 Pull Request 合併**：禁止直接 push 至 `main`。
- **必要狀態檢查（Required Status Checks）**：
  - `deterministic`（由 `ci.yml` 聚合之確定性測試閘門）
  - `repository`（由 `quality.yml` 聚合之品質與凍結契約閘門）
- **嚴格最新狀態政策（Strict Policy）**：`strict_required_status_checks_policy: true`，PR 必須在最新 `main` 狀態下通過檢查才可合併。
- **線性歷史記錄（Linear History）**：啟用 `required_linear_history`，強制使用 squash merge，禁止 merge commit 與 rebase merge。
- **禁止強制推送與分支刪除**：全面阻擋 `non_fast_forward`（force push）與 `deletion`。
- **非必要檢查隔離**：`Release Readiness` 與 `Live Validation` 明確**不**列為 PR 必要檢查，保持手動／排程非阻擋特性。
- **審查人核准門檻**：設定為 0（因應單一維護者架構，維護者可自行合併合規 PR），並強制要求所有 review comment thread 皆須已解決（resolved）。
