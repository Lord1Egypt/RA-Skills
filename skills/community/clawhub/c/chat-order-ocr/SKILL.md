---
name: chat-order-ocr
description: Chat order extraction and grouping from pasted LINE/Facebook messages or OCR text. Use for parsing +1, +2, 一份, 盒, 個等數量、按姓名分組排序、產生可人工覆核的 JSON 或 CSV 名單，以及建立或更新相關的聊天訂單整理工具。
---

# Chat Order OCR

將聊天訊息轉成可覆核的訂單列。優先使用 bundled CLI 做確定性的解析、分組、排序與輸出；不要用模型猜測未出現的姓名、品項或數量。

## 工作流程

1. **辨識輸入來源。** 取得使用者貼上的聊天文字、既有 OCR 文字，或直接取得多張聊天截圖。若使用 CLI 直接讀圖，先確認本機有 Tesseract 與 `chi_tra+eng` 語言資料；若來源是 OCR，讓每筆資料保留 `confidence: check`。
2. **保留原始內容。** 將原始文字另存為 UTF-8 檔案，或透過 stdin 傳給 CLI。不要先人工改寫聊天內容；必要的修正應在結果檔或介面中留下可追蹤紀錄。
3. **執行 CLI。** 使用 `scripts/order_ocr_cli.py`。文字輸入可透過 `--input` 或 stdin；圖片輸入可透過 `--images` 或 `--images-dir` 批次處理。預設輸出 JSON，適合後續程式處理；需要交給使用者或 Excel 時使用 CSV。
4. **檢查結果。** 確認 `summary` 的人數、筆數、總數量，檢查 `confidence: check`，並確認姓名、品項、數量沒有因聊天時間、貼圖或系統訊息而被誤認。
5. **套用分組或排序。** 使用 `--group-by person` 產生姓名 A→Z 分組結果；使用 `--sort name-desc` 產生姓名 Z→A 結果。原始順序使用 `--sort original`。
6. **交付可覆核輸出。** JSON 應包含 `rows`、`summary`、`sort` 與 `group_by`；CSV 應包含姓名、品項、數量、來源與信心欄位。若存在 `check`，明確告知使用者需要人工確認，不要宣稱 OCR 結果完全正確。

## CLI 用法

```bash
CLI=/home/ubuntu/skills/chat-order-ocr/scripts/order_ocr_cli.py

# 從文字檔產生 JSON 摘要與名單
python "$CLI" --input messages.txt --format json --output orders.json

# 從 stdin 讀取 OCR 文字，按姓名分組並輸出 CSV
cat ocr.txt | python "$CLI" --source ocr --group-by person --format csv --output orders.csv

# 批次 OCR 圖檔、套用品項字典並產生 JSON
python "$CLI" --images screenshots/*.jpg --catalog catalog.json --format json --output ocr-orders.json

# 姓名 Z→A 排序，輸出到 stdout
python "$CLI" --input messages.txt --sort name-desc --format json
```

## 批次圖檔 OCR

CLI 使用系統中的 Tesseract 執行逐張 OCR，不會把圖片送到外部服務。安裝環境後可用 `tesseract --list-langs` 確認 `chi_tra` 與 `eng`；缺少語言資料時，先安裝對應的 Tesseract 語言套件。指定 `--images` 可同時傳入多個檔案，指定 `--images-dir` 則會讀取資料夾內的 JPG、JPEG、PNG、WEBP、BMP、TIFF。每張圖片會在 JSON 的 `ocr` 陣列留下檔案路徑、完成／失敗狀態、辨識字元數與解析列數；即使其中一張失敗，其他圖片仍會繼續處理。

批次 OCR 的所有解析列都標示 `source: ocr` 與 `confidence: check`。不要把 OCR 文字當成已核准訂單；交付前必須逐筆檢查人名、品項規格、數量與跨圖重複內容。

## 品項自動對應

使用 `--catalog catalog.json` 提供標準品項與別名。JSON 可以是 `{\"標準品項\": [\"別名一\", \"別名二\"]}`，CLI 會保留 `item` 原始辨識文字，並將對應結果放入 `matched_item`。成功時 `match_status` 為 `已對應`；沒有匹配時保留原文並標示 `未對應，請確認`，同時將 `confidence` 設為 `check`。字典匹配採用去除空白、忽略大小寫與別名包含關係，較長的別名優先；它不是語意模型，不應用來合併未經使用者確認的不同規格。

## 參數選擇

| 目的 | 參數 | 行為 |
| --- | --- | --- |
| 文字或人工貼上來源 | `--source text` | 姓名已知時標示 `high`；未標註姓名仍標示 `check` |
| OCR 來源文字 | `--source ocr` | 所有解析列標示 `check`，要求人工核對 |
| 批次圖檔 OCR | `--images a.jpg b.png` 或 `--images-dir screenshots/` | 逐張使用 Tesseract，保留來源檔案與 OCR 報告 |
| OCR 語言與版面 | `--ocr-lang chi_tra+eng`、`--psm 6` | 指定繁中／英文與頁面分割模式 |
| 品項自動對應 | `--catalog catalog.json` | 保留原始品項並產生 `matched_item` 與 `match_status` |
| 不改變聊天順序 | `--sort original` | 保留原始列順序 |
| 姓名分組 | `--group-by person` | 依姓名 A→Z 排序，JSON 記錄 `group_by: person` |
| 姓名升冪 | `--sort name-asc` | 依姓名 A→Z 排序 |
| 姓名降冪 | `--sort name-desc` | 依姓名 Z→A 排序 |
| 程式後續處理 | `--format json` | 輸出 rows、summary 與排序資訊 |
| 試算表或交付 | `--format csv` | 輸出 UTF-8 BOM CSV，欄位包含信心狀態 |

## 解析規則

CLI 會將含有 `+1`、`＋2`、`一份`、`兩盒`、`3個` 等模式的行視為訂購列，並沿用最近一個看起來像姓名的獨立行作為訂購人。聊天時間、單獨數字、貼圖提示與系統訊息會被略過。像 `櫻桃2公斤 +1` 的品項會保留重量與規格；像 `青龍6粒198 — 一份` 的分隔符會被移除。

這些規則是保守啟發式，不應取代人工覆核。遇到同一行同時有姓名與品項、特殊單位、跨行訊息或品項名稱被 OCR 切斷時，保留原文並在輸出中標記 `check`，再請使用者確認。

## 建立或更新相關網頁工具

若任務是建立前端工具，先用本 CLI 定義與測試解析輸出，再將相同資料欄位映射到介面。介面至少保留姓名、品項、數量、來源與覆核狀態；排序控制應共用 CLI 的 `original`、`name-asc` 與 `name-desc` 詞彙。不要在前端另寫一套互相矛盾的解析規則，除非同步更新 CLI 與測試案例。

若任務只要求批次 OCR，請將 OCR 引擎視為前置步驟：CLI 本身不會讀取圖片，也不應宣稱已辨識圖片。將 OCR 產出的文字用 `--source ocr` 送入 CLI，即可讓下游流程保留待確認狀態。

## 驗證清單

使用至少一組包含姓名、`+1`、`+2`、`一份`、兩個相同姓名與一個 OCR 來源的案例。驗證 JSON 的 `summary.units`、姓名排序、品項保留規格，以及 CSV 的欄位與 UTF-8 編碼。若輸入沒有可辨識數量，輸出空 `rows` 並回報需要調整格式，不要自行補數量。
