# Experiment Template Component Configuration Details

## Component Type Mapping

| User Term | Component Type | Component Label |
|-----------|---------------|----------------|
| Sample Information | detailTable | Sample List |
| Reagents | material | Material |
| Instruments | equipment | Equipment |
| Procedure | editor | Text box |
| Process Data Recording | table | Custom Table |
| Result Information | resultTable | Result Table |

---

## 1. Detail Table (detailTable)

**Fixed fields (16, must be preserved):**
```json
{"label":"Orig Sample ID","prop":"originalSampleCode","disabled":true,"headerType":"fixed"}
{"label":"Sample ID","prop":"sampleCode","disabled":true,"headerType":"fixed"}
{"label":"Sample Type","prop":"sampleType","disabled":true,"headerType":"fixed"}
{"label":"Product Name","prop":"testProjectName","disabled":true,"headerType":"fixed"}
{"label":"Product Type","prop":"productType","disabled":true,"headerType":"fixed"}
{"label":"Product Qty","prop":"productNum","disabled":true,"headerType":"fixed"}
{"label":"Remaining Qty","prop":"sumTotal","type":"number","disabled":false}
{"label":"Unit","prop":"sampleUnit","disabled":true}
{"label":"Storage Status","prop":"storageState","disabled":true}
{"label":"Detection of Genes","prop":"detectionGene","disabled":true}
{"label":"Is Split","prop":"isSplit","disabled":true}
{"label":"Split Quantity","prop":"splitQuantity","disabled":true}
{"label":"Split Proportion","prop":"splitProportion","disabled":true}
```

**Appending custom fields:**
```json
{"label":"Mouse ID","prop":"MouseID","type":"text","value":null,"headerType":"Customize","required":"0"}
```

---

## 2. Material (material)

**Component configuration:**
- `type`: `"material"`
- `label`: `"Material"`
- `value`: Material object array

**Material object structure:**
```json
{
  "id": "uuid-xxxx",
  "name": "CT26 cell line",
  "type": {"id": "SJ2026000006", "name": "CT26 cell line"},
  "changeEvent": 0,
  "flag": false,
  "states": 0
}
```

**Call `et-reagents` first to query available materials**

---

## 3. Equipment (equipment)

**Component configuration:**
- `type`: `"equipment"`
- `label`: `"Equipment"`

**Equipment object structure:**
```json
{
  "id": "uuid-xxxx",
  "name": "Biosafety cabinet (BSC)",
  "type": {"id": "Equipment", "name": "Biosafety cabinet (BSC)", "shebeiName": "Biosafety cabinet (BSC)"},
  "changeEvent": 0,
  "flag": false,
  "states": 0
}
```

**⚠️ Must include `name` and `type.shebeiName`**

**Call `et-instruments` first to query available instruments**

---

## 4. Rich Text (editor)

**Component configuration:**
- `type`: `"editor"`
- `label`: `"Text box"`
- `value`: HTML string

**Example:**
```json
"value": "<ol><li>Thaw and culture cells at 37°C, 5% CO₂.</li><li>Subculture twice weekly.</li></ol>"
```

---

## 5. Custom Table (table)

**Component configuration:**
- `type`: `"table"`
- `label`: `"Custom Table"`
- `propList`: Table header field definitions

**Table header field format:**
```json
{"label":"Cell passage number","prop":"Cellpassagenumber","type":"text","value":null,"headerType":"Customize"}
{"label":"Cell viability (%)","prop":"Cellviability","type":"text","value":null,"headerType":"Customize"}
{"label":"Date of inoculation","prop":"Dateofinoculation","type":"date","value":null,"headerType":"Customize"}
```

---

## 6. Result Table (resultTable)

**Fixed fields (11):**
```json
{"label":"Orig Sample ID","prop":"originalSampleCode","disabled":true,"headerType":"fixed"}
{"label":"Sample ID","prop":"sampleCode","disabled":true,"headerType":"fixed"}
{"label":"Sample Type","prop":"sampleType","disabled":true,"headerType":"fixed"}
{"label":"Project","prop":"testProjectName","disabled":true,"headerType":"fixed"}
{"label":"Volume","prop":"volume","type":"number"}
{"label":"Sum","prop":"total","type":"number"}
{"label":"Unit","prop":"sampleUnit","disabled":true}
{"label":"Next Step","prop":"nextFlow","disabled":true,"required":true}
{"label":"Result","prop":"result","disabled":true,"required":1}
{"label":"Submit to QC","prop":"tjzk","disabled":true}
{"label":"Detection of Genes","prop":"detectionGene","disabled":true}
```

**Formula calculation configuration:**
```json
"menuList": "[{\"label\":\"Calculation\",\"type\":\"jisuan\"}]"
"formula": "{\"formX\":[{\"prop\":\"Tumortakerate\",\"label\":\"Tumor take rate\",\"value\":\"total * 100\"}],\"formY\":[]}"
```

---

## prop Naming Rules

- Fixed fields: System standard prop (`originalSampleCode`, `sampleCode`)
- Custom fields: CamelCase (`MouseID`, `Cellpassagenumber`)

---

## value Default Values

| Component Type | value |
|---------------|-------|
| detailTable/resultTable/table | `"[]"` |
| material/equipment | Complete object array JSON |
| input | `"null"` |
| editor | HTML string |
| porePlate | JSON object (requires `draggLabel`, `itemIndex`) |

---

**Back to:** `../MEMORY.md`
