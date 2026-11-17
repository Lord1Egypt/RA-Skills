# Phase 15.5 OCR 接地轉譯契約

目前狀態：**COMPLETE / MERGED / BASELINE FROZEN**（PR #32，squash merge `5393c3e3e3cfee6cbf6891c452ac1bdd71a5418d`）。Phase 15.6 已完成並合併；OCR JSON schemas 仍為 DEFERRED。

本文件定義 OCR-native evidence 進入既有 Phase 12 source-grounding workflow 的 additive adapter。AGY 仍是唯一 semantic authority；Phase 15.5 只驗證身分、位置、順序與 evidence association，不修正 OCR 文字、不產生 claim、不判斷事實或 citation relevance。

## 1. Frozen handoff

Phase 12 的實際 handoff 是 `SourceInventory.add_source()` 與 `add_unit()` 所承載的 source/unit envelope。Phase 13 `ExtractionResult` 仍是 deterministic document ingestion 的輸出；OCR translation 不建立 fake `ExtractionResult`，也不修改 `ExtractionResult`、Phase 12 schemas 或 `source_grounding.py`。

轉譯結果是 immutable internal evidence object，供 AGY 決定是否 promote 為 source unit。它保存 `source_id`、原始 bytes `source_digest`、frozen Phase 12 locator、exact text 與同一個 `OCREvidence` object/reference。Phase 15.5 不寫 grounding sidecar、不建立 public schema。

## 2. Mechanical locator mapping

### PDF

OCR-native `{"kind":"page","page":N,"total_pages":T}` 只映射為 frozen Phase 12 `{"kind":"page","start":N,"end":N}`。`N` 必須為 1-based 且不大於 `T`；`total_pages` 只留在 OCR-native page identity 與 translation metadata，不放入 Phase 12 locator。相同原始 PDF source digest 與 page 會得到相同 Phase 12 source/page identity。

### Standalone image

Phase 12 沒有 image kind，但 frozen `generic` locator 可表達 source 內的非文件位置。唯一受支援的 standalone image translation 是 OCR-native `{"kind":"image","ordinal":1}`（single image 1 of 1）映射為 `{"kind":"generic","label":"image:1-of-1"}`。ordinal 不是 1、total 不符 1-of-1、或含其他欄位會 fail closed。這是現有 generic kind 的 deterministic label，不新增 locator kind，也不宣稱可直接作 Phase 12 page locator。

Locator 永遠不含 raster/prepared digest、provider/model ID、worker ID、timestamp、temp path 或任何 OS path。Source identity 由 envelope 的 `source_id` 與原始 `source_digest` 決定。

## 3. Text, spans and geometry

`OCREvidence.pages[0].raw_text` 是唯一輸入文字，逐字保留 leading/trailing whitespace、空行、Unicode、標點與換行。Phase 15.5 不使用 `.strip()`、Unicode repair、hyphen/line merge、spelling correction 或 semantic normalization。

目前 frozen Phase 12 source-unit contract 沒有 OCR span/offset 欄位，也沒有可逆 normalized-text mapping；因此 adapter 不產生或模糊推導 offsets。Provider regions/confidence 保留在同一 `OCREvidence` association，geometry 的座標空間仍是 Phase 15.3 prepared image 或 Phase 15.2 raster page space，不改作 Phase 12 locator authority。未來若需要 quote offsets，offset 必須直接指向 exact `raw_text` representation，另行治理。

## 4. PDF and mixed-source ordering

Searchable PDF page 繼續走既有 Phase 13 → AGY/Phase 12 path，不建立 fake OCR evidence。Scanned page 才經 Phase 15.2 transaction，再由本 adapter 轉譯；其 source digest、1-based page、raw text、OCREvidence 與 raster provenance 全部保留。Mixed PDF 的 translation output 依原始 page order 排列，TEXT/OCR route identity 不被語意合併或重排；同一 raw PDF 只有一個 canonical source identity。

## 5. Standalone image provenance

Image source identity 是原始 encoded bytes 的 SHA-256。`prepared_image_digest` 只作 Phase 15.3 derived provenance，不能進入 Phase 12 source identity。`ImagePreparationProvenance` 以 additive association 保留；EXIF display orientation 後的 provider geometry 維持 prepared-image coordinate space，不在此階段映回 encoded orientation。

## 6. Validation and failure

Adapter 在建構結果前驗證 source digest、source ID、locator、page/ordinal identity、OCREvidence source/locator、raw text 與 evidence association。任何 mismatch、malformed evidence、unsupported mapping 或 impossible span mapping 都以穩定 translation error fail closed；不丟頁、不降級 locator、不回傳 partial result。

Phase 15.5 不解析 PDF/image、不 rasterize、不 decode、不執行 OCR、不觸發 provider resolution/fallback。Tests 必須證明 provider、rasterizer、image decoder 與 fallback call count 均為零。

## 7. Authority and boundaries

```text
original source bytes
  → Phase 13 extraction or Phase 15 OCR evidence
  → Phase 15.5 mechanical grounding translation
  → Phase 12 source/locator envelope
  → AGY semantic segmentation, support and grounding decisions
```

Phase 15.5 不判斷 OCR 是否正確、不修補 wording、不產生 claim、不比較 extracted/OCR meaning、不翻譯 locator 至其他格式，也不執行 Phase 12 semantic grounding。Phase 15.6 real-source/release validation 已完成；OCR JSON schemas 維持 DEFERRED。
