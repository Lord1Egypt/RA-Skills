# Phase 15.2 PDFium Renderer 架構修訂

本文件是 Phase 15.2 的 documentation/governance amendment；PR #22 已實作其 C renderer、D orchestration 與 E validation，production release validation 仍另行受控。它補充並在 renderer-specific 決策上優先於 [Phase 15.2 raster contract](phase15-2-raster-contract.md) 與 [Phase 15 OCR architecture](phase15-ocr-architecture.md)；原始來源身分、逐頁路由、固定 raster 語義、錯誤 taxonomy、worker isolation、Phase 12/13 與 Phase 15.1 frozen boundaries 全部保留。

修訂後狀態：

- **Phase 15.2 — COMPLETE / MERGED / BASELINE FROZEN**（A–E 已由 PR #22 合併，squash merge `ffac8e77aab6e35d23f09fee01f1d261ba4b5171`）。
- **pypdfium2 5.13.0 / PDFium 153.0.7999.0 — PREFERRED / APPROVABLE WITH NOTICES / PRODUCTION ADOPTION GATED**。
- **PyMuPDF 1.28.2 — TECHNICALLY VIABLE / LICENSE BLOCKED / NOT PRIMARY**。
- OCR JSON schemas 維持 **DEFERRED**；本文件不發布 schema。

## 1. Renderer 決策與歷史

Phase 15.2 的 primary renderer candidate 改為 exact package `pypdfium2==5.13.0`，搭配該版本官方 standard wheel 內含的 **PDFium 153.0.7999.0 / Chromium-PDFium build 7999**。核准候選 build 的 origin 為 `pdfium-binaries`，engine flags 必須為空，代表 V8 與 XFA 均未啟用。此狀態是 **PREFERRED / APPROVABLE WITH NOTICES**；PR #22 已導入 requirements、lock、worker adapter 與 production-shaped execution，但 release production adoption 仍須通過當期安全與發布驗證。

先前決策歷史不得移除：

- PyMuPDF 1.24.x 維持 **REJECTED / SUPERSEDED**。
- PyMuPDF 1.28.2 維持 technically viable，但在專案建立 AGPL-compliant use/distribution 或有效 Artifex commercial entitlement 前，維持 **LICENSE BLOCKED / NOT PRIMARY**。
- pypdfium2／PDFium 的 permissive licensing materially avoids 目前 PyMuPDF 的 AGPL/commercial entitlement blocker，但不免除第三方授權、notice、SBOM 與實際 distribution review。

## 2. Exact wheel 與 supply-chain policy

Production adoption MUST 同時滿足：

- exact pin `pypdfium2==5.13.0`；不得使用範圍、floating latest 或 prerelease；
- 僅使用 PyPI 官方、standard、non-V8／non-XFA platform wheel；
- 安裝流程強制 `--only-binary=:all:`，並使用核准 wheel SHA-256 allowlist；
- matching wheel 不存在時 fail closed，不得 fallback 至 sdist、system PDFium、下載 native binary 或本機 source compilation；
- 每個核准平台分別保存 wheel filename、SHA-256、wrapper version、PDFium version/build、origin 與 engine flags；
- wheel 與其內含 native PDFium 必須納入 SBOM、security inventory 與 release evidence。

本文件不建立 dependency lock 或 hash allowlist。實際 allowlist 必須在首次 dependency introduction 前，針對要支援的平台與當時 PyPI artifact 重新核對。

## 3. Canonical renderer provenance

Runtime identity 必須使用 pypdfium2 支援的公開 version identities，等同於：

- `pypdfium2.version.PYPDFIUM_INFO`
- `pypdfium2.version.PDFIUM_INFO`

成功 raster 的 canonical provenance 必須能確定性記錄：

| 欄位／身分 | 核准候選值或規則 |
| --- | --- |
| `renderer_id` | `pypdfium2` |
| `renderer_version` | `5.13.0` |
| `renderer_engine_version` | `153.0.7999.0` |
| PDFium build | `7999` |
| origin | `pdfium-binaries` |
| engine flags | exact ordered value；核准 standard build 為空 |
| approved build identity | wheel filename 加核准 SHA-256；不得只記 generic platform name |
| raster settings | dpi、format、colorspace、alpha、annotation/form、rotation、box 與 preprocessing policy |
| geometry | selected box type、effective PDF coordinates、effective rotation、實際 width/height |
| raster digest | SHA-256 of exact PNG bytes supplied to OCR |

既有 provenance model 的 `approved_build_identity` 使用下列 canonical ASCII grammar，承載 wheel、hash、engine build、origin 與 flags，而不新增或改變 Phase 15.2-A model shape：

```text
pypi-wheel:<wheel_filename>@sha256:<64-lowercase-hex>|pdfium-build:7999|origin:pdfium-binaries|flags:none
```

各 component 順序固定如上；`wheel_filename` 必須是 PyPI artifact 的原始 basename，不能是 path。核准 standard build 的 flags token 固定為 `none`，代表 V8/XFA 均停用。未來若另經核准非空 flags，token 必須使用經 governance 定義、按 ASCII 字典序排列且以逗號分隔的 stable names；在該次 review 定義前不得自行產生新值。Runtime 必須把公開 version identities 與 allowlisted identity 精確比對，不能只照抄預期常數。

Canonical identity 不得包含 timestamp、temporary path、absolute library path、host cache path、任意 Python `repr`、environment dump 或 `unknown` placeholder。PDFium native handle、bitmap 或其他 engine object 不得離開 restricted worker／adapter。

## 4. Security traceability

Renderer security review MUST 同時涵蓋 Python wrapper package 與 bundled PDFium/native dependencies。一般 Python package dependency scan 無法單獨證明 PDFium 安全狀態。

每個 approved artifact 必須保留 `pypdfium2` exact version、PDFium exact version、Chromium/PDFium build number、wheel filename 與 wheel SHA-256。未來 CVE/advisory review 必須把 Chromium/PDFium 的 affected-version boundary、branch/build 或可得的 fix commit 映射回 `153.0.7999.0`／build `7999`，並檢查 wrapper release notes、NVD/CVE、Chromium/PDFium security references、OSV/GitHub advisories、適用 distro trackers 與 wheel 內實際 native components。沒有 pypdfium2-specific advisory 不代表 bundled engine 已通過審查。

Security approval 具時效性，至少在下列時點重做：

1. 首次 production dependency adoption 前；
2. 每次 wrapper、PDFium build、wheel 或 platform allowlist upgrade；
3. 每次 public release 前。

若 advisory 只提供 Chromium version boundary，review evidence 必須記錄映射方法與限制；不可只由 package version 較新推定不受影響。形式受影響但主張特定路徑不可達時，仍須書面 VEX／risk acceptance。

## 5. License、notices 與 SBOM

經稽核候選的 pypdfium2 code 採 `Apache-2.0 OR BSD-3-Clause`；PDFium 採 BSD-style license，並包含各自授權的第三方元件。這與本專案 MIT 授權可形成 permissive distribution path，但 production dependency introduction 前必須完成：

- **`THIRD_PARTY_NOTICES / LICENSE BUNDLE COMPLETE`**
- **`SBOM UPDATED`**

Redistribution 必須保存 approved wheel 所附的 relevant license、copyright、attribution、disclaimer 與 NOTICE material。當前稽核 wheel manifest 包含（依實際平台適用）Abseil、AGG、fast_float、FreeType、ICU／Unicode、LCMS、libjpeg-turbo／IJG、OpenJPEG、libpng、libtiff、LLVM libc、pdfium-binaries、PDFium、simdutf 與 zlib。此清單不是永久 exhaustive allowlist；每個實際 approved platform wheel 內的 manifest 才是該 artifact 的權威，且不得假設各平台 wheel 的 native components 或 notices 完全相同。

## 6. V8／XFA 與 optional feature policy

核准候選限 audited standard wheel configuration：V8 disabled、XFA disabled。不得透過 source setup、environment option、alternative wheel 或 system library 靜默啟用 optional engine feature。Engine flags 必須進入 provenance 並在 worker 啟動時比對；非空或不符合 allowlist 時 fail closed。任何未來 V8/XFA-enabled build 必須另做 security、license、supply-chain、resource 與 sandbox review，不能沿用本文件的候選核准。

## 7. Mandatory worker isolation

Production architecture 維持：

```text
parent/orchestrator
        ↓
restricted dedicated worker
        ↓
pypdfium2 / PDFium
        ↓
bounded versioned IPC
```

Worker 必須先完成 restriction，再接收、open 或 parse untrusted PDF bytes。必須保留 no network、minimal filesystem exposure、no credentials、closed inherited descriptors、process-group isolation、parent monotonic watchdog、hard memory/CPU/resource limits、bounded temporary storage、bounded IPC、transaction-owned cleanup 與 native crash isolation。不得在 unrestricted parent process 直接 import/use PDFium 解析或 rasterize untrusted PDF；Python thread timeout 不能取代 killable process boundary。

## 8. Strict PDF admission 與 error mapping

PDF-only admission 不得以 extension、filename 或 caller format hint 作為權威。原始 PDF bytes 的 SHA-256 仍是唯一 source identity，且 sandbox restriction 必須在 PDFium parse 前生效。Worker 可將 PDFium format/open result 作為 controlled corroborating evidence，但不能用 renderer default 擴大至其他格式。

至少映射：

- PDFium format/open-invalid result → `OCR_PDF_INPUT_INVALID`
- password-required result → `OCR_PDF_PASSWORD_REQUIRED`

Parser/renderer page count 必須一致；零頁、無效 MediaBox／rotation 或結構抽取失敗仍 fail closed。

## 9. Exact 300-DPI pixel geometry

固定輸出仍為 300 DPI。禁止將 implementation 定義成單純以 binary float 計算 `scale = 300 / 72`，再接受 renderer helper 的 incidental rounding。稽核已觀察 60 points 乘以 300/72 在 binary float 成為約 `250.00000000000003`，high-level helper 因此產生 251 px；契約預期是 250 px。

對已驗證、已選定且在 render coordinate origin 下的 page box，先求 exact horizontal/vertical point extents：

```text
Wpt = exact(x1 - x0)
Hpt = exact(y1 - y0)

if effective_rotation is 0 or 180:
    rotated_Wpt = Wpt
    rotated_Hpt = Hpt
else if effective_rotation is 90 or 270:
    rotated_Wpt = Hpt
    rotated_Hpt = Wpt

width_px  = ceil_exact(rotated_Wpt × 300 / 72)
height_px = ceil_exact(rotated_Hpt × 300 / 72)
```

`ceil_exact(q)` 是不小於 exact mathematical value `q` 的最小整數。PDF numeric coordinates 必須以可保留其確定值的 decimal/rational representation 進入上述計算；不得讓 binary-float multiplication 位於 ceiling decision boundary。例：`ceil_exact(60 × 300 / 72) = 250`。Negative/zero/non-finite extents 先以 invalid geometry 拒絕。

Adapter 必須把上述 explicit integer target width/height 與 selected geometry 傳給適用且受支援的 low-level PDFium bitmap/render API，不得把尺寸權威交給 high-level helper 的 float rounding。配置 bitmap 前先驗證 expected width、height、pixel product 與 raw bitmap footprint；render/encode 後再驗證 actual dimensions 恰等於 expected dimensions。任何不一致使用 renderer-neutral failure mapping，不得裁切、縮放或改 DPI 補救。

## 10. Rotation 與 box selection

Intrinsic PDF page rotation 必須由 deterministic PDF structure/parser layer 解析有效繼承值，正規化並驗證為 0／90／180／270，記錄為 `effective_rotation`。PDFium render-call rotation 是 additional rotation；adapter 必須以明確參數避免 double rotation，一般情況不得再疊加旋轉。不得以 OCR orientation、heuristic 或 undocumented renderer default 取代有效 PDF rotation。

pypdfium2 individual box getters 不可靠地解析 page-tree inherited boxes，因此 `get_bbox()`、renderer defaults 與 unresolved local-only box getters 都不得作為 box-policy authority。Adapter/worker 必須依下列順序：

1. 由 additive deterministic PDF structure/parser layer 解析 effective inherited MediaBox 與 CropBox；
2. 驗證座標 finite、MediaBox/CropBox positive area，以及 CropBox 位於有效 MediaBox 內；
3. 選擇 valid effective CropBox，否則 effective MediaBox；
4. 將 selected box type 與原始 PDF effective coordinates 顯式傳入 restricted renderer worker；
5. 使用受支援 low-level PDFium geometry/render API 恰好 render 該 rectangle；
6. 在 provenance 記錄 selected box、coordinates、effective rotation 與驗證後尺寸。

這個 additive structure layer 不修改 frozen Phase 13 `extract_pdf`、ExtractionResult 或既有 ingestion behavior。

## 11. Raster、annotation 與 PNG contract

固定 raster contract 保持：300 DPI、PNG、RGB、`alpha=false`、`semantic_preprocessing=none`、`render_annotations=false`。可使用 repository 已存在的 Pillow dependency 做 deterministic in-memory PNG encoding，不需因本決策新增 Pillow dependency。

pypdfium2 呼叫必須顯式設定 `draw_annots=false`；不得依賴 high-level renderer 可能啟用 annotation 的 default。Forms 不得 initialize 或 render，並在適用介面顯式使用等同 `may_draw_forms=false` 的設定。Annotation/form policy 必須被固定 configuration 與 provenance 覆蓋。

`raster_digest = SHA-256(exact PNG bytes supplied to OCR)`。不得雜湊 preview、另一份 re-encode 或 raw bitmap 來替代。契約不宣稱跨平台 pixel-identical 或 PNG-byte-identical output；同一實際 PNG 的 digest 仍必須準確且可重算。

## 12. Resource ceilings 與 IPC

既有 ceilings 不變，包括每個 worker 512 MiB memory、每頁 renderer/encode/validation 30 秒 watchdog、transaction 同時 256 MiB temporary storage、每邊 10,000 px、每頁 25,000,000 pixels 與每頁 100 MiB PNG。Output-size post-check 本身不足以保護 native allocation。

Bitmap allocation 前必須 preflight expected width、expected height、pixel product 與依實際 pixel format/stride 計算的 raw bitmap footprint。Render/encode 後必須驗證 actual dimensions、encoded PNG size 與 IPC payload size。Release validation 必須證明 25-million-pixel worst-case fixture 在 512 MiB worker ceiling 內可執行；若無法滿足，應降低 effective configured limit 或停止 adoption，不得在本文件提高 committed ceiling。

IPC 維持 bounded、versioned JSON header 加 explicit-length bounded PNG payload，header 至少承載 width/height、wrapper/engine/build/wheel identity、engine flags、selected box、effective rotation、raster digest 與 bounded diagnostics。禁止 pickle。PDFium handles、callbacks、bitmap pointers 或其他 native object 不得出現在 IPC。

## 13. Renderer-neutral error taxonomy

既有 public Phase 15.2 errors 足以涵蓋 PDFium，不新增 renderer-specific public code：

- `OCR_PDF_PASSWORD_REQUIRED`
- `OCR_PDF_INPUT_INVALID`
- `OCR_PDF_PAGE_INVALID`
- `OCR_PDF_RESOURCE_LIMIT_EXCEEDED`
- `OCR_RASTERIZATION_FAILED`
- `OCR_PDF_CLEANUP_FAILED`

Known watchdog/cgroup/storage/pixel/IPC ceiling 使用 `OCR_PDF_RESOURCE_LIMIT_EXCEEDED`；非資源原因的 native crash、render failure、identity mismatch 或 invalid raster 使用 `OCR_RASTERIZATION_FAILED`。有既存 primary failure 時 cleanup diagnostic 不得覆蓋它。Admission、resource、renderer 與 cleanup failures 全部在 OCR provider fallback 之外，不得觸發 provider fallback。

## 14. Production adoption gate 與平台政策

本架構修訂列出的 production-adoption review 已由 PR #22 的 C/E 變更完成文件、artifact、license、SBOM、geometry、worker、admission 與 smoke-test gate；後續每次 upgrade 或 public release 仍須重新確認：

- 要支援平台的 exact official wheel SHA-256 allowlist 已核准；
- `THIRD_PARTY_NOTICES / LICENSE BUNDLE COMPLETE`；
- `SBOM UPDATED`；
- wrapper 與 bundled PDFium/native components 的 current security re-check 通過；
- inherited/invalid CropBox/MediaBox 與 rotation geometry fixtures 通過；
- exact pixel arithmetic 與 helper-rounding regression tests 通過；
- worker sandbox、hard limits、watchdog、temp quota、bounded IPC 與 native crash isolation feasibility 已確認；
- raw-byte admission、password、RGB/no-alpha、annotations/forms-off、PNG digest、cleanup 與 repeated raster smoke tests 通過。

PR #22 不代表已合併或完成 release production validation。

平台分類：

| 平台 | 架構狀態 |
| --- | --- |
| Linux x86_64 | primary production-security candidate；仍須實證 controlled cgroup/sandbox enforcement |
| macOS Intel／Apple Silicon | wheel 與 development/API testing compatible；本 amendment 不自動授予 production-security support |
| Windows x86-64／ARM64 | wheel compatible；本 amendment 未核准 production-security support |

Package compatibility 不等於 Phase 15.2 security-contract support。任何平台無法強制必要 restriction/ceiling 時，啟動前以 resource-limit failure 拒絕，不能 best effort 繼續。

## 15. Additive 與 frozen boundaries

現有 `PDFRasterizer` abstraction 足以容納此 adapter，不變更 Phase 15.2-A 的 source identity、page identity、RasterConfiguration、ResourceLimits、WorkerIsolationPolicy、RasterProvenance shape 或 renderer boundary，也不變更 Phase 15.2-B classifier 與 mixed-PDF planning。Wheel/build/flags 的細節收斂至既有 `approved_build_identity`、`renderer_version` 與 `renderer_engine_version` identity documentation；不發布新 schema。

本修訂不要求修改 Phase 12 source digest、Phase 12 locator、Phase 13 ExtractionResult、Phase 13 ingestion production behavior 或 Phase 15.1 OCRProvider contract。若未來實作發現任何 frozen production change 必要，必須停止並回報 `PHASE_15_2_FROZEN_CONTRACT_CHANGE_REQUIRED`，不得以 renderer adapter 繞過。
