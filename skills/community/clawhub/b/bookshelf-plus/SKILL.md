---
name: bookshelf-plus
description: 圖書館管家 Plus：ISBN 多源掃描 + 借還追蹤與到期提醒 + Notion 同步 + 書庫統計與匯出。基於 bookshelf skill 強化，整合 Open Library + Google Books 查 ISBN，新增借出到期日管理與逾期提醒、批量入庫、閱讀進度追蹤、書庫健康報告。
---

# 📚 圖書館管家 Plus（Bookshelf Plus）

## 概述

在 `bookshelf` 基礎上進行全面強化，專注於三大升級方向：
1. **多源 ISBN 查詢** — Open Library + Google Books，雙源互補提高命中率
2. **完整借還生命週期** — 借出日 / 預定還日 / 逾期提醒，追蹤誰借了哪本書
3. **書庫健康報告** — 藏書量、借出率、待讀庫存、逾期風險一鍵生成

**觸發關鍵字：** 新增書籍、圖書館、入庫、借書、還書、書單、ISBN、搜尋書、借給、歸還、匯出書單、逾期、統計、掃描條碼、閱讀打卡、讀書打卡、閱讀進度、打卡、讀了多少頁、連續打卡、閱讀統計、讀書統計

---

## Notion 資料庫結構

**必要欄位：**

| 欄位名 | 類型 | 說明 |
|--------|------|------|
| 名稱（Name） | 標題 | 書名 |
| 作者（Author） | 文字 | 作者名 |
| ISBN | 文字 | 國際標準書號 |
| 分類（Category） | 選擇 | 小說/商業/技術/散文/歷史/童書/其他 |
| 標籤（Tags） | 多選 | 新書/在借/已讀/待讀/逾期/閱讀中 |
| 借出給（BorrowedBy） | 文字 | 借書人 |
| 借出日期（BorrowedDate） | 日期 | 借出時間 |
| 預定還日（DueDate） | 日期 | 預定歸還日期 |
| 歸還日期（ReturnedDate） | 日期 | 實際歸還時間 |
| 閱讀頁數（PagesRead） | 數字 | 已讀頁數 |
| 總頁數（TotalPages） | 數字 | 全書總頁數 |
| 所在位置（Location） | 文字 | 例：書櫃A第2層 |
| 購入日期（PurchaseDate） | 日期 | 購入時間 |
| 封面圖（CoverURL） | 文字 | 書籍封面URL |
| 備註（Notes） | 文字 | 個人備註 |

**找不到 Notion 金鑰？** 告訴用戶去 [notion.so/my-integrations](https://www.notion.so/my-integrations) 建立整合並取得金鑰。

---

## 腳本清單

### 圖書管理（原有）
| 腳本 | 用途 |
|------|------|
| `scripts/isbn_lookup.py` | 多源 ISBN 查詢（Open Library + Google Books） |
| `scripts/isbn_scan.py` | 圖片條碼 ISBN 辨識 |
| `scripts/notion_client.py` | Notion CRUD（Plus 版，含還期欄位） |
| `scripts/lending.py` | 借還生命週期管理 |
| `scripts/check_overdue.py` | 逾期檢查（供 Cron 呼叫） |
| `scripts/batch_import.py` | CSV 批量入庫 |
| `scripts/export_books.py` | 匯出 CSV / Markdown / 報告 |
| `scripts/library_report.py` | 書庫健康報告生成 |

### 閱讀習慣追蹤（新增）
| 腳本 | 用途 |
|------|------|
| `scripts/reading_progress.py` | 每日打卡 / 進度查詢 / Streak / 統計（checkin/status/streak/stats/history） |
| `scripts/reading_stats_dashboard.py` | 生成精美 HTML 閱讀統計儀表板（熱力圖、進度環、趨勢圖） |
| `scripts/reading_cron.py` | Cron 用：每日打卡提醒 + Streak 更新 + 週報 |


---

## 環境依賴

```bash
pip3 install requests notion-client isbnlib Pillow
```

---

## Cron Job 設定

```bash
# 每日 09:00 執行逾期檢查
openclaw cron add \
  --name "bookshelf-overdue-check" \
  --schedule "0 9 * * *" \
  --tz "Asia/Taipei" \
  --payload-kind agentTurn \
  --message "執行逾期檢查：python3 ~/.qclaw/skills/bookshelf-plus/scripts/check_overdue.py --api-key <KEY> --database-id <ID>。若有逾期書籍，主動發送到期提醒。"

# 每日 20:00 執行閱讀打卡提醒
openclaw cron add \
  --name "reading-checkin-reminder" \
  --schedule "0 20 * * *" \
  --tz "Asia/Taipei" \
  --payload-kind agentTurn \
  --message "執行閱讀打卡提醒：python3 ~/.qclaw/skills/bookshelf-plus/scripts/reading_cron.py --log ~/.bookshelf-plus/reading_log.json --format text。根據結果提醒用戶今日閱讀打卡。"
```

---

## 與原有 bookshelf 差異對照

| 功能 | bookshelf（原版） | bookshelf-plus（新） |
|------|-----------------|---------------------|
| ISBN 查詢 | Open Library 單源 | Open Library + Google Books |
| 條碼掃描 | ❌ 無 | ✅ ISBN 圖片辨識 |
| 還期管理 | ❌ 無 | ✅ 預定還日 + 逾期追蹤 |
| 逾期提醒 | ❌ 無 | ✅ Cron 自動檢查 + 推播 |
| 批量入庫 | ❌ 無 | ✅ CSV 批量匯入 |
| 閱讀進度 | ❌ 無 | ✅ 頁數追蹤 + 進度% |
| 書庫報告 | 基本統計 | 完整健康報告 + 逾期風險 |
| 所在位置 | ❌ 無 | ✅ 書本位置管理 |
