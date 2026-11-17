# 🔥 Book Recommendation Engine

智能書籍推薦系統 — 四種推薦演算法 × Open Library 即時書庫 × 8 大主題書單 × 想讀追蹤。

## 安裝

```bash
# 純 Python，無需額外安裝
# （使用標準庫 urllib.request）
```

## 快速開始

```bash
# 混合推薦
python3 scripts/recommender.py recommend -n 5

# Open Library 搜書
python3 scripts/openlibrary_client.py search "原子習慣"

# 主題書單
python3 scripts/booklist_generator.py list
python3 scripts/booklist_generator.py generate startup -o books.md --web

# 想讀追蹤
python3 scripts/wishlist_tracker.py add -t "深度工作" -p 468
python3 scripts/wishlist_tracker.py list
```

## 腳本總覽

| 腳本 | 功能 |
|------|------|
| `recommender.py` | 協同過濾 / 內容相似度 / 熱門暢銷 / 標籤擴展 |
| `openlibrary_client.py` | Open Library API：搜書、作者、暢銷榜 |
| `booklist_generator.py` | 8 大領域結構化書單，含必讀/選讀難度 |
| `wishlist_tracker.py` | 想讀清單：優先順序、價格監控、閱讀記錄 |

## License

MIT
