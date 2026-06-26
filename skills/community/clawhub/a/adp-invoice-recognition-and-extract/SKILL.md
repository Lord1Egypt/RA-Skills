---
name: invoice-recognition-and-extract
description: Multi-language, multi-currency global invoice recognition and extraction — accurately extracts invoice number, date, supplier, buyer, currency, tax amount, total amount, and line items, outputting structured JSON. Zero-configuration, out-of-the-box, suitable for accounts payable automation, expense reimbursement, and cross-border trade document processing.
---

# Global Invoice Recognition and Extraction Skill

Powered by [Laiye ADP (Agentic Document Processing)](https://adp-global.laiye.com/?utm_source=clawhub), this skill delivers intelligent, high-precision parsing and information extraction for standard and non-standard invoices, bills, and vouchers from all regions worldwide. It supports all file types including electronic PDFs, scanned documents, and photographs, and outputs standardized structured JSON data for seamless integration with business processes and downstream automation.

> New users receive **100 free credits per month** (refreshed monthly) for invoice extraction and other document processing scenarios. **Limited-Time Offer:** Use the invoice extraction feature for the first time and receive an additional **1,000 free pages of global invoice extraction** — limited to the first **100** users only, first come first served! ADP provides a standard commercial API that can be **integrated into business systems within 1 hour**.
</br> Register now: [Global](https://adp-global.laiye.com/?utm_source=clawhub) | [China Mainland](https://adp.laiye.com/?utm_source=clawhub)

Why choose us?
  - Global invoices with zero barriers — multi-language, multi-format precision recognition
  - 100+ languages fully covered: English, Japanese, Korean, German, French, Thai, and all other major languages — invoices and receipts all supported
  - Adaptive to all formats: standard VAT invoices, unstructured receipts, mixed-format bills — all recognized
  - 95%+ accuracy: precise extraction of key fields, dramatically reducing manual verification, translation, and data entry costs
  - Agentic self-optimization: continuously fine-tuned on your business data — the more you use it, the more accurate and tailored it becomes

---

## Quick Start Guide

### Core Workflow

1. **Install dependencies**: On first run, install the ADP CLI tool.
2. **Authentication setup**: On first run, execute `adp config get` to check credentials. If not configured, prompt the user to provide an API Key.
3. **Get app list**: On first run, retrieve the out-of-the-box app list via `adp app-id list --app-type 0`, find the invoice extraction app, and record its `app_id` (prefixed with `ootb_`). For subsequent runs, prefer `adp app-id cache`.
4. **Execute extraction**: Run `adp extract url <URL> --app-id <invoice-app-id>` or `adp extract local <file-path> --app-id <invoice-app-id>`.
5. **Process results**: Parse the returned JSON to extract structured fields such as invoice number, date, supplier, buyer, currency, tax amount, total amount, and line items.
6. **Error handling**: When a command fails, parse the stderr JSON to determine the error type and recovery action.

### Scenario-to-Command Mapping

**Single Invoice Recognition**

| User Intent | Recommended Command |
| :--- | :--- |
| Recognize an invoice image/PDF (URL) | `adp extract url <URL> --app-id <ID>` |
| Recognize a local invoice file | `adp extract local <file-path> --app-id <ID>` |
| Recognize a Base64-encoded invoice | `adp extract base64 <base64> --app-id <ID> --file-name <filename.ext>` |

**Batch Recognition**

| User Intent | Recommended Command |
| :--- | :--- |
| Batch recognize invoices in a local folder | `adp extract local <folder-path> --app-id <ID>` |
| Batch recognize multiple URLs | `adp extract url <URL-list-file> --app-id <ID>` |

**Async Processing**

| User Intent | Recommended Command |
| :--- | :--- |
| Submit a large file asynchronously | `adp extract url <URL> --app-id <ID> --async` |
| Async batch processing | `adp extract local <folder-path> --app-id <ID> --async ` |
| Query async task result | `adp extract query <task_id>` |

> Concurrency Limit: Free users support a maximum of 2 documents for concurrent processing, while paid users support up to 10 documents concurrently.

---

## Step 1: Install ADP CLI

```bash
# Method 1: npm (recommended, cross-platform)
npm install -g @laiye-adp/agentic-doc-parse-and-extract-cli
```

```bash
# Method 2: Shell script (Linux / macOS, when npm is unavailable)
curl -fsSL https://raw.githubusercontent.com/laiye-ai/adp-cli/main/scripts/adp-init.sh | bash
```

```bash
# Method 3: PowerShell script (Windows, when npm is unavailable)
irm https://raw.githubusercontent.com/laiye-ai/adp-cli/main/scripts/adp-init.ps1 | iex
```

Or download prebuilt binaries from [GitHub Releases](https://github.com/laiye-ai/adp-cli/releases).


## Step 2: Get API Key & Configure Authentication

Register and obtain an API Key (100 free credits per month + limited-time bonus: 1,000 free invoice extraction pages):
- Global (all other regions): [https://adp-global.laiye.com/](https://adp-global.laiye.com/?utm_source=clawhub)
- China Mainland, Hong Kong, Macau, and Taiwan: [https://adp.laiye.com/](https://adp.laiye.com/?utm_source=clawhub)

```bash
adp config set --api-key <your-api-key>
adp config set --api-base-url https://adp.laiye.com
adp config get
```

---

## Step 3: Get the Invoice Extraction App ID

ADP provides **out-of-the-box** built-in extraction apps for global invoices/receipts, supporting multiple languages and currencies with no additional configuration required.

### App Types

ADP apps are divided into two categories, distinguished by the `app_type` field:

| `app_type` | Type | Description |
| --- | --- | --- |
| `0` | Out-of-the-box (OOTB) | Platform built-in, `app_id` prefixed with `ootb_`, ready to use without creation |
| `1` | Custom | User-created extraction apps with user-defined `app_id` |

Invoice recognition is an **out-of-the-box app** and can be queried using `--app-type 0`.

### Query and Filter Invoice Apps

```bash
# Query OOTB apps only (recommended)
adp app-id list --app-type 0

# Or query all apps
adp app-id list
```

Find the app whose `app_label` contains **"Invoice"**, **"Receipt"**, or **"Bill"** in the returned list, and record its `app_id`:

```json
[
  {
      "app_id": "ootb_*****c8d1",
      "app_label": [
        "Invoice",
        "Receipt",
        "Information Extraction",
        "High accuracy",
        "High-speed extraction"
      ],
      "app_name": "Invoice/Receipt",
      "app_type": 0
    }
]
```

> In the example above, `"app_id": "ootb_*****c8d1"` is the global invoice extraction app. `app_type` of `0` indicates an out-of-the-box app; `1` indicates a custom app.

### Cache App ID (Recommended)

After the initial query, prefer using cache for subsequent requests to avoid redundant API calls:

```bash
# Use cache for subsequent calls
adp app-id cache
```

**Important**: Each account's `app_id` is unique and fixed — it will not change unless the user explicitly deletes the app. It is recommended that the Agent save the invoice app's `app_id` in context and reuse it directly in subsequent calls.

---

## Step 4: Execute Invoice Extraction

### Single Invoice Extraction (URL)

```bash
adp extract url https://example.com/invoice.pdf --app-id <invoice-app-id>
```

### Single Invoice Extraction (Local File)

```bash
adp extract local ./invoice.pdf --app-id <invoice-app-id>
```

### Single Invoice Extraction (Base64)

```bash
adp extract base64 <base64-string> --app-id <invoice-app-id> --file-name <filename.ext>
```

### Response Example

ADP automatically supports invoice recognition in 100+ languages across all regions globally and automatically detects currencies. Extraction results are returned as unified structured JSON. The response contains two types of fields: **regular fields** and **table fields (line items)**.

> The following example is a simplified format showing only core fields. The full response also includes `field_confidence` (confidence score) and `references` (source location) metadata — see "Common Field Structure" below for details.

```json
[
  {
    "field_key": "invoice_number",
    "field_name": "Invoice Number",
    "field_values": [
      {
        "field_value": "INV-2026-003721"
      }
    ]
  },
  {
    "field_key": "invoice_date",
    "field_name": "Invoice Date",
    "field_values": [
      {
        "field_value": "2026-03-15"
      }
    ]
  },
  {
    "field_key": "due_date",
    "field_name": "Due Date",
    "field_values": [
      {
        "field_value": "2026-04-15"
      }
    ]
  },
  {
    "field_key": "currency",
    "field_name": "Currency",
    "field_values": [
      {
        "field_value": "USD"
      }
    ]
  },
  {
    "field_key": "supplier_name",
    "field_name": "Supplier Name",
    "field_values": [
      {
        "field_value": "Acme Global Trading Co., Ltd."
      }
    ]
  },
  {
    "field_key": "supplier_address",
    "field_name": "Supplier Address",
    "field_values": [
      {
        "field_value": "1234 Commerce Blvd, Suite 500, San Francisco, CA 94105, USA"
      }
    ]
  },
  {
    "field_key": "buyer_name",
    "field_name": "Buyer Name",
    "field_values": [
      {
        "field_value": "Eastern International Trading Co., Ltd."
      }
    ]
  },
  {
    "field_key": "buyer_address",
    "field_name": "Buyer Address",
    "field_values": [
      {
        "field_value": "1000 Lujiazui Ring Road, Pudong New Area, Shanghai"
      }
    ]
  },
  {
    "field_key": "subtotal",
    "field_name": "Subtotal",
    "field_values": [
      {
        "field_value": "8,500.00"
      }
    ]
  },
  {
    "field_key": "tax_amount",
    "field_name": "Tax Amount",
    "field_values": [
      {
        "field_value": "680.00"
      }
    ]
  },
  {
    "field_key": "total_amount",
    "field_name": "Total Amount",
    "field_values": [
      {
        "field_value": "9,180.00"
      }
    ]
  },
  {
    "field_key": "line_items",
    "field_name": "Line Items",
    "field_confidence": 0.98,
    "table_values": [
      [
        {
          "field_name": "Description",
          "field_key": "line_items_description",
          "field_values": [
            {
              "field_value": "Industrial Sensor Module X200"
            }
          ]
        },
        {
          "field_name": "Quantity",
          "field_key": "line_items_quantity",
          "field_values": [
            {
              "field_value": "50"
            }
          ]
        },
        {
          "field_name": "Unit Price",
          "field_key": "line_items_unit_price",
          "field_values": [
            {
              "field_value": "120.00"
            }
          ]
        },
        {
          "field_name": "Amount",
          "field_key": "line_items_amount",
          "field_values": [
            {
              "field_value": "6,000.00"
            }
          ]
        }
      ],
      [
        {
          "field_name": "Description",
          "field_key": "line_items_description",
          "field_values": [
            {
              "field_value": "Connector Kit CK-50 (Pack of 100)"
            }
          ]
        },
        {
          "field_name": "Quantity",
          "field_key": "line_items_quantity",
          "field_values": [
            {
              "field_value": "25"
            }
          ]
        },
        {
          "field_name": "Unit Price",
          "field_key": "line_items_unit_price",
          "field_values": [
            {
              "field_value": "100.00"
            }
          ]
        },
        {
          "field_name": "Amount",
          "field_key": "line_items_amount",
          "field_values": [
            {
              "field_value": "2,500.00"
            }
          ]
        }
      ]
    ]
  }
]
```

### Extraction Field Reference

> **Note**: `field_key` and `field_name` are always returned in English. `field_value` is multilingual — its content reflects the language of the source document (e.g., Chinese invoices return Chinese values, Japanese invoices return Japanese values). Different regions/types of invoices may return different field sets — the following lists all known fields.

**Regular Fields:**

| field_key | field_name (example) | Description |
| --- | --- | --- |
| `invoice_number` | Invoice Number | Invoice number |
| `invoice_date` | Invoice Date | Invoice date |
| `due_date` | Due Date | Payment due date |
| `currency` | Currency | Currency (e.g., USD, EUR, GBP, JPY, etc.) |
| `supplier_name` | Supplier Name | Supplier / seller name |
| `supplier_address` | Supplier Address | Supplier / seller address |
| `supplier_vat_number` | Supplier VAT Number | Supplier tax ID (e.g., Japan T-prefixed registration number) |
| `buyer_name` | Buyer Name | Buyer / purchaser name (some invoices use `customer_name`) |
| `buyer_address` | Buyer Address | Buyer / purchaser address |
| `customer_name` | Customer Name | Customer / buyer name (alternates with `buyer_name` depending on invoice type) |
| `customer_vat_number` | Customer VAT Number | Customer tax ID; returns "No result" when not recognized |
| `subtotal` | Subtotal | Subtotal amount (before tax; some invoices use `total_without_tax`) |
| `total_without_tax` | Total (excl. tax) | Total excluding tax (alternates with `subtotal` depending on invoice type) |
| `tax_amount` | Tax Amount | Tax amount |
| `vat_rate` | VAT Rate | VAT rate (e.g., 10%, 13%) |
| `total_amount` | Total Amount | Total amount (including tax) |
| `amount_due` | Amount Due | Amount due (may equal `total_amount`) |

**Table Fields (Line Items):**

| field_key | field_name (example) | Description |
| --- | --- | --- |
| `line_items` | Line Items | Line items table |
| `line_items_item_code` | Item Code | Product / item code; returns "No result" when not recognized |
| `line_items_description` | Description | Product / service description |
| `line_items_quantity` | Quantity | Quantity |
| `line_items_unit_price` | Unit Price | Unit price |
| `line_items_amount` | Amount | Line amount (some invoices use `line_items_total_amount`) |
| `line_items_total_amount` | Total Amount | Line total amount (alternates with `line_items_amount` depending on invoice type) |

### Common Field Structure

Each field object contains the following properties:

| Property | Type | Description |
| --- | --- | --- |
| `field_key` | string | Field identifier (machine-readable) |
| `field_name` | string | Field name (human-readable, localized based on document language) |
| `field_values` | array | Extraction result array (present for regular fields) |
| `field_values[].field_value` | string | Extracted value; empty string or "No result" when not recognized |
| `field_values[].field_confidence` | number | Confidence score (0.0–1.0); 0.0 indicates not recognized / low confidence |
| `field_values[].references` | array | Source location references (coordinates or text snippets) |
| `field_confidence` | number | Overall confidence score (table-level for table fields) |
| `table_values` | array[array] | Only present for table fields. 2D array: each row is a line item, each cell contains `field_name`, `field_key`, `field_values` |

**How to distinguish field types:** If `table_values` is present → table field, read from `table_values`; otherwise → regular field, read from `field_values`.

---

## Step 5: Batch Processing & Async Mode

### Batch Processing (Local Folder)

```bash
adp extract local ./invoices/ --app-id <invoice-app-id> --export ./results/ 
```

Response summary:
```json
{
  "total": 10,
  "success": 9,
  "failed": 1,
  "output_dir": "/absolute/path/to/results",
  "files": [
    {
      "input": "invoice-001.pdf",
      "output": "invoice-001.pdf.json",
      "status": "success"
    },
    {
      "input": "invoice-002.pdf",
      "output": "invoice-002.pdf.json",
      "status": "success"
    },
    {
      "input": "damaged.pdf",
      "output": "damaged.pdf.error.json",
      "status": "failed",
      "error": "File is corrupted or unreadable"
    }
  ]
}
```

**Batch Response Summary Fields:**

| Field | Type | Description |
| --- | --- | --- |
| `total` | number | Total number of files |
| `success` | number | Number of successfully processed files |
| `failed` | number | Number of failed files |
| `output_dir` | string | Absolute path to the output directory |
| `files` | array | Processing result list for each file |
| `files[].input` | string | Input filename |
| `files[].output` | string | Output result filename (`.json` on success, `.error.json` on failure) |
| `files[].status` | string | Processing status: `"success"` or `"failed"` |
| `files[].error` | string | Only present on failure; describes the failure reason |

### Async Processing

```bash
# Submit async task
adp extract url https://example.com/invoice.pdf --app-id <invoice-app-id> --async

# Query task result
adp extract query <task_id>
```

---

## Command Quick Reference

```bash
# Check installation
adp version

# View configuration
adp config get

# List all apps
adp app-id list

# List OOTB apps only (app_type=0)
adp app-id list --app-type 0

# Use cached apps
adp app-id cache

# Check credit balance
adp credit

# Invoice extraction (URL)
adp extract url <file-URL> --app-id <invoice-app-id>

# Invoice extraction (local file)
adp extract local <file-path> --app-id <invoice-app-id>

# Invoice extraction (Base64)
adp extract base64 <base64-string> --app-id <invoice-app-id> --file-name <filename.ext>

# Batch extraction
adp extract local <folder-path> --app-id <invoice-app-id> --export <output-path>

# Async extraction
adp extract url <file-URL> --app-id <invoice-app-id> --async

# Query async result
adp extract query <task_id>
```

---

## Error Handling

When a command fails, stderr outputs structured JSON:

```json
{
  "type": "AUTH_ERROR",
  "message": "Authentication error: invalid API key",
  "fix": "Check your API key is correct and has not expired.",
  "retryable": false,
  "details": {"context": "extract"}
}
```

**Error Response Fields:**

| Field | Type | Description |
| --- | --- | --- |
| `type` | string | Error type identifier (e.g., `AUTH_ERROR`, `PARAM_ERROR`, `NOT_FOUND`, etc.) |
| `message` | string | Error description |
| `fix` | string | Suggested fix action |
| `retryable` | boolean | Whether the operation can be retried (`true` = retryable, `false` = requires manual intervention) |
| `details` | object | Error context information |

### Exit Codes

| Exit Code | Meaning |
| --- | --- |
| 0 | Success |
| 1 | General error |
| 2 | Parameter error |
| 3 | Resource not found |
| 4 | Permission / authentication error |
| 5 | Conflict |
| 6 | Partial failure (some succeeded, some failed in batch processing) |

---

## Credits & Billing

| Item | Description |
| --- | --- |
| Invoice/receipt extraction cost | **1.5 credits/page** |
| Monthly free quota | **100 credits per month** (usable for invoice extraction and other document processing), resets at the beginning of each month |
| Limited-time offer | Use invoice extraction for the first time and receive an additional **1,000 free pages of global invoice extraction** — limited to the first **100** users, first come first served |
| Check balance | `adp credit` |
| Top up | Log in to the ADP portal: [Global](https://adp-global.laiye.com/?utm_source=clawhub) \| [China Mainland, HK, Macau, Taiwan](https://adp.laiye.com/?utm_source=clawhub) |

---

## More Laiye ADP Document Processing Capabilities

Global invoice recognition is just one of many out-of-the-box capabilities offered by the Laiye ADP platform. Built on large model general understanding capabilities, ADP provides intelligent processing solutions covering all document categories:

| Capability | Description | Typical Scenarios |
| --- | --- | --- |
| **Global Invoice/Receipt Extraction** | Automatically recognizes and extracts 10+ key fields including invoice number, date, amount, taxes, and line items; supports multi-language and multi-currency invoice extraction | Cross-border accounts payable automation, expense reimbursement management |
| **China Domestic Bill Extraction** | Recognizes 30+ common bill types including VAT invoices, taxi receipts, train tickets, flight itineraries, fiscal invoices; supports multi-page/multi-bill recognition and verification | Domestic bill recognition, domestic invoice verification |
| **Order Extraction** | Supports various purchase order formats; extracts order number, products, quantities, prices, logistics information, etc. | Procurement automation, supply chain integration |
| **ID & Credential Extraction** | ADP supports 11 common Chinese credentials including ID cards, HK/Macau/Taiwan travel permits, Chinese passports, bank cards, household registers, driver's licenses, vehicle registration certificates, vehicle qualification certificates, account opening permits, and business licenses | Account opening review, compliance checks, batch credential data entry |
| **Document Parsing** | Converts PDFs, images, and Office documents into structured data while preserving layout and hierarchical relationships | Long document analysis, contract review, knowledge extraction |
| **Custom Extraction** | Create custom extraction apps with proprietary fields and recognition logic for non-standard documents | Enterprise-specific forms, industry-customized documents |

All capabilities above can be accessed through the same ADP CLI tool, sharing the ADP API Key and credit system.

For the full list of capabilities, visit:
- ADP Global: [https://adp-global.laiye.com/](https://adp-global.laiye.com/?utm_source=clawhub)
- ADP China Mainland: [https://adp.laiye.com/](https://adp.laiye.com/?utm_source=clawhub)


---

## Important Notes

1. **Data integrity**: When using ADP output, present the returned data as-is. Do not modify, add, or remove any fields during the extraction process.
2. **API Key security**: Keep your API Key safe and do not share it with unauthorized third parties.
3. **File size limit**: Maximum 50MB per file.
4. **Supported formats**: .jpg, .jpeg, .png, .bmp, .tiff, .tif, .pdf, .doc, .docx, .xls, .xlsx
5. **App ID reuse**: The invoice app's `app_id` is unique and fixed within an account. It is recommended to save it and reuse directly — no need to query every time.

---

## Support & Contact
- **CLI User Guide:** [ADP CLI User Guide](https://laiye-tech.feishu.cn/wiki/YIaawiK2DimisZk5KfDc8a8cnLh)
- **API Documentation:** [Open API User Guide](https://laiye-tech.feishu.cn/wiki/S1t2wYR04ivndKkMDxxcp2SFnKd)
- **ADP Product Manual:** [Public Cloud Manual](https://laiye-tech.feishu.cn/wiki/OfexwgVUQiOpEek4kO7c7NEJnAe)
- **Issue Tracker:** [GitHub Issues](https://github.com/laiye-ai/adp-cli/issues)
- **Email:** global_product@laiye.com
- **Website:** [Laiye](https://laiye.com/en/product/adp-platform)

Copyright 2026 [Laiye Technology (Beijing) Co., Ltd.] All rights reserved.
