---
name: book-recommendation-engine
description: 書籍推薦引擎：支援協同過濾 / 內容相似度 / 熱門暢銷 / 標籤擴展四種演算法；內建 8 大主題書單；Open Library API 即時搜書；想讀書單追蹤含價格監控。
---

# 🔥 書籍推薦引擎（Book Recommendation Engine）

## 概述

智能書籍推薦系統，整合多種推薦演算法與即時書庫資料，幫你發現下一本好書。

**觸發關鍵字：** 推薦書、書籍推薦、找書、想讀什麼書、最近暢銷、這本書類似、Open Library、主題書單、創業書單、育兒書單、寫作書單、必讀清單、書單生成、想讀清單追蹤

---

## 支援格式

| 功能 | 說明 |
|------|------|
| 協同過濾 | 基於你和他人的評分，發現品味相近讀者推薦的書 |
| 內容相似度 | 以一本書為种子，找出同作者 / 同分類 / 同標籤的書 |
| 熱門暢銷 | Open Library 實時Trending，即時反映全球借閱熱度 |
| 標籤擴展 | 輸入喜歡的標籤，推薦同類書籍 |
| 主題書單 | 內建 8 大領域結構化書單，含必讀/選讀/難度標記 |
| 想讀追蹤 | 追蹤價格變化、待讀順位、到貨與否 |

---

## 腳本清單

| 腳本 | 用途 |
|------|------|
| `scripts/recommender.py` | 核心推薦引擎（四種演算法 + 圖書館管理）|
| `scripts/openlibrary_client.py` | Open Library API 客戶端（即時搜書、作者、暢銷）|
| `scripts/booklist_generator.py` | 主題書單生成器（8 領域 + 網路摘要）|
| `scripts/wishlist_tracker.py` | 想讀書單追蹤（優先順序、價格監控）|

---

## 環境依賴

```bash
# 純 Python，無需額外依賴（標準庫 urllib + json）
```

---

## 快速使用

```bash
# ── 推薦 ──────────────────────────────────────────────────
# 混合推薦（協同 + 內容 + 熱門，預設）
python3 scripts/recommender.py recommend -n 5

# 基於某本書推薦相似書籍
python3 scripts/recommender.py recommend -b "OL82563W" -n 5

# 標籤推薦
python3 scripts/recommender.py recommend -t 商業 創業 思考 -n 5

# 熱門暢銷
python3 scripts/recommender.py recommend -m popular -n 10

# ── 圖書館 ───────────────────────────────────────────────
# 新增書籍
python3 scripts/recommender.py add-book -t "原子習慣" -a "James Clear" \
  -c 習慣養成 -g 心理學 -r 5 -y 2018

# 對書籍評分（影響協同過濾）
python3 scripts/recommender.py rate <book_id> 5

# ── Open Library ──────────────────────────────────────────
# 搜尋書名
python3 scripts/openlibrary_client.py search "原子習慣"

# ISBN 查詢
python3 scripts/openlibrary_client.py isbn 9789869697203

# 作者全部作品
python3 scripts/openlibrary_client.py author "James Clear"

# 今日熱門
python3 scripts/openlibrary_client.py trending -n 10

# ── 主題書單 ─────────────────────────────────────────────
# 列出所有書單
python3 scripts/booklist_generator.py list

# 生成書單
python3 scripts/booklist_generator.py generate startup -o startup_books.md
python3 scripts/booklist_generator.py generate thinking -o thinking_books.md --web

# ── 想讀追蹤 ─────────────────────────────────────────────
python3 scripts/wishlist_tracker.py add -t "深度工作" -a "Cal Newport" -p 468
python3 scripts/wishlist_tracker.py list
python3 scripts/wishlist_tracker.py priority <book_id> 3
python3 scripts/wishlist_tracker.py read <book_id> -r 5
python3 scripts/wishlist_tracker.py price  # 檢查降價
```
