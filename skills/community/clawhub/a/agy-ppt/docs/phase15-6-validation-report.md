# Phase 15.6 qualification report

狀態：**COMPLETE / MERGED / VALIDATED / BASELINE FROZEN**（PR #35，squash merge `ffab67e057a4d3b0028625399c4732272b9d9183`）。本報告是 internal governance evidence，不是 OCR public schema，也不是 release announcement。

## Qualification identity

| Item | Qualified value |
| --- | --- |
| architecture baseline | `85d3ba4edaf121215dae3d4c86bb1c6a671bd53c` |
| implementation run | `041d722dce2b40a92daaf45d4da61719bd4d2876` |
| pypdfium2 | `5.13.0` |
| PDFium | `153.0.7999.0`, build `7999`, origin `pdfium-binaries`, flags `none` |
| approved macOS x86_64 wheel | `pypdfium2-5.13.0-py3-none-macosx_13_0_x86_64.whl` |
| approved wheel SHA-256 | `2abedfb5c70992b19c780ed58d7f7b929e8ce8ee52c9140158f44317c90ec6c7` |
| Pillow | `12.3.0` |
| live provider | Tesseract adapter `phase15.1`, engine `5.5.2`, local |
| live language/model | `eng`; traineddata SHA-256 `7d4322bd2a7749724879683fc3912cb542f19906c83bcc1a52132556427170b2` |
| qualification host class | macOS x86_64 — DEVELOPMENT / API QUALIFIED |

## Contract and live results

| Case | Result | Evidence boundary |
| --- | --- | --- |
| scanned PDF with CropBox/rotation | PASS | original PDF digest, OCR route, PDFium raster digest, OCREvidence, page locator, Phase 12 unit |
| four-page mixed PDF | PASS | `TEXT, OCR, TEXT, OCR`, exactly two provider calls, source order 1..4, one source digest |
| RGBA PNG | PASS | isolated preparation, white alpha composite, RGB PNG, distinct source/prepared digests, image locator |
| EXIF-oriented JPEG | PASS | display orientation applied, dimensions `48×96`, prepared-coordinate evidence |
| grayscale single-frame TIFF | PASS | RGB PNG preparation and Phase 12 generic image locator |
| multipage TIFF | PASS (expected rejection) | `OCR_IMAGE_FORMAT_UNSUPPORTED` |
| password PDF | PASS (expected rejection) | `OCR_PDF_PASSWORD_REQUIRED` |
| malformed PDF | PASS (expected rejection) | `OCR_PDF_INPUT_INVALID` |
| image resource limit | PASS (expected rejection) | `OCR_IMAGE_RESOURCE_LIMIT_EXCEEDED` |
| worker timeout / abnormal exit | PASS (expected rejection) | stable resource/decode error identities, no partial result |
| deterministic rerun | PASS | same approved runtime produced identical report identities, routes, locators and derived digests |
| provenance privacy | PASS | no host/temp paths, credentials, timestamp, environment dump or random identity |
| live Tesseract English | PASS | actual 5.5.2 engine, verified traineddata digest, local execution, OCREvidence and grounding chain |

Live recognized wording was observed only to confirm non-empty provider output and valid evidence. It is not a semantic accuracy baseline or SLA.

## Platform qualification

- **Linux x86_64:** primary production-security candidate, but this macOS run cannot exercise deployment cgroup v2/hard-isolation enforcement. Status: `DEPLOYMENT ENVIRONMENT VALIDATION REQUIRED`.
- **macOS x86_64:** actual API, worker, PDFium, Pillow and live Tesseract qualification passed. Status: `DEVELOPMENT / API QUALIFIED`; not production-security approved.
- **Windows x86-64 / ARM64:** no Phase 15.6 runtime qualification performed. Status: `PACKAGE COMPATIBLE / PRODUCTION SECURITY NOT QUALIFIED`.

## Security and supply chain review

Review date: 2026-09-09. NVD's current PDFium query includes high-severity `CVE-2026-87585`, affecting PDFium on Windows before Chromium/PDFium `153.0.8010.36`. The approved engine is `153.0.7999.0`; therefore Windows production qualification is blocked by scope and remains explicitly unapproved. The NVD description is Windows-specific, so this finding does not establish impact on the Linux production candidate or macOS development qualification. It must be re-evaluated before any Windows adoption or public release.

NVD records returned for Pillow `12.3.0` describe issues fixed in 12.3.0, including decompression, memory-safety and WindowsViewer command handling fixes. Phase 15.3 admits only PNG/JPEG/single-frame TIFF inside its restricted worker and does not use Pillow viewer, font, EPS, GD, TGA, JPEG2000, PDF or ImageCms paths. No current NVD result was returned for the exact Tesseract `5.5.2` query. These lookups are time-sensitive observations, not a permanent no-vulnerability claim.

The exact pypdfium2 pin, six-platform wheel hash allowlist, wheel-only/no-sdist policy, bundled PDFium identity, THIRD_PARTY_NOTICES/license bundle and SBOM remain intact. No PyMuPDF dependency, network test, mutable model download, new parser, shell execution or credential path was added.

## Release readiness

Result: **RELEASE READY WITH DOCUMENTED PLATFORM LIMITATIONS**.

Phase 15 engineering and contract qualification are complete. A production release still requires deployment-environment Linux hard-isolation validation plus a fresh security/dependency/license/SBOM review. This report creates no version bump, tag, package publication or GitHub Release. OCR JSON schemas remain DEFERRED.
