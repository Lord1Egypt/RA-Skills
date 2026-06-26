# ADP CLI Sample code and response

## 1. Install ADP CLI

First check if ADP CLI is already installed by running `adp version`. If it succeeds, skip to step 2.

If not installed, choose the appropriate method:

```bash
# Method 1: npm (recommended, works on all platforms, China-friendly with npmmirror)
npm install -g @laiye-adp/agentic-doc-parse-and-extract-cli --registry=https://registry.npmmirror.com/ || npm install -g @laiye-adp/agentic-doc-parse-and-extract-cli

# Method 2: Shell script (Linux / macOS, if npm is not available)
curl -fsSL https://raw.githubusercontent.com/laiye-ai/adp-cli/main/scripts/adp-init.sh | bash

# Method 3: PowerShell script (Windows, if npm is not available)
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/laiye-ai/adp-cli/main/scripts/adp-init.ps1" -OutFile "$env:TEMP\adp-init.ps1"; & "$env:TEMP\adp-init.ps1"
```

### Resolving `adp` when it's not on PATH (important for Agents)

After `npm install -g`, the npm global bin directory is often **not** on the current shell's `PATH`, so a bare `adp` call will fail with "command not found". Agents must resolve the absolute path to the `adp` binary instead of relying on `PATH`.

**Resolution rule:**
- **Windows**: `npm prefix -g` returns the directory that already contains `adp.cmd` / `adp.exe`. Use `<prefix>\adp.cmd`.
- **Linux / macOS**: `npm prefix -g` returns the prefix; the binary lives at `<prefix>/bin/adp`.

**Cross-platform one-liner to locate the binary:**

```bash
# Linux / macOS (bash/zsh)
ADP_BIN="$(npm prefix -g)/bin/adp"
"$ADP_BIN" version
```

```powershell
# Windows (PowerShell)
$ADP_BIN = Join-Path (npm prefix -g) "adp.cmd"
& $ADP_BIN version
```

```bash
# Windows (Git Bash / MSYS in Claude Code)
ADP_BIN="$(npm prefix -g)/adp.cmd"
"$ADP_BIN" version
```

**Optional**: prepend the directory to PATH for the current shell session only (does not persist):
```bash
# bash/zsh
export PATH="$(dirname "$ADP_BIN"):$PATH"
```
```powershell
# PowerShell
$env:PATH = "$(Split-Path $ADP_BIN);$env:PATH"
```

### Agent installation logic

1. Run `adp version` — if it succeeds, CLI is already installed and on PATH, skip installation and use bare `adp` for all subsequent commands.
2. If not installed, check if `npm` is available → use Method 1. Else detect OS: Linux / macOS → Method 2; Windows → Method 3.
3. **After install, do NOT assume `adp` is on PATH.** Resolve `ADP_BIN`:
   - **Method 1 (npm)**: use the platform rule above (`npm prefix -g` ± `/bin`).
   - **Method 2 / 3 (shell scripts)**: parse the last line of script output — it prints `ADP_INSTALL_PATH=<absolute path>` for this exact purpose.
4. Verify with `"$ADP_BIN" version` (or `& $ADP_BIN version` in PowerShell). If it succeeds, install is good.
5. For all subsequent `adp ...` examples in this document, substitute the bare `adp` with `"$ADP_BIN"` (or your resolved absolute path) until the user opens a new terminal where PATH is refreshed.

## 2. Configure API Key and Base URL

### Verify configuration

```bash
adp config get
```

**Response example**：
```json
{
  "configured": true,
  "api_key_masked": "9ce0...ab4f",
  "api_base_url": "https://adp.laiye.com/"
}
```
### configuration
```bash
# Configure API Key
adp config set --api-key YOUR_API_KEY

# Configure Base URL
adp config set --api-base-url https://your-api-url.com
```


## 3. Query the list of available applications

```bash
# List available applications
adp app-id list 

# Show cached applications（The application ID cache is permanent and will not expire）
adp app-id cache 
```


**Response example**：
```json
  [
    {
      "app_id": "2f74******58400",
      "app_label": null,
      "app_name": "Custom Application Name",
      "app_type": 1
    },
   {
      "app_id": "ootb_******c8d1",
      "app_label": [
        "invoice",
        "Receipt",
        "Bill",
        "Financial document",
        "Information extraction"
      ],
      "app_name": "Invoice",
      "app_type": 0
    },
   {
      "app_id": "ootb_******a2b5",
      "app_label": [
        "Order",
        "E-commerce logistics",
        "Inventory management",
        "Information extraction"
      ],
      "app_name": "Purchase Order",
      "app_type": 0
    },
    {
      "app_id": "ootb_******y2b4",
      "app_label": [
        "Document parsing",
        "Image extraction",
        "OCR",
        "Structural analysis",
        "Batch Parsing"
      ],
      "app_name": "Document parsing",
      "app_type": 0
    },
  ]
```

## 4. Create a custom extraction application

```bash
# First, use AI to generate field recommendations
adp custom-app ai-generate --app-id YOUR_APP_ID --file-url https://example.com/sample-invoice.pdf

# Second, Create a custom application
adp custom-app create \
  --api-key "9ce0********4b4f" \
  --app-name "Financial document extraction" \
  --extract-fields '[
    {"field_name":"Invoice number","field_type":"string","field_prompt":"Extract the serial number at the top left corner of the invoice"},
    {"field_name":"Invoice date","field_type":"date","field_prompt":"Extract the invoice issuance date"},
    {"field_name":"Product details","field_type":"table","field_prompt": null,"sub_fields": 
    [
      {"field_name":"Contract Number","field_type":"string","field_prompt":"Extract the contract number"},
      {"field_name":"Signing Date","field_type": "date","field_prompt":"Extract the signing date"}
    ]
    }
  ]' \
  --parse-mode "standard" \
  --enable-long-doc true \
  --long-doc-config '[
    {"doc_type":"Contract","doc_desc":"Multi-page contract"},
    {"doc_type":"Tender document","doc_desc":"Engineering tender documents"}
  ]'
```

**Response example**：
```json
{
  "code": "success",
  "message": "",
  "tips": null,
  "data": {
    "app_id": "ed5195882cd311f19359627c0509427d",
    "app_name": "Custom Application Name",
    "app_label": ["Custom Label 1", "Custom Label 2"] , "config_version": "v1"
  }
}
```

## 5. Document Parsing

```bash
adp parse url <File URL> --app-id YOUR_APP_ID
```

**Response example**：
```json
{
  "data": {
    "task_id": "",
    "file_url": "",
    "status": 4,
    "message": "",
    "doc_recognize_result": [
      {
        "page_num": 1,
        "document_content": "Electronic invoice\n\nTax Bureau\n\nInvoice code: 144032009110\n\nInvoice number: 23700770\n\ndate: 2020-12-13",
        "document_details": [
          {
            "type": "Text",
            "text": "Incoice",
            "position": [
              {
                "points": [
                  {"x": 311, "y": 50},
                  {"x": 369, "y": 50},
                  {"x": 369, "y": 59},
                  {"x": 311, "y": 59}
                ]
              }
            ],
            "ocr_confidence": {
              "ocr_mean_confidence": 0.9989976211580984,
              "ocr_min_confidence": 0.9989976211580984,
              "is_overall_confidence": 1
            }
          },
          {
            "type": "Text",
            "text": "invoice number: 23700770",
            "position": [
              {
                "points": [
                  {"x": 493, "y": 32},
                  {"x": 573, "y": 32},
                  {"x": 573, "y": 42},
                  {"x": 493, "y": 42}
                ]
              }
            ],
            "ocr_confidence": {
              "ocr_mean_confidence": 0.9999735751246535,
              "ocr_min_confidence": 0.9997363785557283,
              "is_overall_confidence": 1
            }
          },
          {
            "type": "Text",
            "text": "Date: 2020-12-13",
            "position": [
              {
                "points": [
                  {"x": 493, "y": 50},
                  {"x": 623, "y": 50},
                  {"x": 623, "y": 60},
                  {"x": 493, "y": 60}
                ]
              }
            ],
            "ocr_confidence": {
              "ocr_mean_confidence": 0.9999853806227165,
              "ocr_min_confidence": 0.9998685294404747,
              "is_overall_confidence": 1
            }
          },
          {
            "type": "Picture",
            "text": "https://adp.laiye.com/web/agentic_doc_processor/laiye/file/e4b140162cd511f19d1c627c0509427d",
            "position": [
              {
                "points": [
                  {"x": 541, "y": 329},
                  {"x": 666, "y": 329},
                  {"x": 666, "y": 428},
                  {"x": 541, "y": 428}
                ]
              }
            ],
            "ocr_confidence": {
              "ocr_mean_confidence": 0.9506070037576528,
              "ocr_min_confidence": 0.07206936378157035,
              "is_overall_confidence": 0
            }
          }
        ]
      }
    ]
  },
  "code": "success",
  "message": "",
  "tips": null
}
```

## 6. Document extraction

```bash
adp extract url <file URL> --app-id YOUR_APP_ID
```

**Response example**：
```json
[
  {
    "field_key": "invoice_number",
    "field_name": "invoice number",
    "field_values": [
      {
        "field_value": "24VLT0591617",
        "field_confidence": 1.0,
        "references": []
      }
    ]
  },
  {
    "field_key": "invoice_date",
    "field_name": "date",
    "field_values": [
      {
        "field_value": "2024-11-01",
        "field_confidence": 1.0,
        "references": []
      }
    ]
  },
  {
    "field_key": "currency",
    "field_name": "Currency type",
    "field_values": [
      {
        "field_value": "EUR",
        "field_confidence": 0.0,
        "references": []
      }
    ]
  },
  {
    "field_key": "total_without_tax",
    "field_name": "Total amount (excluding tax)",
    "field_values": [
      {
        "field_value": "€ 1.223,43",
        "field_confidence": 1.0,
        "references": []
      }
    ]
  },
  {
    "field_key": "line_items",
    "field_name": "Product Details Table",
    "references": [],
    "field_confidence": 1.0,
    "table_values": [
      [
        {
          "field_name": "Project code",
          "field_values": [
            {
              "field_value": "241021 SI0421.00",
              "field_confidence": 1.0,
              "references": "Project code: 241021 SI0421.00"
            }
          ],
          "field_key": "line_items_item_code"
        },
        {
          "field_name": "Description",
          "field_values": [
            {
              "field_value": "TESLA MODEL 3 BEV LONG-RANGE DUAL MOTOR AWD",
              "field_confidence": 1.0,
              "references": "Description: TESLA MODEL 3 BEV LONG-RANGE DUAL MOTOR AWD"
            }
          ],
          "field_key": "line_items_description"
        },
        {
          "field_name": "number",
          "field_values": [
            {
              "field_value": "1",
              "field_confidence": 1.0,
              "references": "number: 1"
            }
          ],
          "field_key": "line_items_quantity"
        },
        {
          "field_name": "Unit price",
          "field_values": [
            {
              "field_value": "€ 1.223,43",
              "field_confidence": 1.0,
              "references": "Unit price: € 1.223,43"
            }
          ],
          "field_key": "line_items_unit_price"
        },
        {
          "field_name": "Total amount",
          "field_values": [
            {
              "field_value": "€ 1.223,43",
              "field_confidence": 1.0,
              "references": "Total amount: € 1.223,43"
            }
          ],
          "field_key": "line_items_total_amount"
        }
      ]
    ]
  }
]
```

## 7. Batch Processing 
```bash
# Batch processing of documents in the local folder
adp parse local <folder path> --app-id <app_ID> --export <folder path> --concurrency 2
adp extract local <folder path> --app-id <app_ID> --export <folder path> --concurrency 2 

# Batch processing of documents within the URL list file
adp parse url <URL list file path> --app-id <app_ID> --export <folder path> --concurrency 2
adp extract url <URL list file path> --app-id <app_ID> --export <folder path> --concurrency 2
```

**Note**: Batch processing requires processing all the files in the folder sequentially, and the output result supports being specified to be saved in the user-defined folder path.

## 8. Asynchronous Processing 
```bash
# Batch processing of documents in the local folder
adp parse local <file path> --app-id <app_ID> --export <folder path> --concurrency 2 --async
adp extract local <file path> --app-id <app_ID> --export <folder path> --concurrency 2 --async 

# Batch processing of documents within the URL list file
adp parse url <file URL> --app-id <app_ID> --export <folder path> --concurrency 2 --async
adp extract url <file URL> --app-id <app_ID> --export <folder path> --concurrency 2 --async 

# Query the status and results of asynchronous parsing processing tasks 
adp parse query <task_id>

# Query the status and results of asynchronous extraction processing tasks 
adp extract query <task_id>
```


**Query Response example**：
```json
{
  "Task_ID": "dffe****427d",
  "Status": "SUCCESS"
}
```

## 9. Batch Processing Output

When processing multiple files, the CLI creates an output directory and writes individual result files.

### Sync batch output

```bash
adp extract local ./invoices/ --app-id YOUR_APP_ID --export ./results --concurrency 2
```

**stdout output (summary JSON):**
```json
{
  "total": 3,
  "success": 2,
  "failed": 1,
  "output_dir": "/home/user/results",
  "files": [
    {"input": "invoice1.pdf", "output": "invoice1.pdf.json", "status": "success"},
    {"input": "invoice2.pdf", "output": "invoice2.pdf.json", "status": "success"},
    {"input": "corrupted.pdf", "output": "corrupted.pdf.error.json", "status": "failed", "error": "Bad request: unsupported file format"}
  ]
}
```

**Output directory structure:**
```
results/
  ├── invoice1.pdf.json          # Full extract result (same format as single-file response)
  ├── invoice2.pdf.json
  ├── corrupted.pdf.error.json   # {"input": "corrupted.pdf", "status": "failed", "error": "..."}
  └── _summary.json              # Same content as stdout summary
```

**Agent must:** Read `output_dir` from summary, then read each `{output_dir}/{filename}.json` to get individual results.

### Async batch with --no-wait

```bash
adp extract local ./invoices/ --app-id YOUR_APP_ID --async --no-wait --export tasks.json
```

**Output (tasks.json):**
```json
[
  {"path": "invoice1.pdf", "task_id": "abc123def456"},
  {"path": "invoice2.pdf", "task_id": "ghi789jkl012"}
]
```

**Later, query all tasks:**
```bash
adp extract query --file tasks.json --watch --export ./results
```

---

## 10. Error Scenario Examples

### Authentication error (API Key not configured)

```bash
adp extract url https://example.com/invoice.pdf --app-id YOUR_APP_ID --json
```

**stderr output:**
```json
{
  "type": "AUTH_ERROR",
  "message": "Authentication error: unauthorized",
  "fix": "Check your API key is correct and has not expired.",
  "retryable": false,
  "details": {"context": "extract"}
}
```
**Exit code:** 4

**Agent recovery:** Run `adp config get` to check, then prompt user for API Key.

### Credit balance insufficient

```bash
adp credit --json
```

```json
{
  "credit_balance": 0.0
}
```

**Agent recovery:** Report balance to user. Billing: parse 0.5/page, extract 1-1.5/page.

### Invalid app-id

```bash
adp extract url https://example.com/invoice.pdf --app-id invalid_id --json
```

**stderr output:**
```json
{
  "type": "RESOURCE_ERROR",
  "message": "Resource not found: app not found",
  "fix": "Check the resource ID or path is correct.",
  "retryable": false,
  "details": {"context": "extract"}
}
```
**Exit code:** 3

**Agent recovery:** Run `adp app-id list` to get valid app IDs.

### Unsupported file format

```bash
adp parse local ./readme.txt --app-id YOUR_APP_ID --json
```

**stderr output:**
```json
{
  "type": "PARAM_ERROR",
  "message": "Parameter error: unsupported file type",
  "fix": "Check the input parameters are correct.",
  "retryable": false,
  "details": {"context": "parse"}
}
```
**Exit code:** 2

**Agent recovery:** Check file extension. Supported: .jpg, .jpeg, .png, .bmp, .tiff, .tif, .pdf, .doc, .docx, .xls, .xlsx

### Network timeout

```bash
adp parse url https://example.com/large-doc.pdf --app-id YOUR_APP_ID --json
```

**stderr output:**
```json
{
  "type": "NETWORK_ERROR",
  "message": "Network error: i/o timeout",
  "fix": "Check your network connection and try again.",
  "retryable": true,
  "details": {"context": "parse"}
}
```
**Exit code:** 1

**Agent recovery:** Retry with `--timeout 1800`, or switch to `--async` mode for large files.

### Async task not yet complete

```bash
adp parse query abc123def456 --json
```

```json
{
  "task_id": "abc123def456",
  "status": "PROCESSING"
}
```

**Agent recovery:** Wait and query again. Use `--watch` flag to auto-poll until completion.

### Batch partial failure

```bash
adp extract local ./mixed_docs/ --app-id YOUR_APP_ID --export ./results --json
```

**Exit code:** 6 (partial failure)

**Agent recovery:** Parse the summary JSON, handle successful files normally, report or retry failed files individually.

---

## Description of Response Fields 

### Document Extraction Response Key Fields
- `field_name`: The name of the extracted field. If it contains "table_values", it indicates that this is a table field and the `field_name` is usually the name of the table; if it does not contain "table_values", it indicates an ordinary field and the `field_name` is usually the description of the field
- `field_value`: The specific value of the extraction result
- `field_confidence`: The confidence score of the extraction result, ranging from 0 to 1. The higher the value, the more reliable the extraction result
- `table_values`: The extraction result of the table type, presented in a two-dimensional array format, including the extraction result of each cell and the corresponding field name, confidence level, etc. The array under it usually contains the contents of `field_name`, `field_value`, `field_confidence`, etc. 

## Custom Application Parameter Description 

### parse_mode (Parsing Mode)
There are 3 modes available for selection:
1. `advance`: Enhanced parsing, suitable for documents with complex formats such as seals, signatures, and multi-tables
2. `standard`: Standard parsing, suitable for standard and clear electronic documents
3. `agentic`: Intelligent parsing, intelligently combining multiple models for parsing, significantly improving the stability of parsing for complex documents 

### Other Parameters
- `app_label`: Up to 5 can be added
- `enable-long-doc`: Default is off (false). It can be enabled (true) when dealing with long documents. It precisely extracts fields within the specified document type and uses independent billing (0.5 credit per page). It is usually enabled when the document has more than 20 pages and has multiple types. When enabled, it needs to be used in conjunction with `doc_type` and `doc_desc`.
