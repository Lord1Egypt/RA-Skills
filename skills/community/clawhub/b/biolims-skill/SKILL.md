---
name: biolims
description: Call Bio-LIMS system APIs to manage orders, sample receiving, and experiment templates, including querying, creating, updating orders, sample receive management, barcode scanning, and experiment template creation, querying, modification, copying, and cancellation. Use when the user mentions keywords such as "order", "sample", "patient", "receive", "scan", "barcode", "experiment template", "test template", "et-", etc. The script automatically handles token login and refresh; no manual authentication is needed.
---

# Bio-LIMS (v2.0)

A skill for calling Bio-LIMS backend APIs. All API calls are made through `scripts/biolims.mjs`, with automatic token management.

**Module Features**:
- Order Management
- Sample Receive
- Sample Type Query
- Experiment Template Management

## Quick Start

```bash
# Script path (absolute path)
SCRIPT="/home/biolims/.openclaw/workspace/skills/biolims/scripts/biolims.mjs"

# Query order details
node "$SCRIPT" order ORDER202401180001

# Paginated query of order list (default page 1, 10 per page)
bash "$SCRIPT" order-list
bash "$SCRIPT" order-list 1 20  # Page 1, 20 per page

# Query order sample list
bash "$SCRIPT" order-samples ORDER202401180001

# Query order fee information
bash "$SCRIPT" order-fees ORDER202401180001

# Create new order (Note: field names must be exact!)
# sampleOrderItem cannot be written as samples!
# crmConsumeRmarkets cannot be written as fees!
bash "$SCRIPT" create-order '{
  "order": {
    "name": "John Smith",
    "productId": "PROD001",
    "productName": "Genetic Testing"
  },
  "sampleOrderItem": [
    {
      "slideCode": "BC123",
      "sampleTypeId": "T250724002",
      "sampleType": "Whole Blood",
      "productId": "PROD001",
      "productName": "Genetic Testing"
    }
  ],
  "crmConsumeRmarkets": [
    {
      "fee": 3500.00,
      "feeWay": "Bank Transfer",
      "isFee": "1"
    }
  ]
}'

# Update order
bash "$SCRIPT" update-order '{"order":{"id":"ORDER123","name":"Jane Smith",...}}'

# Complete order
bash "$SCRIPT" complete-order ORDER202401180001

# Cancel order
bash "$SCRIPT" cancel-order ORDER202401180001

# Query all sample types
bash "$SCRIPT" sample-types

# Search sample types (fuzzy match by name)
bash "$SCRIPT" search-sample-type "Blood"

# ==================== Sample Receive Commands ====================

# Query receive order list
bash "$SCRIPT" receive-list
bash "$SCRIPT" receive-list 1 20  # Page 1, 20 per page

# Query single receive order details
bash "$SCRIPT" receive SR202401180001

# Query receive order sample detail list
bash "$SCRIPT" receive-samples SR202401180001
bash "$SCRIPT" receive-samples SR202401180001 1 50  # Page 1, 50 per page

# Scan barcode to get sample info (receive_id is required, must create receive order first)
# Input format: { "sampleReceive": { "id": "...", "name": "...", "acceptDate": "...", "isBoard": "..." }, "barCode": "..." }
bash "$SCRIPT" scan-barcode BC20240118001 SR202401180001

# Scan order number to get unreceived samples
bash "$SCRIPT" scan-order ORD202401180001
bash "$SCRIPT" scan-order ORD202401180001 SR202401180001  # Specify receive order ID

# Create receive order (Note: field names must be exact!)
# sampleReceiveItems cannot be written as samples!
# addBoardInfo cannot be written as boardInfo!
bash "$SCRIPT" create-receive '{
  "sampleReceive": {
    "name": "Clinical Sample Receive",
    "acceptDate": "2024-01-18 10:00",
    "expressNum": "SF1234567890",
    "expressCompanyId": "EC001",
    "expressCompanyName": "SF Express",
    "transportTypeId": "TT001",
    "transportTypeName": "Cold Chain Transport",
    "isBoard": "1"
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
      "productName": "Genetic Testing",
      "sampleNum": "5",
      "unit": "ml",
      "isGood": "1",
      "nextFlow": "Warehousing"
    }
  ],
  "addBoardInfo": "{\"banHao\":\"P001\",\"rowNum\":8,\"colNum\":12}"
}'

# Update receive order (uses same API as create-receive)
bash "$SCRIPT" update-receive '{"sampleReceive":{"id":"SR202401180001",...},...}'

# Complete receive order
bash "$SCRIPT" complete-receive SR202401180001

# Delete sample receive detail items
bash "$SCRIPT" delete-receive-item SR202401180001 "ITEM001,ITEM002"

# Get available order list (for order number mode selection)
bash "$SCRIPT" get-orders-for-receive
bash "$SCRIPT" get-orders-for-receive 1 10  # Page 1, 10 per page

# ==================== Experiment Template Commands ====================

# Query experiment template list
bash "$SCRIPT" et-list
bash "$SCRIPT" et-list 1 20           # Page 1, 20 per page
bash "$SCRIPT" et-list 1 10 "PCR"    # Fuzzy search by template name

# Query template details (three-layer structure: template -> steps -> components)
bash "$SCRIPT" et-detail ET2024000001
bash "$SCRIPT" et-detail ET2024000001 edit   # Edit mode

# Create template (pass JSON directly or read from file)
bash "$SCRIPT" et-create '{"templateName":"...","stepDetails":[...]}'
bash "$SCRIPT" et-create @/tmp/template.json

# Copy template (deep copy, including attachments)
bash "$SCRIPT" et-copy ET2024000001

# Cancel template (supports multiple IDs)
bash "$SCRIPT" et-cancel ET2024000001
bash "$SCRIPT" et-cancel ET001 ET002 ET003

# Complete template (workflow callback, state -> 1)
bash "$SCRIPT" et-complete ET2024000001

# Query all completed templates (for selection by other modules)
bash "$SCRIPT" et-all-completed

# Query experiment types (query available types before creating template)
bash "$SCRIPT" et-exp-types
bash "$SCRIPT" et-exp-types-search "PCR"

# Query approver list
bash "$SCRIPT" et-approvers <group_id>

# Query experiment group list
bash "$SCRIPT" et-groups
```

## Common Usage Scenarios

### Scenario 1: User asks about order information

**User**: "Help me check order ORDER202401180001"

**AI Actions**:
1. Call: `bash "$SCRIPT" order ORDER202401180001`
2. Parse the returned JSON, extract key information
3. Reply to user in a clear list format

**Reply Example** (strictly follow field mapping):
```
OK, found the information for order ORDER202401180001:

=== Patient Information ===
Order ID: ORDER202401180001
Patient Name: John Smith
Gender: Male
Age: 35
Date of Birth: 1989-05-15
Phone Number: [phone_number]
Email: [email]
ZIP Code: 200000

=== Product & Test Information ===
Test Item ID: PROD001
Test Item(s): Genetic Testing Panel
Barcode: BC123456789
Clinical Diagnosis: Cancer Stage II

=== Order Status ===
Status: Complete
Order Progress: Clinical Sample Registration

=== Creator & Approver ===
Created by: HX
Created at: 2024-01-18 10:30:00
Approved by: Dr. Wang
Completed at: 2024-01-18 15:00:00

=== Hospital & Medical Information ===
Medical Institutions: Shanghai General Hospital
Clinical Department: Oncology
Attending Physician: Dr. Wang
Physician Contact No.: [phone_number]
Province: Shanghai
```

**Important Reminders**:
- Use English field display names (e.g., "Patient Name", not Chinese equivalents)
- Patient name is a single field `name`, do not split it for display
- Display by field groups (Patient Information, Product Information, etc.)
- Only show fields that have values
- This system **does not use** firstName/lastName, only the `name` field

### Scenario 2: Query order list

**User**: "What are the recent orders?"

**AI Actions**:
1. Call: `bash "$SCRIPT" order-list 1 10`
2. Parse the returned list
3. Display recent orders

**Reply Example** (list mode, simplified display):
```
Recent 10 orders (72 total):

1. Order ID: DD2602030022
   Patient Name: John Smith
   Test Item(s): LymphDetect
   Status: COMPLETE
   Created at: 2026-02-03 05:47:02

2. Order ID: DD2602030021
   Patient Name: Jane Doe
   Test Item(s): Genetic Panel
   Status: NEW
   Created at: 2026-02-02 10:30:00

3. Order ID: DD2602030020
   Patient Name: Bob Wilson
   Test Item(s): Cancer Screening
   Status: Submitted
   Created at: 2026-02-01 14:20:00

...

To view details of a specific order, please provide the order number.
```

**Important**: List mode only shows key fields, uses English display names, patient name uses single `name` field

### Scenario 3: View order samples

**User**: "What samples does order ORDER202401180001 have?"

**AI Actions**:
1. Call: `bash "$SCRIPT" order-samples ORDER202401180001`
2. Display sample list

**Reply Example**:
```
Sample list for order ORDER202401180001:

1. Blood Sample
   - Barcode: BC202401180001
   - Type: Whole Blood
   - Sampling Time: 2024-01-18 09:30
   - Status: Received

2. Saliva Sample
   - Barcode: BC202401180002
   - Type: Saliva
   - Sampling Time: 2024-01-18 09:35
   - Status: Processing
```

### Scenario 4: Query sample types

**User**: "What sample types are available?" or "I need the type ID for blood samples"

**AI Actions**:
1. If user provided a specific name (e.g., "Blood"), call: `bash "$SCRIPT" search-sample-type "Blood"`
2. If user did not provide a name, call: `bash "$SCRIPT" sample-types`
3. Display sample type list including ID, name, and code

**Reply Example**:
```
Found 1 matching sample type:

Name: Whole Blood
ID: T250724002
Code: WB
Status: Valid

When creating samples, use:
- sampleTypeId: "T250724002"
- sampleType: "Whole Blood"
```

### Scenario 5: Create order

**User**: "Help me create an order, patient name is John Smith, test item is LymphDetect, need one blood sample"

**AI Actions**:
1. Collect required info: name (patient name), productId, productName
2. If user mentions sample type, use `search-sample-type` to query sample type ID
3. Build complete JSON (**must use correct field names**)
4. **Use file method to pass large JSON** (avoid command line escaping issues)
5. Call create order command

**Key Notes for Creating Orders**:

1. **Use file method to pass JSON** (strongly recommended):
   - Windows PowerShell has issues with command line JSON escaping
   - Write JSON to a temp file, then pass using `@filepath`
   ```bash
   # First write JSON to file
   # Then call:
   node biolims.mjs create-order "@C:\path\to\order.json"
   ```

2. **productId must be a system ID**:
   - Wrong: `"productId": "LymphDetect"` (using product name directly)
   - Correct: `"productId": "CP2511240001"` (system product ID)
   - If you don't know the productId, first query existing orders to get the correct ID

3. **Samples must also include productId and productName**:
   - Each sampleOrderItem must include productId and productName
   - Otherwise the server will return a 400 error

**Critically Important - Field Names**:
```json
{
  "order": { ... },
  "sampleOrderItem": [ ... ],    <- Must be sampleOrderItem, NOT samples!
  "crmConsumeRmarkets": [ ... ]  <- Must be crmConsumeRmarkets, NOT fees!
}
```

**Complete JSON Example**:
```json
{
  "order": {
    "name": "John Smith",
    "gender": "1",
    "phone": "[phone_number]",
    "email": "[email]",
    "productId": "CP2511240001",
    "productName": "LymphDetect",
    "crmCustomerId": "HOSP001",
    "crmCustomerName": "Shanghai Hospital",
    "diagnosis": "Lymphoma"
  },
  "sampleOrderItem": [
    {
      "slideCode": "BC202401180001",
      "sampleTypeId": "T250724002",
      "sampleType": "Whole Blood",
      "productId": "CP2511240001",
      "productName": "LymphDetect"
    }
  ],
  "crmConsumeRmarkets": [
    {
      "fee": 3500.00,
      "feeWay": "Bank Transfer",
      "isFee": "1",
      "consumptionTime": "2024-01-18 10:00"
    }
  ]
}
```

**Common Product ID Mapping**:
| Product Name | productId |
|-------------|-----------|
| LymphDetect | CP2511240001 |

(Other product IDs can be obtained by querying existing orders)

**Reply Example**:
```
Order created successfully!

Order ID: DD2602030023
Patient Name: John Smith
Test Item: LymphDetect
Sample: Whole Blood (BC202401180001)
Status: NEW

Order has been saved to the system.
```

## Response Handling

**Key Rules:**
1. **Must check status field**: Only `status === 200` indicates success
2. **order-list response structure**: `{"status":200,"data":{"result":[order array],"total":count}}`
   - Order list is in `data.result`, not directly in `data`
3. **Single order response structure**: `{"status":200,"data":{"result":{order object}}}`
4. **Error response**: `{"status":403/401,"msg":"error message"}`

**Response Handling Steps:**
```javascript
1. Parse JSON
2. Check if response.status is 200
3. If 200, extract data from response.data.result
4. If not 200, check response.msg for error reason
5. Format output
```

**Display Rules (Very Important):**
1. **Use English field display names**:
   - Strictly follow the field mapping table using English names
   - Example: `name` -> "Patient Name: John Smith"
   - Example: `gender` -> "Gender: Female"
   - Reference `references/field-mapping-quick-reference.md` for field mapping table

2. **Correct use of name field**:
   - This system uses a single `name` field for patient name, display as "Patient Name: John Smith"
   - Do NOT look for firstName / lastName (these fields do not exist in this system)
   - Do NOT split the name field into first and last name

3. **Format Requirements**:
   - Do not paste raw JSON directly
   - Use list format for display (WhatsApp does not support markdown tables)
   - Display by groups (Patient Information, Product Information, etc.)
   - Only show fields with values (do not show null or empty strings)

4. **Enum Value Conversion**:
   - gender: 0->Female, 1->Male, 2->Unknown
   - state: 0->Cancelled, 1->Complete, 3->NEW, 15->To Be Modified, 20->Submitted
   - Sample status: 0->Cancel, 1->New, 2->To be received, 3->Received, 4->Scanned

5. **Time Format**:
   - Keep original format or convert to readable format
   - Example: "2024-01-18 10:30:00"

## Order Status Description

- `0` - Cancelled
- `1` - Complete
- `3` - New
- `15` - To Be Modified
- `20` - Submitted

## Gender Codes

- `0` - Female
- `1` - Male
- `2` - Unknown

## Important Notes

1. **Token Management**: The script automatically handles login and token refresh; no manual intervention needed
2. **Error Handling**: If the API returns an error, explain the specific issue to the user (e.g., "order does not exist", "insufficient permissions", etc.)
3. **Data Format**: Creating/updating orders requires a complete JSON structure; refer to `references/api.md`
4. **Privacy Protection**: Be careful to protect privacy when displaying patient information; do not over-expose sensitive data

## Field Mapping Reference

### Fixed Field Mapping

The JSON data returned by orders uses API internal field names (e.g., `name`, `productId`), which need to be mapped to page display names (e.g., "Patient Name", "Test Item ID").

**Main Field Mapping**:
- `id` -> Order ID
- `name` -> Patient Name (**single field, NOT firstName/lastName**)
- `gender` -> Gender (0=Female, 1=Male, 2=Unknown)
- `age` -> Age
- `birthDate` -> Date of Birth
- `nation` -> Ethnicity
- `idCard` -> ID Card No.
- `phone` -> Phone Number
- `email` -> Email
- `medicalNumber` -> EMR ID
- `bedNo` -> Bed No.
- `hospitalPatientid` -> Inpatient/Outpatient No.
- `productId` -> Test Item ID
- `productName` -> Test Item(s)
- `barcode` -> Barcode
- `diagnosis` -> Clinical Diagnosis
- `medicalHistory` -> Health Condition
- `disease` -> Disease
- `stateName` -> Status
- `progress` -> Order Progress
- `creatorNickname` -> Created by
- `createTime` -> Created at
- `confirmerNickname` -> Approved by
- `confirmTime` -> Completed at
- `commissionerNickname` -> Sales
- `crmCustomerName` -> Medical Institutions
- `inspectionDepartmentName` -> Clinical Department
- `attendingDoctorName` -> Attending Physician
- `attendingDoctorPhone` -> Physician Contact No.
- `provinceName` -> Province
- `contractName` -> Contract Name
- `contractPrice` -> Contract Price
- `note` -> Remarks

For the complete mapping table, refer to `references/field-mapping-quick-reference.md`.

### Custom Field Handling

Order data contains two types of custom fields:

1. **Order main table custom fields** (`customFieldValue`)
   - Storage location: `order.customFieldValue` (JSON string)
   - Field mapping API: `GET /system/custom/selAllFields?flag=104-mainTable`

2. **Sample sub-table custom fields** (`customFieldValue`)
   - Storage location: `sampleOrderItem[n].customFieldValue` (JSON string)
   - Field mapping API: `GET /system/custom/selAllFields?flag=104-sampleTable`

**Processing Steps**:
1. Call field mapping API to get `{"Display Name": "apiFieldName"}` mapping
2. `JSON.parse()` to parse the `customFieldValue` string in the order
3. Use the mapping to convert API field names to display names
4. Display to user

**Example**:
```javascript
// 1. Get field mapping
const mapping = await getCustomFields('104-mainTable');
// Returns: {"Patient Note": "patientNote", "Urgency Level": "urgencyLevel"}

// 2. Parse custom fields
const customValues = JSON.parse(order.customFieldValue);
// customValues = {"patientNote": "Urgent case", "urgencyLevel": "High"}

// 3. Convert to display names
// "Patient Note": "Urgent case"
// "Urgency Level": "High"
```

---

## Sample Receive Usage Scenarios

### Scenario 6: Query receive order list

**User**: "What are the recent sample receive orders?"

**AI Actions**:
1. Call: `bash "$SCRIPT" receive-list 1 10`
2. Parse the returned list
3. Display recent receive orders

**Reply Example** (list mode, simplified display):
```
Recent 10 receive orders (45 total):

1. Registration ID: SR202401180001
   Description: Clinical Sample Receive
   Received At: 2024-01-18 10:00:00
   Status: New
   Created by: HX
   Created at: 2024-01-18 09:30:00
   Sample ID: S001,S002,S003
   Barcode: BC001,BC002,BC003

2. Registration ID: SR202401180002
   Description: Research Sample Receive
   Received At: 2024-01-18 14:00:00
   Status: Complete
   Created by: Wang
   Created at: 2024-01-18 13:30:00
   Sample ID: S004,S005
   Barcode: BC004,BC005

...

To view details of a specific receive order, please provide the registration ID.
```

### Scenario 7: Query receive order details

**User**: "Help me check receive order SR202401180001"

**AI Actions**:
1. Call: `bash "$SCRIPT" receive SR202401180001`
2. Parse the returned JSON, extract key information
3. Reply in a clear list format

**Reply Example** (strictly follow field mapping, do not merge fields):
```
OK, found the information for receive order SR202401180001:

=== Sample Receive Information ===
Registration ID: SR202401180001
Code: SR202401180001
Description: Clinical Sample Receive
Received At: 2024-01-18 10:00:00
In Plate: Yes
Project Name: Genetic Testing Project
Classify: Clinical
Type: Research

=== Express & Transport Information ===
Express Bill No.: SF1234567890
Courier: SF Express
Transportation Method: Cold Chain Transport

=== Receive Status ===
Status: New
Created by: HX
Created at: 2024-01-18 09:30:00

To view sample details, use command: receive-samples SR202401180001
```

**Important Reminders**:
- Use English field display names (e.g., "Registration ID", not Chinese equivalents)
- Do not merge fields (display each field separately)
- Display by field groups (Sample Receive Information, Express Information, etc.)
- Only show fields that have values

### Scenario 8: Query receive order sample details

**User**: "What samples does receive order SR202401180001 have?"

**AI Actions**:
1. Call: `bash "$SCRIPT" receive-samples SR202401180001`
2. Display sample list

**Reply Example**:
```
Sample details for receive order SR202401180001 (15 samples total):

1. Sample ID: S001
   Barcode: BC001
   Order ID: ORD001
   Name: John Smith
   Gender: Male
   Sample Type: Whole Blood
   Test Item(s): Genetic Testing
   Sampling Time: 2024-01-18 09:00:00
   Sampling Volume: 5 ml
   Normal: Yes
   Result: Qualified
   Next Step: Warehousing
   Plate Number: P001
   Sample Location: A01

2. Sample ID: S002
   Barcode: BC002
   Order ID: ORD001
   Name: Jane Doe
   Gender: Female
   Sample Type: Plasma
   Test Item(s): Genetic Testing
   Sampling Volume: 3 ml
   Normal: Yes
   Result: Qualified
   Next Step: Warehousing
   Plate Number: P001
   Sample Location: A02

...
```

### Scenario 9: Scan barcode to receive sample

**User**: "Scan barcode BC20240118001"

**Important**: The `scan-barcode` command's `receive_id` is a **required parameter**; you must create a receive order first!

**AI Actions**:
1. **First check if a receive order exists**:
   - If user already provided a receive order ID -> use it directly
   - If no receive order -> first call `create-receive` to create a new one
2. Call: `bash "$SCRIPT" scan-barcode BC20240118001 SR202401180001`
3. Parse the returned sample information
4. Display sample details

**API Input Format**:
```json
{
  "sampleReceive": {
    "id": "SR202401180001",
    "name": "Clinical Sample Receive",
    "acceptDate": "2024-01-18 10:00",
    "isBoard": "1"
  },
  "barCode": "BC20240118001"
}
```

**Reply Example**:
```
Scanned barcode BC20240118001 sample information:

Sample ID: S001
Barcode: BC20240118001
Order ID: ORD001
Name: John Smith
Gender: Male
Sample Type: Whole Blood
Test Item(s): Genetic Testing

This sample has been added to receive order SR202401180001.
```

**If barcode has already been received**:
```
Error: Barcode BC20240118001 has already been received in receive order SR202401170005.
```

**If no receive order ID provided**:
```
Error: Scanning barcode requires creating a receive order first. Please use the create-receive command to create a receive order, or provide the receive order ID.
```

### Scenario 10: Scan order number for batch receiving

**User**: "Scan order ORD202401180001"

**AI Actions**:
1. Call: `bash "$SCRIPT" scan-order ORD202401180001`
2. Parse the returned sample list
3. Display receivable samples

**Reply Example**:
```
Order ORD202401180001 has 3 unreceived samples:

1. Sample ID: S001
   Barcode: BC001
   Name: John Smith
   Gender: Male
   Sample Type: Whole Blood
   Test Item(s): Genetic Testing

2. Sample ID: S002
   Barcode: BC002
   Name: Jane Doe
   Gender: Female
   Sample Type: Plasma
   Test Item(s): Genetic Testing

3. Sample ID: S003
   Barcode: BC003
   Name: Bob Wilson
   Gender: Male
   Sample Type: Serum
   Test Item(s): Genetic Testing

These samples can be batch-added to a receive order.
```

### Scenario 11: Create sample receive order

**User**: "Create a sample receive order, receive time is today at 10am, express number SF1234567890, needs plating"

**AI Actions**:
1. Collect required info: acceptDate (receive time), isBoard (whether to plate)
2. Build complete JSON (**must use correct field names**)
3. Call create receive order command

**Critically Important - Field Names**:
```json
{
  "sampleReceive": { ... },           <- Receive order main table
  "sampleReceiveItems": [ ... ],      <- Must be sampleReceiveItems, NOT samples!
  "addBoardInfo": "..."               <- Must be addBoardInfo, NOT boardInfo!
}
```

**Complete JSON Example**:
```json
{
  "sampleReceive": {
    "name": "Clinical Sample Receive",
    "acceptDate": "2024-01-18 10:00",
    "expressNum": "SF1234567890",
    "expressCompanyId": "EC001",
    "expressCompanyName": "SF Express",
    "transportTypeId": "TT001",
    "transportTypeName": "Cold Chain Transport",
    "isBoard": "1"
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
      "productName": "Genetic Testing",
      "sampleNum": "5",
      "unit": "ml",
      "isGood": "1",
      "nextFlow": "Warehousing"
    }
  ],
  "addBoardInfo": "{\"banHao\":\"P001\",\"rowNum\":8,\"colNum\":12}"
}
```

**Reply Example**:
```
Receive order created successfully!

Registration ID: SR202401180001
Description: Clinical Sample Receive
Received At: 2024-01-18 10:00:00
Express Bill No.: SF1234567890
Courier: SF Express
In Plate: Yes
Status: New

Sample Details:
- Sample ID: S001, Barcode: BC001, Whole Blood, 5ml

Receive order has been saved to the system.
```

---

### Scenario 12: Query receive order with custom fields

**User**: "Query complete information for receive order SR202401180001, including custom fields"

**AI Actions**:
1. Call `get-custom-fields 121-mainTable` to get main table custom field mapping
2. Call `get-custom-fields 121-receiveTable` to get sub-table custom field mapping
3. Call `receive SR202401180001` to query receive order data
4. Parse fixed fields (using field mapping table from TOOLS.md)
5. Parse enum values (Gender, Status, isGood, method, isBoard)
6. Parse `customFieldValue` JSON fields (main table and sub-table)
7. Format display (all fields use English display names)

**Complete Workflow Example**:

```bash
# Step 1: Get main table custom field mapping
bash "$SCRIPT" get-custom-fields 121-mainTable
# Returns: {"Storage Condition": "storageCondition", "Special Notes": "specialNotes"}

# Step 2: Get sub-table custom field mapping
bash "$SCRIPT" get-custom-fields 121-receiveTable
# Returns: {"Sample Source": "sampleSource", "Quality Grade": "qualityGrade"}

# Step 3: Query receive order data
bash "$SCRIPT" receive SR202401180001
```

**Parsing Logic** (pseudocode):
```javascript
// 1. Parse fixed fields
const displayData = {
    "Registration ID": data.sampleReceive.id,
    "Received At": data.sampleReceive.acceptDate,
    "Status": data.sampleReceive.state === 3 ? "New" : "Complete",
    "Express Bill No.": data.sampleReceive.expressNum,
    "Courier": data.sampleReceive.expressCompanyName,
    "In Plate": data.sampleReceive.isBoard === "1" ? "Yes" : "No",
    // ... other fixed fields ...
};

// 2. Parse main table custom fields
if (data.sampleReceive.customFieldValue) {
    const customFields = JSON.parse(data.sampleReceive.customFieldValue);
    // customFields = {"storageCondition": "2-8C", "specialNotes": "Urgent"}

    // Use mapping from step 1 to convert field names
    displayData["Storage Condition"] = customFields["storageCondition"];  // "2-8C"
    displayData["Special Notes"] = customFields["specialNotes"];          // "Urgent"
}

// 3. Parse sample details (including sub-table custom fields)
displayData.samples = data.sampleReceiveItems.map(item => {
    const displayItem = {
        "Sample ID": item.sampleCode,
        "Barcode": item.barCode,
        "Name": item.patientName,
        "Gender": item.gender === 1 ? "Male" : item.gender === 0 ? "Female" : "Unknown",
        "Sample Type": item.dicSampleType,
        "Test Item(s)": item.productName,
        "Sampling Volume": item.sampleNum,
        "Unit": item.unit,
        "Normal": item.isGood === "1" ? "Yes" : "No",
        "Result": item.method === "1" ? "Qualified" : "Unqualified",
        "Next Step": item.nextFlow,
        // ... other fixed fields ...
    };

    // Parse sample custom fields
    if (item.customFieldValue) {
        const customFields = JSON.parse(item.customFieldValue);
        // customFields = {"sampleSource": "Hospital A", "qualityGrade": "Grade A"}

        // Use mapping from step 2 to convert field names
        displayItem["Sample Source"] = customFields["sampleSource"];      // "Hospital A"
        displayItem["Quality Grade"] = customFields["qualityGrade"];      // "Grade A"
    }

    return displayItem;
});
```

**Reply Example**:
```
Receive order details:

Registration ID: SR202401180001
Received At: 2024-01-18 10:00:00
Status: New
Express Bill No.: SF1234567890
Courier: SF Express
In Plate: Yes
Storage Condition: 2-8C
Special Notes: Urgent

Sample Details (2 samples):

Sample #1:
- Sample ID: S001
- Barcode: BC001
- Name: John Smith
- Gender: Male
- Sample Type: Whole Blood
- Test Item(s): Genetic Testing
- Sampling Volume: 5
- Unit: ml
- Normal: Yes
- Result: Qualified
- Next Step: Warehousing
- Sample Source: Hospital A
- Quality Grade: Grade A

Sample #2:
- Sample ID: S002
- Barcode: BC002
- Name: Jane Doe
- Gender: Female
- Sample Type: Serum
- Test Item(s): Protein Testing
- Sampling Volume: 3
- Unit: ml
- Normal: Yes
- Result: Qualified
- Next Step: Testing
- Sample Source: Hospital B
- Quality Grade: Grade A
```

**Important Tips**:
- Custom field mappings may change dynamically; it is recommended to re-fetch them with each query
- `customFieldValue` is a JSON string that must be parsed with `JSON.parse()` first
- All fields must use English display names
- Only display fields with values; do not show empty fields

---

### Scenario 13: Query next step flow list

**User**: "Query next step flow for product PROD001" or "Where does this sample go next?"

**AI Actions**:

**Key: This API requires a product ID; it will error without one**

**Step 1: Confirm product ID**
- If user already provided product ID -> use it directly
- If user did not provide product ID -> **must ask or query first**

**Step 2: Call API**
```bash
# Single product ID
bash "$SCRIPT" get-next-flows PROD001

# Multiple product IDs (intersection)
bash "$SCRIPT" get-next-flows PROD001,PROD002
```

**Step 3: Parse response**
```json
{
    "status": 200,
    "data": {
        "result": [
            {
                "id": "FLOW001",
                "name": "Warehousing",
                "description": "Store sample in warehouse"
            },
            {
                "id": "FLOW002",
                "name": "Testing",
                "description": "Enter testing workflow"
            }
        ],
        "total": 2
    }
}
```

**Reply Example 1 (with product ID)**:
```
Next step flow options for product PROD001:

1. Warehousing (FLOW001)
   - Store sample in warehouse

2. Testing (FLOW002)
   - Enter testing workflow

2 flow options available.
```

**Reply Example 2 (no product ID - must ask first)**:
```
To query next step flow, I need the product ID.

You can:
1. Tell me the product ID directly (e.g., PROD001)
2. Or I can first help you query the available test item list

Which would you prefer?
```

**Common Errors (must avoid)**:
```bash
# Wrong: Calling without providing product ID
bash "$SCRIPT" get-next-flows
# Result: {"error":"Usage: biolims.sh get-next-flows <product_id1,product_id2,...>"}

# Correct: Ask user first or get product ID from context
# AI: "Please provide the product ID, or shall I help you query available test items?"
```

**Business Logic**:
- **Single product ID**: Returns all available next step flows for that product
- **Multiple product IDs**: Returns flows supported by all products (intersection)
  - Example: PROD001 supports [A,B,C], PROD002 supports [B,C,D] -> Returns [B,C]

**Rules AI Must Follow**:
1. **Never** call `get-next-flows` without a product ID
2. If user did not provide a product ID, **must ask first**: "Please provide the test item product ID"
3. Or proactively offer help: "I can first help you query the available test item list, would you like that?"
4. Only call the API after obtaining the product ID

---

### Scenario 14: Required field validation before completing receive order

**User**: "Complete receive order SR202401180001"

**AI Actions**:

**Key: Must validate all required fields before completing**

**Step 1: Query current receive order data**
```bash
bash "$SCRIPT" receive SR202401180001
```

**Step 2: Validate required fields**

**Main table required fields (2):**
- `acceptDate` (Received At) - Receive time
- `isBoard` (In Plate) - Whether to plate

**Sample detail required fields (9 per sample):**
- `orderCode` (Order ID)
- `barCode` (Barcode)
- `productName` (Test Item(s))
- `dicSampleTypeId` (Sample Type ID)
- `sampleNum` (Sampling Volume)
- `unit` (Unit)
- `isGood` (Normal)
- `method` (Result)
- `nextFlow` (Next Step)

**Step 3: Decide whether to complete based on validation results**

**Case A - All fields present:**
```bash
bash "$SCRIPT" complete-receive SR202401180001
```

Reply:
```
Receive order completed successfully!

Registration ID: SR202401180001
Status: Complete
Received At: 2024-01-18 10:00:00

Receive order is now locked and cannot be edited.
```

**Case B - Missing fields (must list specific missing fields):**

Reply:
```
Cannot complete receive order, the following required fields are not filled:

Receive Order Main Table:
- Received At (acceptDate) - Receive time

Sample Details:
Sample #1 (BC001):
- Next Step (nextFlow) - Next step flow
- Normal (isGood) - Whether normal

Sample #2 (BC002):
- Result (method) - Test result

Please fill in this information before completing the receive order.

You can use the following command to update:
bash "$SCRIPT" update-receive '<json>'
```

**Things AI Must Never Do**:
1. Call `complete-receive` directly without validation
2. Assume fields are filled and skip validation
3. Only say "fields are missing" without listing specific fields

---

### Scenario 15: Duplicate barcode error handling

**User**: "Create receive order with samples BC001 and BC001"

**AI Actions**:
1. Build JSON
2. Call `create-receive`
3. Receive error response: `{"status": 400, "msg": "Save failed: duplicate barcode", "data": null}`

**AI should reply like this**:
```
Save failed: duplicate barcode

Duplicate barcode detected: BC001

Barcodes must be unique within the same receive order. Please check:
1. Did you accidentally enter the same barcode twice
2. If there are indeed multiple samples, each sample needs a different barcode

Please modify the duplicate barcode and try again.
```

**Common barcode error scenarios**:

**Scenario A - Duplicate within same receive order:**
```json
{
  "sampleReceiveItems": [
    {"barCode": "BC001", ...},
    {"barCode": "BC001", ...}  // Duplicate
  ]
}
```
Error: `"Save failed: duplicate barcode"`

**Scenario B - Already received by another receive order:**
- Barcode BC001 is already in another receive order
- Scanning will indicate the sample has been received

**AI Handling**:
- Parse error message
- Identify the specific duplicate barcode
- Provide clear resolution suggestions

---

### Scenario 16: Unified handling of API error responses

**After all API calls, AI must check the status field:**

```javascript
// Pseudocode example
const response = JSON.parse(apiResponse);

if (response.status === 200) {
    // Success - display data normally
    displayData(response.data);

} else if (response.status === 400) {
    // Business error - display error in friendly manner
    const errorMsg = response.msg;

    if (errorMsg.includes("duplicate barcode")) {
        return `Save failed: duplicate barcode\n\n${provide resolution suggestions}`;

    } else if (errorMsg.includes("required field")) {
        return `Save failed: missing required fields\n\n${list specific fields}`;

    } else {
        return `Operation failed: ${errorMsg}\n\nPlease check if the input data is correct.`;
    }

} else if (response.status === 401) {
    // Script will auto-retry, AI does not need to handle

} else if (response.status === 500) {
    return "Server error, please try again later.";
}
```

**Error response examples and AI replies:**

| API Response | AI Reply |
|-------------|----------|
| `{"status":400,"msg":"Save failed: duplicate barcode"}` | Save failed: duplicate barcode. Duplicate barcode detected... Please modify and try again. |
| `{"status":400,"msg":"Required field not filled: acceptDate"}` | Save failed: missing required field - Received At (acceptDate). Please fill in and try again. |
| `{"status":500,"msg":"Internal error"}` | Server error, please try again later. |

**Principles AI Must Follow**:
1. **Always check the status field** - Do not assume the call succeeded
2. **Display errors in a friendly manner** - Do not return raw error messages directly
3. **Provide resolution suggestions** - Tell the user how to fix the error
4. **List specific details** - Which field is missing? Which barcode is duplicated?

---

## Sample Receive Status Description

### Receive Order Status

- `3` - New - Editable, saveable, completable
- `1` - Complete - Read-only, not editable

### Sample Qualification Status

- `1` - Qualified
- `0` - Unqualified

### In Plate

- `1` - Yes
- `0` - No

---

## Experiment Template Usage Scenarios

### Scenario 17: Query experiment template list

**User**: "View experiment templates" / "Check latest experiment templates" / "What experiment templates are there"

**AI Actions**:
1. Call: `bash "$SCRIPT" et-list 1 10`
2. Parse the returned `data.result` array, display key fields

**Reply Example**:
```
Found 8 experiment templates (8 total):

1. Template ID: ET2024000001
   Template Name: PCR Testing Experiment Template
   Experiment Type: PCR Amplification
   Status: Complete
   Created by: admin
   Created at: 2024-01-15 10:30:00

2. Template ID: ET2024000002
   Template Name: Cell Culture Testing Template
   Experiment Type: Cell Experiment
   Status: New
   Created by: lab_user
   Created at: 2024-01-20 14:00:00
```

**Status Value Conversion**:
- `3` -> New (editable)
- `20` -> In Workflow
- `15` -> To Be Modified
- `1` -> Complete
- `30` -> Cancelled (excluded from queries automatically)

---

### Scenario 18: Query experiment template details

**User**: "View details of template ET2024000001" / "What steps does ET2024000001 have"

**AI Actions**:
1. Call: `bash "$SCRIPT" et-detail ET2024000001 view`
2. Parse three-layer nested structure, display by step -> component hierarchy

**Reply Example**:
```
Template Details: ET2024000001

=== Basic Information ===
Template Name: PCR Testing Experiment Template
Experiment Type: PCR Amplification
Status: Complete
Created by: admin
Created at: 2024-01-15 10:30:00
Version: 1.0

=== Step Structure (2 steps total) ===

Step 1: Sample Preparation
  - [detailTable] Sample Detail Table
  - [input] Extraction Concentration (number)
  - [input] Extraction Date (date)
  - [attachment] Extraction Record

Step 2: PCR Amplification
  - [detailTable] Sample Detail Table
  - [equipment] Instruments & Equipment
  - [material] Reagents & Consumables
  - [resultTable] Test Result Table
```

---

### Scenario 19: Create experiment template

**User**: "Help me create an XXX testing template"

**AI Actions**:
1. First query experiment types: `bash "$SCRIPT" et-exp-types`
2. First query experiment groups: `bash "$SCRIPT" et-groups`
3. Collect required info: templateName, experimentType, experimentGroup, auditor
4. Build JSON and write to temp file (avoid escaping issues)
5. Call: `bash "$SCRIPT" et-create @/tmp/template.json`

**Create JSON Structure** (templateName required, stepDetails required):
```json
{
  "templateName": "Template Name",
  "experimentType": "Experiment Type ID",
  "experimentTypeName": "Experiment Type Name",
  "experimentGroup": "Experiment Group ID",
  "experimentGroupName": "Experiment Group Name",
  "auditor": "Approver ID",
  "auditorName": "Approver Name",
  "stepDetails": [
    {
      "name": "Step Name",
      "keyId": 0,
      "jsonDatas": [
        {
          "label": "Field Name",
          "type": "input",
          "size": "8",
          "inputType": "text",
          "exclusiveShow": "0"
        }
      ]
    }
  ]
}
```

---

### Scenario 20: Copy experiment template

**User**: "Copy template ET2024000001" / "Create a new one based on template ET001"

**AI Actions**:
1. Call: `bash "$SCRIPT" et-copy ET2024000001`
2. Display new template ID (auto-generated by system, status is New and editable)

---

### Scenario 21: Cancel experiment template

**User**: "Cancel template ET2024000001"

**AI Actions**:
1. **Must confirm first**: "Are you sure you want to cancel template ET2024000001? This action cannot be undone."
2. After user confirms: `bash "$SCRIPT" et-cancel ET2024000001`

---

## Detailed API Information

### Order Module

- Complete API documentation: `references/api.md`
- **Field mapping quick reference**: `references/field-mapping-quick-reference.md` <- Must read when querying orders!

### Sample Receive Module

- Complete API documentation: `references/api-sample-receive.md`
- **Field mapping quick reference**: `references/field-mapping-sample-receive-quick-reference.md` <- Must read when querying receive orders!

### Experiment Template Module

- Complete API documentation: `references/api-experiment-template.md` <- Must read for experiment template operations!
