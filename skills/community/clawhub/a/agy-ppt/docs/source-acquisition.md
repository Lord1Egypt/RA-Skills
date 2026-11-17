# Remote Source Acquisition（Phase 13.5）

本文件描述 Phase 13.5 建立的 **bounded public HTTP/HTTPS source acquisition**：
明確取得一個公開 URL 的位元組，落地成 repository 之外的本機 payload，再交給既有的
Phase 13 extraction。

## 1. 架構位置與邊界

```text
明確指定的公開 URL
  → 驗證 + bounded acquisition          ← 本文件（Phase 13.5）
  → 不可變的下載位元組
  → source digest（Phase 12 authority）
  → repository 外部的本機 payload
  → source_ingestion.ingest_source()    ← Phase 13.1–13.4
  → normalized extraction blocks
  → AGY semantic segmentation
  → Phase 12 grounding
```

兩層邊界嚴格分開：

```text
acquisition ≠ extraction
extraction  ≠ semantic understanding
```

Acquisition 只負責網路行為：它**不解析** payload、**不判斷**格式、**不做**任何語意
判斷。格式判定完全留在 `source_ingestion.py`，語意決策完全留在 AGY。

| 檔案 | 角色 |
| --- | --- |
| `skills/agy-ppt/scripts/source_acquisition.py` | 核心模組，唯一的網路實作 |
| `skills/agy-ppt/scripts/acquire_source.py` | 薄 CLI adapter，完全委派給核心模組 |

## 2. 使用方式

```python
from source_acquisition import acquire_remote_source, acquire_and_ingest

acquisition = acquire_remote_source(
    "https://example.org/source.pdf", "src_example", "/path/to/workspace"
)

acquisition, extraction = acquire_and_ingest(
    "https://example.org/source.pdf", "src_example", "/path/to/workspace"
)
```

CLI：

```bash
python3 skills/agy-ppt/scripts/acquire_source.py \
    --url https://example.org/source.pdf \
    --source-id src_example \
    --output-dir /path/to/workspace

# 取得後直接接上既有 extraction
python3 skills/agy-ppt/scripts/acquire_source.py \
    --url https://example.org/notes.md \
    --source-id src_notes \
    --output-dir /path/to/workspace \
    --ingest
```

CLI 只輸出 provenance metadata，**不會**把來源內容印到終端機。

## 3. 適用範圍

Phase 13.5 是為了**明確、公開、未認證**的來源而設計。

支援的 scheme：

```text
https   （文件建議優先使用）
http
```

一次處理**一個**明確指定的 URL。

### 明確不做的事

```text
crawler / 遞迴連結追蹤
site mirroring
搜尋引擎
browser rendering
JavaScript 執行
CSS 排版
需認證網站
cookies / login session / OAuth / API token
form submission
robots 自動化
遠端 iframe 載入
遠端 asset 載入
OCR
```

取得 HTML 之後仍然完全套用 Phase 13.4 的 network-free extraction 規則：extractor
不會再抓取任何一個額外 URL。

## 4. 安全邊界（請務實閱讀）

Phase 13.5 是 **user-run CLI guardrail**，用來取得操作者刻意選定的來源。它阻擋常見
的危險情境：

| 防護 | 行為 |
| --- | --- |
| Scheme | 只允許 `http`/`https`；`file:`、`ftp:`、`data:`、`javascript:`、`blob:`、`ssh:` 等一律拒絕 |
| URL 內嵌帳密 | 拒絕，且錯誤訊息不回吐帳密內容 |
| 本機別名 | 拒絕 `localhost`、`*.localhost` 等 |
| 目的位址 | 解析 hostname 後檢查**所有**回傳位址，任一為 loopback／private／link-local／multicast／unspecified／reserved 即整體拒絕（fail closed） |
| IPv4-mapped IPv6 | `::ffff:127.0.0.1` 會先解包再分類，不會被繞過 |
| 雲端 metadata | `169.254.169.254` 屬 link-local，已被上述規則涵蓋 |
| Redirect | **每一跳**都重新驗證 scheme、帳密、hostname 與解析位址 |
| Redirect 上限 | 預設 5 跳，超過即 deterministic 失敗，不會無限跟隨 |
| TLS | 使用 urllib 預設 context，正常驗證憑證與 hostname；**沒有**任何停用驗證的選項 |
| Ambient 憑證 | 不使用 browser cookie、`.netrc`、雲端憑證、`Authorization` header 或任何 token |
| Ambient proxy | 不安裝 `ProxyHandler`，因此 `http_proxy`／`https_proxy` 不會靜默改變路由 |
| 本機協定 handler | opener 只安裝 HTTP/HTTPS handler，刻意**不安裝** `FileHandler`、`FTPHandler`、`DataHandler` |

### 誠實的限制

# 這不是 hardened multi-tenant SSRF sandbox。

Host 驗證會解析 hostname 並檢查每一個回傳位址，但接下來的 HTTP 連線會**自行再解析
一次**。因此一個惡意 DNS 伺服器若在這兩次查詢之間回覆不同答案，仍可能把連線導向別處。
這個 **DNS-rebinding / TOCTOU** 空窗是真實存在的殘餘風險，本文件選擇明確記載而不是
粉飾。

實作**沒有**把已驗證的位址 pin 住再連線。

因此：不要把這個模組放在網頁服務後面接受不受信任的 URL 輸入，並假設它是安全的。
它的定位是「操作者自己選定來源時的護欄」，不是「任意惡意 URL 的沙箱」。

## 5. 取得限制

| 項目 | 預設值 |
| --- | --- |
| Redirect 上限 | 5 |
| Response 大小上限 | 25 MiB |
| Timeout（connect 與每次 read） | 30 秒 |
| HTTP method | 只有 `GET` |

大小上限會**雙重**強制：

1. 若 `Content-Length` 超過上限，在下載前就拒絕。
2. `Content-Length` 只是參考值，可能缺少、可能不實、可能是 chunked，所以串流過程中
   累計位元組數同樣受同一上限限制，超過即中止。

Response body 以 64 KiB 逐塊讀取，**不會**一次 `read()` 進記憶體。

HEAD 不被用來當作「資源可下載」的證明；只有實際的 `GET` 才算。

## 6. HTTP 狀態與內容

非成功的最終回應會明確失敗，並與 parser 失敗清楚分離。至少可分辨 `404`、`403`、
`5xx`。HTTP 錯誤頁**絕不會**被當成請求到的來源送進 extraction——失敗時連 payload 檔
都不會留下。

### Content-Encoding

請求時送出 `Accept-Encoding: identity`，讓儲存的位元組就是來源實體本身。

若伺服器仍回傳不支援的 `Content-Encoding`（例如 `gzip`），會以
`REMOTE_CONTENT_ENCODING_UNSUPPORTED` 明確失敗，而不是存下語意模糊的位元組。

### Content-Type

伺服器宣告的 `Content-Type` 只作為 **metadata 記錄**。

# Content-Type 是參考值，不是格式權威。

格式判定仍然完全由既有的 Phase 13 detection 決定。因此一個宣告
`application/pdf` 但內容其實是 HTML 的回應，**不會**因為 header 這樣寫就被當成 PDF。

## 7. Payload 檔名與寫入安全

`Content-Disposition` 的 filename 與 URL basename **都不被信任**，也**不會**用來組成
檔案路徑——這兩者都是攻擊者可控，是路徑穿越的典型入口。

Payload 檔名只由下列可信輸入產生：

```text
已驗證的 source_id  +  allowlist 內的 suffix
```

suffix 取自 URL 路徑副檔名（限 allowlist）或 `Content-Type` 對照表，兩者都沒有時為
`.bin`。另外會再確認最終路徑確實位於呼叫者提供的 output directory 之內。

`Content-Disposition` 可以被記錄成 metadata，但永遠不決定位元組落在哪裡。

### Atomic 寫入

下載先寫入 `<payload>.part`，只有在狀態碼、大小與 digest 全部確認之後，才 atomic
rename 成最終 payload。任何失敗（大小超限、timeout、中斷）都會刪除 partial 檔，
**不會**留下看起來成功的截斷檔案。

## 8. 不修改來源位元組

Acquisition **不會**在計算 digest 前修改任何位元組：

```text
沒有換行轉換
沒有字元編碼正規化
沒有額外解壓縮
```

## 9. Source digest

直接沿用 Phase 12 的 `compute_source_digest()`，全專案只有一個 canonical fingerprint
定義：

```text
source fingerprint = SHA-256 of acquired source bytes
```

本模組**不引入** URL hash、ETag hash、normalized HTTP digest 或 DOM digest 之類的
競爭性 fingerprint。

## 10. Provenance

`AcquisitionResult` 記錄：

```text
schema_version
source_id
requested_url
final_url            （redirect 後的最終 URL）
content_type         （伺服器宣告，參考值）
declared_content_length
downloaded_bytes
source_digest
local_payload_path
redirect_count
retrieved_at
content_disposition  （metadata，不影響路徑）
```

`retrieved_at` 只供稽核。它**不影響**：

```text
source digest
block IDs
source IDs
semantic identity
```

同一份來源在不同時間取得兩次，digest 與 block ID 完全相同。

## 11. Payload 存放位置

Phase 13.5 **不**引入新的隱性永久下載快取。

Payload 一律寫入呼叫者指定的 output directory，應放在 repository 之外（例如簡報
workspace 或暫存目錄）。不會在 Git repository 底下留下任何來源複本。快取如有需要
可作為未來能力。

## 12. Error taxonomy

| Error code | 意義 |
| --- | --- |
| `REMOTE_URL_INVALID` | URL 無法解析、缺少 host，或 `source_id` 不合法 |
| `REMOTE_SCHEME_UNSUPPORTED` | 不是 `http`/`https` |
| `REMOTE_CREDENTIALS_UNSUPPORTED` | URL 內嵌帳密 |
| `REMOTE_HOST_BLOCKED` | 本機別名，或解析到非公開位址 |
| `REMOTE_REDIRECT_BLOCKED` | Redirect 目標未通過重新驗證 |
| `REMOTE_TOO_MANY_REDIRECTS` | 超過 redirect 上限 |
| `REMOTE_HTTP_ERROR` | 最終回應非 2xx |
| `REMOTE_TIMEOUT` | 連線或讀取逾時 |
| `REMOTE_RESPONSE_TOO_LARGE` | 超過大小上限（宣告值或串流實際值） |
| `REMOTE_CONTENT_ENCODING_UNSUPPORTED` | 伺服器回傳不支援的 transport 壓縮 |
| `REMOTE_TLS_FAILED` | TLS 驗證失敗 |
| `REMOTE_ACQUISITION_FAILED` | 其他網路失敗 |

這組 code 與 Phase 13 extraction code、Phase 12 grounding code、image-worker code
刻意不重疊。

## 13. 取得後的 extraction

取得完成後的 payload 走既有 detection，因此 Phase 13.5 之後可從遠端取得的來源是：

```text
PDF（具文字層）
Markdown
純文字
DOCX
靜態 HTML
```

Phase 13.5 **沒有**新增任何 parser 格式。

若遠端 body 是圖片、非 DOCX 的 ZIP、影片或未知二進位，acquisition 本身可能成功，
但 extraction 會回傳既有的 `SOURCE_FORMAT_UNSUPPORTED`。HTTP 成功**不代表**語意上
支援該格式。

## 14. Phase 12 handoff

正確邊界不變：

```text
acquisition metadata + 本機 payload
  → extraction blocks
  → AGY semantic segmentation
  → Phase 12 source inventory units
```

Acquisition **不會**建立 semantic source unit，也**不會**指派 `HIGH`／`MEDIUM`／`LOW`
或 support status。

Phase 12 是 **COMPLETE / FROZEN**：Phase 13.5 沒有、也不需要修改 Phase 12 的任何
契約或 schema。若 Phase 12 source inventory 已支援 source URL metadata，handoff 可以
提供；若沒有，acquisition metadata 就留在 Phase 13 側，**不會**為了塞入新的 URL 欄位
而改動 frozen schema。也不會把來源全文複製進 Phase 12 grounding sidecar。

## 15. 測試方式

Deterministic 單元測試會注入 HTTP transport 與 DNS resolver，因此一般測試套件
**不依賴**網路或 DNS 可用性，也不會連到任何真實主機。

另外有一個 **opt-in** 的 bounded live 驗證：

```bash
AGY_PPT_LIVE_REMOTE=1 \
    python3 skills/agy-ppt/tests/integration/test_remote_acquisition_live.py
```

範圍刻意限制為：一個來源、一次取得、一次 extraction。它取得 RFC 2119
（小型、穩定、公開、非機密），比對已 pin 住的 SHA-256，通過既有純文字 extraction，
確認沒有取得任何額外資源，並在結束後刪除暫存 payload。不消耗 AI 訂閱額度、不呼叫
Codex 或 Kiro、不使用 API fallback、不做 crawling 或輪詢。

網路不可用屬環境狀況，不是 production bug；該情形會如實回報，不會偽造成 PASS。

## 16. 已知限制

- 不支援需認證／私有網站、cookies、login session、OAuth、API token。
- 不支援 crawler、遞迴連結追蹤或 site mirroring。
- 不支援 browser rendering 與 JavaScript，因此 JS 產生的內容不會被取得。
- 不會遞迴抓取 HTML 內的 asset、iframe 或連結。
- 不支援 OCR；掃描影像 PDF 仍不支援。
- 不支援明確的 proxy 設定（ambient proxy 已刻意停用）。
- **不是** hardened multi-tenant SSRF sandbox；存在 DNS-rebinding / TOCTOU 殘餘風險
  （見第 4 節）。
- Extraction 不等於 semantic segmentation；AGY 仍是 semantic authority。
