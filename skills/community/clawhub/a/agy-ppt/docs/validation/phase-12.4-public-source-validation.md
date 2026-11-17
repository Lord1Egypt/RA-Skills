# Phase 12.4 Public Source Validation

本文件記錄 Phase 12 source-grounding 實作對 **真實公開來源** 執行的驗證結果。

驗證使用公開、非機密文件。所有 runtime 產物（下載的來源檔、grounding sidecar
JSON、validation workspace）都 **未** 進入 repository；本文件只保存 metadata、
hash、計數與結果。

## 1. 驗證基本資料

| 項目 | 值 |
| --- | --- |
| 驗證日期 | 2026-09-04 |
| 來源取得時間（UTC） | 2026-09-04T00:47:13Z |
| 受測 agy-ppt commit | `59b999ce426e56476d2a70bfd123fc649d7c657c` |
| 驗證期間是否修改 production code | 否 |
| 是否呼叫真實 Codex 圖片生成 | 否 |
| 是否使用 API fallback | 否 |

Phase 12 production 實作在本次驗證期間完全未變動，因此本報告的結論適用於上述
commit 及其後僅含文件變更的 commit。

## 2. 驗證來源

### Test A

| 項目 | 值 |
| --- | --- |
| 文件 | NIST AI 100-1, Artificial Intelligence Risk Management Framework (AI RMF 1.0) |
| 官方 URL | `https://nvlpubs.nist.gov/nistpubs/ai/nist.ai.100-1.pdf` |
| 發布 | 2023 年 1 月 |
| 位元組大小 | 1,946,127 |
| SHA-256 | `7576edb531d9848825814ee88e28b1795d3a84b435b4b797d3670eafdc4a89f1` |
| HTTP 狀態 | 200 |

### Test B

| 項目 | 值 |
| --- | --- |
| 文件 | RFC 2119, Key words for use in RFCs to Indicate Requirement Levels（BCP 14） |
| 官方 URL | `https://www.rfc-editor.org/rfc/rfc2119.txt` |
| 發布 | 1997 年 3 月 |
| 位元組大小 | 4,723 |
| SHA-256 | `3c2ceb7bfc84cd34720f4a5271338ab9d8280d34bdd1eb250c64306202f2ed8b` |
| HTTP 狀態 | 200 |

兩個 workspace 完全獨立，不共用 `project_id`、`source_id` 或任何 artifact。

> PDF 文字擷取使用作業系統既有的 `pdftotext`。agy-ppt **沒有** 內建任何
> PDF/DOCX/HTML parser，這一點在本次驗證中沒有改變。

## 3. Test A — NIST AI RMF 1.0

Validation scenario：以 AI／技術治理領導層為對象的 7 頁 executive briefing。
不產生任何 slide 圖片。

| 指標 | 值 |
| --- | --- |
| sources | 1 |
| source units | 19 |
| HIGH | 10 |
| MEDIUM | 6 |
| LOW | 3 |
| planned slides | 7 |
| claims | 19 |
| coverage entries | 19 |

Coverage 結果：

| coverage_status | 數量 |
| --- | --- |
| covered | 13 |
| speaker_notes_only | 2 |
| intentionally_omitted | 3（皆有 `omission_reason`） |
| not_applicable | 1 |
| unaccounted | 0 |
| HIGH unaccounted | 0 |

Support 結果：`supported` 19、`unsupported` 0、`pending_review` 0。

最終 assembly gate：`ready=true`，exit code 0。

## 4. Test B — RFC 2119

Validation scenario：4 頁 requirement-level 說明。

| 指標 | 值 |
| --- | --- |
| sources | 1 |
| source units | 10 |
| HIGH | 6 |
| MEDIUM | 2 |
| LOW | 2 |
| planned slides | 4 |
| claims | 10 |
| unaccounted | 0 |

Modal evidence 實際驗證的 modality（`comparison_status="match"`）：

| Modality | 結果 |
| --- | --- |
| MUST | PASS |
| MUST NOT | PASS |
| SHOULD | PASS |
| SHOULD NOT | PASS |
| MAY | PASS |

最終 assembly gate：`ready=true`，exit code 0。

## 5. Negative challenge 結果

所有 challenge 都是 validation-only 構造，不屬於任何最終 deck。

### 5.1 Unsupported claim gate（Test A）

在 Test A 注入一個來源不支持的合成 claim（聲稱 AI RMF 1.0 強制每年第三方演算法
稽核——實際上該框架為自願性且未規定稽核頻率）。

| 階段 | 結果 |
| --- | --- |
| 注入後 gate | FAIL，exit code 1 |
| error codes | `TRACEABILITY_INVALID`, `GROUNDED_QA_INCOMPLETE` |
| 錯誤摘要 | claim 仍為 `pending_review`/`unsupported` 未解決；AGY QA outcome 為 `failed` |
| 移除該 claim 後 gate | PASS，exit code 0 |

### 5.2 HIGH-priority coverage gap（Test A）

將一個真實的 HIGH priority source unit（§5.1 Govern）暫時設為 `unaccounted`。

| 階段 | 結果 |
| --- | --- |
| 注入後 gate | FAIL，exit code 1 |
| error codes | `SOURCE_COVERAGE_INCOMPLETE`, `GROUNDED_QA_INCOMPLETE` |
| 錯誤摘要 | 明確列出該 HIGH unit id 為 unaccounted |
| 修復後 gate | PASS，exit code 0 |

HIGH priority source unit 無法在 coverage accounting 中無聲消失。

### 5.3 Modal mismatch（Test B）

注入一個 claim，將來源的 MAY（"truly optional"）誤述為 MUST。

| 階段 | 結果 |
| --- | --- |
| `modal_evidence.comparison_status` | `mismatch` |
| AGY semantic QA | `failed`，並在 `semantic_findings.modal_findings` 留下紀錄 |
| gate | FAIL，exit code 1 |
| error codes | `TRACEABILITY_INVALID`, `GROUNDED_QA_INCOMPLETE` |
| 修復後 gate | PASS，exit code 0 |

未解決的 modal mismatch 無法通過 gate。

## 6. Resume 驗證

流程：persist artifacts → 模擬 process 結束 → 從磁碟重新載入 → 以相同來源與
相同 `(source_id, locator)`、`(slide_id, sequence)` 輸入重新套用。

| 檢查項 | 結果 |
| --- | --- |
| source unit ID drift | 0 |
| claim ID drift | 0 |
| duplicate source units | 0 |
| duplicate claims | 0 |
| duplicate coverage entries | 0 |
| 遺失的 support 決策 | 0 |
| 遺失的 coverage 決策 | 0 |
| resume 後 gate | `ready=true` |

計數在 resume 前後一致：units 19 / claims 19 / coverage 19。

## 7. Source-change 驗證

官方來源檔本身未被修改；驗證使用一份臨時修改副本。

| 項目 | 值 |
| --- | --- |
| 原始 SHA-256 | `7576edb531d9848825814ee88e28b1795d3a84b435b4b797d3670eafdc4a89f1` |
| 修改副本 SHA-256 | `8ef34396204aa6c67380368de9c5e9088a329458dac427957a583ef0a86add51` |
| `SOURCE_CHANGED` 偵測 | YES |
| error code | `SOURCE_CHANGED` |
| gate exit code | 1 |
| 沿用 stale evidence | NO |
| assembly ready | NO |
| 對照組（未變更 digest） | PASS，exit code 0 |
| 驗證後官方來源檔 hash | 未變更 |

## 8. 語意稽核結果

除了 deterministic validator 之外，另外對每一條 claim 與每一筆 coverage entry
做語意稽核。稽核方式為可重現的機制檢查：每條 claim 的證據關鍵語句必須真的出現在
hash 固定的來源文字中（比對前正規化空白與 pdftotext 斷字），且其 locator 必須指向
真實存在的 source unit、support 決策與 `evidence_note` 必須存在。

| 稽核 | 結果 |
| --- | --- |
| Claim traceability（Test A 19 + Test B 10） | 29/29 PASS |
| Source coverage（Test A 19 + Test B 10） | 29/29 PASS |

## 9. Deterministic regression

在同一 commit 上重跑：

| Suite | 結果 |
| --- | --- |
| Phase 12 source-grounding tests | 33/33 PASS |
| Phase 12.3 workflow integration tests | 32/32 PASS |
| Full unit suite | 454/454 PASS |
| Dependency resolver tests | 20/20 PASS |
| Deterministic recovery scenarios | 10/10 PASS |
| Recovery tests | 95/95 PASS |

## 10. Production bug

本次驗證 **未** 發現 production bug。Phase 12 production code 未被修改。

驗證期間唯一修正的缺陷位於一次性的驗證稽核腳本（布林轉換錯誤），該腳本不屬於
repository。

## 11. Reproducibility statement

Validation sources were public and non-confidential.
Runtime source files and grounding sidecars were not committed.
The report records the source URLs, source fingerprints, test commit, and
validation outcomes.

本次 grounding evidence 是為驗證而建立的 validation fixture。其可稽核性來自本文件
記錄的 source URL、SHA-256 與 section locator：任何人都可以自行取得同一份
hash 相符的來源文件，並獨立重新驗證上述每一條 claim 的對應關係。

## 12. Limitations

* agy-ppt 未內建通用 PDF/DOCX/HTML parser。本次 PDF 文字擷取依賴作業系統既有工具。
* AGY 仍是 semantic authority：source segmentation、claim support、coverage 判斷與
  numeric/modal 語意判斷都由 AGY 提供，Python 不會自行推導。
* Deterministic validators 不會獨立證明 factual truth。它們只驗證 schema、ID 與
  reference 完整性、coverage accounting、source freshness 與 assembly readiness
  contract。
* Modal 與 numeric 語意解讀由 AGY 提供；validator 只比對已記錄的
  `comparison_status`，不自行判斷 modality 是否等價。
* 本次驗證的計數（19/10 source units、19/10 claims）是 validation scenario 的樣本
  規模，**不是** product performance claim。
