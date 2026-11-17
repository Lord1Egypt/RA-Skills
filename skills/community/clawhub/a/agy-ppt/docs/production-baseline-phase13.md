# agy-ppt Phase 13 Production Baseline

本文件是 Phase 13（Source Ingestion & Acquisition）的 production capability 摘要，
供 release 判斷與後續開發參照。它**不**重複實作細節：

- Extraction 細節見 [`source-ingestion.md`](source-ingestion.md)
- Acquisition 細節見 [`source-acquisition.md`](source-acquisition.md)
- Grounding 細節見 [`source-grounding.md`](source-grounding.md)

## 1. Phase 13 範圍

| Sub-phase | 內容 | PR |
| --- | --- | --- |
| 13.1 | Ingestion contract：normalized block／locator 契約、stable ID、error taxonomy | [#3](https://github.com/sujunmin/agy-ppt/pull/3) |
| 13.2 | PDF（具文字層）／Markdown／純文字 extraction | [#3](https://github.com/sujunmin/agy-ppt/pull/3) |
| 13.3 | DOCX extraction | [#4](https://github.com/sujunmin/agy-ppt/pull/4) |
| 13.4 | 本機靜態 HTML extraction | [#5](https://github.com/sujunmin/agy-ppt/pull/5) |
| 13.5 | 公開 HTTP/HTTPS source acquisition | [#6](https://github.com/sujunmin/agy-ppt/pull/6) |

Phase 13 是 Phase 12 grounding 的**上游生產者**，不是它的替代品。

## 2. 架構

```text
明確指定的來源
  → （選用）Phase 13.5 acquisition        source_acquisition.py
  → 不可變的本機 payload
  → deterministic format detection        source_ingestion.py
  → deterministic extraction
  → normalized blocks + locators
  → AGY semantic segmentation             ← AGY，非本層
  → Phase 12 source grounding             ← frozen
```

三個層級的責任嚴格分離：

```text
acquisition ≠ extraction
extraction  ≠ semantic understanding
```

| 模組 | 擁有 |
| --- | --- |
| `scripts/source_acquisition.py` | HTTP/HTTPS、redirect、SSRF 護欄、bounded download、provenance、本機 payload |
| `scripts/source_ingestion.py` | format detection、五種格式 extraction、normalized blocks、locators |
| `scripts/acquire_source.py` / `scripts/ingest_source.py` | 薄 CLI adapter，完全委派 |

Acquisition 內**沒有** parser 邏輯；ingestion 內**沒有**網路邏輯。兩者皆已驗證。

## 3. 支援的來源

| 來源 | Acquisition | Extraction | Semantic layer |
| --- | --- | --- | --- |
| 本機 PDF（具文字層） | local | 支援 | AGY |
| 本機 Markdown | local | 支援 | AGY |
| 本機純文字 | local | 支援 | AGY |
| 本機 DOCX | local | 支援 | AGY |
| 本機靜態 HTML | local | 支援 | AGY |
| 公開遠端 PDF | HTTP/HTTPS | 下載後支援 | AGY |
| 公開遠端 Markdown | HTTP/HTTPS | 下載後支援 | AGY |
| 公開遠端純文字 | HTTP/HTTPS | 下載後支援 | AGY |
| 公開遠端 DOCX | HTTP/HTTPS | 下載後支援 | AGY |
| 公開遠端靜態 HTML | HTTP/HTTPS | 下載後支援 | AGY |

同一份位元組不論來自本機或遠端，都會產生**相同的 digest、block ID、locator 與順序**。

## 4. 不支援

```text
OCR / 掃描或純影像 PDF
HTML browser rendering
JavaScript 產生的內容
CSS 可見性／版面重建
crawler / site mirroring / 遞迴 asset 抓取
需認證或私有來源、cookies、session login、OAuth、API token
PowerPoint ingestion
spreadsheet ingestion
明確的 proxy 設定
```

## 5. Locator 契約摘要

所有 human-facing 索引皆為 **1-based**，且全部使用 frozen Phase 12 的 locator kind，
因此 handoff 不需任何轉換。

| 格式 | Phase 12 kind | 結構欄位 |
| --- | --- | --- |
| PDF | `page` | `start` / `end`（頁碼，1-based，無 off-by-one） |
| Markdown | `section` | `heading_path`、`start_line` / `end_line` |
| 純文字 | `line_range` | `start` / `end`（行號） |
| DOCX | `section` | `heading_path`、`start_element` / `end_element`、`table_index`、`start_row` / `end_row` |
| HTML | `section` | `heading_path`、`start_element` / `end_element`、`list_index`、`table_index`、`start_row` / `end_row` |

DOCX 與 HTML 皆為 flow-based，**不提供也不虛構** rendered 頁碼、螢幕位置或捲動位移。

Locator 不外露 parser 內部 node index、0-based 頁碼、絕對檔案路徑或暫存目錄身分。

## 6. Digest authority

全專案只有一個 source fingerprint 定義：

```text
原始來源位元組 → source_grounding.compute_source_digest() → SHA-256
```

Acquisition 與 ingestion 都委派給它。**沒有**競爭性的 URL hash、DOM hash、
DOCX XML hash、normalized text hash 或 ETag hash 被當成 Phase 12 source identity。

Block ID 由 `(source_id, locator, ordinal)` deterministic 推導，與檔案位置、
輸出目錄、process ID、timestamp 無關。`retrieved_at` 只供稽核，不影響任何 ID。

## 7. Extractor version

```text
extractor_version = "1"
```

與 release version 及 Git tag 無關；extraction 行為改變時才遞增。

## 8. 安全邊界

### Extraction

HTML extraction 為 network-free：不執行 JavaScript、不使用 browser、不套用 CSS、
不下載任何遠端或本機參照資源、不追蹤超連結、不抓取 iframe。已下載的遠端 HTML 仍由
同一個 network-free extractor 解析。

### Acquisition

| 護欄 | 行為 |
| --- | --- |
| Scheme | 只允許 `http`/`https` |
| URL 帳密 | 拒絕，錯誤訊息不回吐 |
| 目的位址 | 解析後檢查**所有**位址；任一為 loopback／private／link-local／multicast／unspecified／reserved 即整體拒絕 |
| IPv4-mapped IPv6 | 先解包再分類 |
| Redirect | 每一跳重新驗證 scheme／帳密／hostname／位址；上限 5 |
| 大小 | 上限 25 MiB，`Content-Length` 與串流計數雙重強制 |
| Timeout | 30 秒（connect 與每次 read） |
| Method | 只有 `GET` |
| TLS | 正常驗證，無停用選項 |
| Ambient 憑證 | 不使用 cookie、`.netrc`、雲端憑證、`Authorization`、token |
| Ambient proxy | 不安裝 `ProxyHandler` |
| 協定 handler | 只安裝 HTTP/HTTPS，刻意不安裝 `FileHandler`／`FTPHandler`／`DataHandler` |
| 寫入 | atomic rename，失敗清除 partial |
| Payload 位置 | 呼叫者指定，repository 之外，無隱性永久快取 |

### 誠實的限制

# 這不是 hardened multi-tenant SSRF sandbox。

Hostname 會在連線前驗證，但**已驗證的 IP 沒有被 pin 到後續 HTTP 連線**，該連線會自行
再解析一次。因此存在 **DNS-rebinding / TOCTOU** 空窗。

定位是「操作者自行選定來源時的 CLI 護欄」，不適合放在網頁服務後面接受不受信任的 URL。

## 9. Error taxonomy

三組 error code namespace 完全不重疊（已驗證）：

| 層 | Codes |
| --- | --- |
| Extraction | `SOURCE_FORMAT_UNSUPPORTED`、`SOURCE_FILE_NOT_FOUND`、`SOURCE_READ_FAILED`、`SOURCE_ENCODING_UNSUPPORTED`、`SOURCE_TEXT_UNAVAILABLE`、`SOURCE_EXTRACTION_FAILED` |
| Acquisition | `REMOTE_URL_INVALID`、`REMOTE_SCHEME_UNSUPPORTED`、`REMOTE_CREDENTIALS_UNSUPPORTED`、`REMOTE_HOST_BLOCKED`、`REMOTE_REDIRECT_BLOCKED`、`REMOTE_TOO_MANY_REDIRECTS`、`REMOTE_HTTP_ERROR`、`REMOTE_TIMEOUT`、`REMOTE_RESPONSE_TOO_LARGE`、`REMOTE_CONTENT_ENCODING_UNSUPPORTED`、`REMOTE_TLS_FAILED`、`REMOTE_ACQUISITION_FAILED` |
| Grounding（frozen） | `SOURCE_INVENTORY_INVALID`、`TRACEABILITY_INVALID`、`SOURCE_REFERENCE_MISSING`、`SOURCE_COVERAGE_INCOMPLETE`、`GROUNDED_QA_INCOMPLETE`、`SOURCE_CHANGED` |

關鍵語意分離：

- 結構有效但無可擷取文字 → `SOURCE_TEXT_UNAVAILABLE`
- 結構損毀 → `SOURCE_EXTRACTION_FAILED`
- HTTP 成功但格式不支援 → 仍是 `SOURCE_FORMAT_UNSUPPORTED`（HTTP 成功不代表語意支援）
- HTTP 錯誤頁**絕不**進入 extraction；失敗時不留 payload

## 10. Runtime 依賴

Phase 13 新增的宣告依賴：

| 套件 | 最低版本 | License | 狀態 | 理由 |
| --- | --- | --- | --- | --- |
| `pypdf` | `>=4.2.0` | BSD-3-Clause | 新增直接依賴 | PDF 文字擷取；無必要 runtime 相依 |
| `python-docx` | `>=1.1.0` | MIT | 新增直接依賴 | DOCX 結構擷取；相依 `lxml`／`typing_extensions` 已由 `python-pptx` 引入 |
| `lxml` | `>=4.9.0` | BSD-3-Clause | 由 transitive 提升為明確宣告 | 靜態 HTML 解析，可停用網路存取 |

三者授權皆與本專案 MIT 相容。Acquisition 只使用標準庫，未新增依賴。

## 11. AGY 權責

Phase 13 只做**結構性**擷取：頁、heading、行號、段落、清單、表格、格式 metadata。

它**不**決定：

```text
什麼重要
哪個 section 是 HIGH priority
claim 的語意
來源是否支持某個 claim
哪些內容該進投影片
semantic coverage
semantic segmentation
```

這些全部仍屬 AGY。Extracted block **不是** Phase 12 semantic source unit；Phase 13
不會自動升級 block，也不會寫出任何 Phase 12 artifact，更不會指派
`HIGH`／`MEDIUM`／`LOW` 或 support status。

Worker routing 不變：`AGY → worker → AGY`，禁止 worker 互相串接。

## 12. Phase 12 相容性

Phase 12 為 **COMPLETE / FROZEN**。Phase 13 全程未修改
`source_grounding.py`、`validate_source_grounding.py`、四個 Phase 12 schema、
Phase 12 grounding tests、`project_state.py`、`assemble_ppt.py`、Codex adapter 或
Kiro bridge，也未觸發任何 `PHASE_12_COMPATIBILITY_CHANGE_REQUIRED`。

五種格式的 locator 皆通過 frozen `validate_locator()` 並被 `SourceInventory.add_unit()`
接受。

## 13. 驗證證據

- Deterministic 測試不消耗 AI 訂閱額度、不呼叫 Codex 或 Kiro、不使用 API fallback。
- Acquisition 的 deterministic 測試會注入 HTTP transport 與 DNS resolver，因此一般
  測試套件**不依賴**網路或 DNS 可用性。
- 另有一個 **opt-in** 的 bounded live 驗證（一個來源、一次取得、一次 extraction）：

  ```bash
  AGY_PPT_LIVE_REMOTE=1 \
      python3 skills/agy-ppt/tests/integration/test_remote_acquisition_live.py
  ```

  它取得 RFC 2119（`https://www.rfc-editor.org/rfc/rfc2119.txt`，小型、穩定、公開、
  非機密），比對已 pin 住的 SHA-256
  `3c2ceb7bfc84cd34720f4a5271338ab9d8280d34bdd1eb250c64306202f2ed8b`，通過既有純文字
  extraction，並在結束後刪除暫存 payload。

下載的來源內容、runtime payload 與 grounding sidecar 一律**不進 repository**。

本文件刻意不記錄測試數量：實際數字應以每次 release gate 的執行結果為準，不應以文件
中的舊數字冒充。

## 14. 已知限制

- 不支援 OCR；掃描／純影像 PDF 不支援。
- 不支援需認證或私有遠端來源。
- 不支援 crawler、site mirroring 或遞迴資源抓取。
- 不支援 browser／JavaScript rendering；JS 產生的內容不會被擷取。
- 遠端取得存在 DNS-rebinding / TOCTOU 殘餘風險（見第 8 節）。
- PDF granularity 為 page 層級，不做版面語意重建。
- DOCX 無 rendered 頁碼；headers／footers／footnotes／endnotes／comments／
  tracked-change 語意／內嵌圖片文字皆不擷取；heading 僅依內建 style 判定，
  自訂或本地化樣式名稱會被視為普通段落。
- HTML 不重建 CSS 版面；只有 `h1`–`h6`、`p`、`ul`、`ol`、`table` 會成為 block，
  裸 `div`／`span` 中的文字不會被擷取；表格不展開 `rowspan`／`colspan`；
  `noscript`、JSON-LD 與 `<title>` 不擷取。
- 純文字只做空行切分，不做 semantic chunking。
- Extraction 不等於 semantic segmentation；AGY 仍是 semantic authority。
