# Experiment Template Component Configuration Complete Reference

## Component Type List

| type | Description | value Format |
|------|-------------|-------------|
| `detailTable` | Detail table (sample list) | `"[]"` |
| `resultTable` | Result table | `"[]"` |
| `table` | Custom table | `"[]"` |
| `material` | Material | Complete material array JSON |
| `equipment` | Equipment | Complete equipment array JSON |
| `porePlate` | Well plate | JSON object (requires draggLabel, itemIndex) |
| `input` | Single-line input | `"null"` |
| `editor` | Rich text | HTML string |
| `dropdown` | Dropdown select | `"null"` |

---

## Common Component Fields

```json
{
  "label": "Component display name",
  "type": "Component type",
  "size": 24,
  "value": "...",
  "propList": "[...]",
  "menuList": "[...]",
  "productList": "[]",
  "plate": "",
  "inputType": "null",
  "formula": "{\"formX\":[],\"formY\":[]}",
  "keyId": 0
}
```

---

## propList Configuration (Table Column Definitions)

**Fixed fields (headerType: "fixed"):**
```json
{"label":"Sample ID","prop":"sampleCode","disabled":true,"headerType":"fixed"}
```

**Custom fields (headerType: "Customize"):**
```json
{"label":"Mouse ID","prop":"MouseID","type":"text","value":null,"headerType":"Customize","required":"0"}
```

**Rules:**
- Only append custom fields; do not modify fixed fields
- Custom fields must use `"headerType": "Customize"`

---

## menuList Configuration

**Result table calculation button:**
```json
"menuList": "[{\"label\":\"Calculation\",\"type\":\"jisuan\"}]"
```

---

## formula Complete Structure

```json
"formula": "{\"formX\":[
  {
    \"prop\":\"Tumortakerate\",
    \"label\":\"Tumor take rate\",
    \"value\":\"total * 100\",
    \"props\":\"total * 100\",
    \"propList\":[],
    \"judgeStr\":[],
    \"valueList\":[],
    \"propsList\":[]
  }
],\"formY\":[]}"
```

**Field descriptions:**
- `formX`: Row formula array
- `formY`: Column formula array (usually empty)
- `prop`: Target field prop
- `value/props`: Formula expression
- `propList/propsList`: Dependent field list
- `judgeStr`: Conditional judgment
- `valueList`: Value list

---

## Complete Example (Cell_Culture Template Components)

See `../templates/experiment-template-cell-culture.json`

---

**Back to:** `experiment-template-api.md`
