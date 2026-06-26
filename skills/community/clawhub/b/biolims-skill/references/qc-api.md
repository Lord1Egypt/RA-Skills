# Sequencing QC Module API Reference

## Command Quick Reference

| Command | Description |
|---------|-------------|
| `seq-qc-list [page] [rows]` | QC order list |
| `seq-qc-detail <qc_id>` | QC order details |
| `seq-qc-item-list <qc_id> [page] [rows]` | QC sample details |
| `get-seq-qc-custom-fields 257-mainTable` | Main table custom fields |
| `get-seq-qc-custom-fields 257-itemTable` | Detail table custom fields |
| `save-seq-qc '<json>'` | Save QC order |
| `delete-seq-qc-item <item_ids>` | Delete QC details |
| `recall-seq-qc <qc_id>` | Withdraw QC order |
| `export-seq-qc <qc_id>` | Export Excel |

**QC order status:** 3=New, 1=Complete

---

## method Field Enum

| Value | Display |
|-------|---------|
| `1` | Qualified |
| `0` | Unqualified |

---

## Complete QC Order

**❌ Do not use:** `transactChargeSequencingQc` (returns "The server is busy")

**✅ Correct method:**
```bash
# Step 1: Get details
node biolims.mjs seq-qc-detail <qc_id>

# Step 2: Call changeState
POST /system/activiti/HandleTasks/changeState
{
  "businessKey": "QC order ID",
  "state": "60",
  "stateName": "Complete",
  "params": <complete object returned by seq-qc-detail>,
  "moduleId": "SequencingQc",
  "formName": "Sequencing QC"
}
```

---

**Detailed API documentation:** `api.md`
