# Phase 15.6 OCR pipeline qualification contract

本文件定義 Phase 15.6 的 real-source／end-to-end／platform／security／release-readiness qualification。它只驗證已凍結的 Phase 15.1–15.5 pipeline，不建立新的 OCR execution、evidence、locator、fallback 或 grounding 語意。AGY 仍是 sole orchestrator、semantic authority 與 single source of truth；OCR 仍只提供 extraction、evidence 與 provenance。

目前狀態：**COMPLETE / MERGED / VALIDATED / BASELINE FROZEN**（PR #35，squash merge `ffab67e057a4d3b0028625399c4732272b9d9183`）；實際結果見 [qualification report](phase15-6-validation-report.md)。OCR JSON schemas 維持 **DEFERRED**。

## 1. Qualification objective

Phase 15.6 驗證 representative source structures 的 contract correctness、determinism、identity chain、routing、admission/preparation、evidence integrity、grounding translation、failure behavior、resource/security boundary、platform/build identity 與 reproducibility。它不建立 OCR accuracy SLA，不承諾 universal language accuracy，也不把實際辨識文字視為 semantic truth。

Frozen validation path：

```text
original source bytes
  → deterministic admission / PDF raster or image preparation
  → frozen OCR provider execution
  → OCREvidence
  → Phase 15.5 mechanical grounding translation
  → frozen Phase 12 source/unit envelope
  → AGY semantic reasoning
```

Qualification harness 必須呼叫既有 Phase 15.2、15.3、15.5 production interfaces，不得複製其 classifier、renderer、decoder、provider、fallback 或 locator logic。

## 2. Corpus and fixture policy

Required deterministic corpus 由 project-owned synthetic generation code 或明確可再散布的 fixtures 建立，不提交 customer/confidential sources、個資、credentials 或無再散布權的 commercial scans。若 manual qualification 使用 repository 外部文件，只能記錄不敏感的結果 metadata。

Corpus 至少涵蓋：

- PDF：searchable、fully scanned、mixed searchable/scanned、multi-page、rotation、CropBox/MediaBox、password、malformed/non-PDF 與 resource simulation；
- PNG：RGB、grayscale、transparency 與 realistic text；
- JPEG：RGB、EXIF display orientation 與 CMYK/YCCK；
- TIFF：valid single-frame 與 deterministic multipage rejection。

Fixtures 可含多語文字、表格、旋轉、對比與 annotation，但 qualification 不是 OCR benchmark research。必要 CI 的文字結果由 deterministic fake provider 控制；不得依賴 host OCR accuracy。

## 3. Contract CI and live qualification

`contract CI` 是 PR required gate：使用 fixed synthetic inputs、approved Python dependencies 與 deterministic fake providers，驗證 pipeline contracts、identity、ordering、provenance、errors 與 grounding translation。它不得需要 network、mutable download、host credentials 或 uncontrolled system Tesseract。

`live engine qualification` 是明確 opt-in operator/developer command，只在 exact supported Tesseract 5.x、可驗證 traineddata/model identity 與 controlled environment 存在時執行。它不得自動下載 model。Live qualification 驗證 invocation、evidence、identity 與 provenance integrity；recognized wording 可觀察，但不是 universal frozen truth。環境不符時必須回報 `NOT QUALIFIED IN CURRENT ENVIRONMENT`，不得冒充 PASS。

代表語言至少包含 project policy 已支援且現有環境已安裝、可驗證的 language data。缺少 language pack 時記錄為 environment limitation，不得在 test 中臨時下載。

## 4. Runtime and supply-chain identity

Qualification 必須核對：

- `pypdfium2==5.13.0`；
- PDFium `153.0.7999.0`／build `7999`／origin `pdfium-binaries`；
- standard wheel flags `none`，亦即 V8/XFA disabled；
- current platform approved wheel filename 與 SHA-256 allowlist；
- actual installed Pillow version；
- live 時的 Tesseract/provider version、engine identity、language configuration 與 sorted traineddata model manifest。

Runtime identity mismatch 必須 fail qualification。Supply-chain review 必須確認 wheel-only、no source-build fallback、approved hashes、third-party notices、license bundle、SBOM 與 no PyMuPDF。Qualification 不因方便而 upgrade dependencies。

## 5. Platform qualification

| Platform | Allowed Phase 15.6 classification |
| --- | --- |
| Linux x86_64 | primary production-security candidate；只有在 deployment-like controlled environment 實證 hard isolation 後才可 production-qualified |
| macOS Intel / Apple Silicon | development/API qualification；test PASS 不等於 production-security qualification |
| Windows x86-64 / ARM64 | package-compatible only；未另經治理不得宣稱 production-security qualified |

Linux hard-isolation qualification 必須實際驗證 dedicated worker、process group、watchdog、memory/resource enforcement、descriptor handling、bounded IPC/temp storage、cleanup、no network/no credentials 與 crash containment。若 current CI 無 cgroup v2 或 equivalent deployment enforcement，狀態必須是 `DEPLOYMENT ENVIRONMENT VALIDATION REQUIRED`。

## 6. End-to-end qualification

### PDF and mixed PDF

Scanned PDF chain 必須可追溯 original PDF digest → admission → selected page geometry/rotation → exact raster PNG digest → OCR request/evidence → Phase 15.5 page locator → Phase 12 source/unit。Mixed PDF 必須以 `TEXT, OCR, TEXT, OCR` 的 representative four-page input 驗證 mechanical classification、OCR-only scanned pages、1..4 ordering、single original PDF identity、兩條 extraction route 在 grounding envelope 的 mechanical convergence，以及零 semantic merge/correction。

### Standalone images

PNG/JPEG/single-frame TIFF chain 必須可追溯 original image digest → restricted preparation worker → RGB opaque PNG → prepared digest → OCR request/evidence → Phase 15.5 `image:1-of-1` generic locator → Phase 12 source/unit。EXIF qualification 驗證 display transform 與 prepared dimensions；provider geometry 仍在 prepared-image coordinate space，不 reverse-map。

Source digest 永遠是 original raw bytes。Raster/prepared digest 永遠只是 derived evidence，不能成為 source identity。

## 7. Failure and fail-closed qualification

Required safe cases：invalid/password PDF、malformed/unsupported image、multipage TIFF、dimension/output/resource limit、worker timeout/abnormal exit、provider unavailable/version/language/model error，以及 frozen Phase 15.1 allow_fallback false/true operational paths。

每個 required failure 必須保留 stable error identity、停止 complete transaction、不得回傳 partial success/fabricated evidence/semantic recovery。Admission、renderer、decoder、preparation與resource failures 不得觸發 provider fallback；provider fallback 只能遵循 frozen single-fallback semantics。

## 8. Determinism and privacy

同一 approved runtime/version/platform/config 重跑 representative fixtures，必須得到相同 source digest、route、locator、raster/prepared digest、evidence serialization、grounding translation 與 error code。不得宣稱 frozen contract 未保證的 cross-platform PNG/pixel equality。

Canonical qualification evidence 不得包含 local/temp paths、user/home identity、credentials、environment dump、random ID、object address 或 prohibited timestamp。Diagnostics 必須 bounded、secret-safe 且不能把 arbitrary subprocess stderr 變成 canonical identity。

## 9. Security review

每次 qualification 必須審查 exact pypdfium2/PDFium build、Pillow、live Tesseract/native dependencies 與 Python dependency inventory。Review 必須查 wrapper 與 bundled native components；普通 Python package scanner 不足以單獨證明 PDFium 安全。Relevant critical/high vulnerability 若影響 exact production path，結果為 `RELEASE BLOCKED`，不得靜默 upgrade 或略過。

Deterministic qualification 不增加 unsafe parser、network、shell、arbitrary code loading、credential handling 或 mutable model download。Frozen workers 的 existing isolation/resource semantics不得降低。

## 10. Qualification result and release readiness

Phase 15.6 產生 internal governance report，不發布 OCR schema。Report 至少記錄 exact git baseline、renderer/build、decoder/provider/model identities、fixture categories、每項 `PASS`／`FAIL`／`SKIPPED`／`ENVIRONMENT_REQUIRED`、platform classification、known limitations 與 unresolved release blockers；不得包含 secrets 或 host paths。

Phase 15.6 completion 表示 Phase 15 engineering pipeline contract-complete 且 qualification evidence 已記錄，不代表建立 release、tag 或 version bump。Final readiness 僅能是：

- `RELEASE READY`；
- `RELEASE READY WITH DOCUMENTED PLATFORM LIMITATIONS`；
- `RELEASE BLOCKED`。

若 Linux hard isolation 尚待 deployment environment，Phase 15 可 complete，但 readiness 必須是 `RELEASE READY WITH DOCUMENTED PLATFORM LIMITATIONS`。任何 public release 前仍須重新執行 time-sensitive security、dependency、wheel/license/SBOM 與 live environment review。

## 11. Frozen boundaries

Phase 12/13 與 Phase 15.1–15.5 contracts 維持 frozen。Phase 15.6 不發布 schemas、不修改 source identity、locator、OCREvidence、provider/fallback、renderer、image preparation 或 grounding translation semantics。若 representative qualification 揭露需要 semantic frozen change，必須停止並回報 `PHASE_15_6_FROZEN_CONTRACT_DEFECT_FOUND`。
