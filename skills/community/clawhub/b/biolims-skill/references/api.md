# Bio-LIMS API Reference (v2.0)

Base URL: `http://your-server/biolims`

Authentication:
- Header: `Token: {access_token}` (automatically managed by script)
- Header: `X-DS: droplet` (data source identifier)

---

## API List

### Order Management

| Command | Endpoint | Description |
|---------|----------|-------------|
| `order <id>` | POST `/order/selectOrder` | Query specific order details |
| `order-list [page] [rows]` | POST `/order/selectAllOrderList` | Paginated order list query |
| `create-order '<json>'` | POST `/order/saveOrUpdateOrderAllData` | Create new order |
| `update-order '<json>'` | POST `/order/saveOrUpdateOrderAllData` | Update order |
| `order-samples <id>` | POST `/order/selectSampleOrderItem` | Query order sample list |
| `order-fees <id>` | POST `/order/selectFee` | Query order fee information |
| `complete-order <id>` | POST `/order/completeTask?id=xxx` | Complete order |
| `cancel-order <id>` | POST `/order/cancelTask?id=xxx` | Cancel order |

---

## Authentication API

### Login

**Endpoint**: POST `/user/Login?username={username}&password={encrypted_password}`

**Request headers**:
```
Content-Type: application/json
code: droplet
```

**Password encryption**:
- Uses AES-CBC encryption
- Key: `your-16byte-key!` (16 bytes)
- IV: `your-16byte-iv!!` (16 bytes)
- Encrypted content: `{"password":"plaintext","captCode":"","time":timestamp_ms,"secretKey":"your-secret-key"}`
- Output: Base64 encoded

**Response**: Token is in the `token` field of the response header

---

## Order API Details

### 1. Query Order Details

**Request body**:
```json
{
  "orderId": "ORDER202401180001"
}
```

**Response fields**:
- `id` - Order number
- `name` - Patient name (**single field, not firstName/lastName**)
- `gender` - Gender (0-Female, 1-Male, 2-Unknown)
- `age` - Age
- `birthDate` - Date of birth
- `nation` - Ethnicity
- `idCard` - ID card number
- `phone` - Phone number
- `email` - Email
- `medicalNumber` - Electronic medical record number
- `bedNo` - Bed number
- `hospitalPatientid` - Inpatient/outpatient number
- `productId` - Product ID
- `productName` - Product name
- `barcode` - Barcode
- `diagnosis` - Clinical diagnosis
- `medicalHistory` - Health condition
- `disease` - Disease
- `state` - Order status (0-Cancelled, 1-Complete, 3-New, 15-To Be Modified, 20-Submitted)
- `stateName` - Status name
- `progress` - Order progress
- `createTime` - Creation time
- `creatorNickname` - Creator nickname
- `confirmerUsername` - Approver username
- `confirmerNickname` - Approver nickname
- `confirmTime` - Completion time
- `commissionerNickname` - Sales representative nickname
- `crmCustomerName` - Medical institution
- `inspectionDepartmentName` - Submitting department
- `attendingDoctorName` - Attending physician
- `provinceName` - Province name
- `contractName` - Contract name
- `contractPrice` - Contract unit price

Complete field list reference: `field-mapping-quick-reference.md`

---

### 2. Paginated Order List Query

**Request body**:
```json
{
  "bioTechLeaguePagingQuery": {
    "page": 1,
    "rows": 10,
    "sort": {
      "sortFiled": "createTime",
      "sortOrder": -1
    },
    "pagingSearchOne": {
      "matchMode": ["id", "name", "phone"],
      "value": "Search keyword"
    },
    "query": [
      [
        {
          "fieldName": "state",
          "operator": "and",
          "matchMode": "equals",
          "value": "1",
          "isCustomed": false
        }
      ]
    ]
  }
}
```

**Response**: Contains order list and total record count

---

### 3. Create/Update Order

**Important: Field names must be strictly accurate!**
- ✅ Sample information field name: `sampleOrderItem` (not `samples` or `sampleItems`)
- ✅ Fee information field name: `crmConsumeRmarkets` (not `fees` or `payments`)
- Using wrong field names will prevent data from being saved to the system!

**Request body structure**:
```json
{
  "order": {
    "id": "ORDER202401180001",  // Required for update, empty or omit for create
    "name": "John Smith",              // Required (patient name, single field)
    "gender": "1",              // Optional: 0=Female, 1=Male, 2=Unknown
    "age": 35,
    "birthDate": "1989-05-15",  // Format: YYYY-MM-DD
    "nation": "Han",           // Ethnicity
    "idCard": "310000199001011234",  // ID card number
    "phone": "13800000000",
    "email": "user@example.com",
    "medicalNumber": "EMR123456",   // Electronic medical record number
    "bedNo": "B-301",               // Bed number
    "hospitalPatientid": "P123456", // Inpatient/outpatient number
    "zipCode": "200001",
    "productId": "PROD001",         // Required
    "productName": "Genetic Testing Panel",  // Required
    "diagnosis": "Lymphoma",          // Clinical diagnosis
    "medicalHistory": "No underlying conditions",   // Health condition
    "disease": "Lymphoma",            // Disease
    "crmCustomerId": "HOSP001",
    "crmCustomerName": "Shanghai General Hospital",
    "inspectionDepartmentId": "DEPT001",
    "inspectionDepartmentName": "Oncology",
    "attendingDoctorId": "DR001",
    "attendingDoctorName": "Dr. Wang",
    "confirmerUsername": "approver001",  // Required when submitting order
    "confirmerNickname": "Approver",    // Required when submitting order
    "customFieldValue": "{\"field1\":\"value1\"}",  // JSON string
    "note": "Remarks"
  },
  "sampleOrderItem": [          // Note: field name must be sampleOrderItem
    {
      "id": "",                 // Empty for new, fill sample ID for update
      "name": "Blood Sample",
      "slideCode": "BC202401180001",  // Barcode, globally unique
      "sampleTypeId": "T250724002",   // Sample type ID (required)
      "sampleType": "Whole Blood",    // Sample type name (required)
      "samplingDate": "2024-01-18 09:30",  // Format: YYYY-MM-DD HH:mm
      "note": "Fasting sample"
    }
  ],
  "crmConsumeRmarkets": [       // Note: field name must be crmConsumeRmarkets
    {
      "id": "",                 // Empty for new
      "fee": 3500.00,
      "feeWay": "Bank Transfer",
      "isFee": "1",             // 0=Unpaid, 1=Paid
      "consumptionTime": "2024-01-18 10:00",
      "note": "First payment"
    }
  ]
}
```

**Key notes**:
1. `order` object contains order main table information
2. `sampleOrderItem` array contains sample details (field name must be correct!)
3. `crmConsumeRmarkets` array contains fee details (field name must be correct!)
4. `order.id` is empty or omitted when creating
5. `order.id` must be filled when updating
6. Sample `slideCode` must be globally unique
7. `customFieldValue` is in JSON string format

---

### 4. Query Order Sample List

**Request body**:
```json
{
  "orderId": "ORDER202401180001",
  "bioTechLeaguePagingQuery": {
    "page": 1,
    "rows": 100,
    "sort": {},
    "query": []
  }
}
```

**Response fields**:
- `id` - Sample detail ID
- `name` - Sample name
- `slideCode` - Barcode
- `sampleType` - Sample type name
- `samplingDate` - Sampling time
- `status` - Sample status
- `receiveDate` - Receive time

---

### 5. Query Order Fee Information

**Request body**:
```json
{
  "orderId": "ORDER202401180001"
}
```

**Response fields**:
- `id` - Fee record ID
- `fee` - Payment amount
- `feeWay` - Payment method
- `isFee` - Payment status (0-Unpaid, 1-Paid)
- `consumptionTime` - Payment time

---

### 6. Complete Order

**Endpoint**: POST `/order/completeTask?id={order_id}`

**Description**: Changes order status to "Complete"

---

### 7. Cancel Order

**Endpoint**: POST `/order/cancelTask?id={order_id}`

**Description**: Changes order status to "Cancelled"

---

### 8. Query Sample Types

**Endpoint**: POST `/order/selectPopupsSampleType`

**Request body**:
```json
{
  "page": 1,
  "rows": 100,
  "sort": {},
  "query": []
}
```

**Response fields**:
- `id` - Sample type ID (e.g. "T250724002")
- `name` - Sample type name (e.g. "Whole Blood")
- `code` - Sample type code (e.g. "WB")
- `stateName` - Status (e.g. "Valid")

**Use case**: When creating orders, you need to fill in sample type ID and name. Use this API to query all available sample types.

---

### 9. Search Sample Types

**Endpoint**: POST `/order/selectPopupsSampleType`

**Request body**:
```json
{
  "page": 1,
  "rows": 100,
  "sort": {},
  "pagingSearchOne": {
    "matchMode": ["name"],
    "value": "Blood"
  },
  "query": []
}
```

**Description**:
- Fuzzy search by sample type name
- For example, searching "Blood" can match "Whole Blood", "cfDNA", etc.
- Response format is the same as the query sample types API

**Use case**: When the user provides a sample type name but doesn't know the exact ID, use this API to match

---

## Order Status Description

| Status Code | Status Name | Description |
|------------|-------------|-------------|
| 0 | Cancelled | Order has been cancelled |
| 1 | Complete | Order completed |
| 3 | New | Newly created, editable |
| 15 | To Be Modified | Pending modification after change |
| 20 | Submitted | Submitted, pending review |

---

## Gender Codes

| Code | Description |
|------|-------------|
| 0 | Female |
| 1 | Male |
| 2 | Unknown |

---

## Response Format

**Success response**:
```json
{
  "status": 200,
  "data": {
    // Data content
  }
}
```

**Error response**:
```json
{
  "status": 403,
  "msg": "Error message"
}
```

---

## Error Handling

- HTTP 200 + status:200 - Success
- HTTP 200 + status:403 - Authentication failure or business error
- HTTP 401 - Token expired, need to re-login
- HTTP 500 - Server error

---

## Notes

1. **Token management**: Script automatically handles Token acquisition, caching, and refresh
2. **Data source**: All requests must include `X-DS: droplet` header
3. **Time format**: Date uses `yyyy-MM-dd`, datetime uses `yyyy-MM-dd HH:mm`
4. **Pagination**: Page numbers start from 1
5. **JSON format**: All requests and responses use JSON format

---

## Custom Field Management

### Query Custom Field Mapping

**Endpoint**: GET `/system/custom/selAllFields?flag={flag}`

**Parameters**:
- `flag=104-mainTable` - Query order main table custom fields
- `flag=104-sampleTable` - Query sample sub-table custom fields

**Response format**:
Returns JSON object where Key is the page display name and Value is the API field name

```json
{
  "status": 200,
  "msg": "OK",
  "data": {
    "Display Name 1": "apiFieldName1",
    "Display Name 2": "apiFieldName2",
    ...
  }
}
```

**Usage**:
1. Order main table custom fields are stored in `order.customFieldValue` (JSON string)
2. Sample sub-table custom fields are stored in `sampleOrderItem[n].customFieldValue` (JSON string)
3. Need to `JSON.parse()` the string first, then use field mapping to convert to display names

---

## API Field Complete Mapping Reference

### Patient Information Fields

> ⚠️ This system uses a single `name` field for patient name. firstName / lastName fields **do not exist**!

| API Field | Display Name | Required | Data Type | Description |
|-----------|-------------|----------|-----------|-------------|
| `id` | Order ID | ReadOnly | String | Order number |
| `name` | Patient Name | **Required** | String | Patient name (single field) |
| `gender` | Gender | Optional | String | Gender: 0=Female, 1=Male, 2=Unknown |
| `age` | Age | Optional | Integer | Age |
| `birthDate` | Date of Birth | Optional | String | Date of birth (YYYY-MM-DD) |
| `nation` | Ethnicity | Optional | String | Ethnicity |
| `nativePlace` | Native Place | Optional | String | Native place |
| `idCard` | ID Card No. | Optional | String | ID card number |
| `phone` | Phone Number | Optional | String | Phone number |
| `email` | Email | Optional | String | Email |
| `medicalNumber` | EMR ID | Optional | String | Electronic medical record number |
| `bedNo` | Bed No. | Optional | String | Bed number |
| `hospitalPatientid` | Inpatient/Outpatient No. | Optional | String | Inpatient/outpatient number |
| `zipCode` | ZIP Code | Optional | String | ZIP code |

### Product & Test Information Fields

| API Field | Display Name | Required | Data Type | Description |
|-----------|-------------|----------|-----------|-------------|
| `productId` | Test Item ID | **Required** | String | Test product ID |
| `productName` | Test Item(s) | **Required** | String | Test product name |
| `barcode` | Barcode | Optional | String | Order-level barcode |
| `diagnosis` | Clinical Diagnosis | Optional | String | Clinical diagnosis |
| `medicalHistory` | Health Condition | Optional | String | Health condition/history |
| `disease` | Disease | Optional | String | Disease |
| `yongyao` | Medication | Optional | String | Medication status |
| `guomin` | Allergy Info | Optional | String | Allergy information |
| `samplingLocation` | Sampling Location | Optional | String | Sampling location |

### Order Status Fields

| API Field | Display Name | Required | Data Type | Description |
|-----------|-------------|----------|-----------|-------------|
| `state` | Status Code | ReadOnly | String | Status code |
| `stateName` | Status | ReadOnly | String | Status name |
| `progress` | Order Progress | ReadOnly | String | Order progress |
| `changeStatus` | Change Status | ReadOnly | String | Change status flag |
| `orderChangeId` | Change ID | ReadOnly | String | Order change ID |

### Creator & Approver Fields

| API Field | Display Name | Required | Data Type | Description |
|-----------|-------------|----------|-----------|-------------|
| `creatorUsername` | Creator Username | ReadOnly | String | Creator username |
| `creatorNickname` | Created by | ReadOnly | String | Creator nickname |
| `createTime` | Created at | ReadOnly | String | Creation time |
| `confirmerUsername` | Approver Username | Required* | String | Approver username |
| `confirmerNickname` | Approved by | Required* | String | Approver nickname |
| `confirmTime` | Completed at | ReadOnly | String | Completion time |
| `modifierUsername` | Modifier Username | ReadOnly | String | Last modifier username |
| `modifyTime` | Modify Time | ReadOnly | String | Last modification time |
| `commissionerUsername` | Sales Username | Optional | String | Sales representative username |
| `commissionerNickname` | Sales | Optional | String | Sales representative nickname |

*Required when submitting order

### Hospital & Medical Information Fields

| API Field | Display Name | Required | Data Type | Description |
|-----------|-------------|----------|-----------|-------------|
| `crmCustomerId` | Hospital ID | Optional | String | Medical institution ID |
| `crmCustomerName` | Medical Institutions | Optional | String | Medical institution name |
| `inspectionDepartmentId` | Department ID | Optional | String | Department ID |
| `inspectionDepartmentName` | Clinical Department | Optional | String | Department name |
| `attendingDoctorId` | Doctor ID | Optional | String | Attending physician ID |
| `attendingDoctorName` | Attending Physician | Optional | String | Attending physician name |
| `attendingDoctorPhone` | Physician Contact No. | Optional | String | Attending physician phone |
| `provinceId` | Province ID | Optional | String | Province ID |
| `provinceName` | Province | Optional | String | Province name |

### Contract & Price Information Fields

| API Field | Display Name | Required | Data Type | Description |
|-----------|-------------|----------|-----------|-------------|
| `contractId` | Contract ID | Optional | String | Contract number |
| `contractName` | Contract Name | Optional | String | Contract name |
| `settlementCustomerId` | Settlement Customer ID | Optional | String | Settlement customer ID |
| `settlementCustomerName` | Settlement Customer | Optional | String | Settlement customer name |
| `contractPrice` | Contract Price | Optional | Decimal | Contract unit price |
| `discountPrice` | Discounted Price | Optional | Decimal | Discounted price |
| `discountRate` | Discount Rate | Optional | Decimal | Discount rate |
| `refundAmount` | Refund Amount | Optional | Decimal | Refund amount |
| `receivableAmount` | Receivable Amount | ReadOnly | Decimal | Receivable amount |

### Other Fields

| API Field | Display Name | Required | Data Type | Description |
|-----------|-------------|----------|-----------|-------------|
| `note` | Remarks | Optional | String | Remarks |
| `oldId` | Orig. Order ID | Optional | String | Original order number |
| `family` | Family Contact | Optional | String | Family contact |
| `familyPhone` | Family Contact No. | Optional | String | Family contact phone |
| `familySite` | Family Address | Optional | String | Family address |
| `customFieldValue` | Custom Fields | Optional | JSON String | Custom fields (JSON string) |

### Sample Item Fields

Located in the `sampleOrderItem` array (**not** `samples`!)

| API Field | Display Name | Required | Data Type | Description |
|-----------|-------------|----------|-----------|-------------|
| `id` | Sample ID | ReadOnly | String | Sample record ID |
| `name` | Sample Name | Optional | String | Sample name |
| `gender` | Gender | Optional | String | Gender |
| `slideCode` | Barcode | **Required** | String | Barcode (globally unique) |
| `sampleTypeId` | Sample Type ID | **Required** | String | Sample type ID |
| `sampleType` | Sample Type | **Required** | String | Sample type name |
| `samplingDate` | Sampling Time | Optional | String | Sampling time |
| `recipientNickname` | Received by | ReadOnly | String | Receiver |
| `receiveDate` | Received at | ReadOnly | String | Receive time |
| `status` | Sample Status | ReadOnly | String | Sample status |
| `creatorNickname` | Created by | ReadOnly | String | Creator |
| `createTime` | Created at | ReadOnly | String | Creation time |
| `customFieldValue` | Custom Fields | Optional | JSON String | Sample custom field values |
| `note` | Remark | Optional | String | Sample remark |

### Enum Value Reference

#### Gender
- `0` = Female
- `1` = Male
- `2` = Unknown

#### Order Status
- `0` = Cancelled
- `1` = Complete
- `3` = NEW
- `15` = To Be Modified
- `20` = Submitted

#### Sample Status
- `0` = Cancel
- `1` = New
- `2` = To be received
- `3` = Received
- `4` = Scanned

### Required Fields Summary

**Required when creating order**:
- `name` - Patient Name (single field)
- `productId` / `productName` - Test Item(s)

**Additional required when submitting order**:
- `confirmerUsername` / `confirmerNickname` - Approved by

**Required sample detail fields**:
- `slideCode` - Barcode (must be unique)
- `sampleTypeId` / `sampleType` - Sample Type

**Format validation**:
- `phone` - Phone number format
- `email` - Email format
- `idCard` - ID card format
- `slideCode` - Barcode globally unique
