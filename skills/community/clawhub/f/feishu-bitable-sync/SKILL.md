---
name: feishu-bitable-sync
description: |
  Feishu Bitable Data Sync - Sync data between multiple bitables or external sources.
  
  **Features**:
  - Sync data between two bitables
  - Import data from external sources
  - Two-way sync with conflict resolution
  - Scheduled sync support
  
  **Trigger**:
  - User mentions "sync data", "数据同步", "bitable sync"
  - User wants to import or export bitable data
---

# Feishu Bitable Data Sync

## ⚠️ Pre-requisites

- ✅ **Get app_token**: From bitable URL or list API
- ✅ **Get table_id**: From bitable table list
- ✅ **Field types**: Must match exactly (text=1, number=2, date=5, person=11, etc.)

---

## 📋 Quick Reference

| Intent | Tool | action | Required Params |
|--------|------|--------|-----------------|
| List bitables | feishu_bitable_app | list | - |
| List tables | feishu_bitable_app_table | list | app_token |
| Query records | feishu_bitable_app_table_record | list | app_token, table_id |
| Create records | feishu_bitable_app_table_record | batch_create | app_token, table_id, records |
| Update records | feishu_bitable_app_table_record | batch_update | app_token, table_id, records |
| Delete records | feishu_bitable_app_table_record | batch_delete | app_token, table_id, record_ids |

---

## 🛠️ Sync Patterns

### 1. One-way Sync (Source → Destination)

```json
// Step 1: Read source data
{
  "action": "list",
  "app_token": "source_token",
  "table_id": "source_table",
  "page_size": 500
}

// Step 2: Transform and write to destination
{
  "action": "batch_create",
  "app_token": "dest_token", 
  "table_id": "dest_table",
  "records": [
    {"fields": {"字段A": "值1", "字段B": "值2"}}
  ]
}
```

### 2. Two-way Sync with Conflict Resolution

Compare records by unique identifier and handle conflicts:

```json
// Pseudo-code for sync:
// 1. Fetch both bitables
// 2. Compare by unique field (如: 任务ID)
// 3. If source is newer: update dest
// 4. If dest is newer: update source (or skip)
// 5. Report sync results

{
  "action": "list",
  "app_token": "token",
  "table_id": "table",
  "filter": {
    "conjunction": "and",
    "conditions": [{"field_name": "同步状态", "operator": "is", "value": ["未同步"]}]
  }
}
```

### 3. Import from CSV

Convert CSV to bitable records:

```csv
任务名称,负责人,截止日期,优先级
任务A,张三,2026-04-01,高
任务B,李四,2026-04-02,中
```

```json
{
  "action": "batch_create",
  "app_token": "Mxxx",
  "table_id": "Txxx",
  "records": [
    {"fields": {"任务名称": "任务A", "负责人": [{"id": "ou_xxx"}], "截止日期": 1743446400000, "优先级": "高"}},
    {"fields": {"任务名称": "任务B", "负责人": [{"id": "ou_yyy"}], "截止日期": 1743532800000, "优先级": "中"}}
  ]
}
```

### 4. Scheduled Sync Marker

Use a special field to track sync status:

| 唯一标识 | 数据 | 同步时间 | 同步状态 |
|---------|------|---------|---------|
| TASK_001 | {...} | 1743446400000 | 已同步 |

```json
{
  "action": "batch_update",
  "app_token": "Mxxx",
  "table_id": "Txxx",
  "records": [
    {"record_id": "rec_xxx", "fields": {"同步状态": "已同步", "同步时间": 1743446400000}}
  ]
}
```

---

## 💰 Pricing

| Version | Price | Features |
|---------|-------|----------|
| Free | ¥0 | Manual sync, up to 100 records |
| Pro | ¥15/month | Auto sync, 500 records, conflict resolution |
| Team | ¥45/month | Scheduled sync, API, unlimited |

---

## 📝 Example

**User says**: "把A表格的任务同步到B表格，只同步未完成的任务"

**Execute**:
1. List records from source with filter for 未完成
2. Transform records to match destination schema
3. Batch create or update destination records
4. Mark source records as 已同步

---

## 🔧 Field Type Reference

| Type ID | Field Type |
|---------|-----------|
| 1 | Text |
| 2 | Number |
| 3 | Single Select |
| 4 | Multi Select |
| 5 | Date |
| 7 | Checkbox |
| 11 | Person |
| 13 | Phone |
| 15 | URL |
| 17 | Attachment |
| 1001 | Created Time |
| 1002 | Modified Time |
