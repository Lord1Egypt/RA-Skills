# CLI 範例

## 貼上文字並產生 JSON

```bash
printf '家家\n櫻桃2公斤 +1\nLena\n台灣葡萄 +2\n' \
  | python /home/ubuntu/skills/chat-order-ocr/scripts/order_ocr_cli.py \
      --format json
```

## 依姓名分組並輸出 CSV

```bash
python /home/ubuntu/skills/chat-order-ocr/scripts/order_ocr_cli.py \
  --input messages.txt \
  --group-by person \
  --format csv \
  --output orders-by-person.csv
```

## OCR 文字保留人工確認狀態

```bash
cat ocr-result.txt \
  | python /home/ubuntu/skills/chat-order-ocr/scripts/order_ocr_cli.py \
      --source ocr \
      --sort name-asc \
      --format json \
      --output ocr-orders.json
```

## 批次圖檔 OCR 與品項對應

```bash
python /home/ubuntu/skills/chat-order-ocr/scripts/order_ocr_cli.py \
  --images screenshots/001.jpg screenshots/002.png \
  --catalog /home/ubuntu/skills/chat-order-ocr/references/catalog.example.json \
  --source ocr \
  --group-by person \
  --format json \
  --output ocr-orders.json
```

也可以掃描整個資料夾：

```bash
python /home/ubuntu/skills/chat-order-ocr/scripts/order_ocr_cli.py \
  --images-dir screenshots/ \
  --catalog catalog.json \
  --format csv \
  --output orders.csv
```

JSON 的 `ocr` 陣列會記錄每張圖片的完成狀態、來源檔名、辨識字元數與產生的訂單列數。JSON 列中的 `confidence: check` 代表需要人工檢查，不代表該筆必然錯誤。`item` 保留 OCR 原文，`matched_item` 是品項字典對應結果；CSV 以 UTF-8 BOM 輸出，適合直接用 Excel 開啟。
