# Report Module API Reference

## Report Task Distribution

| Command | Description |
|---------|-------------|
| `report-pending-list <page> <rows>` | Pending report list (accepts only 2 parameters!) |
| `report-assign-writer @<json>` | Assign writer |
| `report-generate @<json>` | Create report order |

**API path:** `/experimentalcenter/inspectionreport/report/`

**Business rules:**
- Merge generation (state='1'): Same order, same batch number, writer already assigned
- LymphDetect: Only supports merging 3 samples from the same order
- Individual generation (state='0'): Each sample independently

---

## Report List

| Command | Description |
|---------|-------------|
| `report-list [page] [rows]` | Report list |
| `report-detail <report_id> edit` | Report details (edit mode) |
| `report-items <report_id>` | Report sample details |
| `report-templates [page] [rows]` | Available report templates |
| `report-save @<json>` | Save report basic information |
| `report-file-generate <report_id>` | Generate Word file |

**Report status:** 0=Cancelled, 1=Complete, 3=New, 15=To Be Modified, 20=In Process

**Rules:**
- Before generating file, required: `reportDate` + `reportTemplateId`
- New (3): Editable, can generate report, can submit
- In Process (20): Can generate report, cannot modify
- Complete (1): Read-only, can download

---

## Report Sending

| Command | Description |
|---------|-------------|
| `report-sending-list <state> <page> <rows>` | Sending list (1=pending, 2=sent, 3=all) |
| `report-send-confirm @<json>` | Email sending (sendState='0', sendType=0) |
| `report-send-offline @<json>` | Express delivery sending (sendState='1', sendType=1) |

**Rules:**
- Email sending: Email address required
- Already sent (arc='1'): Cannot send again
- Withdraw: Must provide reason

---

## Complete Flow

```
report-pending-list → (report-assign-writer) → report-generate → report-detail
→ report-items → report-templates → report-save → report-file-generate
```

---

**Detailed API documentation:** `api.md`
