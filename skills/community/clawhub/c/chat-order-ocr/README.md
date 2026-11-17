# Chat Order OCR｜聊天訂單整理工具

將 LINE、Facebook 或其他聊天視窗中貼上的訂單文字，整理成可人工覆核的訂單列。工具採用保守的規則式解析，不會自行猜測未出現的姓名、品項或數量。

## 功能特色

| 功能 | 說明 |
|---|---|
| 訂單辨識 | 支援 `+1`、`＋2`、`一份`、`兩盒`、`3個` 等常見數量格式 |
| 姓名歸屬 | 訂單會沿用最近一個獨立出現、看起來像姓名的訊息 |
| 訊息過濾 | 自動略過聊天時間、系統訊息、單獨數字與一般閒聊 |
| 分組排序 | 支援原始順序、姓名升冪、姓名降冪，以及依姓名分組 |
| 品項對應 | 可透過 JSON 品項字典保留原文並對應標準品項 |
| 可覆核輸出 | JSON 與 CSV 均保留來源與信心狀態，方便人工檢查 |

## 環境需求

需要 Python 3.9 或更新版本。本工具的文字解析不需要額外套件；若要從圖片進行 OCR，請另外安裝 Tesseract 與 `chi_tra`、`eng` 語言資料。

## 快速開始

將聊天文字保存為 `messages.txt`，執行：

```bash
python3 scripts/order_ocr_cli.py \
  --input messages.txt \
  --source text \
  --group-by person \
  --format json \
  --output orders.json
```

若需要給試算表使用，可輸出 CSV：

```bash
cat messages.txt | python3 scripts/order_ocr_cli.py \
  --source text \
  --group-by person \
  --format csv \
  --output orders.csv
```

姓名降冪排序：

```bash
python3 scripts/order_ocr_cli.py \
  --input messages.txt \
  --sort name-desc \
  --format json
```

## 品項字典

可使用 `references/catalog.example.json` 作為格式範例：

```bash
python3 scripts/order_ocr_cli.py \
  --input messages.txt \
  --catalog references/catalog.example.json \
  --format json
```

工具會保留 `item` 原始文字，並另外產生 `matched_item` 與 `match_status`。未能對應的品項會標示為「未對應，請確認」，不會自動合併相似但可能代表不同規格的品項。

## 輸出欄位

JSON 輸出包含 `rows`、`summary`、`sort` 與 `group_by`。每筆訂單列通常包含以下資訊：

| 欄位 | 意義 |
|---|---|
| `person` | 訂購人 |
| `item` | 聊天訊息中的原始品項文字 |
| `matched_item` | 品項字典對應後的標準名稱 |
| `qty` | 數量 |
| `source` | `text` 或 `ocr` |
| `confidence` | `high` 或 `check` |

若來源是 OCR，所有解析列都會標示 `confidence: check`，交付或出貨前必須逐筆確認姓名、品項規格、數量，以及是否有跨圖片重複內容。

## 測試

執行內建測試：

```bash
python3 scripts/test_order_ocr_cli.py
```

## 專案結構

```text
.
├── README.md
├── SKILL.md
├── references/
│   ├── catalog.example.json
│   ├── cli_examples.md
│   └── complex_chat_fixture.txt
└── scripts/
    ├── order_ocr_cli.py
    └── test_order_ocr_cli.py
```

## 授權與使用提醒

本專案適合協助整理訂單草稿，不取代人工核對。尤其是 OCR 文字、含價格或重量的品項、同音異字，以及同一品項的不同規格，都應在實際出貨前確認。
