# Phase 15 OCR Provider Architecture & Default Engine Evaluation

本文件是 `agy-ppt` Phase 15（OCR Ingestion & Provider Architecture）的架構決策紀錄（Architecture Decision Record, ADR），定義提供者架構（Provider Architecture）、自備 OCR（Bring Your Own OCR, BYO-OCR）整合機制、預設本機引擎評估決策與工程實作路線圖。

Phase 15 狀態為 **COMPLETE / MERGED / BASELINE FROZEN**。Phase 15.1 provider foundation 已由 PR #17 合併；Phase 15.2 A–E 由 PR #22 合併（squash merge `ffac8e77aab6e35d23f09fee01f1d261ba4b5171`）；Phase 15.3 由 PR #26 合併（squash merge `54c3cd5a26b98f1eb6a6a2fbc1ea08fbe5cccd9f`）；Phase 15.4 由 PR #29 合併；Phase 15.5 由 PR #32 合併；Phase 15.6 qualification 由 PR #35 合併（squash merge `ffab67e057a4d3b0028625399c4732272b9d9183`）。各階段規範分別見 PDF raster、PDFium renderer、standalone image、provider UX、grounding translation 與 [validation contract](phase15-6-validation-contract.md)。OCR JSON schemas 維持 DEFERRED。

---

## 1. 架構核心原則：BYO-OCR 與責任分離

`agy-ppt` 採用**提供者導向（Provider-based）**的 OCR 架構。系統**絕不**強制所有使用者只能綁定單一特定 OCR 引擎，而是定義標準化、可驗證的整合邊界：

```text
來源文件（掃描 PDF / 圖片）
        ↓
OCR 提供者解析（Provider Resolution）
        │
        ├── 使用者/專案顯式指定提供者（Custom / Enterprise / Cloud OCR）
        │        ↓
        │   驗證提供者契約（Provider Contract Validation）
        │        ↓
        │   執行提供者萃取
        │
        └── 未顯式指定提供者
                 ↓
           agy-ppt 預設本機提供者（Default Local Provider: Tesseract 5）
                 ↓
        標準化 OCR 證據（Normalized OCR Evidence）
                 ↓
        AGY 語意層（語意切分、論點對齊、數值校驗）
                 ↓
        Phase 12 來源接地（Frozen Grounding Architecture）
```

### 關鍵職責邊界

```text
OCR 提供者（Provider）   = 辨識與位置證據生產者（Recognition & Location Evidence）
AGY                     = 唯一語意權威（Semantic Authority & Claim Verification）
Phase 12 Grounding      = 凍結的接地契約與追溯驗證（Frozen Grounding System）
```

- **OCR 絕非語意權威**：`raw_text` 是必要的 canonical 辨識文字。邊界框與信賴度是建議能力；`regions` 可為空，region 的邊界框可省略，絕不可虛構。沒有 bounding-box 能力的提供者仍可產出有效證據。
- **禁止自動升級**：OCR regions **絕不可**自動升級為 Phase 12 語意來源單元（Semantic Source Units），必須經由 AGY 進行語意切分與審查。
- **Frozen 邊界**：Phase 12 與 Phase 13 維持 FROZEN。Phase 15.1 擁有 OCR-native source-relative locator，不修改 Phase 12 locator validation，也不宣稱直接相容；轉換與整合契約屬 Phase 15.5。

---

## 2. 提供者解析與備援政策（Resolution & Fallback Policy）

### 2.1 確定性解析優先順序（Provider Resolution Precedence）

當文件或頁面需要進行 OCR 時，系統依以下順序確定性解析提供者（單次呼叫覆寫優先於持久化設定）：

1. **命令列／呼叫顯式提供者覆寫**（`--ocr-provider`）
2. **專案層級顯式設定**（`project.ocr.provider`）
3. **使用者／全域層級顯式設定**（`user.ocr.provider`）
4. **agy-ppt 預設本機提供者**（`tesseract`）

以上是選擇優先序，不是依序嘗試的 provider chain。選定後不因失敗而改試較低優先設定；未指定時選用 Tesseract，預設提供者不可用即回報 `OCR_PROVIDER_UNAVAILABLE`。Phase 15.1 僅建立解析基礎，不實作 CLI 或設定檔 UX。

### 2.2 嚴格禁止靜默備援（No Silent Fallback）

若使用者已顯式指定特定提供者（例如 `ocr.provider = "custom-cloud-ocr"`），但該提供者因網路異常、憑證無效或契約不符而失敗：

> [!CAUTION]
> **嚴禁靜默切換回預設本機提供者。**

```text
顯式指定提供者失敗 ──(預設: allow_fallback=false)──> 立即報錯 (FAIL)
```

靜默備援會破壞辨識品質的可預期性與可重現性，並可能在使用者預期使用高精度私有模型時，產出不符預期的辨識結果。

### 2.3 顯式備援宣告與歷程記錄（Explicit Fallback）

僅操作性失敗且使用者**顯式啟用備援**（`ocr.allow_fallback = true`）時，才可轉向預設 Tesseract，至多一次；Tesseract 自身失敗不得再備援或重試成環。

提供者／設定／provenance 失敗為 terminal：`OCR_PROVIDER_NOT_FOUND`、`OCR_PROVIDER_CONTRACT_INVALID`、`OCR_PROVIDER_CAPABILITY_MISSING`、`OCR_PROVIDER_VERSION_UNAVAILABLE`、`OCR_PROVIDER_VERSION_UNSUPPORTED`、`OCR_SOURCE_CHANGED`，以及 `OCR_MODEL_CHANGED` 都必須立即停止，不能靠備援繞過。`OCR_SOURCE_CHANGED` 是原始來源 bytes digest 改變；`OCR_MODEL_CHANGED` 是已驗證 model/traineddata identity 或 digest 與執行前實際值不一致（`expected_model_digest != current_model_digest`），不得改寫 source_digest。完整分類以 [provider contract](ocr-provider-contract.md#8-解析備援與版本政策) 為準。

原本符合備援條件的操作性失敗，若 `allow_fallback = false`，回報 `OCR_FALLBACK_NOT_ALLOWED`，並保留原始失敗作為 cause。Terminal 失敗直接保留其代碼，不包裝成此錯誤。

此時系統**必須**在辨識歷程（Provenance）中完整記錄：

- `requested_provider`：原始請求之提供者（如 `enterprise-ocr`）
- `actual_provider`：實際執行之提供者（如 `tesseract`）
- `fallback_used`：`true`
- `fallback_reason`：明確失敗代碼（如 `OCR_PROVIDER_UNAVAILABLE`）

未使用備援時 `fallback_used = false`、`fallback_reason = null`；`requested_provider` 與 `actual_provider` 仍須記錄。無覆寫時兩者均為 `tesseract`，不可填入虛構身分。

---

## 3. 預設本機引擎評估（Default Engine Evaluation）

agy-ppt 仍需內建開箱即用的預設本機 OCR 解決方案，作為無顯式設定使用者的可靠基底。

### 3.1 候選引擎評估矩陣

本評估明確區分「**目前觀察官方版本（Current Observed Version，截至 2026-09-06）**」與「**規劃支援版本範圍（Planned Supported Version Range）**」，嚴禁將動態的「最新版（latest）」作為重現性契約：

| 候選對象 | 目前觀察官方版本 (Current Observed) | 規劃支援版本範圍 (Planned Range) | 軟體授權 | 繁體中文 (zh-TW) | 英文 | 離線執行能力 | macOS (含 Apple Silicon) | Linux CI (Ubuntu) | 評估分類 (Classification) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **Tesseract OCR** | 5.5.3 (官方發布) | 5.x（Phase 15 目標） | Apache 2.0 | 支援 (`chi_tra` 需就緒並校驗指紋) | 支援 (`eng`) | 100% 離線 (本地 traineddata) | 完整支援 (`brew`)，原生 arm64 | 發行版套件可用 (`apt-get`)，無執行期權重下載 | **DEFAULT LOCAL PROVIDER**（選定） |
| **PaddleOCR (PP-OCR)** | v3.7.0 / PP-OCRv6 (官方發布) | PP-OCRv4 / PP-OCRv6 | Apache 2.0 | 優異 (`chinese_cht` / 統一多語言) | 支援 | 依賴模型權重，預設動態下載 | 安裝相依沉重，macOS arm64 相容性脆弱 | 相依 PaddlePaddle (1GB+)，CI 易超時/OOM | **OPTIONAL PROVIDER / ADAPTER** |
| **Apple Vision** | macOS 11+ 內建 (Vision framework) | macOS 11+ / 12+ | 專有 (Apple) | 優異 | 優異 | 100% 離線 (硬體加速) | 系統內建，免安裝額外二進位 | **完全無法在 Linux 執行** | **PLATFORM-SPECIFIC PROVIDER** |
| **OCRmyPDF** | 17.11.0 (PyPI 穩定版) | v16.x – v17.x | MPL-2.0 | 依賴後端 (Tesseract) | 依賴後端 | 本地工具鏈 | 需安裝完整 PDF 工具鏈 | CI 依賴 Ghostscript/qpdf/unpaper | **PDF WORKFLOW WRAPPER** |
| **EasyOCR** | 1.7.2 (PyPI 穩定版) | v1.7.x | Apache 2.0 | 支援 (`ch_tra`) | 支援 | 依賴 PyTorch 權重 | 相依 PyTorch (1.5GB+)，安裝耗時 | CI 下載 PyTorch 極重，記憶體消耗大 | **OPTIONAL PROVIDER / ADAPTER** |
| **RapidOCR** | 1.4.4 (`rapidocr-onnxruntime`) | v1.3.x – v1.4.x | Apache 2.0 | 支援 (ONNX 權重) | 支援 | 需管理 ONNX 模型檔 | 輕量 ONNX Runtime，跨平台良好 | 輕量，但繁體模型需額外管理與校驗 | **OPTIONAL PROVIDER / ADAPTER** |

### 3.2 預設引擎選定決策：Tesseract OCR (v5.x)

- **選定預設本機提供者**：**Tesseract OCR (v5.x)**
- **版本政策**：provider version 為必要 provenance，無法確定時以 `OCR_PROVIDER_VERSION_UNAVAILABLE` 終止辨識；成功偵測但不符合相容政策時使用 `OCR_PROVIDER_VERSION_UNSUPPORTED`。Tesseract 的 adapter version 與 engine version 分開記錄；適用的 engine version 亦必須可確定。5.x 是目前目標，不是已完成各版本實測的聲明。
- **決策信心度**：**HIGH**
- **核心選定理由**：
  1. **發行版套件可用性與本機執行（無執行期模型下載）**：Tesseract 與所需語言包皆可透過主流作業系統發行版套件管理器取得（macOS `brew` 原生支援 Apple Silicon；Ubuntu Linux CI 透過 `apt-get` 安裝）。一旦安裝所需引擎與經釘選／校驗之語言資料，OCR 執行完全在本機進行，**不需於執行時期動態下載可變動的 OCR 模型（no runtime download of mutable OCR models）**，杜絕 Actions 超時與非預期模型漂移風險。
     - **繁體中文語言包特別要求**：繁體中文語言資料（如 `chi_tra` traineddata）必須在執行環境中就緒，其來源出處與雜湊指紋（provenance / digest）必須由未來實作完整擷取並記錄於 OCR 證據歷程中，絕不可假設任何環境皆預先具備該語言資料。
  2. **完全離線與無隱藏連線**：模型以靜態 `.traineddata` 檔案發行，可釘選特定版本 commit SHA 與 SHA-256 雜湊值進行確定性校驗，執行過程無任何遙測或動態聯網。
  3. **豐富的結構化定位資訊**：原生 TSV / hOCR 輸出具備完整邊界框座標（`left`, `top`, `width`, `height`）、階層結構（頁、區塊、段落、行、詞）與 0–100 的信心度指標。
  4. **雙語混合支援**：透過 `-l chi_tra+eng` 原生支援繁體中文與英文混合文件辨識。
  5. **寬鬆開源授權**：Apache 2.0 授權條款與本專案 MIT 授權完全相容。

### 3.3 其他候選者定位與分級

- **PaddleOCR**：辨識精度極佳，但運行庫沉重且預設下載行為不易受控，定位為未來 **Phase 15.4 的進階選用提供者（Optional Provider Adapter）**。
- **Apple Vision**：macOS 原生表現頂尖，但無法跨平台與 Linux CI 運行，定位為未來的 **平台專用外掛提供者（Platform-Specific Adapter）**。
- **OCRmyPDF**：本質是產出 Searchable PDF 的封裝工具，與 agy-ppt 提取結構化文字證據的需求不合，定位為 **非核心支援工具**。

---

## 4. 文件類型啟用與路由架構（Activation & Routing）

以下是 Phase 15.2/15.3 的後續路由規劃，Phase 15.1 不實作此流程，也不修改 frozen Phase 13 extraction：

```text
來源文件
   │
   ├── 純數位 PDF（具完整文字層）
   │        ↓
   │     Phase 13 確定性文字擷取（pypdf，無 OCR）
   │
   ├── 純影像 / 掃描 PDF（deterministic extracted_text.strip() 為空）
   │        ↓
   │     確定性頁面光柵化（Rasterization） → OCR 提供者
   │
   ├── 混合型 PDF（部分頁面具文字，部分為掃描圖）
   │        ↓
   │     頁層級路由（Page-Level Routing）：
   │       - 具文字頁面 → Phase 13 原生擷取
   │       - 純影像頁面 → 光柵化 + OCR 提供者
   │
   ├── 已具備文字層之 Searchable / OCR PDF
   │        ↓
   │     使用既有文字層；稀疏非空白文字仍為 SEARCHABLE
   │     Phase 15.2 不引入 force_ocr；品質式 OCR 覆寫需後續契約
   │
   └── 獨立圖片（PNG, JPEG, single-frame TIFF）
            ↓
         受限 worker 驗證與機械式 RGB PNG 準備 → OCR 提供者（使用影像原生 locator）
```

Phase 15.2 逐原始頁碼升序機械分類與路由，不以抽取錯誤、文字品質或圖片面積判為 SCANNED。抽取失敗直接失敗。Scanned page 先完成有界 rasterization，再進入 Phase 15.1 provider resolution/fallback；任何必要頁面失敗皆 fail closed，不提供 partial success。詳細版本、資源、provenance 與錯誤規則見 [Phase 15.2 契約](phase15-2-raster-contract.md)。獨立 PNG、JPEG 與 single-frame TIFF 屬 Phase 15.3，使用受限 decoder worker、EXIF display orientation、opaque RGB PNG preparation 與獨立 image error family；完整規則見 [Phase 15.3 契約](phase15-3-image-contract.md)。

---

## 5. 來源身分與衍生歷程（Identity & Provenance）

### 5.1 來源指紋唯一權威（Source Digest Authority）

所有 OCR 來源指紋維持全專案唯一權威：

```text
source_digest = SHA-256(原始來源位元組 raw source bytes)
```

光柵化後之頁面影像、中間臨時檔案或萃取文字的雜湊值**不可**取代 `source_digest`。

### 5.2 確定性 OCR 成果識別與失效機制（Stale Detection）

下列維度用於識別 OCR evidence；若未來設計成果重用，必須納入有效性判斷。Phase 15.2 不建立 persistent raster cache/reuse：
- `source_digest`
- 頁碼／影像 locator
- 提供者身分與版本（`provider_id`, `provider_version`）
- 適用的引擎身分／版本與確定性有序 `model_manifest`（逐模型記錄，不假設只有一個 digest）
- 語言與執行設定（`language_config`, `execution_config`）
- 未來光柵化階段的設定與 renderer version（Phase 15.2 才產生，不在 15.1 虛構）

既有 evidence 的相關 identity 變更不得靜默沿用舊證據。Phase 15.2 每次處理產生實際 raster_digest 作衍生 provenance，不把它當 source_digest，不新增 OCR_RASTER_CHANGED；未來 raster cache 的 staleness/invalidation 另行治理。

Canonical evidence 必須保留 `schema_version`、`source_id`、原始 bytes 的 `source_digest`、每筆 OCR-native `locator`／`raw_text`／`regions`、`capabilities`、provider ID/version、適用的 engine identity/version、有序 model manifest、語言／執行設定，以及 requested/actual provider、執行位置、外傳宣告、fallback_used/reason。欄位位置與必要性以 [canonical contract](ocr-provider-contract.md#6-標準化-ocr-證據模型canonical-ocr-evidence-schema) 為準。

不得使用 `"unknown"` 等 placeholder provenance。可選資訊缺漏可省略；必要 provenance 缺漏必須報錯。Tesseract 必須記錄實際使用的每份 traineddata 身分、來源與 SHA-256，不自動下載模型。Model manifest 的固定排序不取代語言設定本身的呼叫順序。

---

## 6. 高風險數值與符號防護（High-Risk OCR QA）

OCR 辨識常見字形混淆（如 `0`/`O`、`1`/`I`/`l`、`5`/`S`、`8`/`B`、小數點遺漏、負號丟失、百分比與貨幣符號扭曲）。

- **禁止抽取層靜默修正**：OCR 抽取階段**絕不**可擅自將文字修改（例如將 `O` 猜測為 `0`），更不可透過大型語言模型進行未具說明的「自動潤稿」。
- **原始文字唯一權威**：`raw_text` 是 Phase 15.1 canonical recognized-text evidence；不設 `normalized_text` 為第二個 canonical 文字權威。未來衍生文字必須明確追溯至 raw evidence，不能靜默改變 OCR 意義或數值。
- **語意層警示提示**：於 OCR 證據物件中標記數值與敏感符號區塊，供 AGY 語意審查時作為高風險關注訊號。

---

## 7. 隱私與遠端提供者邊界（Privacy Boundary）

- **預設本機提供者零外洩保證**：預設的 Tesseract 5 完全在本地 process 執行，宣告 `source_may_leave_local_machine = false`。
- **自備遠端提供者顯式揭露**：若使用者自備並配置雲端或遠端 OCR 服務（如 Cloud Vision），提供者契約中必須明確宣告：
  ```json
  "execution_location": "remote",
  "source_may_leave_local_machine": true
  ```
- 系統啟動時若偵測到遠端提供者，必須顯式告知操作人員來源內容將傳輸至本機之外，杜絕靜默外傳。

---

## 8. Phase 15 工程實作路線圖（Roadmap）

Phase 15 分為七個嚴謹推進的子階段：

```text
Phase 15.0
OCR 提供者架構、BYO-OCR 契約與預設引擎評估決策 (AGY 主導架構/文件)
   │
Phase 15.1
OCR 提供者契約核心規格與預設本機提供者基礎建設 (COMPLETE / MERGED / BASELINE FROZEN)
   │
Phase 15.2
掃描與純影像 PDF OCR 支援 (光柵化與頁層級路由)
   │
Phase 15.3
獨立圖片格式 (PNG, JPEG, single-frame TIFF) OCR 支援與圖片原生 Locator
   │
Phase 15.4
自備 OCR (BYO-OCR) 管理 UX 與受信任程式碼 provider registration
   │
Phase 15.5
OCR 證據 → AGY 語意層 → Phase 12 來源接地整合
   │
Phase 15.6
真實公開來源驗證、確定性門檻測試與生產發布就緒
```

### 未來階段就緒狀態（Future Phase Readiness Status）

- **Phase 15.1**: COMPLETE / MERGED / BASELINE FROZEN (PR #17, squash merge `9a5059a47fbb474119bb895d2080b20adaaa31f4`); deterministic and repository required checks passed
- **Phase 15.2**: COMPLETE / MERGED / BASELINE FROZEN；PR #22 包含 A/B contracts、C PDFium renderer、D mixed-PDF OCR orchestration 與 E consolidation；production release validation 仍受 [PDFium production-adoption policy](phase15-2-pdfium-renderer-amendment.md#14-production-adoption-gate-與平台政策) 約束
- **Phase 15.3**: COMPLETE / MERGED / BASELINE FROZEN（PR #26，squash merge `54c3cd5a26b98f1eb6a6a2fbc1ea08fbe5cccd9f`）；PNG、JPEG 與 single-frame TIFF 的 admission、preparation、isolation、resource、error 與 evidence 規則見 [Phase 15.3 contract](phase15-3-image-contract.md)
- **Phase 15.4**: COMPLETE / MERGED / BASELINE FROZEN（PR #29，squash merge `1340fbc4bc9e7e570871d2ea8d7d907900a821cb`）；operator/configuration UX 見 [Phase 15.4 contract](phase15-4-provider-ux-contract.md)
- **Phase 15.5**: COMPLETE / MERGED / BASELINE FROZEN（PR #32，squash merge `5393c3e3e3cfee6cbf6891c452ac1bdd71a5418d`）；OCR→Phase 12 additive translation 見 [Phase 15.5 contract](phase15-5-grounding-translation-contract.md)
- **Phase 15.6**: COMPLETE / MERGED / VALIDATED / BASELINE FROZEN（PR #35，squash merge `ffab67e057a4d3b0028625399c4732272b9d9183`）；real-source、E2E、platform、security 與 release-readiness 規範見 [Phase 15.6 contract](phase15-6-validation-contract.md) 與 [qualification report](phase15-6-validation-report.md)

Overall: **Phase 15 — COMPLETE / MERGED / BASELINE FROZEN**。Release readiness 為 **RELEASE READY WITH DOCUMENTED PLATFORM LIMITATIONS**：Linux hard isolation 尚須 deployment-environment validation；macOS 僅 development/API qualified；Windows 尚未 production-security qualified。

### 已合併 Phase 15.1 範圍（Production-Engineering-Worker Scope）

- 定義 `OCRProvider` 抽象基底介面與 `OCRProviderCapabilities` 結構。
- 建立 provider validation、canonical OCREvidence、provider-neutral provenance、有序 model manifest。
- 建立 provider resolution foundation、no-silent-fallback 與穩定 OCR error taxonomy。
- 建立預設 Tesseract adapter、availability/version detection、structured output parsing 與 traineddata provenance。
- 建立確定性 fake/test provider 與 provider contract tests，測試不消耗 AI 額度。

明確排除 PDF rasterization、scanned-PDF workflow、mixed-page routing、standalone image ingestion、Phase 12 grounding integration、cloud OCR、PaddleOCR、Apple Vision 實作與 dynamic custom-provider registration UX。Adapter 可接收呼叫者準備好的影像及原始來源身分；不負責上述 ingestion 流程。

實作安全約束：不得使用 `shell=True`、不安全指令串接、靜默 network OCR、自動 mutable model download 或 credentials/API keys。本次僅修改文件，不建立 Python modules、schema files、tests、adapters、execution 或 CLI behavior。
