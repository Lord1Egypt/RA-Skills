<p align="center">
  <strong>🌐 語言切換：</strong>
  <a href="docs/README.zh.md">中文</a> |
  <a href="docs/README.en.md">English</a> |
  <a href="docs/README.es.md">Español</a> |
  <a href="docs/README.ar.md">العربية</a>
</p>

# Agent PaddleOCR Vision —— 基於 PaddleOCR 的文件理解與agent行動

**將文件轉換為 AI agent 可執行的行動指引。** 本技能僅支援 PaddleOCR 雲端 API，自動分類文件類型並提供結構化的建議參數與提示詞。

## 功能概述

- 使用 PaddleOCR 雲端 API 進行文字辨識（支援表格、公式、多語言）
- 自動分類 15 類文件：發票、名片、收據、表格、合約、身分證、護照、銀行對帳單、駕照、稅表、財務報告、會議記錄、履歷、旅遊行程、一般文件
- 為每類文件生成建議行動（create_expense、add_contact、summarize 等）
- 批次處理整個資料夾
- 產生可搜尋 PDF（根據 bounding box 嵌入文字層，支援文字選取與搜尋）
- 輸出 `extracted_fields` 結構化資料，agent 自行決定如何處理
- API 5xx/timeout 自動重試（指數退避）
- Batch 並行處理（`--workers` 參數）
- CSV 匯出（`--format csv`）
- 美化排版（`--format pretty` 輸出人類可讀格式）

## 安裝步驟

### 系統依賴

Ubuntu/Debian：

```bash
sudo apt-get update
sudo apt-get install -y python3 python3-pip poppler-utils
```

macOS：

```bash
brew install python poppler
```

### Python 套件

```bash
cd skills/agent-paddleocr-vision
pip3 install -r scripts/requirements.txt
```

### PaddleOCR API 設定

必須設定兩個環境變數：

```bash
export PADDLEOCR_DOC_PARSING_API_URL=https://your-api.paddleocr.com/layout-parsing
export PADDLEOCR_ACCESS_TOKEN=your_access_token
```

*注意：API URL 必须以 `/layout-parsing` 结尾。*

## 使用方式

### 單一文件

```bash
# 基本用法：處理圖片或 PDF，輸出 pretty JSON
python3 scripts/doc_vision.py --file-path ./invoice.jpg --pretty

# 同時生成可搜尋 PDF
python3 scripts/doc_vision.py --file-path ./document.pdf --make-searchable-pdf --output result.json

# 只要純文字
python3 scripts/doc_vision.py --file-path ./doc.pdf --format text
```

### 批次處理

```bash
# 處理指定資料夾內所有支援的檔案（.pdf, .png, .jpg, .jpeg, .bmp, .tiff, .webp）
python3 scripts/doc_vision.py --batch-dir ./inbox --output-dir ./out
```

批次結果：
- 會輸出一個總結 JSON（包含總筆數、成功/失敗數、各類型統計）
- 每個檔案都會在 `--output-dir` 產生獨立的 JSON 檔

### Docker

```bash
docker build -t agent-paddleocr-vision:latest .
docker run --rm -v $(pwd)/data:/data \
  -e PADDLEOCR_DOC_PARSING_API_URL -e PADDLEOCR_ACCESS_TOKEN \
  agent-paddleocr-vision:latest \
  --file-path /data/invoice.jpg --pretty --make-searchable-pdf
```

## 輸出格式

```json
{
  "ok": true,
  "document_type": "invoice",
  "confidence": 0.94,
  "text": "完整辨識的文字內容（跨頁以雙換行分隔）",
  "pruned_result": { ...原始 PaddleOCR API 回傳的結構資料... },
  "suggested_actions": [
    {
      "action": "create_expense",
      "description": "將此發票金額記入帳務系統",
      "parameters": {
        "amount": "1200",
        "vendor": "某某科技有限公司",
        "date": "2025-03-15",
        "tax_id": "12345678"
      },
      "confidence": 0.92
    },
    {
      "action": "archive",
      "description": "將此發票歸檔至文件庫",
      "parameters": {},
      "confidence": 0.96
    },
    {
      "action": "tax_report",
      "description": "加入本期稅務報表",
      "parameters": { "tax_period": "2025-03" },
      "confidence": 0.78
    }
  ],
  "extracted_fields": {
    "amount": "1200",
    "vendor": "某某科技有限公司",
    "date": "2025-03-15"
  },
  "top_action": "create_expense",
  "metadata": {
    "pages": 1,
    "backend": "paddleocr",
    "source": "/absolute/path/to/invoice.jpg"
  },
  "searchable_pdf": "/absolute/path/to/invoice.searchable.pdf"
}
```

### 欄位說明

| 欄位 | 說明 |
|------|------|
| ok | 處理是否成功 |
| document_type | 文件類型（invoice、business_card…） |
| confidence | 分類信心指數 (0–1) |
| text | 從所有頁面萃取的全部文字（Markdown 格式） |
| pruned_result | 原始 API 回應，包含每頁的 layoutParsingResults，可用於進階處理 |
| suggested_actions | 建議行動列表，已依信心排序 |
| extracted_fields | 結構化擷取欄位（金額、日期、姓名等），供 agent 直接使用 |
| top_action | 信心最高的行動名稱 |
| metadata | 包含頁數、使用的後端、來源路徑等 |
| searchable_pdf | 可搜尋 PDF 的路徑（僅在 `--make-searchable-pdf` 時出現） |

## Agent 整合建議

1. **使用 `extracted_fields`**：直接取用結構化資料（金額、日期、vendor 等），agent 自行決定如何處理。
2. **提供互動按鈕**：將 `suggested_actions` 轉換為快速回覆按鈕，讓使用者點選執行。
3. **自動執行**：確認後，呼叫對應函數並傳入 `suggested_actions` 中的 `parameters`。

範例（Node.js 風格 pseudo-code）：

```javascript
const result = await callAgentVision({ 'file-path': '/path/to/doc.pdf' });
if (result.document_type === 'invoice') {
  for (const act of result.suggested_actions) {
    showButton(act.description, { action: act.action, params: act.parameters });
  }
}
```

## 可搜尋 PDF 詳細說明

`--make-searchable-pdf` 會產生一個新的 PDF，其中包含可選取的、可搜尋的文字層。這是如何實現的：

1. 將輸入 PDF 的每一頁轉為 200 DPI 的點陣圖（使用 `pdf2image` 與系統的 `poppler`）
2. 根據 PaddleOCR 回傳的 `layoutParsingResults[].prunedResult` 中的 fragment `bbox` 座標，在對應位置添加「不可見」的文字（使用 `reportlab`）
3. 圖片維持為背景，文字層疊加在上方；搜尋時 PDF 閱讀器會匹配嵌入的文字

若 API 未回傳任何 bounding box 資料，則退化的版本會將整頁文字疊加在頁面底部，仍可搜尋但位置不精確。

### 必要軟體

- 系統：`poppler-utils`（Ubuntu: `apt-get install poppler-utils`；macOS: `brew install poppler`）
- Python: `reportlab`、`pypdf`、`pillow`、`pdf2image`

## 文件類型對照表

| 類型 | 辨識關鍵字/結構 | 建議行動 |
|------|----------------|----------|
| 發票 (invoice) | 發票號碼、金額、統一編號、稅額、賣方/买方 | create_expense、archive、tax_report |
| 名片 (business_card) | 姓名、電話、Email、公司職稱 | add_contact、save_vcard |
| 收據 (receipt) | 商店名稱、實付金額、交易日期 | create_expense、split_bill |
| 表格 (table) | 表格線條、多欄對齊、表頭 | export_csv、analyze_data |
| 合約 (contract) | 條款編號、簽署人、簽名、生效日 | summarize、extract_dates、flag_obligations |
| 身分證 (id_card) | 身分證字號、姓名、出生日期、性別 | extract_id_info、verify_age |
| 護照 (passport) | 護照號碼、國籍、簽發日、有效期 | store_passport_info、check_validity |
| 銀行對帳單 (bank_statement) | 帳戶號碼、帳單期間、餘額、交易明細 | categorize_transactions、generate_report |
| 駕照 (driver_license) | 駕照編號、車類別、有效期、地址 | store_license_info、check_expiry |
| 稅表 (tax_form) | 稅年度、總收入、應納稅額、扣除額 | summarize_tax、suggest_deductions |
| 一般 (general) | 無特定模式 | summarize、translate、search_keywords |
| 財務報告 (financial_report) | 營收、淨利、毛利率、資產負債 | summarize_financials、compare_periods、flag_risks |
| 會議記錄 (meeting_minutes) | 出席者、決議、待辦事項 | extract_action_items、create_calendar_events、send_summary |
| 履歷 (resume) | 姓名、Email、學歷、技能 | create_candidate_profile、match_jobs、extract_skills |
| 旅遊行程 (travel_itinerary) | 航班、酒店、目的地、日期 | create_calendar_events、set_reminders、check_visa |

## 常見問題

### PaddleOCR API 回傳 403 或 404

檢查：
- `PADDLEOCR_DOC_PARSING_API_URL` 是否正確，是否以 `/layout-parsing` 結尾
- `PADDLEOCR_ACCESS_TOKEN` 是否有效且未過期
- 網路是否可存取該 API 端點

### 可搜尋 PDF 無法生成

確認已安裝：
```bash
pip3 show reportlab pypdf pdf2image
```
並確認系統有 `poppler`：
```bash
which pdftoppm  # 應指向 /usr/bin/pdftoppm 或其他
```

若仍失敗，請查看 `stderr` 的錯誤訊息，常見原因：
- 原始 PDF 無法轉換（檔案損壞或加密）
- bounding box 資料缺失（仍會生成，但文字位置不精確）

### 辨識率不佳

- 確認文件清晰、無模糊、無反光
- 如果是中文，PaddleOCR 預設會辨識；若為其他語言，API 通常會自動偵測
- 調整文件 DPI（建議 300 DPI 以上）

### Batch 模式執行速度慢

- 可考慮平行處理（例如 GNU parallel）
- 若使用雲端 API，注意速率限制；可增加 `--timeout` 或分批上傳

## 架構說明

```
doc_vision.py  →  主入口
   ├─ ocr_engine.py      → 呼叫 PaddleOCR API，回傳 text + pruned_result
   ├─ classify.py        → 根據文字內容判斷文件類型
   ├─ actions.py         → 提取參數並產生建議行動列表
   ├─ (no templates)     → 結構化資料直接輸出，無需模板
   └─ make_searchable_pdf.py → 使用 bbox 生成可搜尋 PDF
```

## 開發新文件類型

1. 在 `scripts/classify.py` 加入匹配函數與常數：
   ```python
   DOC_TYPE_MY_TYPE = "my_type"
   def match_my_type(text: str) -> float:
       patterns = [r"關鍵字1", r"關鍵字2"]
       return sum(bool(re.search(p, text, re.IGNORECASE)) for p in patterns) / len(patterns)
   ```
   並在 `classify()` 的 `scores` 字典加入 `DOC_TYPE_MY_TYPE: match_my_type(text)`。

2. 在 `scripts/actions.py` 加入生成函數：
   ```python
   def suggest_my_type(text: str, metadata) -> List[Action]:
       # 提取 param，返回 Action list
       ...
   SUGGESTION_DISPATCH[DOC_TYPE_MY_TYPE] = suggest_my_type
   ```

3. 在 `templates/` 新增 `my_type.md`（Jinja2 模板），內容為給 agent 的指示與可參數。

4. 在 `docs/README.zh.md` 的「文件類型對照表」新增列。

## 效能與資源

- 單次請求通常耗時 2–15 秒（取決於文件頁數與 API 速度）
- 記憶體使用：處理 PDF 時可能達到文件大小 × 2–3 倍
- Batch 模式無內建並行，如需加速可自行多行程包裝

## 授權

MIT-0（非常寬鬆，可自由使用、修改、發行）

## 版本歷史

- v1.1.0 — 新增 4 種文件類型、API 重試、並行 batch、CSV 匯出、美化排版（2025-03-15）
- v1.0.0 — 初始版本（2025-03-15）

---

**Problems?** Check `stderr` output or open an issue on GitHub.