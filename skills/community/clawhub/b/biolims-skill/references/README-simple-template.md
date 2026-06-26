# Simplified Experiment Template Creation Guide (Updated 2026-03-10)

## 📋 Overview

**Simplified template structure:** 1 step + 2 components (detail table + result table), suitable for standard experiment workflows.

This structure is the **minimum viable configuration** for Bio-LIMS experiment templates, suitable for standardized experiments that don't require custom fields.

---

## 🚀 Quick Creation Flow

### Step 1: Query Available Experiment Types

```bash
node biolims.mjs experiment-type-config-list 1 20
```

**Response example:**
```json
{
  "status": 200,
  "data": {
    "result": [
      {
        "id": "SYLX2026000001",
        "experimentalTypeName": "Protein Detection",
        "databaseTableSuffix": "WBTA"
      },
      {
        "id": "SYLX2026000002",
        "experimentalTypeName": "Drug Administration & Observation",
        "databaseTableSuffix": "DAAM"
      }
      // ... more types
    ]
  }
}
```

### Step 2: Generate Template JSON File

Use the helper script to auto-generate a properly formatted JSON file:

```bash
node /home/biolims/.openclaw/workspace/skills/biolims/scripts/create-simple-template.js \
  "First Drug Administration" \
  SYLX2026000002 \
  GLY \
  admin \
  Administrator
```

**Parameter description:**
| Parameter | Description | Required | Default |
|-----------|-------------|----------|---------|
| Template name | Name of the template | Required | - |
| Experiment type ID | From experiment-type-config-list | Required | - |
| Experiment group ID | Usually GLY (Admin personnel group) | Required | - |
| Approver ID | Approver username | Optional | approver |
| Approver name | Approver nickname | Optional | Administrator |

**Output example:**
```
✅ Template JSON file generated

📄 File path: /home/biolims/.openclaw/workspace/temp/create-et-2026-03-10T14-20-00.json

📋 Template info:
   Name: First Drug Administration
   Type: Drug Administration & Observation (SYLX2026000002)
   Group: Admin Personnel Group (GLY)
   Approver: Administrator (admin)

🚀 Next step:
   node biolims.mjs et-create @/home/biolims/.openclaw/workspace/temp/create-et-2026-03-10T14-20-00.json
```

### Step 3: Create Template

```bash
node biolims.mjs et-create @/home/biolims/.openclaw/workspace/temp/create-et-<timestamp>.json
```

**Success response:**
```json
{
  "status": 200,
  "msg": "OK",
  "data": {
    "id": "ET2026000014",
    "templateName": "First Drug Administration",
    "state": "3",
    "statusName": "New"
  }
}
```

---

## 📊 Common Experiment Type Reference

| ID | Name | Database Suffix | Code |
|----|------|----------------|------|
| SYLX2026000001 | Protein Detection | WBTA | WB |
| SYLX2026000002 | Drug Administration & Observation | DAAM | DA |
| SYLX2026000003 | Animal Modeling | ANTI | AT |
| SYLX2026000004 | Cell Phenotype | FCCC | FC |
| SYLX2026000005 | Molecular Detection | RPRP | MC |
| SYLX2026000006 | Drug Treatment | CTTA | CA |
| SYLX2026000007 | Cell Culture | MCCP | CP |
| SYLX2026000008 | Cell Operations | MCLT | CT |

---

## 🔧 Template Structure Details

### Three-Level Structure of Simplified Template

```
Template
└── Step 1 (keyId=0)
    ├── Detail Table (detailTable, keyId=0)
    │   └── 16 predefined columns (sample code, sample type, test items, etc.)
    └── Result Table (resultTable, keyId=1)
        └── 11 predefined columns (volume, total, result, next flow, etc.)
```

### Detail Table Predefined Columns

| Column Name | Field | Editable |
|-------------|-------|----------|
| Orig Sample ID | originalSampleCode | No |
| Sample ID | sampleCode | No |
| Sample Type | sampleType | No |
| Sample Type ID | sampleTypeId | No (hidden) |
| Test Item | testProjectName | No |
| Product Type | productType | No |
| Product Qty | productNum | No |
| Sample Mixing | mixNumber | No |
| index | indexCode | No |
| Remaining Qty | sumTotal | Yes (number) |
| Unit | sampleUnit | No |
| Storage Status | storageState | No |
| Detection Gene | detectionGene | No |
| Is Split | isSplit | No |
| Split Quantity | splitQuantity | No |
| Split Product | splitProportion | No |

### Result Table Predefined Columns

| Column Name | Field | Editable |
|-------------|-------|----------|
| Orig Sample ID | originalSampleCode | No |
| Sample ID | sampleCode | No |
| Sample Type | sampleType | No |
| Test Item | testProjectName | No |
| Volume | volume | Yes (number) |
| Total | total | Yes (number) |
| Unit | sampleUnit | No |
| Next Flow | nextFlow | Yes (required) |
| Result | result | Yes (required) |
| Submit to QC | tjzk | No |
| Detection Gene | detectionGene | No |

---

## ⚠️ Notes

1. **Template state transitions:**
   - New (state=3) → In Process (state=20) → Complete (state=1)
   - Only templates with state=3 can be edited
   - Upon completion, resultTable custom fields are automatically registered to the metadata table

2. **Approver configuration:**
   - Approver must be an existing user in the system
   - Use `et-approvers GLY` to query available approver list

3. **Experiment group configuration:**
   - Default uses GLY (Admin Personnel Group)
   - Use `et-groups` to query all experiment groups

4. **Template naming:**
   - Component labels of the same type within the same step cannot be duplicated
   - Template name should clearly describe the experiment content

---

## 🔗 Related Documentation

- **Complete API documentation:** `api-experiment-template.md`
- **Script location:** `/home/biolims/.openclaw/workspace/skills/biolims/scripts/create-simple-template.js`
- **Template output directory:** `/home/biolims/.openclaw/workspace/temp/`

---

## 💡 Usage Examples

### Example 1: Create Protein Detection Template

```bash
# 1. Generate JSON
node create-simple-template.js "Standard Protein Extraction Process" SYLX2026000001 GLY

# 2. Create template
node biolims.mjs et-create @/home/biolims/.openclaw/workspace/temp/create-et-*.json
```

### Example 2: Create Cell Culture Template

```bash
# 1. Generate JSON
node create-simple-template.js "Cell Subculture" SYLX2026000007 GLY admin Administrator

# 2. Create template
node biolims.mjs et-create @/home/biolims/.openclaw/workspace/temp/create-et-*.json
```

### Example 3: View Created Templates

```bash
node biolims.mjs et-list 1 10
```

### Example 4: View Template Details

```bash
node biolims.mjs et-detail ET2026000014 edit
```

---

**Last updated:** 2026-03-10
**Version:** v1.0
