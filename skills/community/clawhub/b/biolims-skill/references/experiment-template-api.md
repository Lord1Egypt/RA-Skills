# Experiment Template Module API Reference

## Command Quick Reference

| Command | Description |
|---------|-------------|
| `et-list [page] [rows] [templateName]` | Query template list |
| `et-detail <template_id> [view\|edit]` | Template details (three-level nesting) |
| `et-create '<json>' or @<filepath>` | Create/update template |
| `et-copy <template_id>` | Deep copy template |
| `et-cancel <id1> [id2 ...]` | Cancel template (creator only) |
| `et-complete <template_id>` | Complete template (state→1, read-only) |
| `et-all-completed [page] [rows]` | Query completed templates |
| `et-step-add <template_id> <step_id> <1\|0>` | Add step |
| `et-step-delete <step_uuid>` | Delete step |
| `et-formula-list/update/delete` | Formula management |
| `et-threshold-list/update/delete` | Threshold management |
| `et-exp-types [keyword]` | Experiment type list |
| `et-groups` | Experiment group list |
| `et-approvers <group_id>` | Approver list |
| `et-reagents [page] [rows]` | Reagent list |
| `et-instruments [type]` | Instrument list |
| `et-check-sql '<sql>'` | Validate SQL syntax |

**Template status:** 3=New, 20=In Process, 15=To Be Modified, 1=Complete (read-only), 30=Cancelled

---

## ⚠️ Key Business Rules

1. Each step **must** contain a detail table (detailTable) and a result table (resultTable)
2. Component labels of the same type within the same step cannot be duplicated
3. Only state=3 is editable; only the creator can cancel
4. After completion (state=1), editing is not possible; must cancel to rebuild

---

## Required Component Fields

`label`, `type`, `size`, `value`, `propList`, `menuList`, `productList`, `plate`, `formula`, `keyId`

**value format:**
| Component Type | value |
|---------------|-------|
| detailTable/resultTable/table/material/equipment | `"[]"` |
| input (single value) | `"null"` |
| editor (rich text) | HTML string |

---

## ⚠️ Material/Equipment Component value Format

**Material (each item):**
```json
[{
  "id": "mat-001",
  "name": "Material name",
  "type": {
    "id": "SJ2026000006",
    "name": "Material name",
    "spec": "",
    "pici": "",
    "predictNum": 1
  },
  "pici": "",
  "flag": false,
  "states": 0
}]
```

**Equipment (each item):**
```json
[{
  "id": "UUID",
  "name": "Instrument name",
  "orderNumber": 2,
  "note": "3",
  "code": "Equipment",
  "sysCode": "1",
  "typeId": "erwr",
  "typeName": "1",
  "state": "1",
  "createDate": "2023-01-09 15:04:43",
  "createUser": "admin",
  "keyNumber": "1-0",
  "type": {
    "id": "Equipment",
    "name": "Instrument name",
    "shebeiName": "Instrument name",
    "types": "Equipment",
    "key": "YQ260003"
  },
  "types": "Equipment",
  "flag": false,
  "states": 0,
  "changeEvent": 0
}]
```

**❗ Must include:** `name`, `type` object (with `shebeiName`), `types`, `flag`, `states`

---

## ⚠️ Well Plate (porePlate) Special Rules

value is a JSON object string that **must** contain:
- `draggLabel`
- `itemIndex`

Otherwise the page will crash!

---

## Formula Calculation (formula) Configuration

**No formula:**
```json
"formula": "{\"formX\":[],\"formY\":[]}"
```

**With formula (Tumor take rate = total * 100):**
```json
"formula": "{\"formX\":[{
  \"prop\":\"Tumortakerate\",
  \"label\":\"Tumor take rate\",
  \"value\":\"total * 100\",
  \"props\":\"total * 100\"
}],\"formY\":[]}"
```

**menuList (calculation button):**
```json
"menuList": "[{\"label\":\"Calculation\",\"type\":\"jisuan\"}]"
```

---

## Create Template Flow

**⚠️ Must ask in order:**
1. Experiment type → `et-exp-types`
2. Experiment group → `et-groups`
3. Approver → `et-approvers <group_id>`

**Prohibited:** Auto-inferring, reusing previous selections, creating directly before user confirmation

---

## ⚠️ detailTable/resultTable propList Rules (❗ Important)

**Fixed fields (headerType: "fixed") must be preserved, deletion prohibited!**

### detailTable Fixed Fields (8)
| prop | label | headerType |
|------|-------|------------|
| `originalSampleCode` | Orig Sample ID | fixed |
| `sampleCode` | Sample ID | fixed |
| `sampleType` | Sample Type | fixed |
| `testProjectName` | Product Name | fixed |
| `productType` | Product Type | fixed |
| `productNum` | Product Qty | fixed |
| `sumTotal` | Remaining Qty | fixed |
| `sampleUnit` | Unit | fixed |

### resultTable Fixed Fields (6)
| prop | label | headerType |
|------|-------|------------|
| `sampleCode` | Sample ID | fixed |
| `volume` | Volume | fixed |
| `total` | Sum | fixed |
| `sampleUnit` | Unit | fixed |
| `nextFlow` | Next Step | fixed |
| `result` | Result | fixed |

### Custom Field Rules
- **Position:** Append after fixed fields
- **headerType:** Must use `"Customize"`
- **Example:** `{"label":"Mouse ID","prop":"MouseID","type":"text","headerType":"Customize","required":"1"}`

### ❌ Wrong Example
- Replacing the entire propList with custom fields, losing all fixed fields
- Result: Template created successfully but page displays abnormally

### ✅ Correct Approach
```json
"propList": "[
  {\"label\":\"Orig Sample ID\",\"prop\":\"originalSampleCode\",\"disabled\":true,\"headerType\":\"fixed\"},
  ...(7 fixed fields)...,
  {\"label\":\"Mouse ID\",\"prop\":\"MouseID\",\"type\":\"text\",\"headerType\":\"Customize\",\"required\":\"1\"}
]"
```

---

## Template Files

- Complete example: `../templates/experiment-template-cell-culture.json`

---

**Detailed component configuration:** `api-experiment-template.md`
