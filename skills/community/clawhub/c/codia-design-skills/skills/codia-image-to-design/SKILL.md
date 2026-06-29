---
name: codia-image-to-design
description: Convert screenshots or images into editable Codia design data. Trigger when the user asks to turn an image, screenshot, poster, UI, or design mockup into structured editable design output.
api: image-to-design
endpoint: POST /v2/open/image_to_design
cli: codia-design image-to-design
credits_per_call: 13
sync: true
response_type: design_tree
---

# codia-image-to-design

## Runtime And Auth

Use the local `codia-design` CLI for this feature. Before calling the API, verify that `codia-design` is available. If it is missing and global npm installs are allowed, install it with `npm install -g @codia-ai/codia-design-cli`. Then check `codia-design auth status`; if it is not connected, run `codia-design auth login --platform codex` or bind an API key with `codia-design auth set --api-key api_key_xxx`. Never print API keys or `~/.codia/design-skills/config.json`.

Convert UI screenshots into editable hierarchical design trees (VisualElement trees).

## CLI Command

```bash
codia-design image-to-design --image <PATH|URL> [--out FILE]
```

## Parameters

| Flag | Type | Required | Default | Description |
|---|---|---|---|---|
| `--image` | path \| URL | yes | — | Local PNG/JPG/WebP path, or public HTTPS URL |
| `--out` | path | no | stdout | Write JSON results to file (recommended for large responses) |

## Response

```json
{
  "ok": true,
  "data": {
    "configuration": {
      "scalingFactor": 1.0,
      "baseWidth": 375,
      "measurementUnit": "px"
    },
    "visualElement": {
      "elementId": "root_001",
      "elementName": "Body",
      "elementType": "Body",
      "layoutConfig": { "positionMode": "Normal" },
      "styleConfig": {
        "widthSpec":  { "sizing": "FIXED", "value": 375 },
        "heightSpec": { "sizing": "FIXED", "value": 812 }
      },
      "contentData": null,
      "processingMeta": { "detectionScore": 1.0, "surfaceArea": 304500 },
      "childElements": []
    }
  }
}
```

### configuration field

| Field | Type | Description |
|---|---|---|
| `scalingFactor` | number | All values must be multiplied by this factor to get the actual pixels |
| `baseWidth` | number | Canvas base width (375=mobile, 1440=desktop) |
| `measurementUnit` | string | `"px"` or `"pt"` |

### VisualElement node structure

Every node (including the `visualElement` root node and all `childElements`) has the same schema:

| Field | Type | Description |
|---|---|---|
| `elementId` | string | Node ID (regenerated for each call, not stable across calls) |
| `elementName` | string | Human-readable tag name |
| `elementType` | string | Node type, see the table below |
| `layoutConfig` | object | Positioning information |
| `styleConfig` | object | visual style |
| `contentData` | object \| null | Node content (only Text/Image has value) |
| `processingMeta` | object | Detection confidence and area |
| `childElements` | array | child nodes (recursive) |

### elementType value

| elementType | has child nodes | contentData field | description |
|---|---|---|---|
| `Body` | yes | — | Root node, always exists |
| `Layer` | yes | — | Universal container (card, section, etc.) |
| `Group` | yes | — | Pure grouping, no self-visualization |
| `Text` | no | `textValue: string` | Text leaf node |
| `Image` | no | `imageSource: string` | Image (CDN URL) |
| `Vector` | no | `vectorData` | Vector shape |
| `Component` | Varies | `componentReference` | Detected UI component |

### layoutConfig key fields

```
positionMode: "Flex" | "Absolute" | "Normal" | "Relative"
```

- `"Flex"` — Participate in the flex layout of the parent node. The parent node’s `flexAttributes` describe the direction/alignment
- `"Absolute"` — absolute positioning, read `absoluteAttrs.coord.x` / `.y` to get the offset
- `flexAttributes`: `{ flexDirection, alignItems, justifyContent, flexWrap }` (on Flex container)

### styleConfig key fields

| Field | Type | Description |
|---|---|---|
| `widthSpec` / `heightSpec` | `{sizing, value}` | `sizing`: FIXED=exact px / FILL=fill parent / FIT_CONTENT=shrink |
| `textConfig` | object | `fontSize`, `fontFamily`, `fontStyle`, `lineHeight`, `letterSpacing`, `textAlign` |
| `textColor` | `{rgbValues, hexCode}` | Text color |
| `borderConfig` | object | `borderWidth`, `borderStyle`, `borderColor`, `borderRadius: [tl,tr,br,bl]` |
| `backgroundConfig` | object | `type`: `"COLOR"` / `"IMAGE"` / `"LINEAR_GRADIENT"` + respective fields |
| `opacityLevel` | number | 0–255, divided by 255 to get CSS opacity |
| `paddingValues` | array | `[top, right, bottom, left]` |

## Usage Example

```bash
# local file
codia-design image-to-design --image ./screenshot.png --out result.json

# URL pattern
codia-design image-to-design --image https://example.com/screen.png --out result.json
```

Traverse the tree after reading the results (Node.js):

```js
const { data } = require('./result.json');
const { scalingFactor } = data.configuration;

function walk(node, depth = 0) {
  const pad = '  '.repeat(depth);
  if (node.elementType === 'Text') {
    console.log(pad + '[Text]', node.contentData?.textValue);
  } else if (node.elementType === 'Image') {
    console.log(pad + '[Image]', node.contentData?.imageSource);
  } else {
    console.log(pad + '[' + node.elementType + ']', node.elementName);
  }
  node.childElements?.forEach(c => walk(c, depth + 1));
}
walk(data.visualElement);

//Extract all text nodes
function extractText(node, results = []) {
  if (node.elementType === 'Text') results.push(node.contentData?.textValue);
  node.childElements?.forEach(c => extractText(c, results));
  return results;
}
```

Low confidence node filtering (`processingMeta.detectionScore < 0.5`) is recommended for use in production code.

## Input Limits

The maximum size and file size of input images depend on the plan level:

| Packages | Maximum resolution | Maximum file size |
|---|---|---|
| Free | 1440×1440 | 5 MB |
| Starter | 4096×4096 | 20 MB |
| Pro | 10000×10000 | 50 MB |

## Errors & Billing

| HTTP | Meaning | Fix |
|---|---|---|
| 400 | The image URL is not accessible or the format is not supported | Confirm that the URL is publicly accessible and the format is PNG/JPG/WebP |
| 402 | Insufficient credits | `codia-design credits` Recharge after confirming the balance |
| 429 | Rate limit exceeded | Retry after backing off |
| 500 | Service internal error | Safe to try again |

**Credits**: 13 credits/request. After the command completes, the CLI checks `available_credits` and reminds the user if the remaining balance is below 26 credits (2x estimate); this does not block generation. · **Duration**: Synchronous, mobile screenshots are usually < 10s, desktop intensive pages are longer
