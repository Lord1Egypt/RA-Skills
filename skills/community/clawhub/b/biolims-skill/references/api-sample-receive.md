# Bio-LIMS Sample Receive API Reference (v2.0)

Clinical Sample Receive Module API Reference Document

**Module path**: BioTechLeague_SampleCenter/SampleCenterClinicalReceive
**Last updated**: 2026-02-09

---

## API Endpoint List

### Core Endpoints

| Endpoint Path | Method | Description | Command |
|--------------|--------|-------------|---------|
| `/samplecenter/clinicalSampleReceive/getSampleReceiveList` | POST | Paginated receive order list query | `receive-list` |
| `/samplecenter/clinicalSampleReceive/getSampleReceive` | POST | Query single receive order details | `receive` |
| `/samplecenter/clinicalSampleReceive/getSampleReceiveItemList` | POST | Paginated sample receive detail query | `receive-samples` |
| `/samplecenter/clinicalSampleReceive/saveOrUpdateAllData` | POST | Save or update receive order | `create-receive`, `update-receive` |
| `/samplecenter/clinicalSampleReceive/completeTask` | POST | Complete receive order | `complete-receive` |

### Barcode Scanning Endpoints

| Endpoint Path | Method | Description | Command |
|--------------|--------|-------------|---------|
| `/samplecenter/clinicalSampleReceive/scanBarcode` | POST | Scan barcode to get sample info | `scan-barcode` |
| `/samplecenter/clinicalSampleReceive/scanOrderCode` | POST | Scan order code to get unreceived samples | `scan-order` |
| `/samplecenter/clinicalSampleReceive/getOrderInfo` | POST | Get available order list | `get-orders-for-receive` |

### Sample Operation Endpoints

| Endpoint Path | Method | Description | Command |
|--------------|--------|-------------|---------|
| `/samplecenter/clinicalSampleReceive/deleteSampleReceiveItem` | POST | Delete sample receive detail | `delete-receive-item` |

### Dropdown/Query Endpoints

| Endpoint Path | Method | Description | Command |
|--------------|--------|-------------|---------|
| `/samplecenter/clinicalSampleReceive/getExpressCompanyList` | POST | Get express company list | `get-express-companies` |
| `/samplecenter/clinicalSampleReceive/getDicListByTypeId` | POST | Get dictionary data | `get-dictionary` |
| `/samplecenter/clinicalSampleReceive/getSampleTypeList` | POST | Get sample type list | `get-sample-types-for-receive` |
| `/samplecenter/clinicalSampleReceive/getNextFlowListNew` | POST | Get next flow direction list | `get-next-flows` |
| `/samplecenter/clinicalSampleReceive/getUnitList` | POST | Get unit list | `get-units` |
| `/samplecenter/clinicalSampleReceive/getApproverList` | POST | Get approver list | `get-approvers` |
| `/samplecenter/clinicalSampleReceive/getProductList` | POST | Get test items list | `get-products` |

### Well Plate Management Endpoints

| Endpoint Path | Method | Description | Command |
|--------------|--------|-------------|---------|
| `/samplecenter/clinicalSampleReceive/autoAddBoard` | POST | Auto-add well plate | `auto-add-board` |
| `/samplecenter/clinicalSampleReceive/clearHolePlate` | POST | Clear well plate | `clear-hole-plate` |
| `/samplecenter/clinicalSampleReceive/deleteHolePlate` | POST | Delete well plate | `delete-hole-plate` |
| `/samplecenter/clinicalSampleReceive/changeSampleLocation` | POST | Change sample location | `change-sample-location` |

### Import/Export Endpoints

| Endpoint Path | Method | Description | Command |
|--------------|--------|-------------|---------|
| `/samplecenter/clinicalSampleReceive/parseReceiveSheetFile` | POST | Parse Excel file | `parse-receive-file` |
| `/samplecenter/clinicalSampleReceive/batchImport` | POST | Batch import samples | `batch-import` |
| `/samplecenter/clinicalSampleReceive/batchExport` | POST | Batch export samples | `batch-export-receive` |
| `/samplecenter/clinicalSampleReceive/validTemplateInformation` | POST | Query print templates | `get-print-templates` |
| `/samplecenter/clinicalSampleReceive/println` | POST | Print | `print-receive` |

### Custom Field Endpoints

| Endpoint Path | Method | Description | Command |
|--------------|--------|-------------|---------|
| `/system/custom/selAllFields` | GET | Get custom field mapping | `get-custom-fields` |

---

## Endpoint Detailed Description

### 1. Query Receive Order List

**Command**: `receive-list [page] [rows]`

**Endpoint**: `POST /samplecenter/clinicalSampleReceive/getSampleReceiveList`

**Request body**:
```json
{
    "bioTechLeaguePagingQuery": {
        "page": 1,
        "rows": 10,
        "sort": {},
        "query": []
    }
}
```

**Response structure**:
```json
{
    "status": 200,
    "data": {
        "result": [
            {
                "id": "SR202401180001",
                "code": "SR202401180001",
                "name": "Clinical Sample Receive Order",
                "acceptDate": "2024-01-18 10:00:00",
                "state": "3",
                "stateName": "New",
                "creatorNickname": "Operator",
                "createTime": "2024-01-18 09:30:00",
                "itemCodes": "S001,S002,S003",
                "itemBarCodes": "BC001,BC002,BC003",
                "customFieldValue": "{}"
            }
        ],
        "total": 50
    }
}
```

---

### 2. Query Single Receive Order Details

**Command**: `receive <receive_id>`

**Endpoint**: `POST /samplecenter/clinicalSampleReceive/getSampleReceive`

**Request body**:
```json
{
    "id": "SR202401180001"
}
```

**Response structure**:
```json
{
    "status": 200,
    "data": {
        "result": {
            "id": "SR202401180001",
            "code": "SR202401180001",
            "name": "Clinical Sample Receive Order",
            "acceptDate": "2024-01-18 10:00:00",
            "expressNum": "SF1234567890",
            "expressCompanyId": "EC001",
            "expressCompanyName": "SF Express",
            "transportTypeId": "TT001",
            "transportTypeName": "Cold chain transport",
            "isBoard": "1",
            "state": "3",
            "stateName": "New",
            "creatorUsername": "user01",
            "creatorNickname": "Operator",
            "createTime": "2024-01-18 09:30:00",
            "customFieldValue": "{}"
        }
    }
}
```

---

### 3. Query Sample Receive Detail List

**Command**: `receive-samples <receive_id> [page] [rows]`

**Endpoint**: `POST /samplecenter/clinicalSampleReceive/getSampleReceiveItemList`

**Request body**:
```json
{
    "id": "SR202401180001",
    "bioTechLeaguePagingQuery": {
        "page": 1,
        "rows": 50,
        "sort": {},
        "query": []
    }
}
```

**Response structure**:
```json
{
    "status": 200,
    "data": {
        "result": [
            {
                "id": "ITEM001",
                "sampleCode": "S001",
                "barCode": "BC001",
                "orderCode": "ORD001",
                "patientName": "John Smith",
                "gender": "1",
                "dicSampleType": "Whole Blood",
                "dicSampleTypeId": "T250724002",
                "productId": "PROD001",
                "productName": "Genetic Testing",
                "samplingDate": "2024-01-18 09:00:00",
                "sampleNum": "5",
                "unit": "ml",
                "isGood": "1",
                "nextFlow": "Storage",
                "nextFlowId": "FLOW001",
                "state": "3",
                "creatorNickname": "Operator",
                "createTime": "2024-01-18 09:30:00",
                "customFieldValue": "{}"
            }
        ],
        "total": 15
    }
}
```

---

### 4. Create/Update Receive Order

**Command**: `create-receive '<json>'` or `update-receive '<json>'`

**Endpoint**: `POST /samplecenter/clinicalSampleReceive/saveOrUpdateAllData`

**Request body structure**:
```json
{
    "sampleReceive": {
        "id": "SR202401180001",
        "name": "Clinical Sample Receive Order",
        "acceptDate": "2024-01-18 10:00",
        "expressNum": "SF1234567890",
        "expressCompanyId": "EC001",
        "expressCompanyName": "SF Express",
        "transportTypeId": "TT001",
        "transportTypeName": "Cold chain transport",
        "isBoard": "1",
        "customFieldValue": "{}"
    },
    "sampleReceiveItems": [
        {
            "sampleCode": "S001",
            "barCode": "BC001",
            "orderCode": "ORD001",
            "patientName": "John Smith",
            "gender": "1",
            "dicSampleType": "Whole Blood",
            "dicSampleTypeId": "T250724002",
            "productId": "PROD001",
            "productName": "Genetic Testing",
            "sampleNum": "5",
            "unit": "ml",
            "isGood": "1",
            "nextFlow": "Storage",
            "nextFlowId": "FLOW001",
            "customFieldValue": "{}"
        }
    ],
    "addBoardInfo": "{\"banHao\":\"P001\",\"rowNum\":8,\"colNum\":12}"
}
```

**Important notes**:
- `sampleReceive` - Receive order main table object (required)
- `sampleReceiveItems` - Sample receive detail list (optional, array)
- `addBoardInfo` - Well plate information (optional, JSON string format)

**Required fields**:
- `acceptDate` - Receive time (required)
- `isBoard` - In plate (required, "0"=No, "1"=Yes)
- If `isBoard = "1"`, plate number cannot be empty

**Response structure**:
```json
{
    "status": 200,
    "msg": "Save successful",
    "data": {
        "result": {
            "id": "SR202401180001"
        }
    }
}
```

---

### 5. Complete Receive Order

**Command**: `complete-receive <receive_id>`

**Endpoint**: `POST /samplecenter/clinicalSampleReceive/completeTask?id=<receive_id>`

**Request method**: URL parameter

**Example**:
```
POST /samplecenter/clinicalSampleReceive/completeTask?id=SR202401180001
```

**Response structure**:
```json
{
    "status": 200,
    "msg": "Completed successfully"
}
```

**Business rules**:
- Only receive orders with status "New (3)" can be completed
- After completion, status changes to "Complete (1)"
- After completion, receive order and samples cannot be edited

---

### 6. Scan Barcode

**Command**: `scan-barcode <barcode> <receive_id> [acceptDate] [isBoard]`

**Endpoint**: `POST /samplecenter/clinicalSampleReceive/scanBarcode`

**⚠️ Important: Must include complete sampleReceive object**

**Request body (correct format)**:
```json
{
    "sampleReceive": {
        "id": "SR202401180001",
        "acceptDate": "2024-01-18 10:00",
        "isBoard": "1"
    },
    "barCode": "BC20240118001"
}
```

**Command parameter description:**
- `barcode`: Barcode to scan
- `receive_id`: Receive order ID
- `acceptDate`: Optional, receive time. If not provided, script auto-queries the receive order
- `isBoard`: Optional, in plate (0/1). If not provided, script auto-queries the receive order

**Usage examples:**
```bash
# Simplified usage (recommended) - script auto-queries receive order info
biolims.sh scan-barcode BC20240118001 SR202401180001

# Full usage - manually provide all parameters
biolims.sh scan-barcode BC20240118001 SR202401180001 "2024-01-18 10:00" 1
```

**Response structure**:
```json
{
    "status": 200,
    "data": {
        "result": {
            "sampleCode": "S001",
            "barCode": "BC20240118001",
            "orderCode": "ORD001",
            "patientName": "John Smith",
            "gender": "1",
            "dicSampleType": "Whole Blood",
            "productName": "Genetic Testing"
        }
    }
}
```

**Business rules**:
- Validates barcode exists in order sample details
- Checks if barcode has been received by another receive order
- If `receive_id` is provided, excludes duplicate check for current receive order

---

### 7. Scan Order Code

**Command**: `scan-order <order_code> [receive_id] [acceptDate] [isBoard]`

**Endpoint**: `POST /samplecenter/clinicalSampleReceive/scanOrderCode`

**⚠️ Important: Must include complete sampleReceive object and ids array**

**Request body (correct format)**:
```json
{
    "sampleReceive": {
        "id": "SR202401180001",
        "acceptDate": "2024-01-18 10:00",
        "isBoard": "0"
    },
    "ids": ["ORD202401180001"]
}
```

**Command parameter description:**
- `order_code`: Order code to scan
- `receive_id`: Optional, receive order ID. Default "NEW" (create new receive order)
- `acceptDate`: Optional, receive time. If not provided:
  - receive_id = "NEW": Uses current time
  - receive_id = existing ID: Auto-queries receive order
- `isBoard`: Optional, in plate (0/1). Default 0

**Usage examples:**
```bash
# Create new receive order (using current time)
biolims.sh scan-order ORD202401180001

# Add to existing receive order (auto-query info)
biolims.sh scan-order ORD202401180001 SR202401180001

# Create new receive order (specify time and plate)
biolims.sh scan-order ORD202401180001 NEW "2024-01-18 10:00" 1

# Add to existing receive order (manually provide all parameters)
biolims.sh scan-order ORD202401180001 SR202401180001 "2024-01-18 10:00" 0
```

**Special status codes:**
- `status: 2004` - Insufficient well plate positions. Need to ask user whether to auto-create new well plate

**Response structure**:
```json
{
    "status": 200,
    "data": {
        "result": [
            {
                "sampleCode": "S001",
                "barCode": "BC001",
                "orderCode": "ORD202401180001",
                "patientName": "John Smith",
                "gender": "1",
                "dicSampleType": "Whole Blood",
                "productName": "Genetic Testing"
            },
            {
                "sampleCode": "S002",
                "barCode": "BC002",
                "orderCode": "ORD202401180001",
                "patientName": "Jane Doe",
                "gender": "0",
                "dicSampleType": "Plasma",
                "productName": "Genetic Testing"
            }
        ]
    }
}
```

**Business rules**:
- Only selects orders with "Complete" status
- Batch retrieves all unreceived samples under the order
- If `receive_id` is provided, excludes samples already received by current receive order

---

### 8. Get Available Order List

**Command**: `get-orders-for-receive [page] [rows]`

**Endpoint**: `POST /samplecenter/clinicalSampleReceive/getOrderInfo`

**Request body**:
```json
{
    "bioTechLeaguePagingQuery": {
        "page": 1,
        "rows": 10,
        "sort": {},
        "query": []
    }
}
```

**Response structure**:
```json
{
    "status": 200,
    "data": {
        "result": [
            {
                "id": "ORD202401180001",
                "firstName": "John",
                "lastName": "Smith",
                "productName": "Genetic Testing",
                "state": "1",
                "stateName": "Complete",
                "createTime": "2024-01-18 08:00:00"
            }
        ],
        "total": 25
    }
}
```

**Business rules**:
- Used for selecting orders in order code mode
- Returns available orders for user selection
- Only shows completed orders

---

### 9. Delete Sample Receive Detail

**Command**: `delete-receive-item <receive_id> <item_id1,item_id2,...> [isBoard]`

**Endpoint**: `POST /samplecenter/clinicalSampleReceive/deleteSampleReceiveItem`

**⚠️ Important: Correct request body format**

Field names must match exactly, otherwise error code 2001 will be returned:

```json
{
    "ids": ["ITEM001", "ITEM002"],
    "sampleReceiveId": "KXJY2602090002",
    "sampleReceive": {
        "id": "KXJY2602090002",
        "isBoard": "0"
    }
}
```

**Common wrong field names (will cause 2001 error):**
- ❌ `sampleReceiveItemsId` - Wrong
- ❌ `itemIds` - Wrong
- ❌ `id` (used alone) - Wrong
- ✅ `ids` - Correct

**Command parameter description:**
- `receive_id`: Receive order ID
- `item_id1,item_id2,...`: Sample detail IDs to delete (comma-separated)
- `isBoard`: Optional, in plate (0=No, 1=Yes), default 0

**Usage examples:**
```bash
# Delete single sample detail (not in plate)
biolims.sh delete-receive-item KXJY2602090002 aaa00000000000000000000000000001

# Delete multiple sample details (not in plate)
biolims.sh delete-receive-item KXJY2602090002 ITEM001,ITEM002

# Delete sample detail (in plate)
biolims.sh delete-receive-item KXJY2602090002 ITEM001 1
```

**Response structure**:
```json
{
    "status": 200,
    "msg": "OK",
    "data": { ... }
}
```

**Error response (wrong field names):**
```json
{
    "status": 2001,
    "msg": "Please select the record(s) data to be deleted"
}
```

**Business rules**:
- Receive order must be in editable state (New/3)
- Only receive orders with "New" status can have sample details deleted
- Can batch delete multiple sample details
- Field names must strictly match: `ids`, `sampleReceiveId`, `sampleReceive`

---

## Custom Field API

### Query Custom Field Definitions

**Endpoint**: `GET /system/custom/selAllFields?flag=<flag>`

**Flag identifiers**:
- `121-mainTable` - Receive order main table custom fields
- `121-receiveTable` - Sample detail sub-table custom fields

**Example**:
```bash
GET /system/custom/selAllFields?flag=121-mainTable
```

**Response structure**:
```json
{
    "status": 200,
    "data": {
        "Storage Condition": "storageCondition",
        "Sample Source": "sampleSource",
        "Collection Method": "collectionMethod"
    }
}
```

**Usage**:
1. Both receive orders and sample details have their own `customFieldValue` field (JSON string format)
2. Call this API to get field mapping
3. Convert API field name → Display name for presentation
4. `customFieldValue` needs `JSON.parse()` first, then combine with mapping for parsing

---

## Status Enums

### Receive Order Status

| Code | Status Name | Description |
|------|------------|-------------|
| `3` | New | Editable, can save, can complete |
| `1` | Complete | Read-only, cannot edit |

### Gender

| Code | Display |
|------|---------|
| `0` | Female |
| `1` | Male |
| `2` | Unknown |

### isGood (Normal)

| Code | Display |
|------|---------|
| `1` | Qualified |
| `0` | Unqualified |

### isBoard (In Plate)

| Code | Display |
|------|---------|
| `1` | Yes |
| `0` | No |

---

## Error Handling

All endpoints follow a unified response format:

**Success response**:
```json
{
    "status": 200,
    "msg": "Success",
    "data": { ... }
}
```

**Failure response**:
```json
{
    "status": 403,
    "msg": "Insufficient permissions"
}
```

**Common error codes**:
- `200` - Success
- `401` - Token expired, need to re-login
- `403` - Insufficient permissions
- `500` - Server error

---

## Business Rules Summary

### Creating Receive Order

1. **Required fields**:
   - `acceptDate` - Receive time
   - `isBoard` - In plate

2. **Plate validation** (when `isBoard = "1"`):
   - Plate number cannot be empty
   - Plate type must be selected

3. **Numeric validation**:
   - `sampleNum` (sampling volume) cannot be less than 0
   - `periodOfValidity` (validity period) cannot be less than 0

4. **Uniqueness validation**:
   - Barcode cannot be duplicated within the same receive order
   - Plate number cannot be duplicated within the same receive order

### Completing Receive Order

1. Only receive orders with status "New (3)" can be completed
2. After completion, status changes to "Complete (1)"
3. After completion, receive order and all samples cannot be edited

### Barcode Scanning

1. **Barcode scanning**:
   - Barcode must exist in order sample details
   - Barcode cannot have been received by another receive order

2. **Order code scanning**:
   - Can only select orders with "Complete" status
   - Auto-retrieves all unreceived samples

---

## Dropdown/Query Endpoint Details

### 10. Get Express Company List

**Command**: `get-express-companies [page] [rows]`

**Endpoint**: `POST /samplecenter/clinicalSampleReceive/getExpressCompanyList`

**Request body**:
```json
{
    "bioTechLeaguePagingQuery": {
        "page": 1,
        "rows": 100,
        "sort": {},
        "query": []
    }
}
```

**Response structure**:
```json
{
    "status": 200,
    "data": {
        "result": [
            { "id": "EC001", "name": "SF Express", "code": "SF" },
            { "id": "EC002", "name": "YTO Express", "code": "YTO" }
        ],
        "total": 10
    }
}
```

---

### 11. Get Dictionary Data

**Command**: `get-dictionary <type_id> [page] [rows]`

**Endpoint**: `POST /samplecenter/clinicalSampleReceive/getDicListByTypeId`

**Request body**:
```json
{
    "typeId": "transport_type",
    "bioTechLeaguePagingQuery": {
        "page": 1,
        "rows": 100,
        "sort": {},
        "query": []
    }
}
```

**Common dictionary types**:
- `transport_type` - Transport method

**Response structure**:
```json
{
    "status": 200,
    "data": {
        "result": [
            { "id": "TT001", "name": "Cold chain transport" },
            { "id": "TT002", "name": "Room temperature transport" }
        ],
        "total": 5
    }
}
```

---

### 12. Get Sample Type List (Sample Receive)

**Command**: `get-sample-types-for-receive [page] [rows]`

**Endpoint**: `POST /samplecenter/clinicalSampleReceive/getSampleTypeList`

**Request body**:
```json
{
    "bioTechLeaguePagingQuery": {
        "page": 1,
        "rows": 100,
        "sort": {},
        "query": []
    }
}
```

**Response structure**:
```json
{
    "status": 200,
    "data": {
        "result": [
            { "id": "T250724002", "name": "Whole Blood", "code": "WB" },
            { "id": "T250724003", "name": "Plasma", "code": "PL" }
        ],
        "total": 20
    }
}
```

---

### 13. Get Next Flow Direction List

**Command**: `get-next-flows <product_id1,product_id2,...> [page] [rows]`

**Endpoint**: `POST /samplecenter/clinicalSampleReceive/getNextFlowListNew`

**⚠️ Required parameters**:
- `product_id1,product_id2,...` - **At least one product ID** (multiple comma-separated)
- If no product ID is provided, the command returns an error

**Request body**:
```json
{
    "productIdList": ["PROD001", "PROD002"],
    "bioTechLeaguePagingQuery": {
        "page": 1,
        "rows": 100,
        "sort": {},
        "query": []
    }
}
```

**Usage examples**:
```bash
# Single product ID
biolims.sh get-next-flows PROD001

# Multiple product IDs (intersection)
biolims.sh get-next-flows PROD001,PROD002,PROD003

# Specify pagination
biolims.sh get-next-flows PROD001 1 50
```

**Business rules**:
- **Product ID required**: Must provide at least one product ID
- **Intersection logic**: With multiple product IDs, returns flow directions supported by all products (intersection)
  - Example: PROD001 supports [Storage, Testing, Preservation], PROD002 supports [Testing, Preservation, Archiving] → Returns [Testing, Preservation]
- **Single product**: Returns all available next flow directions for that product
- **Empty result**: If no common flow directions, returns empty list

**OpenClaw AI usage guide**:
1. ⚠️ **Never** call this endpoint without a product ID
2. If user hasn't provided a product ID, must proactively ask: "Please provide the test item product ID"
3. Can call `get-products` first to query available product list
4. Get product ID from context (e.g. from `productId` field in sample info)

**Response structure**:
```json
{
    "status": 200,
    "data": {
        "result": [
            { "id": "FLOW001", "name": "Storage" },
            { "id": "FLOW002", "name": "QC" }
        ],
        "total": 5
    }
}
```

---

### 14. Get Unit List

**Command**: `get-units [page] [rows]`

**Endpoint**: `POST /samplecenter/clinicalSampleReceive/getUnitList`

**Request body**:
```json
{
    "bioTechLeaguePagingQuery": {
        "page": 1,
        "rows": 100,
        "sort": {},
        "query": []
    }
}
```

**Response structure**:
```json
{
    "status": 200,
    "data": {
        "result": [
            { "id": "U001", "name": "ml" },
            { "id": "U002", "name": "μl" },
            { "id": "U003", "name": "g" }
        ],
        "total": 10
    }
}
```

---

### 15. Get Approver List

**Command**: `get-approvers [keyword] [page] [rows]`

**Endpoint**: `POST /samplecenter/clinicalSampleReceive/getApproverList`

**Request body**:
```json
{
    "entity": "Wang",
    "bioTechLeaguePagingQuery": {
        "page": 1,
        "rows": 10,
        "sort": {},
        "query": []
    }
}
```

**Parameter description**:
- `entity` - Search keyword (username or nickname), optional

**Response structure**:
```json
{
    "status": 200,
    "data": {
        "result": [
            { "username": "user01", "nickname": "Dr. Wang" },
            { "username": "user02", "nickname": "Wang Li" }
        ],
        "total": 15
    }
}
```

---

### 16. Get Test Items List

**Command**: `get-products [page] [rows]`

**Endpoint**: `POST /samplecenter/clinicalSampleReceive/getProductList`

**Request body**:
```json
{
    "bioTechLeaguePagingQuery": {
        "page": 1,
        "rows": 100,
        "sort": {},
        "query": []
    }
}
```

**Response structure**:
```json
{
    "status": 200,
    "data": {
        "result": [
            { "id": "PROD001", "name": "Genetic Testing", "code": "GT001" },
            { "id": "PROD002", "name": "Cancer Screening", "code": "CS001" }
        ],
        "total": 50
    }
}
```

---

## Well Plate Management Endpoint Details

### 17. Auto-Add Well Plate

**Command**: `auto-add-board <receive_id> <row_num> <col_num> <plate_number>`

**Endpoint**: `POST /samplecenter/clinicalSampleReceive/autoAddBoard`

**Request body**:
```json
{
    "id": "SR202401180001",
    "rowNum": 8,
    "colNum": 12,
    "banHao": "P001"
}
```

**Parameter description**:
- `row_num` - Number of rows (e.g. 8)
- `col_num` - Number of columns (e.g. 12)
- `plate_number` - Plate number (e.g. P001)

**Common well plate types**:
- 8x12 = 96-well plate
- 4x6 = 24-well plate
- 16x24 = 384-well plate

**Business rules**:
- Auto-adds well plate based on current sample count
- Arranges samples into well plate positions by rules

---

### 18. Clear Well Plate

**Command**: `clear-hole-plate <receive_id> <plate_number>`

**Endpoint**: `POST /samplecenter/clinicalSampleReceive/clearHolePlate`

**Request body**:
```json
{
    "id": "SR202401180001",
    "counts": "P001"
}
```

**Business rules**:
- Clears all sample position information on the specified well plate
- Removes samples from the well plate but does not delete sample records

---

### 19. Delete Well Plate

**Command**: `delete-hole-plate <receive_id> <plate_number>`

**Endpoint**: `POST /samplecenter/clinicalSampleReceive/deleteHolePlate`

**Request body**:
```json
{
    "id": "SR202401180001",
    "counts": "P001"
}
```

**Business rules**:
- Well plates with samples cannot be deleted
- Must clear the well plate before deleting

---

### 20. Change Sample Location

**Command**: `change-sample-location <sample_item_id> <x> <y> <plate_number>`

**Endpoint**: `POST /samplecenter/clinicalSampleReceive/changeSampleLocation`

**Request body**:
```json
{
    "sampleReceiveItemId": "ITEM001",
    "x": 5,
    "y": 3,
    "counts": "P001"
}
```

**Parameter description**:
- `x` - Column position (starting from 1)
- `y` - Row position (starting from 1)
- `plate_number` - Plate number

**Business rules**:
- Called when user drags sample to new position
- Cannot move samples after receive order is completed

---

## Import/Export Endpoint Details

### 21. Parse Excel File

**Command**: `parse-receive-file <file_id> [receive_id]`

**Endpoint**: `POST /samplecenter/clinicalSampleReceive/parseReceiveSheetFile`

**Request body**:
```json
{
    "fileId": "FILE001",
    "id": "SR202401180001"
}
```

**Business rules**:
- Parses uploaded Excel template file
- Converts file content to sample receive detail data

---

### 22. Batch Export Samples

**Command**: `batch-export-receive <receive_id>`

**Endpoint**: `POST /samplecenter/clinicalSampleReceive/batchExport`

**Request body**:
```json
{
    "id": "SR202401180001"
}
```

**Business rules**:
- Batch exports sample detail data from current receive order
- Exports as Excel file

---

### 23. Query Print Templates

**Command**: `get-print-templates [page] [rows]`

**Endpoint**: `POST /samplecenter/clinicalSampleReceive/validTemplateInformation`

**Request body**:
```json
{
    "bioTechLeaguePagingQuery": {
        "page": 1,
        "rows": 100,
        "sort": {},
        "query": []
    }
}
```

**Business rules**:
- Queries valid print template information list
- Used for print function template selection

---

### 24. Print Receive Order

**Command**: `print-receive '<json>'`

**Endpoint**: `POST /samplecenter/clinicalSampleReceive/println`

**Request body**:
Specific parameter format depends on print template requirements

**Business rules**:
- Calls print function
- Requires specifying template ID and receive order ID

---

### 25. Batch Import Samples

**Command**: `batch-import '<json>'`

**Endpoint**: `POST /samplecenter/clinicalSampleReceive/batchImport`

**Request body**:
```json
{
    "id": "REC2024011800001",
    "sampleReceiveItems": [
        {
            "barCode": "BC001",
            "orderCode": "ORD001",
            "productName": "Blood Test",
            "dicSampleTypeId": "ST001",
            "sampleNum": 5,
            "unit": "mL",
            "isGood": "1",
            "method": "1",
            "nextFlow": "Testing"
        }
    ]
}
```

**Business rules**:
- Batch imports sample details to specified receive order
- Usually used with `parse-receive-file`
- After parsing Excel, call this endpoint to batch save sample data

---

### 26. Get Custom Field Mapping

**Command**: `get-custom-fields <flag>`

**Endpoint**: `GET /system/custom/selAllFields?flag={flag}`

**Parameter description**:
- `flag`: Field type identifier
  - `121-mainTable`: Receive order main table custom fields
  - `121-receiveTable`: Sample detail sub-table custom fields

**Usage examples**:
```bash
# Get receive order main table custom fields
biolims.sh get-custom-fields 121-mainTable

# Get sample detail sub-table custom fields
biolims.sh get-custom-fields 121-receiveTable
```

**Business rules**:
- System-level endpoint (`/system/custom`)
- Returns custom field display name and API field name mapping
- Used for dynamically parsing `customFieldValue` JSON field

**Response structure**:
```json
{
    "status": 200,
    "data": {
        "Storage Condition": "storageCondition",
        "Special Notes": "specialNotes",
        "Sample Source": "sampleSource"
    }
}
```

**OpenClaw Integration Flow**:
1. Login to get Token
2. Call `get-custom-fields` to get field mapping (separately for main table and sub-table)
3. Query receive order data
4. Parse fixed fields (see Chapter 9 field mapping)
5. Use field mapping to parse `customFieldValue` JSON string
6. Format and display to user

---

## Chapter 8: Custom Field System

### 8.1 Custom Field Overview

Bio-LIMS supports dynamic custom field configuration, allowing system administrators to add business-specific fields without modifying code.

**Custom field types**:
- **Main table custom fields** (`121-mainTable`): Receive order level custom information
- **Sub-table custom fields** (`121-receiveTable`): Sample detail level custom information

**Storage method**:
- Fixed fields: Actual columns in database tables
- Custom fields: Stored in `customFieldValue` field (JSON format string)

### 8.2 Custom Field API

**Endpoint**: `GET /system/custom/selAllFields?flag={121-mainTable|121-receiveTable}`

**Authentication requirements**:
- `Token`: User authentication token
- `X-DS`: Data source identifier (fixed value: `droplet`)
- `X-XSRF-TOKEN`: CSRF protection token
- `Cookie`: Cookie containing XSRF-TOKEN

**Return format**:
```json
{
    "Display Name": "apiFieldName"
}
```

Example: `{"Storage Condition": "storageCondition"}`

### 8.3 OpenClaw Integration Steps

Complete 7-step integration flow:

#### Step 1: Authentication Login
```bash
# Call login to get Token and XSRF-TOKEN
# Token auto-cached for 25 minutes
```

#### Step 2: Get Custom Field Mapping
```bash
# Get main table custom fields
mainTableFields=$(biolims.sh get-custom-fields 121-mainTable)

# Get sub-table custom fields
subTableFields=$(biolims.sh get-custom-fields 121-receiveTable)
```

#### Step 3: Query Receive Order Data
```bash
receiveData=$(biolims.sh receive REC2024011800001)
```

#### Step 4: Parse Fixed Fields
Refer to Chapter 9 field mapping table to convert API field names to English display names.

#### Step 5: Parse Enum Values
Refer to Section 9.6 enum value table to convert enum codes to readable text.

#### Step 6: Parse Main Table customFieldValue
```javascript
// Example: Parse main table custom fields
const mainCustomFields = JSON.parse(receiveData.sampleReceive.customFieldValue || '{}');
const displayCustomFields = {};

for (const [displayName, apiFieldName] of Object.entries(mainTableFields)) {
    if (mainCustomFields[apiFieldName]) {
        displayCustomFields[displayName] = mainCustomFields[apiFieldName];
    }
}
```

#### Step 7: Parse Sample Detail Custom Fields
```javascript
// Example: Parse each sample's custom fields
receiveData.sampleReceiveItems.forEach(item => {
    const itemCustomFields = JSON.parse(item.customFieldValue || '{}');
    const displayCustomFields = {};

    for (const [displayName, apiFieldName] of Object.entries(subTableFields)) {
        if (itemCustomFields[apiFieldName]) {
            displayCustomFields[displayName] = itemCustomFields[apiFieldName];
        }
    }

    item.customFieldsDisplay = displayCustomFields;
});
```

### 8.4 API Call Sequence Diagram

```
User → OpenClaw AI
              ↓
         [1. Login]
              ↓
      (Token + Cookie + XSRF)
              ↓
    [2. Get Custom Fields (Main)]
              ↓
    [3. Get Custom Fields (Sub)]
              ↓
    [4. Query Receive Data]
              ↓
    [5. Parse Fixed Fields] (Chapter 9.1-9.5)
              ↓
    [6. Parse Enums] (Chapter 9.6)
              ↓
    [7. Parse customFieldValue (Main)]
              ↓
    [8. Parse customFieldValue (Items)]
              ↓
         Format & Display
              ↓
    Display to User (English field names)
```

### 8.5 Request Header Configuration

All API requests must include the following headers:

| Header | Value | Description |
|--------|-------|-------------|
| `Content-Type` | `application/json` | JSON request body |
| `Token` | `{token}` | Authentication token obtained after login |
| `X-DS` | `droplet` | Data source identifier (fixed value) |
| `X-XSRF-TOKEN` | `{xsrf_token}` | CSRF protection token (extracted from Cookie) |
| `Cookie` | `XSRF-TOKEN={xsrf_token}` | XSRF-TOKEN in Cookie |

**Token management**:
- Token validity: 25 minutes (auto-cached)
- Token expiry: Auto re-login when API returns `status: 401`
- XSRF-TOKEN: Auto-extracted from login response Cookie

---

## Chapter 9: Complete Field Mapping Reference

This chapter provides complete mapping tables for all fixed fields, used for OpenClaw AI to correctly parse and display data.

### 9.1 Receive Order Basic Information Fields

**Field location**: `data.sampleReceive`

| API Field | English Display Name | Type | Required | Description |
|-----------|---------------------|------|----------|-------------|
| `id` | Registration ID | String | - | Receive order unique identifier (primary key) |
| `acceptDate` | Received At | DateTime | ✅ | Receive date and time |
| `isBoard` | In Plate | String | ✅ | In plate (1=Yes, 0=No) |
| `customFieldValue` | Custom Fields | JSON String | - | Custom fields (needs parsing) |

### 9.2 Express Logistics Information Fields

**Field location**: `data.sampleReceive`

| API Field | English Display Name | Type | Required | Description |
|-----------|---------------------|------|----------|-------------|
| `expressNum` | Express Bill No. | String | - | Express bill number |
| `expressCompanyName` | Courier | String | - | Express company name |
| `transportTypeName` | Shipping Method | String | - | Transport method |

### 9.3 Status Information Fields

**Field location**: `data.sampleReceive`

| API Field | English Display Name | Type | Required | Description |
|-----------|---------------------|------|----------|-------------|
| `state` | Status Code | Integer | - | Status code (3=New, 1=Complete) |
| `stateName` | Status | String | - | Status name |

**Status enum** (see 9.6):
- `3` → "New" (editable)
- `1` → "Complete" (read-only)

### 9.4 Creator and Approver Information

**Field location**: `data.sampleReceive`

| API Field | English Display Name | Type | Required | Description |
|-----------|---------------------|------|----------|-------------|
| `creatorNickname` | Created by | String | - | Creator nickname |
| `createDate` | Created At | DateTime | - | Creation time |
| `confirmerNickname` | Approved by | String | - | Approver nickname |
| `confirmDate` | Approved At | DateTime | - | Approval time |

**List aggregation fields** (only returned in list queries):
| API Field | English Display Name | Description |
|-----------|---------------------|-------------|
| `itemCodes` | Sample IDs | Sample code list (comma-separated) |
| `itemBarCodes` | Barcodes | Barcode list (comma-separated) |

### 9.5 Sample Receive Detail Fields

**Field location**: `data.sampleReceiveItems[]` (array)

**⚠️ Extremely important**: Sample data must be stored in the `sampleReceiveItems` array. Cannot use other field names (such as `samples`, `items`)!

#### 9.5.1 Sample Identification Fields

| API Field | English Display Name | Type | Required | Description |
|-----------|---------------------|------|----------|-------------|
| `id` | Item ID | String | - | Sample detail unique identifier |
| `sampleCode` | Sample ID | String | - | Sample code |
| `barCode` | Barcode | String | ✅ | Sample barcode (unique) |
| `orderCode` | Order ID | String | ✅ | Order number |

#### 9.5.2 Patient Information Fields

| API Field | English Display Name | Type | Required | Description |
|-----------|---------------------|------|----------|-------------|
| `patientName` | Name | String | - | Patient name |
| `gender` | Gender | Integer | - | Gender (0=Female, 1=Male, 2=Unknown) |
| `age` | Age | String | - | Age |
| `phone` | Phone | String | - | Phone number |

#### 9.5.3 Sample Information Fields

| API Field | English Display Name | Type | Required | Description |
|-----------|---------------------|------|----------|-------------|
| `dicSampleType` | Sample Type | String | - | Sample type name (for display) |
| `dicSampleTypeId` | Sample Type ID | String | ✅ | Sample type ID (for submission) |
| `productName` | Test Item(s) | String | ✅ | Test item name |
| `productId` | Test Item ID | String | - | Test item ID |

#### 9.5.4 Sampling Information Fields

| API Field | English Display Name | Type | Required | Description |
|-----------|---------------------|------|----------|-------------|
| `samplingDate` | Sampling Time | DateTime | - | Sampling time |
| `sampleNum` | Sampling Volume | Decimal | ✅ | Sampling volume |
| `unit` | Unit | String | ✅ | Unit |
| `periodOfValidity` | Validity Period | String | - | Validity period |

#### 9.5.5 Sample Status Fields

| API Field | English Display Name | Type | Required | Description |
|-----------|---------------------|------|----------|-------------|
| `isGood` | Normal | String | ✅ | Is normal (1=Yes, 0=No) |
| `method` | Result | String | ✅ | Result (1=Qualified, 0=Unqualified) |
| `nextFlow` | Next Step | String | ✅ | Next flow direction |

#### 9.5.6 Well Plate Position Fields

| API Field | English Display Name | Type | Required | Description |
|-----------|---------------------|------|----------|-------------|
| `counts` | Plate Number | String | Conditional* | Plate number |
| `posId` | Sample Location | String | - | Sample position (e.g.: A1, B2) |
| `x` | X Coordinate | Integer | - | X coordinate |
| `y` | Y Coordinate | Integer | - | Y coordinate |

*When `isBoard="1"`, `counts` (plate number) is required

#### 9.5.7 Custom Fields

| API Field | English Display Name | Type | Required | Description |
|-----------|---------------------|------|----------|-------------|
| `customFieldValue` | Custom Fields | JSON String | - | Sample-level custom fields (needs parsing) |

### 9.6 Enum Value Reference Table

OpenClaw must use the following enum values for code conversion:

#### Gender
| Code | English Display |
|------|----------------|
| `0` | Female |
| `1` | Male |
| `2` | Unknown |

#### Receive Status
| Code | English Display | Description |
|------|----------------|-------------|
| `3` | New | New status (editable) |
| `1` | Complete | Completed (read-only) |

#### isGood (Normal)
| Code | English Display |
|------|----------------|
| `"1"` | Yes |
| `"0"` | No |

#### method (Result)
| Code | English Display |
|------|----------------|
| `"1"` | Qualified |
| `"0"` | Unqualified |

#### isBoard (In Plate)
| Code | English Display |
|------|----------------|
| `"1"` | Yes |
| `"0"` | No |

### 9.7 Required Fields Summary

#### Receive Order Main Table Required Fields
- `acceptDate` - Received At
- `isBoard` - In Plate

#### Sample Detail Required Fields (9)
1. `orderCode` - Order ID
2. `barCode` - Barcode
3. `productName` - Test Item(s)
4. `dicSampleTypeId` - Sample Type ID
5. `sampleNum` - Sampling Volume
6. `unit` - Unit
7. `isGood` - Normal
8. `method` - Result
9. `nextFlow` - Next Step

#### Conditional Required Fields (when isBoard="1")
- `counts` - Plate Number
- Orifice Plate Type

### 9.8 Business Rules

1. **Barcode uniqueness**: Barcodes cannot be duplicated within the same receive order
2. **Barcode association**: Barcodes must exist in order sample details
3. **Plate number uniqueness**: Plate numbers cannot be duplicated within the same receive order
4. **State transition**: Status can only flow from 3 (New) to 1 (Complete), irreversible
5. **Completion restriction**: Receive orders with status 1 (Complete) cannot be edited
6. **Plate restriction**: When `isBoard="1"`, well plate information must be provided

### 9.9 Well Plate Information Fields (addBoardInfo)

**Field name**: `addBoardInfo` (not `boardInfo`!)

**Format**: JSON string

**Structure**:
```json
{
    "banHao": "P001",
    "rowNum": 8,
    "colNum": 12
}
```

**Field description**:
- `banHao`: Plate number
- `rowNum`: Number of rows (usually 8 or 16)
- `colNum`: Number of columns (usually 12 or 24)

### 9.10 OpenClaw Parsing Example Code

```javascript
// Complete example for parsing receive order data
function parseReceiveForDisplay(apiData, mainFieldsMap, subFieldsMap) {
    const receive = apiData.sampleReceive;
    const items = apiData.sampleReceiveItems || [];

    // Parse main table fixed fields
    const displayData = {
        "Registration ID": receive.id,
        "Received At": receive.acceptDate,
        "In Plate": convertBoolean(receive.isBoard),
        "Express Bill No.": receive.expressNum,
        "Courier": receive.expressCompanyName,
        "Shipping Method": receive.transportTypeName,
        "Status": receive.stateName || convertStatus(receive.state),
        "Created by": receive.creatorNickname,
        "Created At": receive.createDate,
        "Approved by": receive.confirmerNickname,
        "Approved At": receive.confirmDate
    };

    // Parse main table custom fields
    if (receive.customFieldValue) {
        const customFields = JSON.parse(receive.customFieldValue);
        for (const [displayName, apiFieldName] of Object.entries(mainFieldsMap)) {
            if (customFields[apiFieldName]) {
                displayData[displayName] = customFields[apiFieldName];
            }
        }
    }

    // Parse sample details
    displayData.samples = items.map(item => {
        const displayItem = {
            "Sample ID": item.sampleCode,
            "Barcode": item.barCode,
            "Order ID": item.orderCode,
            "Name": item.patientName,
            "Gender": convertGender(item.gender),
            "Age": item.age,
            "Phone": item.phone,
            "Sample Type": item.dicSampleType,
            "Test Item(s)": item.productName,
            "Sampling Time": item.samplingDate,
            "Sampling Volume": item.sampleNum,
            "Unit": item.unit,
            "Validity Period": item.periodOfValidity,
            "Normal": convertBoolean(item.isGood),
            "Result": convertMethod(item.method),
            "Next Step": item.nextFlow,
            "Plate Number": item.counts,
            "Sample Location": item.posId
        };

        // Parse sample custom fields
        if (item.customFieldValue) {
            const customFields = JSON.parse(item.customFieldValue);
            for (const [displayName, apiFieldName] of Object.entries(subFieldsMap)) {
                if (customFields[apiFieldName]) {
                    displayItem[displayName] = customFields[apiFieldName];
                }
            }
        }

        return displayItem;
    });

    return displayData;
}

// Helper functions: Enum conversion
function convertGender(code) {
    const map = { 0: "Female", 1: "Male", 2: "Unknown" };
    return map[code] || "Unknown";
}

function convertStatus(code) {
    const map = { 3: "New", 1: "Complete" };
    return map[code] || "Unknown";
}

function convertBoolean(value) {
    return value === "1" ? "Yes" : "No";
}

function convertMethod(value) {
    return value === "1" ? "Qualified" : "Unqualified";
}
```

---

## Last Updated

**Version**: v2.0
**Date**: 2026-02-09
**Document**: SampleCenterClinicalReceive_Module_Design_Document_V2.0.html
**New content**: Chapter 8 (Custom Field System), Chapter 9 (Complete Field Mapping Reference)
```
