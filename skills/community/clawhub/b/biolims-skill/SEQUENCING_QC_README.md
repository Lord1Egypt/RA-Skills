# Sequencing QC - OpenClaw Integration Documentation

## Overview

The Sequencing QC module has been successfully integrated into OpenClaw, supporting management of sequencing quality control workflows through a conversational interface.

## Features

- QC order management (create, query, save, process)
- QC detail management (query, delete)
- Import/export functionality
- Template editing functionality
- External API support (JWT authentication)

---

## Available Commands (13)

### 1. Query QC Order List

Paginated query of sequencing QC order list.

```bash
node biolims.mjs seq-qc-list [page] [rows]
```

**Parameters:**
- `page`: Page number (optional, default 1)
- `rows`: Rows per page (optional, default 10)

**Example:**
```bash
node biolims.mjs seq-qc-list 1 10
```

**Response Example:**
```json
{
  "status": 200,
  "msg": "OK",
  "data": {
    "total": 14,
    "result": [
      {
        "id": "XJZK260213001",
        "description": null,
        "createUser": "yq",
        "createUserName": "YQ",
        "createDate": "2026-02-13 03:55:51",
        "status": "3",
        "flowcellId": null
      }
    ]
  }
}
```

---

### 2. Query QC Order Details

Query detailed information of a single sequencing QC order.

```bash
node biolims.mjs seq-qc-detail <qc_id>
```

**Parameters:**
- `qc_id`: QC order ID

**Example:**
```bash
node biolims.mjs seq-qc-detail XJZK260213001
```

---

### 3. Save QC Data

Save or update all data of a QC order, including the main table information and QC details.

```bash
node biolims.mjs save-seq-qc '<json>'
# Or read from file
node biolims.mjs save-seq-qc @qc_data.json
```

**Required Fields:**
- `sequencingQc`: QC order main table object
  - `id`: QC order ID (required, cannot be empty)
  - `description`: QC description
  - `refNo`: Reference number
  - `fcNo`: FC number
  - `machineNo`: Machine number
  - `flowcellId`: Flowcell ID
  - `status`: Status
- `sequencingQcItem`: QC detail list (optional)

**Example JSON:**
```json
{
  "sequencingQc": {
    "id": "XJZK260213001",
    "description": "First batch sequencing QC",
    "refNo": "REF001",
    "fcNo": "FC001",
    "machineNo": "Machine-01",
    "flowcellId": "FC0115001",
    "status": "3"
  },
  "sequencingQcItem": [
    {
      "id": "item-uuid-1",
      "sampleCode": "SAMPLE001",
      "orderCode": "ORD001",
      "testProjectName": "Whole Genome Sequencing",
      "method": "qualified",
      "customFieldValue": "[{\"lod_score\":\"15\"}]"
    }
  ]
}
```

---

### 4. Query QC Detail List

Paginated query of QC detail list.

```bash
node biolims.mjs seq-qc-item-list <qc_id> [page] [rows]
```

**Parameters:**
- `qc_id`: QC order ID
- `page`: Page number (optional, default 1)
- `rows`: Rows per page (optional, default 10)

**Example:**
```bash
node biolims.mjs seq-qc-item-list XJZK260213001 1 10
```

---

### 5. Delete QC Details

Delete specified QC detail records.

```bash
node biolims.mjs delete-seq-qc-item <item_ids>
```

**Parameters:**
- `item_ids`: QC detail ID list (comma-separated)

**Example:**
```bash
node biolims.mjs delete-seq-qc-item "item-uuid-1,item-uuid-2"
```

---

### 6. Process QC Order

Process a QC order (complete the workflow), changing the status from "In Progress" to "Completed".

```bash
node biolims.mjs transact-seq-qc <qc_id>
```

**Parameters:**
- `qc_id`: QC order ID

**Example:**
```bash
node biolims.mjs transact-seq-qc XJZK260213001
```

---

### 7. Export QC Data

Export QC data to an Excel file.

```bash
node biolims.mjs export-seq-qc <qc_id>
```

**Parameters:**
- `qc_id`: QC order ID

**Example:**
```bash
node biolims.mjs export-seq-qc XJZK260213001
```

---

### 8. Import QC Data

Import Excel QC data (requires multipart/form-data format).

```bash
node biolims.mjs import-seq-qc <file_path> <qc_id>
```

**Note:** This command requires file upload; it is recommended to use the frontend interface.

---

### 9. Recall QC Order

Recall a QC order, changing the status from "Completed" back to "In Progress".

```bash
node biolims.mjs recall-seq-qc <qc_id>
```

**Parameters:**
- `qc_id`: QC order ID

**Example:**
```bash
node biolims.mjs recall-seq-qc XJZK260213001
```

---

### 10. Online Template Editing

Edit QC templates online.

```bash
node biolims.mjs seq-qc-edit-template '<json>'
```

---

### 11. Get Template Import Button Action

Get template import button action configuration.

```bash
node biolims.mjs seq-qc-import-template-btn '<json>'
```

---

### 12. Import Edited Template Data

Import edited template data into a QC order.

```bash
node biolims.mjs seq-qc-import-template '<json>'
```

---

### 13. External API Update QC Items

External systems update QC items via JWT authentication.

```bash
node biolims.mjs update-seq-qc-by-sample <flowcell_id> '<samples_json>'
```

**Parameters:**
- `flowcell_id`: Flowcell ID
- `samples_json`: Sample data JSON array

**Example JSON:**
```json
[
  {
    "sample_id": "SAMPLE001",
    "method": "qualified",
    "lod_score": "15",
    "custom_field1": "value1"
  },
  {
    "sample_id": "SAMPLE002",
    "method": "unqualified"
  }
]
```

**Example:**
```bash
node biolims.mjs update-seq-qc-by-sample FC0115001 '[{"sample_id":"SAMPLE001","method":"qualified"}]'
```

---

## Workflow

### Typical QC Workflow:

```
1. Create QC order (via frontend or API)
   |
2. Query QC order list
   node biolims.mjs seq-qc-list
   |
3. View QC order details
   node biolims.mjs seq-qc-detail XJZK260213001
   |
4. View QC details
   node biolims.mjs seq-qc-item-list XJZK260213001
   |
5. Save QC data
   node biolims.mjs save-seq-qc @qc_data.json
   |
6. Process QC order (complete)
   node biolims.mjs transact-seq-qc XJZK260213001
```

---

## Status Description

| Status Value | Description | Available Actions |
|--------------|-------------|-------------------|
| 3 | In Progress | Save, delete details, process |
| 1 | Completed | Recall, export |

---

## Important Notes

### 1. Base URL Configuration

All API requests go through the Gateway; the `/biolims` prefix must be added before the endpoint path.

**Full URL Format:**
```
http://{server}:{port}/biolims/experimentalcenter/sequencingQc/{endpoint}
```

### 2. Required HTTP Headers

The following HTTP headers must be included with every request:

| Header | Required | Description |
|--------|----------|-------------|
| Content-Type | Yes | application/json;charset=UTF-8 |
| Token | Yes | User authentication token |
| accept-language | Yes | Language identifier (en or zh_CN) |
| X-XSRF-TOKEN | Yes | CSRF protection token |
| X-Sole-ID | Yes | Unique session identifier |
| X-DS | Yes | Data source identifier |

**Note:** The biolims.mjs script automatically handles these headers.

### 3. Response Format

All APIs return a unified format:

```json
{
  "status": 200,      // 200=Success, 400=Business error, 401=Unauthorized, 500=Server error
  "msg": "OK",        // Status message
  "data": { ... }     // Business data
}
```

**Paginated List Response:**
```json
{
  "status": 200,
  "msg": "OK",
  "data": {
    "total": 25,        // Total record count
    "result": [ ... ]   // Current page data array
  }
}
```

---

## Test Verification

Tested commands:
```bash
seq-qc-list - Query QC order list
seq-qc-detail - Query QC order details
seq-qc-item-list - Query QC details
```

All tests returned `status: 200`

---

## Usage Examples

### Via Command Line:
```bash
# Query QC order list
node biolims.mjs seq-qc-list 1 10

# Query specific QC order details
node biolims.mjs seq-qc-detail XJZK260213001

# Query QC details
node biolims.mjs seq-qc-item-list XJZK260213001 1 20

# Save QC data
node biolims.mjs save-seq-qc @qc_data.json

# Process QC order
node biolims.mjs transact-seq-qc XJZK260213001
```

### Via OpenClaw Conversation:
```
User: View all sequencing QC orders
Bot: [Executes seq-qc-list]

User: View details of QC order XJZK260213001
Bot: [Executes seq-qc-detail XJZK260213001]

User: View details of QC order XJZK260213001
Bot: [Executes seq-qc-item-list XJZK260213001]

User: Process QC order XJZK260213001
Bot: [Executes transact-seq-qc XJZK260213001]
```

---

## Related Documentation

- Original design document: `SequencingQc_Module_Design_Document.html`
- Experiment Center documentation: `EXPERIMENT_CENTER_README.md`
- Full command list: `EXPERIMENT_CENTER_FULL_COMMANDS.md`

---

## Support

For help, please refer to:
- This document - Sequencing QC usage guide
- API original documentation - Detailed interface specifications
- OpenClaw conversation - Use commands directly

All Sequencing QC features are available through OpenClaw conversation!
