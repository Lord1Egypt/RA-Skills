# 📚 bookshelf-plus

> 圖書館管家 Plus — OpenClaw Skill for AI Assistant

強化版個人圖書館管理系統，整合 **多源 ISBN 查詢**、**借還生命週期追蹤**、**逾期自動提醒**、**批量入庫**、**書庫健康報告**，支援 Notion 同步儲存。

---

## ✨ 功能特色

| 功能 | 說明 |
|------|------|
| 🔍 **多源 ISBN 查詢** | Open Library + Google Books 雙源，查詢成功率更高 |
| 📷 **ISBN 條碼掃描** | 上傳圖片自動辨識書籍條碼 |
| 📋 **完整借還追蹤** | 借出日 → 預定還日 → 逾期提醒，誰借了哪本書一目了然 |
| 🔔 **自動逾期提醒** | 每日 Cron 自動檢查逾期，主動推播提醒 |
| 📦 **批量入庫** | CSV 檔案一鍵匯入大量書籍 |
| 📊 **書庫健康報告** | 總藏書、分類分布、借出率、逾期風險完整呈現 |
| 📤 **多元匯出** | 支援 CSV / Markdown / 完整報告 |
| ☁️ **Notion 同步** | 所有資料自動同步至 Notion 資料庫 |

---

## 📁 目錄結構

```
bookshelf-plus/
├── SKILL.md                         ← OpenClaw 技能入口說明
└── scripts/
    ├── isbn_lookup.py               ← 多源 ISBN 查詢（OL + GB）
    ├── isbn_scan.py                 ← 圖片條碼 ISBN 辨識
    ├── notion_client.py             ← Notion CRUD（新增/查詢/更新/刪除）
    ├── lending.py                   ← 借還生命週期管理
    ├── check_overdue.py             ← 逾期檢查（Cron 呼叫）
    ├── batch_import.py              ← CSV 批量入庫
    ├── export_books.py             ← 匯出 CSV / Markdown / 報告
    └── library_report.py            ← 書庫健康報告生成
```

---

## 🚀 快速開始

### 1. 安裝依賴

```bash
pip3 install requests notion-client isbnlib Pillow
```

### 2. 設定 Notion

1. 前往 [notion.so/my-integrations](https://www.notion.so/my-integrations) 建立整合
2. 取得 **Integration Token**
3. 在 Notion 建立書籍資料庫，參考下方「Notion 資料庫欄位」
4. 將資料庫分享給整合（Share → Invite）

### 3. Notion 資料庫欄位

| 欄位名 | 類型 |
|--------|------|
| 名稱（Name） | 標題 |
| 作者（Author） | 文字 |
| ISBN | 文字 |
| 分類（Category） | 選擇 |
| 標籤（Tags） | 多選 |
| 借出給（BorrowedBy） | 文字 |
| 借出日期（BorrowedDate） | 日期 |
| 預定還日（DueDate） | 日期 |
| 歸還日期（ReturnedDate） | 日期 |
| 閱讀頁數（PagesRead） | 數字 |
| 總頁數（TotalPages） | 數字 |
| 所在位置（Location） | 文字 |
| 語言（Language） | 選擇 |
| 封面圖（CoverURL） | 文字 |
| 備註（Notes） | 文字 |

### 4. 環境變數（可選，方便快速呼叫）

```bash
export NOTION_KEY="secret_xxxx"
export NOTION_DATABASE_ID="xxxx"
```

---

## 📖 使用範例

### ISBN 查詢
```bash
python3 scripts/isbn_lookup.py --isbn 9780134685991
```

### 借出書籍（含還期）
```bash
python3 scripts/lending.py borrow \
  --title "原子習慣" \
  --borrower 小明 \
  --due-date 2026-09-01 \
  --api-key $NOTION_KEY \
  --database-id $NOTION_DATABASE_ID
```

### 還書
```bash
python3 scripts/lending.py return \
  --title "原子習慣" \
  --api-key $NOTION_KEY \
  --database-id $NOTION_DATABASE_ID
```

### 逾期檢查
```bash
python3 scripts/check_overdue.py \
  --api-key $NOTION_KEY \
  --database-id $NOTION_DATABASE_ID
```

### 書庫健康報告
```bash
python3 scripts/library_report.py \
  --api-key $NOTION_KEY \
  --database-id $NOTION_DATABASE_ID \
  --format markdown -o report.md
```

### CSV 批量入庫
```bash
python3 scripts/batch_import.py \
  --csv ~/books.csv \
  --api-key $NOTION_KEY \
  --database-id $NOTION_DATABASE_ID
```

### 匯出書單
```bash
python3 scripts/export_books.py \
  --api-key $NOTION_KEY \
  --database-id $NOTION_DATABASE_ID \
  --format markdown -o bookshelf.md
```

---

## ⏰ 逾期提醒 Cron 設定

在 OpenClaw 中設定每日自動逾期檢查：

```bash
openclaw cron add \
  --name "bookshelf-overdue-check" \
  --schedule "0 9 * * *" \
  --tz "Asia/Taipei" \
  --payload-kind agentTurn \
  --message "執行逾期檢查：python3 ~/.qclaw/skills/bookshelf-plus/scripts/check_overdue.py --api-key YOUR_KEY --database-id YOUR_ID。若有逾期書籍，主動發送到期提醒。"
```

---

## 🔄 與原版 bookshelf 差異

| 功能 | bookshelf（原版） | bookshelf-plus |
|------|-----------------|----------------|
| ISBN 查詢 | Open Library 單源 | OL + Google Books 雙源 |
| 條碼掃描 | ❌ | ✅ |
| 還期管理 | ❌ | ✅ 預定還日 + 逾期追蹤 |
| 逾期提醒 | ❌ | ✅ Cron 自動檢查 |
| 批量入庫 | ❌ | ✅ CSV 批量匯入 |
| 閱讀進度 | ❌ | ✅ 頁數追蹤 + % |
| 書庫報告 | 基本統計 | 完整健康報告 |
| 所在位置 | ❌ | ✅ |
| 語言/年份 | ❌ | ✅ |

---

## 📄 授權

MIT License — 自由使用、修改與散佈。

---

## 👤 作者

[xuan905](https://github.com/xuan905)
