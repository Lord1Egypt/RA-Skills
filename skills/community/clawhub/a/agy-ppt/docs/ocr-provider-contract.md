# OCR Provider Contract Specification

本文件是 Phase 15.1 OCR provider foundation 的規範性架構文件。Phase 15.1 provider foundation 已由 PR #17 合併；公開 JSON schemas 與後續 ingestion/grounding 仍未建立。

Phase 15.1 維持 COMPLETE / MERGED / BASELINE FROZEN；Phase 15.2 已為 COMPLETE / MERGED / BASELINE FROZEN，Phase 15.3 已建立 additive [standalone image OCR contract](phase15-3-image-contract.md)，OCR schemas 為 DEFERRED。後續 ingestion/orchestration 文件不改動本階段 provider 契約。

## 1. 提供者能力分級（Capability Tiers）

| 分級 | 能力 | 缺漏行為 |
| --- | --- | --- |
| REQUIRED | Provider ID/version、raw_text、OCR-native locator、能力與執行位置／外傳宣告 | 缺必要契約或能力即拒絕；版本不可確定使用 OCR_PROVIDER_VERSION_UNAVAILABLE |
| RECOMMENDED | Bounding boxes、原生 confidence、偵測語言 | 接受但記錄能力降級，不捏造數據 |
| OPTIONAL | Word boxes、tables、layout regions、orientation | 接受並略過未支援功能 |

能力分級不豁免必要 provenance。raw_text 必須存在；regions 可以是空陣列。沒有 bounding-box 能力的 provider 仍可產出有效證據。

## 2. 提供者能力宣告物件（OCRProviderCapabilities）

| 欄位 | 規則 |
| --- | --- |
| text、locators | 必要 boolean，必須為 true |
| execution_location | 必要，local 或 remote |
| source_may_leave_local_machine | 必要 boolean；remote 必須為 true |
| bounding_boxes、confidence | 可選 boolean，未宣告視為 false |
| word_boxes、orientation、tables、layout_regions | 可選 boolean，未宣告視為 false |

Canonical evidence 保留實際 provider 的 capabilities，execution/privacy 欄位須與 provenance 一致。宣告不代表任意第三方程式受到 sandbox 保護。

## 3. 定位器契約（Locator Contract）

Phase 15.1 擁有 OCR-native source-relative locator，索引為 1-based 正整數，不接受 boolean，不使用暫存路徑作身分。

### 3.1 多頁文件（PDF）

概念表示：`{"kind": "page", "page": 1, "total_pages": 42}`。page 必要；total_pages 可在已知時提供且不得小於 page。此位置由呼叫者提供，不表示 Phase 15.1 負責 PDF rasterization。

Phase 15.2 呼叫者必須先驗證 PDF total_pages 並在逐頁呼叫提供它；此為 PDF orchestration 的較強前置條件，不改變 Phase 15.1 通用 optional 規則。

### 3.2 獨立圖片（PNG, JPEG, single-frame TIFF）

概念表示：`{"kind": "image", "ordinal": 1}`。不得虛構 PDF 頁碼。Phase 15.3 每個已接受來源恰為 image 1 of 1；多 frame TIFF 不在該階段。定義此 locator 本身不表示 provider 負責 standalone image ingestion。

### 3.3 Frozen ownership

以上結構不直接相容於 frozen Phase 12 locator：Phase 12 page 使用 start/end，現有 validator 不接受 image kind。Phase 15.1 不修改 Phase 12 locator validation，也不直接將 OCR locator 交給它。已合併的 Phase 15.5 additive adapter 依 [grounding translation contract](phase15-5-grounding-translation-contract.md) 機械轉譯 locator；Phase 12 與 Phase 13 production contracts 維持 FROZEN。

## 4. 座標系統與邊界框規範（Bounding Box Contract）

Bounding boxes 是 RECOMMENDED，不是 REQUIRED。regions 可為空；region 的 bounding_box 可省略。沒有幾何證據時不得填入虛構全頁框、零框或 placeholder。

若提供 bounding_box，須包含有限數值 x、y、width、height；原點為影像左上角，X 向右、Y 向下，相對頁面／影像寬高正規化至 [0.0, 1.0]，且框不得超出影像範圍。原始像素資訊可作輔助證據。

## 5. 辨識信賴度契約（Confidence Semantics）

保留原生 confidence 的 raw_confidence、confidence_scale、confidence_source，例如 89.5、0-100、tesseract_word_average。各引擎尺標不保證可直接比較。沒有資料時省略，不捏造統一分數。

## 6. 標準化 OCR 證據模型（Canonical OCR Evidence Schema）

本節為文件欄位契約，不是已實作的 JSON Schema。OCREvidence 由 OCR 層擁有，不擴充 Phase 12 inventory 或 Phase 13 ExtractionResult。

| 欄位位置 | 必要性與語意 |
| --- | --- |
| schema_version | 必要，OCR evidence 格式版本，與 provider/engine version 分離 |
| source_id | 必要，穩定原始來源識別碼 |
| source_digest | 必要，原始 raw source bytes 的 SHA-256，小寫 64 位 hex；不可用 raster、文字或 URL digest 取代 |
| capabilities | 必要，實際 provider 的能力宣告 |
| provider.provider_id | 必要、非空，與 actual_provider 一致 |
| provider.provider_version | 必要、可確定的 provider/adapter version |
| provider.engine_name、provider.engine_version | 有底層引擎時必要，例如 Tesseract；沒有獨立引擎才可省略 |
| model_manifest | 必要、確定性有序模型陣列，依第 6.1 節 |
| language_config | 必要，實際語言選擇與順序，包括有效預設值 |
| execution_config | 必要，有效辨識設定，不含 credentials、API keys、私有絕對路徑 |
| provenance.requested_provider | 必要，原始選定 provider；未顯式指定時為 tesseract |
| provenance.actual_provider | 必要，實際產出證據的 provider |
| provenance.execution_location | 必要，local 或 remote |
| provenance.source_may_leave_local_machine | 必要 boolean，與 capabilities 一致 |
| provenance.fallback_used | 必要 boolean |
| provenance.fallback_reason | 必要；備援時為原始 failure code，未備援時為 null |
| pages | 必要陣列，容納來源位置的辨識證據；名稱不表示 image locator 是 PDF page |
| pages[].locator | 必要，OCR-native locator，依第 3 節 |
| pages[].raw_text | 必要字串，canonical recognized-text evidence，保留引擎辨識文字與換行 |
| pages[].regions | 必要陣列，可為空，作為 raw evidence 的補充 |
| pages[].regions[].region_id、text | Region 存在時必要；ID 確定性，text 不得語意改寫 |
| pages[].regions[].bounding_box、confidence | 可選，提供時遵守第 4、5 節 |
| pages[].high_risk_signals | 可選，數字／符號審查訊號，不改寫文字或判定 claim |

未備援時 requested/actual provider 相同。fallback_reason = null 明確表示「沒有備援原因」，不是未知資訊的 placeholder。

### 6.1 Model manifest

model_manifest 逐一記錄模型，不假設只有一個 model digest。每筆需有可確定的 model_id；可取得的 model_version、model_digest（SHA-256）、model_source 應記錄。按 model_id，再按可用 version/digest/source 字串作固定字典序排序，不依檔案列舉順序或時間戳。語言執行順序另存 language_config，不因 manifest 排序而改變。

未使用模型時可為空陣列；不得把必要模型資訊缺失偽裝成「無模型」。自訂 provider 不適用或無法取得的可選資訊可省略，不能因此宣稱完整模型可重現性。

Tesseract 必須逐一記錄實際 traineddata 的 model_id、model_digest 與可驗證 model_source。來源識別不含 credentials／私有絕對路徑，不從檔名猜測；可選 model_version 缺漏則省略。不自動下載可變模型，不以單一聚合 digest 取代 manifest。

### 6.2 缺漏與文字權威

不得捏造 "unknown" 等 placeholder provenance。可選資訊缺漏可省略；必要 provenance 缺漏必須報錯。Provider version 或適用的 engine version 無法確定使用 OCR_PROVIDER_VERSION_UNAVAILABLE；其他必要 provenance 缺漏使用 OCR_PROVIDER_CONTRACT_INVALID。

raw_text 是 Phase 15.1 唯一 canonical 辨識文字。不要求 normalized_text，也不讓它成為第二個 canonical 權威；不做 semantic cleanup、repair 或數值修補。未來 derived text 必須明確追溯至 raw evidence，不能靜默改變意義或數值。

## 7. 錯誤分類體系（Error Taxonomy）

OCR namespace 與 frozen Phase 12/13 分離。下列後續階段代碼的定義不表示該階段已實作。

| 代碼 | 語意與行為 |
| --- | --- |
| OCR_PROVIDER_NOT_FOUND | 指定 ID 不存在；terminal |
| OCR_PROVIDER_UNAVAILABLE | Binary/endpoint 無法存取；操作性失敗 |
| OCR_PROVIDER_CONTRACT_INVALID | 必要契約或 provenance 無效；terminal |
| OCR_PROVIDER_CAPABILITY_MISSING | 缺文字或 locator 等必要能力；terminal |
| OCR_PROVIDER_VERSION_UNAVAILABLE | Provider version 或適用的 engine version 無法確定；terminal，辨識失敗 |
| OCR_PROVIDER_VERSION_UNSUPPORTED | 已偵測版本不符合支援相容政策；terminal |
| OCR_PROVIDER_OUTPUT_INVALID | 引擎輸出損毀／無法解析；操作性失敗；必要 canonical 契約錯誤使用 CONTRACT_INVALID |
| OCR_PROVIDER_FAILED | 引擎崩潰或非零 exit code；操作性失敗 |
| OCR_LANGUAGE_UNSUPPORTED | 請求語言不受支援；設定失敗，terminal |
| OCR_MODEL_UNAVAILABLE | 必要模型／traineddata 未就緒；設定失敗，terminal |
| OCR_EXTRACTION_FAILED | 輸入影像造成辨識失敗；操作性失敗 |
| OCR_TEXT_UNAVAILABLE | 有效辨識未發現文字；警告，保留空 raw_text，不自動備援 |
| OCR_RASTERIZATION_FAILED | 後續 Phase 15.2 renderer 不可用／版本無效、render execution 或 raster output/provenance 失敗；在 provider fallback 之外；PDF input/resource 錯誤另依 Phase 15.2 契約 |
| OCR_FALLBACK_NOT_ALLOWED | 原本可備援的操作性失敗，但備援未啟用；保留原始 cause |
| OCR_SOURCE_CHANGED | 原始 bytes digest 改變；停止使用舊證據，terminal，不備援 |
| OCR_MODEL_CHANGED | 已驗證的 model/traineddata identity 或 bytes digest 與執行前實際值不一致；provenance staleness，terminal，不備援 |
| OCR_PROVIDER_CHANGED | Provider 身分改變，既有證據過期；不是備援觸發器 |
| OCR_CONFIG_CHANGED | 語言／執行設定改變，既有證據過期；不是備援觸發器 |

## 8. 解析、備援與版本政策

Phase 15.2 的 OCR_PDF_PASSWORD_REQUIRED、OCR_PDF_INPUT_INVALID、OCR_PDF_PAGE_INVALID、OCR_PDF_RESOURCE_LIMIT_EXCEEDED、OCR_PDF_CLEANUP_FAILED 屬 [PDF orchestration error family](phase15-2-raster-contract.md)，不是 provider failures，不觸發備援。Raster provenance 置於 additive transaction envelope；raster_digest 不取代 source_digest，不新增 OCR_RASTER_CHANGED，也不發布 schema。

Phase 15.3 的 OCR_IMAGE_FORMAT_UNSUPPORTED、OCR_IMAGE_INPUT_INVALID、OCR_IMAGE_RESOURCE_LIMIT_EXCEEDED、OCR_IMAGE_DECODE_FAILED、OCR_IMAGE_CLEANUP_FAILED 屬 [standalone image orchestration error family](phase15-3-image-contract.md#9-stable-image-error-taxonomy)，不是 provider failures，且不觸發備援。Prepared-image provenance 置於 additive transaction envelope；prepared_image_digest 不取代 source_digest，也不發布 schema。

選擇順序為 call/CLI override → project setting → user setting → default Tesseract。這是 selection precedence，不是 provider chain；CLI／設定檔語法仍屬概念。選定後不得因失敗改試較低優先設定。

Terminal 契約／設定／provenance 失敗，尤其 OCR_PROVIDER_NOT_FOUND、OCR_PROVIDER_CONTRACT_INVALID、OCR_PROVIDER_CAPABILITY_MISSING、OCR_PROVIDER_VERSION_UNAVAILABLE、OCR_PROVIDER_VERSION_UNSUPPORTED、OCR_SOURCE_CHANGED、OCR_MODEL_CHANGED，不論 allow_fallback 為何都必須直接終止。OCR_SOURCE_CHANGED 僅表示原始來源 bytes 的 SHA-256 改變；OCR_MODEL_CHANGED 表示同一來源下，預期 model/traineddata identity 或 digest（expected_model_digest != current_model_digest）已過期。後者不得改寫 source_digest，也不得以備援掩蓋。

只有第 7 節標為操作性失敗的 provider failure，且目標尚非 default Tesseract，才具備援資格：

- allow_fallback = true：最多轉向 Tesseract 一次，重新驗證其契約，記錄 requested/actual provider 與原始 failure code。
- allow_fallback = false（預設）：回報 OCR_FALLBACK_NOT_ALLOWED，保留原始 failure 為 cause。
- 預設 Tesseract 自身失敗或備援也失敗：回報實際失敗，保留已有 cause 歷程，不再切換或形成循環；沒有成功 evidence 就不偽造成功 provenance。

若在執行或既有 evidence reuse 前發現 OCR_MODEL_CHANGED，呼叫者必須停止，不得在舊 provenance 下繼續，也不得事後靜默改寫 expected digest。恢復需要以新驗證的 model provenance 重新進行明確 OCR resolution/execution，或恢復原先預期的 model bytes/configuration。

Evidence 相關 identity 變更（provider、provider version、engine/model identity、model/traineddata digest、language/execution/preprocessing 設定及原始 source digest）都會使既有 evidence stale；其中 model bytes 的即時不一致使用 OCR_MODEL_CHANGED 表示。診斷可保留 provider_id、model_id、expected_digest、actual_digest 等確定性欄位，不得把 filesystem path、timestamp 或任意 stderr 當作 canonical identity。

Provider version 是必要 provenance。無法確定時，在辨識前以 OCR_PROVIDER_VERSION_UNAVAILABLE 失敗；成功偵測但不符合相容政策時使用 OCR_PROVIDER_VERSION_UNSUPPORTED。預設 Tesseract adapter 的 provider version 與 engine version 分離；Phase 15 目前以 **Tesseract 5.x** 為目標，不宣稱全部版本已驗證。

## 9. Phase 15.1 範圍與安全邊界

範圍僅含 OCRProvider、OCRProviderCapabilities、provider validation、canonical evidence、provider-neutral provenance、resolution foundation、no-silent-fallback、stable errors、Tesseract adapter／availability/version detection／structured output parsing／traineddata provenance，以及 deterministic fake provider／contract tests。

不含 PDF rasterization、scanned-PDF workflow、mixed-page routing、standalone image ingestion、Phase 12 grounding integration、cloud OCR、PaddleOCR、Apple Vision 實作或 dynamic custom-provider registration UX。Provider 接收已準備影像與原始來源身分，不負責文件工作流程。

Phase 12/13 維持 FROZEN。不得使用 shell=True、不安全指令串接、靜默 network OCR、自動 mutable model download 或 credentials/API keys；deterministic tests 不消耗 AI 額度。未來遠端整合須明確授權外傳，但不在 Phase 15.1 實作。
