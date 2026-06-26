# Sample Receive Module API Reference

## Command Quick Reference

| Command | Description |
|---------|-------------|
| `receive-list [page] [rows]` | Receive order list |
| `receive <receive_id>` | Receive order details |
| `receive-samples <receive_id> [page] [rows]` | Receive order sample details |
| `create-receive '<json>'` | Create receive order |
| `update-receive '<json>'` | Update receive order |
| `complete-receive <receive_id>` | Complete receive order |
| `scan-barcode <barcode> <receive_id>` | Scan barcode |
| `scan-order <order_code> [receive_id]` | Scan order code |
| `delete-receive-item <receive_id> <item_ids> [isBoard]` | Delete sample details |
| `get-next-flows <product_ids>` | Next flow direction |
| `get-express-companies` | Express company list |
| `get-sample-types-for-receive` | Sample type list |
| `get-products` | Test items list |
| `get-units` | Unit list |
| `get-approvers` | Approver list |
| `auto-add-board <receive_id> <row> <col> <plate_number>` | Add well plate |
| `get-custom-fields 121-mainTable` | Receive order main table custom fields |
| `get-custom-fields 121-receiveTable` | Sample detail custom fields |

**Receive order status:** 3=New, 1=Complete

---

## Key Points for Creating Receive Orders

| Field | Correct Value | ❌ Wrong |
|-------|--------------|---------|
| Main table field name | `sampleReceive` | order, receive |
| Sample array | `sampleReceiveItems` | samples, items |
| Well plate field | `addBoardInfo` | boardInfo |

**Main table required:** `acceptDate`, `isBoard`

**Detail required:** `orderCode`, `barCode`, `productName`, `dicSampleTypeId`, `sampleNum`, `unit`, `isGood`, `method`, `nextFlow`

---

## Query Next Flow API

**URL:** `POST /samplecenter/clinicalSampleReceive/getNextFlowListNew`

**Request parameters:**
```json
{
  "bioTechLeaguePagingQuery": {"page":1,"rows":10,"sort":{},"pagingSearchOne":{},"query":[]},
  "sort": {},
  "pagingSearchOne": {},
  "query": [],
  "tableData": [],
  "page": 1,
  "rows": 20,
  "totalRecords": 1,
  "modelId": "ClinicalSampleReceive",
  "productId": "CP2603120001",
  "ids": ["sample detail ID1", "sample detail ID2", ...]
}
```

**Note:** `ids` is the sample detail `id` array returned by `receive-samples`

---

## nextFlowId Calculation Rules

| Flow Direction | nextFlowId | nextFlow |
|---------------|-----------|----------|
| Nucleic Acid Extraction | SYLX2024000001-NAE | Nucleic acid extraction |
| Library Preparation | SYLX2024000007-LP | Library Preparation |
| Enrichment | SYLX2024000003-E | Enrichment |
| Sequencing | SYLX2024000008-Se | Sequencing |
| Sample Storage | SampleIn-SampleIn | Sample Storage |

**Rule:** When ID contains SYLX, use `${id}-${suffix}`; otherwise use ID directly

---

## update-receive JSON Format

```json
{
  "sampleReceive": { "id": "KXJY2602270002" },
  "sampleReceiveItems": [
    {
      "id": "sample detail ID",
      "nextFlowId": "SYLX2024000001-NAE",
      "nextFlow": "Nucleic acid extraction",
      "isGood": "1"
    }
  ]
}
```

---

**Detailed API documentation:** `api.md`
