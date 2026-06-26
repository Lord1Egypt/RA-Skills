# Sample Receive Field Mapping Quick Reference

**Version**: V2.0
**Last updated**: 2026-02-09

---

## Important Principles

1. **Strictly use English display names** - Do not translate to Chinese
2. **Do not consolidate fields** - Each API field has a unique display name
3. **One-to-one mapping** - Each API field displayed separately
4. **Only display fields with values** - Do not display null or empty strings
5. **Field names must be accurate when creating receive orders** - Using wrong field names will cause data loss

---

## ⚠️ Create/Update Receive Order Field Names (Extremely Important)

Field names in the JSON structure must be strictly accurate when creating or updating receive orders:

### Correct Field Names

```json
{
  "sampleReceive": { ... },           ✅ Receive order main table
  "sampleReceiveItems": [ ... ],      ✅ Sample receive details (must be this name!)
  "addBoardInfo": "..."               ✅ Well plate information (JSON string format)
}
```

### Wrong Field Names (Will Cause Data Loss)

```json
{
  "sampleReceive": { ... },
  "samples": [ ... ],                 ❌ Wrong! Sample data will not be saved
  "items": [ ... ],                   ❌ Wrong! Sample data will not be saved
  "receiveItems": [ ... ],            ❌ Wrong! Sample data will not be saved
  "boardInfo": "...",                 ❌ Wrong! Well plate data will not be saved
  "plateInfo": "..."                  ❌ Wrong! Well plate data will not be saved
}
```

**Key reminders**:
- `sampleReceiveItems` - Field name for sample receive details (cannot be simplified or renamed)
- `addBoardInfo` - Field name for well plate information (cannot be simplified or renamed)
- Using any other name will prevent that section of data from being saved to the system!

---

## Sample Receive Information

| API Field | Display Name | Example | Description |
|-----------|-------------|---------|-------------|
| `id` | Registration ID | SR202401180001 | Receive order number |
| `code` | Code | SR202401180001 | Receive order number |
| `name` | Description | Clinical Sample Receive Order | Receive order name/description |
| `acceptDate` | Received At | 2024-01-18 10:00 | **Required**, receive time |
| `isBoard` | In Plate | Yes/No | **Required**, 0→No, 1→Yes |
| `projectId` | Project ID | PROJ001 | Project ID |
| `projectName` | Project Name | Gene Testing Project | Project name |
| `classify` | Classify | Clinical | 0→Clinical, 1→Scientific Service |
| `type` | Type | Research | 0→QC Sampling, 1→Research |

---

## Express & Transport Information

| API Field | Display Name | Example |
|-----------|-------------|---------|
| `expressNum` | Express Bill No. | SF1234567890 |
| `expressCompanyId` | Courier ID | EC001 |
| `expressCompanyName` | Courier | SF Express |
| `transportTypeId` | Transport Type ID | TT001 |
| `transportTypeName` | Transportation Method | Cold chain transport |

---

## Receive Status

| API Field | Display Name | Enum Conversion |
|-----------|-------------|----------------|
| `state` | Status Code | 3/1 |
| `stateName` | Status | New/Complete |

**Status enum**:
- 3 → New
- 1 → Complete

---

## Creator & Approver

| API Field | Display Name | Description |
|-----------|-------------|-------------|
| `creatorUsername` | Creator Username | Creator username |
| `creatorNickname` | Created by | Creator nickname |
| `createTime` | Created at | Creation time |
| `confirmerUsername` | Approver Username | Approver username |
| `confirmerNickname` | Approved by | Approver nickname |
| `confirmTime` | Approved at | Completion time |

---

## List Aggregation Fields

| API Field | Display Name | Description |
|-----------|-------------|-------------|
| `itemCodes` | Sample ID | All sample codes under the receive order (comma-separated) |
| `itemBarCodes` | Barcode | All barcodes under the receive order (comma-separated) |

---

## Sample Receive Items

Located in the `sampleReceiveItems` array. One receive order can contain multiple samples.

### Basic Information

| API Field | Display Name | Example | Description |
|-----------|-------------|---------|-------------|
| `id` | ID | ITEM001 | Sample detail record ID |
| `sampleCode` | Sample ID | S001 | Sample code |
| `barCode` | Barcode | BC001 | Sample barcode |
| `orderCode` | Order ID | ORD001 | Associated order number |
| `patientName` | Name | John Smith | Patient name |
| `gender` | Gender | Male/Female/Unknown | 0→Female, 1→Male, 2→Unknown |

### Sample Type & Test Items

| API Field | Display Name | Example | Description |
|-----------|-------------|---------|-------------|
| `dicSampleType` | Sample Type | Whole Blood | Sample type name |
| `dicSampleTypeId` | Sample Type ID | T250724002 | Sample type ID |
| `productId` | Test Item ID | PROD001 | Test item ID |
| `productName` | Test Item(s) | Genetic Testing | Test item name |

### Sampling Information

| API Field | Display Name | Example | Description |
|-----------|-------------|---------|-------------|
| `samplingDate` | Sampling Time | 2024-01-18 09:00 | Sampling time |
| `sampleNum` | Sampling Volume | 5 | Sampling volume (cannot be less than 0) |
| `unit` | Unit | ml | Sampling volume unit |
| `periodOfValidity` | Validity Period (Days) | 30 | Validity period (days, cannot be less than 0) |
| `expirationDate` | Expired Date | 2024-02-18 09:00 | Expiration date |
| `samplingSite` | Sampling Position | Left arm | Sampling position |

### Quality & Flow Direction

| API Field | Display Name | Example | Description |
|-----------|-------------|---------|-------------|
| `isGood` | Normal | Yes/No | Is normal: 1→Yes, 0→No |
| `method` | Result | Qualified/Unqualified | Test result: 1→Qualified, 0→Unqualified |
| `nextFlowId` | Next Step ID | FLOW001 | Next flow direction ID |
| `nextFlow` | Next Step | Storage | Next flow direction name |

### Well Plate & Position

| API Field | Display Name | Example | Description |
|-----------|-------------|---------|-------------|
| `posId` | Sample Location | A01 | Position in well plate |
| `counts` | Plate Number | P001 | Plate number |

### Other Information

| API Field | Display Name | Example | Description |
|-----------|-------------|---------|-------------|
| `dataTraffic` | Throughput | 10X | Data throughput |
| `emrid` | EMR ID | EMR123456 | Electronic medical record ID |
| `dataSource` | Data Source | Clinical | Data source |
| `note` | Remarks | Remark info | Remarks |
| `state` | Status | 3 | Sample status |
| `projectOrder` | Project Order | PO001 | Project order |
| `creatorUsername` | Creator Username | user01 | Creator username |
| `creatorNickname` | Created by | Operator | Creator nickname |
| `createTime` | Created at | 2024-01-18 09:30:00 | Creation time |

---

## Well Plate Information

`addBoardInfo` field format (JSON string):

```json
{
    "banHao": "P001",
    "rowNum": 8,
    "colNum": 12
}
```

| Field | Display Name | Description |
|-------|-------------|-------------|
| `banHao` | Plate Number | Plate number |
| `rowNum` | Row Count | Number of rows (8, 4, etc.) |
| `colNum` | Column Count | Number of columns (12, 6, etc.) |

**Common well plate types**:
- 8x12 (96-well plate)
- 4x6 (24-well plate)
- 16x24 (384-well plate)

---

## Enum Value Reference Table

### Gender

- `0` → Female
- `1` → Male
- `2` → Unknown

### Receive Status

- `3` → New - Editable, can save, can complete
- `1` → Complete - Read-only

### isGood (Normal)

- `1` → Qualified
- `0` → Unqualified

### isBoard (In Plate)

- `1` → Yes
- `0` → No

### Classify

- `0` → Clinical
- `1` → Scientific Service

### Type

- `0` → QC Sampling
- `1` → Research

---

## Display Template

### Detailed Receive Order Information (Single)

```
=== Sample Receive Information ===
Registration ID: SR202401180001
Description: Clinical Sample Receive Order
Received At: 2024-01-18 10:00:00
In Plate: Yes
Status: New

=== Express & Transport Information ===
Express Bill No.: SF1234567890
Courier: SF Express
Transportation Method: Cold chain transport

=== Creator & Approver ===
Created by: Operator
Created at: 2024-01-18 09:30:00

=== Sample Items ===
1. Sample ID: S001
   Barcode: BC001
   Name: John Smith
   Gender: Male
   Sample Type: Whole Blood
   Test Item(s): Genetic Testing
   Sampling Volume: 5 ml
   Normal: Yes
   Result: Qualified
   Next Step: Storage
   Plate Number: P001
   Sample Location: A01
```

### Receive Order List (Multiple)

```
Found X receive orders:

1. Registration ID: SR202401180001
   Description: Clinical Sample Receive Order
   Received At: 2024-01-18 10:00:00
   Status: New
   Created by: Operator
   Created at: 2024-01-18 09:30:00
   Sample ID: S001,S002,S003
   Barcode: BC001,BC002,BC003

2. Registration ID: SR202401180002
   ...
```

---

## Common Error Examples

### ❌ Wrong Approach

```
Samples: BC001,BC002  ← Wrong: Consolidated multiple barcodes
Patient: Zhang San          ← Wrong: Translated to Chinese
Gender: Male            ← Wrong: Translated to Chinese
```

### ✅ Correct Approach

```
Barcode: BC001,BC002
Name: Zhang San
Gender: Male
```

---

## Required Fields Summary

### Required When Saving Receive Order

1. `acceptDate` - Received At
2. `isBoard` - In Plate

### Additional Required When In Plate (isBoard = "1")

1. Plate Number - Cannot be empty
2. Orifice Plate Type - Must be selected (rows x columns)

### Numeric Validation Fields

1. `sampleNum` - Sampling Volume cannot be less than 0
2. `periodOfValidity` - Validity Period cannot be less than 0

### Business Rule Validation

1. `barCode` - Barcode cannot be duplicated within the same receive order
2. `barCode` - Barcode must exist in order sample details (scan mode)
3. `counts` - Plate number cannot be duplicated within the same receive order

---

## Custom Fields Description

### Receive Order Main Table Custom Fields

- **Storage location**: `sampleReceive.customFieldValue` (JSON string)
- **Field mapping API**: `GET /system/custom/selAllFields?flag=121-mainTable`

### Sample Detail Sub-Table Custom Fields

- **Storage location**: `sampleReceiveItems[n].customFieldValue` (JSON string)
- **Field mapping API**: `GET /system/custom/selAllFields?flag=121-receiveTable`

### Processing Steps

1. Call field mapping API to get `{"Display Name": "apiFieldName"}` mapping
2. `JSON.parse()` to parse the `customFieldValue` string
3. Use the mapping to convert API field names to display names
4. Display to user

**Example**:
```javascript
// 1. Get field mapping
const mapping = await getCustomFields('121-mainTable');
// Returns: {"Storage Condition": "storageCondition", "Sample Source": "sampleSource"}

// 2. Parse custom fields
const customValues = JSON.parse(receive.customFieldValue);
// customValues = {"storageCondition": "-80°C", "sampleSource": "Clinical"}

// 3. Convert to display names
// "Storage Condition": "-80°C"
// "Sample Source": "Clinical"
```

---

**Last updated**: 2026-02-09
**Version**: 2.0
