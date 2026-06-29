---
name: codia-pdf-to-design
description: Convert PDF pages into editable Codia design data. Trigger when the user asks to extract PDF pages into structured design data or editable visual layouts.
api: pdf-to-design
endpoint: POST /v2/open/pdf_to_design
cli: codia-design pdf-to-design
credits_per_call: 13
sync: true
response_type: design_tree
---

# codia-pdf-to-design

## Runtime And Auth

Use the local `codia-design` CLI for this feature. Before calling the API, verify that `codia-design` is available. If it is missing and global npm installs are allowed, install it with `npm install -g @codia-ai/codia-design-cli`. Then check `codia-design auth status`; if it is not connected, run `codia-design auth login --platform codex` or bind an API key with `codia-design auth set --api-key api_key_xxx`. Never print API keys or `~/.codia/design-skills/config.json`.

Extract one or more pages of a PDF into structured design trees (one tree per page).

## CLI Command

```bash
codia-design pdf-to-design --pdf <PATH|URL> --pages <0,1,2> [--out FILE]
```

> **Note**: `--pages` is **zero-based**. Use `0` for the first page and `1` for the second page. `pdf-to-ppt` uses the same zero-based convention through the Task API.

## Parameters

| Flag | Type | Required | Default | Description |
|---|---|---|---|---|
| `--pdf` | path \| URL | yes | — | Local PDF path, or public HTTPS URL |
| `--pages` | string | recommended | All pages for local multipart only | Comma-separated zero-based page numbers, such as `0,1,2`; always pass this for predictable cost and output |
| `--out` | path | no | stdout | Write JSON results to file |

**Two input modes:**
- Local file (`--pdf ./doc.pdf`) → multipart upload, the CLI repeats `page_no` once per page (`0`, `1`, `2`) when `--pages 0,1,2` is provided
- URL (`--pdf https://...`) → JSON request, the API expects `page_no` as a number array such as `[0,1,2]`; the CLI builds this from `--pages`

## Response

```json
{
  "ok": true,
  "data": {
    "configuration": {
      "scalingFactor": 1.0,
      "baseWidth": 260.94,
      "measurementUnit": "px"
    },
    "size": { "width": 260.94, "height": 240.94 },
    "pages": [
      {
        "page_no": 0,
        "schema": {
          "elementId": "Page 1_1",
          "elementType": "Layer",
          "childElements": []
        }
      }
    ]
  }
}
```

### Top-level fields

| Field | Type | Description |
|---|---|---|
| `data.configuration` | object | Same as image-to-design(scalingFactor/baseWidth/measurementUnit) |
| `data.size` | `{width, height}` | Document size shared by all pages (document units) |
| `data.pages` | array | One element per requested page, each containing a zero-based `page_no` and `schema` |

### pages[i].schema field (design tree node)

Each `schema` node is consistent with the `visualElement` structure of image-to-design, including:

| Field | Description |
|---|---|
| `elementId` | Unique identifier of the node |
| `elementType` | Types: `Layer`, `Group`, `Text`, `Image`, `Vector`, etc. |
| `childElements` | Array of child nodes (recursive structure) |
| `boundingBox` | `[x, y, width, height]` — Precise geometry in document coordinates, the most reliable source of positioning for PDFs |
| `displayOrder` | Z-axis order within the page, the smaller the value, the first to be drawn |
| `styleConfig.transformMatrix` | 6-element affine transformation `[a,b,c,d,e,f]`, required when processing rotated/beveled text |
| `styleConfig.characterData` | Independent style indexed by character (exist when there are multiple fonts in a text node) |
| `contentData.vectorData` | Vector path object: `pathItems[]` (`{pathType, coordinates[]}`) + fill/stroke attributes |
| `contentData.imageData` | base64 bytes of embedded image |

## Usage Example

```bash
# Local PDF, process first 3 pages
codia-design pdf-to-design --pdf ./report.pdf --pages 0,1,2 --out result.json

# URL pattern
codia-design pdf-to-design --pdf https://example.com/doc.pdf --pages 0,1 --out result.json
```

Iterate over all pages of text:

```js
const { data } = require('./result.json');
for (const [i, page] of data.pages.entries()) {
  console.log('-- Page', i, '--');
  extractText(page.schema).forEach(t => console.log(t));
}

function extractText(node, acc = []) {
  if (node.elementType === 'Text') acc.push(node.contentData?.textValue);
  node.childElements?.forEach(c => extractText(c, acc));
  return acc;
}
```

## Input Limits

The maximum rendering size and file size of each page of the input PDF depend on the plan tier:

| Packages | Maximum resolution per page | Maximum file size |
|---|---|---|
| Free | 1440×1440 | 5 MB |
| Starter | 4096×4096 | 20 MB |
| Pro | 10000×10000 | 50 MB |

## Errors & Billing

| HTTP | Meaning | Fix |
|---|---|---|
| 400 | Missing pdf_file / pdf_url, page_no format error, PDF encryption | Check that the file is not encrypted; URL pattern needs to provide `--pages` |
| 402 | Insufficient credits | Each page processed consumes 13 credits |
| 429 | Rate limit exceeded | Retry after backing off |
| 500 | Service internal error | Safe to try again |

**Credits**: 13 credits/page. After the command completes, the CLI checks `available_credits` and reminds the user if the remaining balance is below 2x the estimated page cost; this does not block generation. · **Duration**: Synchronous, long documents grow linearly by the number of pages
