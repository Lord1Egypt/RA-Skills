# Phase 15.3 Standalone Image OCR Contract

本文件是 Phase 15.3 獨立圖片 OCR ingestion 的規範性架構契約。Phase 15.3 狀態為 **COMPLETE / MERGED / BASELINE FROZEN**（implementation PR #26，squash merge `54c3cd5a26b98f1eb6a6a2fbc1ea08fbe5cccd9f`）；Phase 15.1 provider foundation 與 Phase 15.2 PDF OCR baseline 均維持 FROZEN。本階段只新增 PNG、JPEG 與單 frame TIFF 的機械式 admission、準備與 OCR evidence orchestration，不修改 Phase 12/13、Phase 15.1 或 Phase 15.2 契約。OCR JSON schemas 維持 DEFERRED。未來若需改變本契約，必須經明確治理，不得在 Phase 15.4+ incidental 修改。

## 1. 支援範圍與凍結邊界

Phase 15.3 僅接受內容辨識為下列格式的獨立圖片：

- PNG
- JPEG
- TIFF，且 frame count 必須恰為 1

多 frame TIFF、GIF、WEBP、HEIF/HEIC、BMP、SVG、AVIF、PDF 與其他 Pillow 可解碼格式均不在本階段。多 frame TIFF 不得只取 frame 0、flatten 或逐 frame OCR；它以 `OCR_IMAGE_FORMAT_UNSUPPORTED` 確定性失敗，擴充留待未來明確治理。

Phase 15.3 不實作通用 image catalog ingestion、Phase 15.4 custom-provider registration UX、Phase 15.5 OCR → AGY／Phase 12 grounding translation、Phase 15.6 live/release validation 或 OCR JSON schemas。AGY 仍是唯一語意權威；image preparation 與 OCR evidence 不作語意判斷。

## 2. 來源身分與 locator

唯一 canonical 來源身分為：

```text
source_digest = SHA-256(original raw source image bytes)
```

不得以 decoded pixels、EXIF-corrected pixels、prepared PNG、OCR input digest、檔案路徑或時間戳取代。實作須重用既有 raw-byte SHA-256 authority，不建立競爭性來源雜湊語意。

每個已接受來源恰代表一張圖片，沿用 Phase 15.1 OCR-native locator：

```json
{"kind":"image","ordinal":1}
```

其語意為 image 1 of 1；不虛構 PDF page，也不在 Phase 15.3 轉換為 frozen Phase 12 locator。

## 3. Content-based admission

檔名與副檔名不具權威。受限 worker 內的 decoder-reported format 必須恰為 PNG、JPEG 或 TIFF；Pillow 的較廣格式支援不會擴張 allowlist。可辨識但不支援的格式與多 frame TIFF 使用 `OCR_IMAGE_FORMAT_UNSUPPORTED`；結構無效、malformed 或 truncated input 使用 `OCR_IMAGE_INPUT_INVALID`。

不得啟用 `LOAD_TRUNCATED_IMAGES` 或同等寬鬆模式。不得停用 Pillow decompression-bomb protection；warning 與 error 均須升級為確定性的 image resource failure，另仍需執行本契約的明確 dimensions/pixels limits。

## 4. Canonical preparation pipeline

每個已接受來源必須經同一 provider-neutral pipeline：

1. 驗證 raw input 與 resource envelope。
2. 解碼恰一張圖片／frame。
3. 套用標準 EXIF display orientation。
4. 依第 5 節正規化 color/alpha。
5. 編碼為 opaque RGB PNG，不攜帶 ICC metadata。
6. 對實際 provider input bytes 計算 `prepared_image_digest`。
7. 將完全相同的 prepared PNG bytes 交給 OCR provider。

不得因不同 provider 而直接傳遞原始 JPEG/TIFF/PNG encoding。不得執行 sharpening、denoise、thresholding、binarization、auto contrast、histogram equalization、deskew、crop/content detection、quality resize、super-resolution、language-aware processing 或 LLM processing。

### 4.1 EXIF orientation 與 geometry

JPEG/TIFF 有 EXIF orientation 時，worker 必須決定性讀取並套用標準 display transform；缺漏或 normal orientation 不作幾何 transform。不得 in-place 修改原始來源。Preparation provenance 必須記錄原始 orientation value（存在時）、是否套用 transform，以及 prepared dimensions。

Phase 15.3 provider geometry 一律解讀於 **prepared-image coordinate space**：EXIF display orientation 與 color/alpha normalization 之後、Phase 15.5 translation 之前。Phase 15.3 不映回 encoded/original orientation；沒有 provider geometry 時不得捏造。

## 5. Color、alpha 與 ICC

Canonical provider input 為 RGB、opaque、no-alpha PNG：

- RGB：保留 decoder 產生的 RGB values。
- L/grayscale：以核准 decoder 的 channel replication 決定性轉為 RGB。
- LA、RGBA、palette transparency：先解析 palette／透明度，再以 opaque white `#FFFFFF` 作 alpha composite，最後轉為 RGB。部分透明 pixel 使用標準 source-over compositing；透明度不得留入 provider input。
- Palette without transparency：決定性解析 palette 後轉為 RGB。
- CMYK/YCCK JPEG：由核准 decoder 解碼，接著明確轉為 RGB；不得把該模式留給 provider。
- 其他未核准／不安全模式：fail closed，不作猜測性轉換。

Phase 15.3 不進行 ICC color-managed conversion，不呼叫 host display profile 或 LCMS transform。偵測得到時只記錄 `icc_profile_present=true`；prepared PNG 移除 ICC metadata，canonical evidence 不序列化原始 ICC bytes。

## 6. Preparation provenance 與 determinism

Derived execution identity 為：

```text
prepared_image_digest = SHA-256(exact prepared PNG bytes supplied to OCR)
```

它只屬 derived provenance，絕不可取代 `source_digest`。Immutable preparation provenance 必須可記錄：

- decoder ID 與 decoder version
- source format
- original width/height 與 mode
- 原始 EXIF orientation（存在時）與 transform-applied boolean
- `icc_profile_present`
- alpha policy 與 color-conversion policy
- target format PNG 與 target mode RGB
- prepared width/height
- `prepared_image_digest`

不得記錄 timestamps、host paths、temporary paths 或 environment dump。核准 decoder 是 repository 既有 Pillow dependency；除非另有 security governance，不因 Phase 15.3 升級。Determinism 承諾限於同一核准 implementation/version/platform/configuration 的 prepared result，不承諾跨版本或跨平台 PNG byte identity；raw source identity 不受 decoder output 影響。

## 7. Restricted decoder worker

Production boundary 必須為：

```text
parent/orchestrator
  -> restricted dedicated image worker
  -> Pillow decoder/preparer
  -> bounded result IPC
  -> OCR provider
```

Worker 必須在收到、開啟或解析 untrusted image bytes 前建立限制。至少包含 dedicated subprocess、parent monotonic watchdog、process-group termination/reaping、無 network、無 credentials、minimal environment/filesystem exposure、實務可行範圍內關閉 inherited descriptors、bounded IPC、bounded temporary storage、native decoder crash containment 與 deterministic cleanup。不得使用 pickle、shell command、任意外部 decoder 或 hidden download；Pillow image object 不得跨 worker boundary。

IPC 使用 versioned bounded JSON header、explicit binary payload length 與 bounded prepared PNG payload。Header 只含受限、machine-readable identity/provenance/diagnostics。

## 8. Hard resource ceilings

| Resource | Committed ceiling |
| --- | ---: |
| Raw image bytes | 100 MiB |
| Width | 10,000 px |
| Height | 10,000 px |
| Pixels | 25,000,000 |
| TIFF frame count | 1 |
| Estimated decoded packed footprint | 100 MiB |
| Prepared PNG bytes | 100 MiB |
| Decode/preparation timeout | 30 seconds |
| Worker memory | 512 MiB |
| Temporary storage | 256 MiB |

Configured limits 可為較低正值，但不可超過 ceiling；boolean 不是合法 numeric limit。Worker 必須在可行的最早時點 preflight raw size、dimensions、pixel product、frame count 與 estimated packed footprint，並在 preparation 後驗證 actual dimensions、pixel product、PNG bytes 與 IPC payload。

Decompression bomb、dimension/pixel/footprint/output ceiling、watchdog timeout 或 worker memory/storage violation 一律為 `OCR_IMAGE_RESOURCE_LIMIT_EXCEEDED`。

## 9. Stable image error taxonomy

| Error | Semantics |
| --- | --- |
| `OCR_IMAGE_FORMAT_UNSUPPORTED` | 可辨識但超出 allowlist/capability，包括多 frame TIFF |
| `OCR_IMAGE_INPUT_INVALID` | Malformed、structurally invalid、truncated 或 admission-invalid source |
| `OCR_IMAGE_RESOURCE_LIMIT_EXCEEDED` | Dimension、pixel、decoded footprint、prepared output、time、memory 或 storage limit |
| `OCR_IMAGE_DECODE_FAILED` | 無法由其他 image error 更準確表示的意外 decoder/preparation failure |
| `OCR_IMAGE_CLEANUP_FAILED` | 沒有更早 primary failure 時的 cleanup-only failure |

以上均為 machine-stable Phase 15.3 errors、`provider_fallback_eligible=false`，不得偽裝成 provider failure。若 primary failure 與 cleanup failure 同時發生，保留 primary failure，cleanup 只留 bounded deterministic diagnostics。

## 10. Provider execution、evidence 與 fail-closed

只有 worker 成功產生並驗證 prepared PNG 後，才可沿用 frozen Phase 15.1 provider resolution/execution/fallback。Image admission、decode、preparation、resource、worker 與 cleanup failure 的 provider call count 必須為 0，且不得觸發 provider fallback。有效 prepared input 遇 provider operational failure 時，才依既有明確 `allow_fallback` 規則最多備援一次；terminal provider failures 不備援。

Provider request 使用 exact prepared PNG bytes，但 `source_id`、`source_digest` 與 `{"kind":"image","ordinal":1}` 均指向原始獨立圖片。成功結果重用 Phase 15.1 `OCREvidence`、保留 exact `raw_text`，並由 additive immutable transaction envelope 關聯 `ImagePreparationProvenance`；不發布 schema、不修復文字、不捏造 geometry。

Standalone image OCR transaction 是 atomic/fail closed。任何必要 admission、resource、decode/preparation、provider/fallback、evidence validation 或必要 cleanup failure 都不產生 completed OCR result、partial evidence 或 semantic recovery。

## 11. Adoption gate

Phase 15.3 implementation 必須以 deterministic synthetic fixtures 驗證 admission、single-frame TIFF、EXIF rotate/mirror、RGB/grayscale/palette/alpha/CMYK、ICC no-transform、identity separation、resource bounds、worker failures、provider fallback boundary、evidence validation 與 repeated execution。Phase 15.1/15.2 regressions、frozen-contract guard、repository hygiene/security、README parity/link checks 與 exact `deterministic`／`repository` contexts 必須通過，方可視為 implementation-ready。
