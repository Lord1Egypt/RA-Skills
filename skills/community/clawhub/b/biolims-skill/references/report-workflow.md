# Report Module Workflow

## Complete Flow

```
report-pending-list → (report-assign-writer) → report-generate → report-detail
→ report-items → report-templates → report-save → report-file-generate
```

---

## Command Distinction

| Command | Function | API |
|---------|----------|-----|
| `report-generate @<json>` | Create report order | insertReports |
| `report-file-generate <id>` | Generate Word file | ReportGeneration |

---

## report-pending-list

**Accepts only 2 parameters:** `report-pending-list <page> <rows>`
- ✅ Correct: `report-pending-list 1 50`
- ❌ Wrong: `report-pending-list 1 1 50`

---

## report-generate Rules

**Must pass complete fields:**
- Take data from the complete record returned by `report-pending-list`
- **Key fields:** `code` (required), `productId` (required)
- `changeEvent`: 0
- `state`: "0" = generate individually, "1" = merge and generate

**Merge generation conditions:**
- All samples must be from the same order and same batch number
- Writer must be assigned first (run `report-assign-writer` first)

**LymphDetect project:** Only supports merging 3 samples from the same order; individual generation is not allowed

---

## report-save Key Points

**Required fields:**
- `sendUserId`: Full UUID (e.g. `00000000000000000000000000000001`), ❌ cannot use username
- `customFieldValue`: Complete JSON string
- `reportTemplate` + `reportTemplateId`: Both must be set
- `sampleReportItems`: Complete array, add `"changeEvent": 0` for each sample
- `logs`: String format (not an array!)
- `listlogs`: Empty array `[]`

**Steps:**
1. `report-detail <id> edit`
2. `report-items <id>`
3. `report-templates`
4. Build JSON
5. `report-save @<json>`

---

## Complete Report Order (Two Steps)

**Step 1:** Query action ID
```
POST /system/activiti/HandleTasks/selectHandleTasks
{"appTypeTableId": "SampleReport"}
```

**Step 2:** Complete report order
```
POST /system/activiti/HandleTasks/HandleTasks
{"appTypeTableId": "38", "contentid": "SR number", "formName": "Report", "note": ""}
```

After completion, status changes from "3" (NEW) to "1" (Complete)

---

## Report Sending Rules

| Method | Command | sendState | sendType |
|--------|---------|-----------|----------|
| Email | `report-send-confirm` | "0" | 0 (number) |
| Express | `report-send-offline` | "1" | 1 (number) |

**Rules:**
- Email sending: Email address required
- Already sent (arc='1'): Cannot send again
- Withdraw: Must provide reason

---

## Report Status

| Status | Description |
|--------|-------------|
| 0 | Cancelled |
| 1 | Complete |
| 3 | New (editable) |
| 15 | To Be Modified |
| 20 | In Process (can generate report, cannot modify) |

---

**Back to:** `../MEMORY.md`
