# Bio-LIMS Key Operation Rules

## ⚠️ Prohibited Auto-Completion (Must Wait for User Confirmation)

### Experiment Template: Do Not Auto-Call et-complete

After creating/copying a template, **absolutely do not auto-call `et-complete`**:
- After completion, the template becomes read-only (state=1) and cannot be edited
- Only call when the user explicitly says "complete" or "submit"
- After creation, ask: "Template created. Would you like to complete it now or continue editing?"

**Lesson learned:** On 2026-03-09, unauthorized call made the template read-only

---

### Experiment Order: Do Not Skip Steps, Wait for Confirmation at Each Step

- "Generate result" = Call `addExperimentResult` to save results, **not** complete the experiment order
- After completing one step, **wait for user confirmation** before proceeding to the next

---

### Before Creating Experiment Template: Must Ask 3 Key Pieces of Information in Order

Before calling `et-create`, **must ask and confirm in order**:
1. Experiment type → `et-exp-types`
2. Experiment group → `et-groups`
3. Approver → `et-approvers <group_id>`

**Prohibited:** Auto-inferring, reusing previous selections, creating directly before user confirmation

---

### Before Creating Experiment Order: Must Ask for Protocol and Experimenter

Each time an experiment order is created, **must ask first**:
1. Protocol → `get-create-experiment-options <suffix>`
2. Experimenter

**Prohibited:** Auto-inferring protocol, reusing previous selections

---

### Sample Receive: Do Not Auto-Complete When Modifying Flow Direction

- User requests "modify next flow direction" → Only call `update-receive`, **do not call `complete-receive`**

---

### Report Sending: Must Ask for Email Before Sending

Email sending flow: First `report-sending-list`, then ask for email, then `report-send-confirm`

---

## 🚫 Field Names: No Guessing Allowed

| Correct Field Name | ❌ Wrong Field Name | Description |
|-------------------|-------------------|-------------|
| `slideCode` | barCode, barcode | Sample barcode |
| `dicSampleTypeId` | sampleTypeId | Sample type ID |
| `sampleType` | dicSampleTypeName | Sample type name |
| `sampleOrderItem` | samples, items | Sample array |

**Rule:** When unsure, check documentation or existing orders first

---

## 🏥 medicalNumber Field Rules

**When creating an order:**
- ❌ **Prohibited** from fabricating medicalNumber
- ✅ **Must pass empty value**: `"medicalNumber": ""` or `null`
- System will auto-generate and return it

**When modifying an order:**
- ✅ **Must include** the medicalNumber returned by the system
- Use `order <order_id>` to query and retrieve it

---

## 📋 customFieldValue Format

| Table | Correct Format | Wrong Format |
|-------|---------------|-------------|
| Order sample `sampleOrderItem` | `[{"Remark":""}]` (array) | `{"drainageSite":"..."}` |
| Receive order sample `sampleReceiveItem` | `[{"Integrity":""}]` (array) | Object format |

**Lesson learned:** Incorrect format causes receive order completion failure

---

## 🔀 nextFlowId Format (Receive Order vs Experiment Order)

**Sample receive `update-receive`:**
- ✅ **Requires concatenation**: `nextFlowId = id + "-" + databaseTableSuffix`
- Example: `"nextFlowId": "SYLX2024000001-NAE"`

**Experiment order `experiment-save`:**
- ✅ **No concatenation needed**: Use the raw `id` value directly

**Common flow directions (receive order format):**
| Flow Direction | nextFlowId | nextFlow |
|---------------|-----------|----------|
| Nucleic Acid Extraction | SYLX2024000001-NAE | Nucleic acid extraction |
| Library Preparation | SYLX2024000007-LP | Library Preparation |
| Enrichment | SYLX2024000003-E | Enrichment |
| Sequencing | SYLX2024000008-Se | Sequencing |
| Sample Storage | SampleIn-SampleIn | Sample Storage |

---

## 📊 Order Custom Field Mapping

Call `get-order-custom-fields 104-mainTable` to get the mapping:

| Chinese Label | code |
|--------------|------|
| Clinical Diagnosis | test1 |
| Collection Time | test2 |
| Test Method | test3 |
| Submission Time | test4 |
| Barcode Number | test5 (required) |
| Submitting Institution | test6 |

---

## 🧪 databaseTableSuffix Mapping

| Prefix | suffix | Code | Name |
|--------|--------|------|------|
| HS | HS | HS | Nucleic Acid Extraction (New) |
| WK | WK | WK | Library Preparation (New) |
| FJ1129 | FJ1129 | FI | Enrichment (New) |
| SJCX | SJCX | SJCX | Sequencing |

---

## ✅ Complete QC Order

**❌ Do not use:** `transactChargeSequencingQc` (returns "The server is busy")

**✅ Correct:**
```
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

**Back to:** `../MEMORY.md`
