# 自訂 OCR 提供者整合指南（Custom OCR Providers Guide）

本文件提供 BYO-OCR 的架構整合指引。Phase 15.1 provider foundation 已由 PR #17 合併；Phase 15.4 operator/configuration UX 依 [Phase 15.4 provider UX contract](phase15-4-provider-ux-contract.md) 實作，僅管理受信任程式碼已註冊的 provider，不允許設定驅動的任意程式碼載入。

Phase 15.1 至 Phase 15.6 均為 COMPLETE / MERGED / BASELINE FROZEN；Phase 15.4 已由 PR #29 合併（squash merge `1340fbc4bc9e7e570871d2ea8d7d907900a821cb`），Phase 15.5 已由 PR #32 合併（squash merge `5393c3e3e3cfee6cbf6891c452ac1bdd71a5418d`），Phase 15.6 已由 PR #35 合併（squash merge `ffab67e057a4d3b0028625399c4732272b9d9183`）。OCR JSON schemas 維持 DEFERRED。

## 1. 核心整合原則

Provider 只產出辨識與來源位置證據；AGY 是唯一語意權威。所有提供者必須遵守 [OCR Provider Contract](ocr-provider-contract.md)。

Phase 15.1 建立 OCRProvider、OCRProviderCapabilities、provider validation、canonical OCREvidence、provider-neutral provenance、resolution foundation、no-silent-fallback、stable errors、Tesseract default adapter、availability/version detection、structured output parsing、traineddata provenance、deterministic fake provider 與 contract tests。

Phase 15.4 已提供受信任 registry 的 discovery、inspection、validation 與 project/user configuration UX；不包含 Phase 12 grounding integration、cloud OCR、PaddleOCR、Apple Vision adapter 或設定驅動的 dynamic code loading。

### Operator commands

```bash
python3 skills/agy-ppt/scripts/manage_ocr_providers.py list
python3 skills/agy-ppt/scripts/manage_ocr_providers.py show [--provider ID]
python3 skills/agy-ppt/scripts/manage_ocr_providers.py validate [--provider ID] [--language LANG]
python3 skills/agy-ppt/scripts/manage_ocr_providers.py set --scope project|user --provider ID [--allow-fallback|--no-allow-fallback]
python3 skills/agy-ppt/scripts/manage_ocr_providers.py unset --scope project|user
```

命令輸出為 bounded deterministic JSON。`list`、`show`、`validate`、`set` 與 `unset` 均不執行 OCR、不建立 evidence、不下載模型，也不觸發 fallback。Project 設定為 `<project>/.agy/ocr-provider.json`；user 設定位於 operator config root 的 `agy-ppt/ocr-provider.json`。設定只接受 `provider` 與 boolean `allow_fallback`，不儲存 secrets。

## 2. 必要證據與可選能力

| 分級 | 項目 | 行為 |
| --- | --- | --- |
| REQUIRED | Provider ID/version、raw_text、OCR-native source-relative locator、capabilities、execution/privacy 宣告及必要 provenance | 缺漏即拒絕；版本不可確定使用 OCR_PROVIDER_VERSION_UNAVAILABLE |
| RECOMMENDED | Bounding boxes、原生 confidence、偵測語言 | 缺漏可接受並記錄降級 |
| OPTIONAL | Word boxes、tables、layout regions、orientation | 略過未支援項目 |

raw_text 是 canonical recognized-text evidence。regions 可為空，region 的 bounding_box 可省略；不能虛構全頁框或零框。沒有 bounding-box 能力的 provider 仍可產出有效證據。

不做語意 cleanup／repair；不要求 normalized_text，也不讓它成為第二個 canonical 文字權威。任何未來 derived text 都必須追溯至 raw evidence，不得靜默改變意義或數值。

### Canonical provenance 檢查

以 [canonical evidence 欄位契約](ocr-provider-contract.md#6-標準化-ocr-證據模型canonical-ocr-evidence-schema) 為準，必須保留：

- schema_version、source_id、原始 raw source bytes 的 SHA-256 source_digest。
- 每筆 OCR-native locator、raw_text、regions，以及實際 provider 的 capabilities。
- requested_provider、actual_provider、provider ID/version，以及適用的 engine identity/version。
- 確定性有序 model_manifest、language_config 與 execution_config。
- execution_location、source_may_leave_local_machine、fallback_used、fallback_reason。

model_manifest 逐模型記錄，不假設只有一個 model digest；固定排序規則見 contract 第 6.1 節，語言呼叫順序另行保存。Tesseract 每份實際 traineddata 的身分、來源與 SHA-256 都必須可確定。不捏造 "unknown" 等 placeholder；可選資訊缺漏可省略，必要 provenance 缺漏必須報錯。未備援時 fallback_reason = null，requested/actual provider 相同。

## 3. 提供者概念適配器結構（Conceptual Adapter Patterns）

### 模式 A：Python 內部類別適配器（In-Process Adapter）

概念 OCRProvider 介面宣告 provider_id、provider_version 與 OCRProviderCapabilities，接收呼叫者準備好的影像、原始來源身分、OCR-native locator 與執行設定，回傳或轉換為 canonical OCREvidence。Phase 15.4 只允許受信任 application code 建立並注入 `Mapping[str, OCRProvider]`；registry key 必須等於 provider ID，設定檔不能載入 provider 程式碼。

辨識前驗證必要契約；辨識後驗證 raw evidence 與 provenance。不能由 region 自動產生 Phase 12 semantic source unit。

### 模式 B：外部命令列包裝器（CLI Wrapper Adapter）

Adapter 接收已準備影像，不自行 rasterize PDF。以安全 argv 呼叫本機引擎，禁止 shell=True 或不安全指令串接；採有限 timeout、驗證 exit code、解析 structured output，再組裝 raw_text、regions 與 provenance。只能清理由 adapter 擁有的暫存資源，不刪除呼叫者來源。

Phase 15.2 先完成有界 rasterization 才進入 provider fallback 邊界；rasterization／PDF input／resource failure 不得觸發 provider fallback。呼叫者保留原始 PDF source_digest、原始 1-based page／total_pages，以及外層逐頁 raster_provenance；raster_digest 僅為實際 prepared PNG bytes 的衍生指紋，不是來源身分。沒有 persistent raster cache/reuse。必要 scanned page 最終失敗時整個 PDF transaction fail closed，不能交付部分成功。

Tesseract 是 Phase 15.1 預設 adapter 的目標，支援目標為 **Tesseract 5.x**。Provider/adapter version 與 engine version 分開記錄。必要版本無法確定時以 OCR_PROVIDER_VERSION_UNAVAILABLE 終止；已偵測但不符合相容政策時使用 OCR_PROVIDER_VERSION_UNSUPPORTED，不備援繞過。

### 模式 C：遠端／雲端適配器（後續階段）

Cloud、PaddleOCR、Apple Vision 的實作不屬 Phase 15.1。未來 remote provider 必須宣告 execution_location = remote 與 source_may_leave_local_machine = true，並明確告知及取得外傳授權。此文件不建立網路呼叫或 credential configuration。

## 4. Locator 與 Frozen 邊界

Phase 15.1 擁有 OCR-native source-relative locator，page／image 索引均為 1-based。Page 使用 page（已知時可附 total_pages）；image 使用 ordinal，不能虛構 PDF 頁碼。

這不是與 Phase 12 直接相容的 locator contract。Frozen Phase 12 page 使用 start/end，現有 validator 不接受 image kind。Phase 15.1 不修改 Phase 12 locator validation；轉換及 grounding integration 屬 Phase 15.5，在整合契約存在前不能宣稱直接相容。Phase 12 與 Phase 13 維持 FROZEN。

## 5. 提供者解析與備援政策實務（Resolution & Fallback Policy）

### 5.1 選擇優先序

設定選擇順序為 call/CLI override → project setting → user setting → default tesseract。這是 selection precedence，不是依次嘗試 provider 的 chain；Phase 15.4 管理層直接重用 Phase 15.1 resolver。

### 5.2 Terminal failures

以下失敗直接終止，不能因 allow_fallback = true 而繞過：

- OCR_PROVIDER_NOT_FOUND。
- OCR_PROVIDER_CONTRACT_INVALID。
- OCR_PROVIDER_CAPABILITY_MISSING。
- OCR_PROVIDER_VERSION_UNAVAILABLE。
- OCR_PROVIDER_VERSION_UNSUPPORTED。
- OCR_SOURCE_CHANGED。
- OCR_MODEL_CHANGED。

其他設定失敗亦依 [錯誤分類](ocr-provider-contract.md#7-錯誤分類體系error-taxonomy) 終止。Terminal error 保留原始代碼，不改包成 OCR_FALLBACK_NOT_ALLOWED。

### 5.3 操作性失敗與單次備援

依 contract 分類的操作性失敗，且選定 provider 尚非 default Tesseract，才具備援資格：

- allow_fallback = true：至多轉向 Tesseract 一次，驗證 fallback provider 契約，保留原始 cause。
- allow_fallback = false（預設）：回報 OCR_FALLBACK_NOT_ALLOWED，同時保留原始失敗為 cause。
- Tesseract 自身或備援失敗：回報實際錯誤，不再切換或形成循環。

OCR_SOURCE_CHANGED 僅表示原始來源 bytes 的 SHA-256 改變；OCR_MODEL_CHANGED 表示已驗證的 model/traineddata identity 或 digest 與執行前實際值不一致。模型 staleness 不得改寫 source_digest，也不得由 fallback 掩蓋；需重新驗證 model provenance 後建立新的 OCR evidence，或恢復原先預期的模型 bytes/configuration。

成功備援的 provenance 片段如下；這不是完整 OCREvidence：

```json
{
  "requested_provider": "custom-ocr",
  "actual_provider": "tesseract",
  "fallback_used": true,
  "fallback_reason": "OCR_PROVIDER_UNAVAILABLE"
}
```

未指定 provider 時選用 tesseract；它不可用即回報 OCR_PROVIDER_UNAVAILABLE。原始失敗診斷不得包含 credentials 或私有來源內容。

## 6. 提供者合規自我檢查清單（Compliance Checklist）

- [ ] Provider version 可確定；適用的 engine version 可確定且符合相容政策。
- [ ] 所有必要 provenance 都存在；沒有 placeholder 或假模型身分。
- [ ] 原始 source_digest 未被 raster／text digest 取代。
- [ ] OCR-native locator 為來源相對且 1-based，沒有直接 Phase 12 相容聲明。
- [ ] raw_text 保留原始辨識內容，regions 可空，沒有虛構 bounding box 或信賴度。
- [ ] Model manifest 確定性排序，記錄實際模型，語言與有效設定完整。
- [ ] Terminal failure 不備援；操作性備援必須顯式啟用且最多一次。
- [ ] 本機 provider 不連外、不自動下載 mutable models、不使用 credentials/API keys。
- [ ] Deterministic fake-provider tests 不依賴實際引擎、網路或 AI 訂閱額度。
- [ ] 不修改 frozen Phase 12/13 production contracts，不自動建立 grounding artifacts。

## 7. 常見整合錯誤與診斷（Common Errors & Troubleshooting）

| 錯誤 | 處理方式 |
| --- | --- |
| OCR_PROVIDER_NOT_FOUND | 修正 provider ID；不能備援掩蓋設定錯誤 |
| OCR_PROVIDER_CONTRACT_INVALID／OCR_PROVIDER_CAPABILITY_MISSING | 補齊必要契約／能力；沒有 bounding boxes 本身不是此錯誤 |
| OCR_PROVIDER_VERSION_UNAVAILABLE | 提供可確定版本後再辨識；不得填入 unknown |
| OCR_PROVIDER_VERSION_UNSUPPORTED | 使用符合相容政策的版本；Tesseract 目前目標為 5.x |
| OCR_PROVIDER_UNAVAILABLE／OCR_PROVIDER_FAILED | 修復可用性／程序失敗；僅依第 5 節政策備援 |
| OCR_LANGUAGE_UNSUPPORTED／OCR_MODEL_UNAVAILABLE | 由操作者準備所需語言／模型與 provenance，不由執行層自動下載 |
| OCR_SOURCE_CHANGED | 停止使用舊證據，依新來源重新建立證據；不備援 |
| OCR_FALLBACK_NOT_ALLOWED | 查閱原始 cause，修復操作性失敗或顯式啟用備援 |
