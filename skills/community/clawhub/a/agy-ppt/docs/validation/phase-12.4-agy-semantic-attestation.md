# Phase 12.4 AGY Semantic Attestation

本文件保存 **AGY semantic authority** 對 Phase 12 source grounding 的獨立語意驗證
結果。

本文件不保存 runtime source files、grounding sidecar JSON，也不保存來源文件原文。

## 1. 與 deterministic evidence 的分工

Phase 12.4 的驗證證據刻意分成兩份文件，provenance 不得混用：

| 文件 | 性質 | 由誰負責 |
| --- | --- | --- |
| [`phase-12.4-public-source-validation.md`](phase-12.4-public-source-validation.md) | deterministic / engineering validation evidence | engineering agent |
| 本文件 | AGY semantic authority attestation | AGY |

前者驗證的是 validator 行為：schema、ID/reference integrity、coverage accounting、
source freshness、assembly readiness contract、negative challenge、resume 與
source-change。後者驗證的是語意：source segmentation、claim support、coverage
判斷、以及 modal/numeric 語意解讀。

兩份文件的 source unit 與 claim 計數**不同**，這是預期結果，不是矛盾：AGY 的語意
審查是獨立重新 segmentation，並未沿用 engineering validation run 的 fixture 切法或
其 priority 分類。兩者共同的固定基準是下列 SHA-256 來源指紋。

本文件所記錄的語意判斷由 AGY 提供；engineering agent 只負責如實持久化，未重新推導
或覆寫任何語意結論。

## 2. Test A — NIST AI RMF 1.0

| 項目 | 值 |
| --- | --- |
| Source | NIST AI RMF 1.0 / NIST AI 100-1 |
| URL | `https://nvlpubs.nist.gov/nistpubs/ai/nist.ai.100-1.pdf` |
| SHA-256 | `7576edb531d9848825814ee88e28b1795d3a84b435b4b797d3670eafdc4a89f1` |

AGY semantic validation：

| 指標 | 值 |
| --- | --- |
| source units | 20 |
| planned slides | 7 |
| factual / source-dependent claims | 20 |
| supported final | 20 |
| unsupported unresolved | 0 |
| pending unresolved | 0 |
| semantic claim audit | 20/20 PASS |

## 3. NIST coverage evidence

| Priority | 數量 |
| --- | --- |
| HIGH | 13 |
| MEDIUM | 4 |
| LOW | 3 |

| coverage_status | 數量 |
| --- | --- |
| covered | 17 |
| speaker_notes_only | 1 |
| intentionally_omitted | 1 |
| not_applicable | 1 |
| HIGH unaccounted | 0 |

## 4. Semantic qualification evidence

| 指標 | 值 |
| --- | --- |
| material overstatements | 0 |
| lost qualifications | 0 |
| unsupported extrapolations | 0 |

具體保留的語意限定：

* NIST AI RMF 1.0's voluntary / non-mandatory nature was preserved.
* Risk-tolerance language was not converted into a prescriptive mandate.
* Profiles were represented as context-specific adaptations rather than a rigid
  checklist.

換言之，語意審查特別確認簡報未把「自願性框架」表述為強制規範、未把「組織自行決定
風險容忍度」轉寫成硬性要求、也未把 profile 機制描述成固定檢核表。

## 5. Test B — RFC 2119

| 項目 | 值 |
| --- | --- |
| Source | RFC 2119 |
| URL | `https://www.rfc-editor.org/rfc/rfc2119.txt` |
| SHA-256 | `3c2ceb7bfc84cd34720f4a5271338ab9d8280d34bdd1eb250c64306202f2ed8b` |

Modal 語意結果：

| Modality | 結果 |
| --- | --- |
| MUST | PASS |
| MUST NOT | PASS |
| SHOULD | PASS |
| SHOULD NOT | PASS |
| MAY | PASS |

| 指標 | 值 |
| --- | --- |
| modal semantic audit | 10/10 PASS |

## 6. Modal boundary

以下轉換屬 semantic overstatement：

```text
MAY → MUST
```

RFC 2119 的 MAY／OPTIONAL 表示項目「truly optional」；將其表述為 MUST 會把可選項
提升為絕對要求，屬實質語意誇大。

AGY semantic judgement：

| 項目 | 值 |
| --- | --- |
| `modal_evidence.comparison_status` | `mismatch` |
| Content QA | `failed` |

deterministic gate 隨後依這份已持久化的 AGY 決策阻擋 workflow：gate 不會自行判斷
modality 是否等價，它只是拒絕在未解決的 mismatch 與 `failed` 的 Content QA 之下
繼續進入 assembly。

## 7. Independence statement

```text
AGY performed an independent semantic review of the pinned public sources.

Prior engineering-agent support decisions were not treated as semantic authority.

Kiro did not perform semantic judgement for this attestation.

Codex was not used.
```

## 8. Production boundary

```text
AGY remains semantic authority.

Deterministic validators do not independently prove factual truth.

No bundled universal PDF/DOCX/HTML parser is provided.

Modal and numeric semantic interpretation remains AGY-supplied.
```

## 9. Reproducibility

本文件只保存 metadata、來源 hash、計數、語意結論與簡短描述，不含來源原文的大量
引用、下載檔案或 runtime JSON。

上述兩份來源皆為公開、非機密文件，並以 SHA-256 固定版本。任何審查者都可以自行取得
hash 相符的同一份文件，獨立重做語意審查並與本文件的結論比對。
