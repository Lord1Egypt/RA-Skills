# Order Module API Reference

## Command Quick Reference

| Command | Description |
|---------|-------------|
| `order <order_id>` | Query order details |
| `order-list [page] [rows]` | Order list (data.result array) |
| `order-samples <order_id>` | Order sample list |
| `order-fees <order_id>` | Order fees |
| `create-order '@<filepath>'` | Create order from file |
| `update-order '<json>'` | Update order |
| `complete-order <order_id>` | Complete order |
| `cancel-order <order_id>` | Cancel order |
| `sample-types [page] [rows]` | Sample type list |
| `search-sample-type <name>` | Search sample type |
| `get-order-custom-fields 104-mainTable` | Order main table custom field mapping |
| `get-products` | Test items list |

**Order status:** 0=Cancelled, 1=Complete, 3=New, 15=To Be Modified, 20=Submitted

---

## Create Order Flow (Two Steps)

### Step 0: Query Test Item ID
```bash
node biolims.mjs get-products
```

### Step 1: Save Order (Get Order ID)
```json
{
  "order": {
    "id": "",
    "productId": "CP2603120001",
    "productName": "CellCulture",
    "stateName": "NEW",
    "customFieldValue": "[]",
    "medicalNumber": null
  },
  "logs": "",
  "crmConsumeRmarkets": [],
  "crmConsumeListlogs": [],
  "sampleOrderItem": [],
  "sampleOrderItemListlogs": []
}
```

### Step 2: Fill in Main Table and Sample Information
Use the order ID returned from Step 1. See JSON structure below.

---

## Order JSON Structure

```json
{
  "order": {
    "id": "DD2603120000002",
    "name": "Patient Name",
    "gender": "1",
    "age": 14,
    "birthDate": "2020-05-25",
    "nation": "Han",
    "nativePlace": "Beijing",
    "bedNo": "Bed 039",
    "phone": "13800000000",
    "hospitalPatientid": "A003-5001",
    "idCard": "310000199001011234",
    "email": "user@example.com",
    "zipCode": "000000",
    "productId": "CP2603120001",
    "productName": "CellCulture",
    "diagnosis": "Tumor enlargement",
    "note": "Remarks",
    "family": "Family contact",
    "familyPhone": "13800000001",
    "familySite": "Family address",
    "commissionerNickname": "Sales representative",
    "crmCustomerName": "Submitting institution",
    "provinceName": "Province",
    "customFieldValue": "[{\"id\":\"\",\"columnName\":\"test1\",\"displayName\":\"Clinical Diagnosis\",\"value\":\"\"}]"
  },
  "logs": "",
  "crmConsumeRmarkets": [],
  "crmConsumeListlogs": [],
  "sampleOrderItem": [
    {
      "id": "",
      "changeEvent": 1,
      "name": "Patient Name",
      "gender": "1",
      "status": "1",
      "slideCode": "A0312001",
      "sampleTypeId": "T250311001",
      "sampleType": "Mouse",
      "customFieldValue": "[]"
    }
  ],
  "sampleOrderItemListlogs": []
}
```

---

## ⚠️ Field Name Reference Table (No Guessing!)

| Correct Field Name | ❌ Wrong Field Name | Description |
|-------------------|-------------------|-------------|
| `slideCode` | barCode, barcode | Sample barcode |
| `sampleTypeId` | dicSampleTypeId | Sample type ID |
| `sampleType` | dicSampleTypeName | Sample type name |
| `sampleOrderItem` | samples, items | Sample array |
| `crmConsumeRmarkets` | fees, payments | Fee array |

---

## customFieldValue Format

First query field definitions:
```bash
node biolims.mjs get-order-custom-fields 104-mainTable
```

Format (JSON string):
```json
"[
  {\"id\":\"\",\"columnName\":\"test1\",\"displayName\":\"Clinical Diagnosis\",\"value\":\"Tumor enlargement\"},
  {\"id\":\"\",\"columnName\":\"test2\",\"displayName\":\"Collection Time\",\"value\":\"2026-03-03 15:58\"}
]"
```

**Field mapping:**
| columnName | displayName |
|-----------|------------|
| test1 | Clinical Diagnosis |
| test2 | Collection Time |
| test3 | Test Method |
| test4 | Submission Time |
| test5 | Barcode Number (required) |
| test6 | Submitting Institution |

---

## Template Files

- Order creation template: `../templates/order-create-template.json`

---

**Detailed API documentation:** `api.md`
