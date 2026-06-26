# Experiment Center Module API Reference

## Experiment Type Configuration

| Command | Description |
|---------|-------------|
| `experiment-type-config-list [page] [rows]` | Query experiment type configuration (get suffix) |

**⚠️ Important:** The `suffix` parameter for all experiment operations must use the `databaseTableSuffix` value returned by this API.

---

## Sample Pool

| Command | Description |
|---------|-------------|
| `experiment-sample-pool <suffix> [page] [rows]` | Sample pool list |
| `experiment-sample-pool-by-code <suffix> <code>` | Query by code |

---

## Experiment Order Management

| Command | Description |
|---------|-------------|
| `experiment-list <suffix> [page] [rows]` | Experiment order list |
| `experiment-template <suffix> <exp_id> <flow_id>` | Query components and fields |
| `get-create-experiment-options <suffix>` | Get protocols + experimenters |
| `quick-create-experiment <suffix> <protocol_id> <experimenter_id> [name]` | Quick create |
| `experiment-add-samples <suffix> <exp_id> <flow_id> "<sample_pool_id>"` | Add samples |
| `change-product '@<file>'` | Modify product type |
| `generate-result` | Generate result table |
| `update-result <suffix> <exp_id> <flow_id> '<json>'` | Update result table |
| `update-detail <suffix> <exp_id> <flow_id> '<json>'` | Update detail table |
| `complete-experiment <suffix> <exp_id> [flow_id]` | Complete experiment order |

---

## Standard Flow for Creating Experiment Orders

1. `experiment-type-config-list` → Get `databaseTableSuffix`
2. `get-create-experiment-options <suffix>` → **Show to user for selection** of protocol and experimenter
3. `quick-create-experiment` → Create
4. `experiment-add-samples` → Add samples (optional)

---

## Experiment Order Completion Flow

Create → Add samples → Modify product type (optional) → `generate-result` → `update-result` → `complete-experiment`

---

## Modify Product Type (change-product)

**⚠️ Independent URL:** Modifying product type uses an independent API, different from the URL for updating other fields

### Full URL
```
POST http://your-server/biolims/experimentalcenter/experiment/changeProduct
```

### Request Parameters Structure

```json
{
  "id": "Detail table component ID (type=\"detailTable\")",
  "ids": ["Sample detail ID array"],
  "databaseTableSuffix": "Experiment type suffix",
  "productList": "Product type JSON string"
}
```

### Request Parameters Example

```json
{
  "id": "aaa00000000000000000000000000001",
  "ids": [
    "aaa00000000000000000000000000002",
    "aaa00000000000000000000000000003"
  ],
  "databaseTableSuffix": "Cell_Culture",
  "productList": "[{
    \"productTypeId\": \"T250311001\",
    \"productType\": \"Mouse\",
    \"productNum\": 1,
    \"code\": \"MS\"
  }]"
}
```

### Request Parameter Key Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Detail table component ID (type="detailTable") |
| `ids` | array | Sample detail ID array (can be multiple) |
| `databaseTableSuffix` | string | Experiment type suffix (e.g. Cell_Culture) |
| `productList` | string | **JSON string** (note: string, not object) |

### productList Structure

```json
[
  {
    "productTypeId": "Product type ID",
    "productType": "Product type name",
    "productNum": Product quantity (number),
    "code": "Product code"
  }
]
```

### Call Example

```bash
curl -X POST http://your-server/biolims/experimentalcenter/experiment/changeProduct \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{
    "id": "aaa00000000000000000000000000001",
    "ids": ["aaa00000000000000000000000000002"],
    "databaseTableSuffix": "Cell_Culture",
    "productList": "[{\"productTypeId\":\"T250311001\",\"productType\":\"Mouse\",\"productNum\":1,\"code\":\"MS\"}]"
  }'
```

### Difference from updateExperimentFlow

| Feature | changeProduct | updateExperimentFlow |
|---------|---------------|---------------------|
| **Purpose** | Only modify product type and quantity | Modify samples/reagents/equipment/custom fields etc. |
| **URL** | `/changeProduct` | `/updateExperimentFlow` |
| **Parameters** | Simple structure (4 fields) | Complex structure (stepDetails array) |
| **productList** | JSON string | Nested in jsonDatas.value |
| **Logging** | Auto-recorded | Must manually pass logArr |

---

## Query Experiment Order Information

### Query Experiment Order Main Table Information

**Full URL:**
```
POST http://your-server/biolims/experimentalcenter/experiment/selectnodeexperimenter
```

**Request parameters structure:**
```json
{
  "bioTechLeaguePagingQuery": {
    "page": 1,
    "rows": 9999
  },
  "page": 1,
  "rows": 9999,
  "id": "Experiment order ID",
  "databaseTableSuffix": "Experiment type suffix",
  "templateCode": "Template code"
}
```

**Request parameters example:**
```json
{
  "bioTechLeaguePagingQuery": {"page": 1, "rows": 9999},
  "page": 1,
  "rows": 9999,
  "id": "CC20260002",
  "databaseTableSuffix": "Cell_Culture",
  "templateCode": "ET2026000044"
}
```

### Query Experiment Order Component Details

**Full URL:**
```
POST http://your-server/biolims/experimentalcenter/experiment/selectOrAddExperimentFlowTemplate
```

**Request parameters structure:**
```json
{
  "experimentFlowId": "Experiment order ID or flow ID",
  "flow": "Flow node ID (e.g. Activity_1h3w2cm)",
  "databaseTableSuffix": "Experiment type suffix"
}
```

**Request parameters example:**
```json
{
  "experimentFlowId": "CC20260002",
  "flow": "Activity_1h3w2cm",
  "databaseTableSuffix": "Cell_Culture"
}
```

**Response:** Contains component details (stepDetails, jsonDatas), can be used to get:
- Detail table component ID (`id` field of `type="detailTable"`)
- Sample detail IDs (parse `value` JSON to get each sample's `id`)

---

## Update Experiment Order Component Fields (updateExperimentFlow)

### API Rules

| Modification Type | URL | Description |
|------------------|-----|-------------|
| **Modify product type** | `Independent URL` | Use only when modifying product/product type |
| **Modify other content** | `/biolims/experimentalcenter/experiment/updateExperimentFlow` | Modify samples/reagents/equipment/custom fields etc. |

### Full URL
```
POST http://your-server/biolims/experimentalcenter/experiment/updateExperimentFlow
```

### Request Parameters Structure

```json
{
  "id": "Experiment order ID",
  "peopleGroupsId": "",
  "peopleGroupsName": "",
  "stepDetails": [
    {
      "id": "Step ID",
      "name": "Step name",
      "stepItemId": "Step item ID",
      "jsonDatas": [Component array]
    }
  ],
  "databaseTableSuffix": "Cell_Culture",
  "experimentId": "CC20260001",
  "logArr": {"Modification log"}
}
```

### Component Types and Modification Rules

| Component Type | type Value | Modifiable Fields |
|---------------|-----------|-------------------|
| **Sample List** | `detailTable` | MouseID, Tumorcelllotnumber, volume, sumTotal etc. |
| **Material** | `material` | practicalNum, pici, states |
| **Equipment** | `equipment` | states, note |
| **Custom Table** | `table` | All custom fields (based on propList definition) |
| **Result Table** | `resultTable` | **result (required)**, **Tumortakerate**, nextFlow, tjzk, notes, volume, total etc. |
| **Text box** | `editor` | HTML text content |

**⚠️ Note:** `MouseID` is defined in both **Sample List** and **Result Table**, and must be **filled separately**!
- Sample List `MouseID`: Mouse ID in sample details
- Result Table `MouseID`: Mouse ID corresponding to result records (must match Sample List)

### Modification Example

**Modify Sample List fields:**
```json
{
  "id": "bbb00000000000000000000000000001",
  "stepDetails": [{
    "id": "bbb00000000000000000000000000002",
    "jsonDatas": [{
      "label": "Sample List",
      "type": "detailTable",
      "value": "[{\"MouseID\":\"New ID\",\"Tumorcelllotnumber\":\"New batch number\"}]"
    }]
  }],
  "logArr": {
    "detailBox": [{
      "id": "Sample ID",
      "contentvalue": "Details:<br>'Mouse ID' :changed from' Old ID 'to' New ID'"
    }]
  }
}
```

### Log Recording (logArr)

| Component Type | logArr Field | Description |
|---------------|-------------|-------------|
| Sample List | `detailBox` | Record sample detail modifications |
| Material | `materialBox` | Record reagent modifications |
| Equipment | `deviceBox` | Record equipment modifications |
| Custom Table | `tableBox` | Record custom table modifications |
| Text box | `textBox` | Record text box modifications |
| Result Table | `resultBox` | Record result table modifications |

### Formula Calculation

`formula.formX` defines auto-calculated fields:
```json
"formula": {
  "formX": [{
    "prop": "Tumortakerate",
    "label": "Tumor take rate",
    "value": "total * 100"
  }]
}
```

### Key Rules

1. **Product type modification** → Use independent URL
2. **Other field modifications** → Use `updateExperimentFlow`
3. **Required fields** → `id`, `stepDetails`, `experimentId`
4. **Log recording** → All modifications must be recorded in `logArr`
5. **changeField** → Record modified field names (comma-separated)

---

### Complete Request Parameters Example (Cell Culture Experiment Order Update) - ✅ Verified Successfully

**Scenario:** Update Sample List, Custom Table, and Result Table - three components

**⚠️ Key rules:**
1. **Outermost `id`** = `data.id` returned by API (experiment order main table ID)
2. **`stepDetails[0].id`** = `stepDetails[0].id` returned by API (step ID)
3. **The two must be different** - This is the most common mistake!
4. **`experimentId`** = Experiment order number (e.g. CC20260004)
5. **`logArr`** must contain 8 boxes: deviceBox, materialBox, textBox, tableBox, detailBox, resultBox, editBox, tableBox2

```json
{
  "id": "ccc00000000000000000000000000001",
  "peopleGroupsId": "",
  "peopleGroupsName": "",
  "stepDetails": [{
    "id": "ccc00000000000000000000000000002",
    "name": "Tumor Cell Culture And Inoculation",
    "keyId": 0,
    "jsonDatas": [
      {
        "label": "Sample List",
        "id": "ccc00000000000000000000000000003",
        "exclusiveShow": "0",
        "type": "detailTable",
        "size": "24",
        "value": "[{\"MouseID\":\"M001\",\"Tumorcelllotnumber\":\"CT26-1115\",\"changeField\":\"MouseID,Tumorcelllotnumber\",...}]",
        "propList": [],
        "menuList": [],
        "productList": [],
        "plate": "",
        "inputType": "null",
        "formula": {"formX":[],"formY":[]},
        "keyId": "0"
      },
      {
        "label": "Custom Table",
        "id": "ccc00000000000000000000000000004",
        "exclusiveShow": "0",
        "type": "table",
        "size": "24",
        "value": "[{\"Cellpassagenumber\":\"5\",\"Cellviability\":\"97.2\",\"Cellconcentration\":\"3.2e6\",\"Injectionvolumepermouse\":\"0.10\",\"Dateofinoculation\":\"2026-01-22\",\"MouseIDs\":\"M001\",\"changeField\":\"Cellpassagenumber,Cellviability,Cellconcentration,Injectionvolumepermouse,Dateofinoculation,MouseIDs\",\"id\":1,\"flag\":false}]",
        "propList": [],
        "menuList": [],
        "productList": [],
        "plate": "",
        "inputType": "null",
        "formula": {"formX":[],"formY":[]},
        "keyId": "3"
      },
      {
        "label": "Result Table",
        "id": "ccc00000000000000000000000000005",
        "exclusiveShow": 0,
        "type": "resultTable",
        "size": 24,
        "value": "[{\"MouseID\":\"M001\",\"Tumortakerate\":\"100\",\"notes\":\"Tumor present at Day 7\",\"changeField\":\"MouseID\",...}]",
        "propList": [...],
        "menuList": [{"label":"Calculation","type":"jisuan"}],
        "productList": [],
        "plate": "",
        "inputType": "null",
        "formula": {"formX":[{"prop":"Tumortakerate","label":"Tumor take rate","value":"total * 100"}],"formY":[]},
        "keyId": 4,
        "checkList": []
      }
    ]
  }],
  "databaseTableSuffix": "Cell_Culture",
  "lastStep": true,
  "experimentId": "CC20260004",
  "logArr": {
    "deviceBox": [],
    "materialBox": [],
    "textBox": [],
    "tableBox": [{"realId":"","id":1,"contentvalue":"Form:<br>Cell culture data filled"}],
    "detailBox": [{"realId":"Sample ID","sampleCode":"LCMS...","contentvalue":"MouseID: M001, Tumorcelllotnumber: CT26-1115"}],
    "resultBox": [{"realId":"Result ID","sampleCode":"LCMS...","contentvalue":"result: 100, Tumortakerate: 100"}],
    "editBox": [],
    "tableBox2": []
  }
}
```

### ID Rules (⚠️ Most Critical!)

| Location | Value | Source |
|----------|-------|--------|
| **Outermost `id`** | `ccc00000000000000000000000000001` | `data.id` returned by API (experiment order main table ID) |
| **`stepDetails[0].id`** | `ccc00000000000000000000000000002` | `stepDetails[0].id` returned by API (step ID) |
| **`experimentId`** | `CC20260004` | Experiment order number |
| **Relationship** | Must be different | ⚠️ **Most common mistake!** |

### changeField Rules

| Component | changeField | Description |
|-----------|------------|-------------|
| **Sample List** | `MouseID,Tumorcelllotnumber` | Only include modified fields |
| **Custom Table** | `Cellpassagenumber,Cellviability,Cellconcentration,Injectionvolumepermouse,Dateofinoculation,MouseIDs` | **Must include all 6 fields** |
| **Result Table** | `result,Tumortakerate,notes` | Only include modified fields |

**⚠️ Field ownership:**
- `MouseID` → **Sample List** (detailTable)
- `Tumortakerate` → **Result Table** (resultTable)
- `result` → **Result Table** (resultTable)

### Record Count Rules

| Component | Record Count | Description |
|-----------|-------------|-------------|
| Sample List | 20 records | 1 per sample |
| Custom Table | 20 records | Corresponds to Sample List, 1 MouseID per record |
| Result Table | 20 records | 1 per sample |

### Call Example

```bash
TOKEN="your-token-here"
curl -X POST "http://your-server/biolims/experimentalcenter/experiment/updateExperimentFlow" \
  -H "Content-Type: application/json" \
  -H "Token: $TOKEN" \
  -H "X-DS: endemo" \
  -H "X-Sole-ID: $(cat /proc/sys/kernel/random/uuid)" \
  -H "accept-language: en" \
  -d @/tmp/update.json
```

---

## databaseTableSuffix Description

### ⚠️ Important: Dynamically Retrieved, Not Fixed Mapping

`databaseTableSuffix` **is not a fixed value** and must be dynamically queried via API.

### Query Method

```bash
# 1. Query experiment type configuration
node biolims.mjs experiment-type-config-list [page] [rows]

# 2. Get databaseTableSuffix from the response
# Response example:
# {
#   "status": 200,
#   "data": {
#     "result": [
#       {
#         "experimentType": "Cell Culture",
#         "databaseTableSuffix": "Cell_Culture",  # ← Use this value
#         "state": "1"
#       },
#       {
#         "experimentType": "NA Extraction",
#         "databaseTableSuffix": "HS",
#         "state": "1"
#       }
#     ]
#   }
# }
```

### Usage Rules

| Scenario | Action |
|----------|--------|
| **Before creating experiment order** | Call `experiment-type-config-list` first to get available `databaseTableSuffix` |
| **All experiment operations** | `suffix` parameter must use the `databaseTableSuffix` value returned by this API |
| **No hardcoding** | ❌ Do not use fixed mapping tables; the system may add/modify experiment types |

### Common suffix Examples (For Reference Only, Actual Query Results Prevail)

| experimentType | databaseTableSuffix | Description |
|----------------|---------------------|-------------|
| Cell Culture | `Cell_Culture` | Cell culture |
| NA Extraction | `HS` | Nucleic acid extraction |
| Library Prep | `WK` | Library preparation |
| Enrichment | `FJ1129` | Enrichment |
| Sequencing | `SJCX` | Sequencing |

**⚠️ Note:** The above examples may change at any time. **Must use `experiment-type-config-list` response results as the source of truth**.

---

**Detailed API documentation:** `api.md`
```
