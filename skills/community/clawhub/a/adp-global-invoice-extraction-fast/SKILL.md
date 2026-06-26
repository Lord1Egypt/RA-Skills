---
name: adp-global-invoice-extraction-fast
description: High-performance API for global invoice recognition. Each page is parsed in 5 seconds with reliable high-concurrency support. It extracts full invoice data and returns structured JSON directly, ideal for financial automation and cross-border document processing.
---

# 🚀 Laiye ADP Global Document Intelligent Extraction · Fast
Developed by the ADP Intelligent Document Processing team of Laiye Technology. Tailored for **global cross-border finance, automation, system integration and high-concurrency production scenarios**, it delivers low-latency, high-throughput, full-format and multi-language intelligent extraction for invoices, bills and receipts. It fully supports structured standard documents, unstructured overseas purchase invoices and receipts. Whether it is electronic PDFs, scanned copies or images, **each page can be parsed and output as standardized JSON structured data in as fast as 5 seconds**. It supports enterprise-level batch processing and 7×24 stable service, empowering end-to-end workflow automation, intelligent reconciliation and data warehousing.

## ⭐ Core Advantages of High-Speed Edition
⚡ Ultra-fast Processing: Each page is parsed within 5 seconds. It supports large-scale concurrent calls to meet high-intensity processing requirements in production environments.  
✅ Enterprise-grade High-throughput Architecture: Low-latency response and stable processing for massive files.  
🌐 Multi-language Support: Recognizes invoices and receipts in English, Japanese, Korean, German, French, Thai and hundreds of other languages.  
📄 Full-format Compatibility: Adapts to VAT invoices worldwide, tax documents from Southeast Asia, unstructured receipts and mixed-format vouchers.  
🎯 Over 99% Extraction Accuracy: Accurately extracts key fields and greatly reduces costs for manual verification, translation and data entry.  
🤖 Continuous AI Optimization: The model keeps iterating and improving based on business data, and supports customized adaptation for enterprises.  

## 📌 Application Scenarios
| User Group | Usage Scenarios |
| ---- | ---- |
| Enterprise Finance & Shared Service Center | Batch processing of multi-language documents for automated bookkeeping, settlement and reconciliation. |
| System Integrators | API integration with up to 10 concurrent requests and low latency, complying with production-level SLA requirements. |
| Developers & Technical Teams | Integrate high-performance ADP API to build stable and efficient automated document processing workflows. |

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

Find the app whose `app_label` contains **"Invoice"**, **"Receipt"**, **"high accuracy"**, **high-speed extraction** in the returned list, and record its `app_id`:

```json
[
  {
      "app_id": "ootb_*****d9e2",
      "app_label": [
        "Invoice",
        "Receipt",
        "global invoices",
        "high accuracy",
        "high-speed extraction"
      ],
      "app_name": "Invoice/Receipt",
      "app_type": 0
    }
]
```

> In the example above, `"app_id": "ootb_*****d9e2"` is the global invoice extraction app. `app_type` of `0` indicates an out-of-the-box app; `1` indicates a custom app.

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
| `field_key` | string | Field identifier (e.g., `invoice_number`) |
| `field_name` | string | Field name (e.g., "Invoice Number") |
| `field_values` | array | List of extracted values (supports multiple values for fields that may have multiple entries, such as line items) |
| `field_values[].field_value` | string | Extracted value (the actual content extracted from the document) |
| `field_values[].field_confidence` | float | Confidence score for the extracted value (range: 0.0 to 1.0, where 1.0 indicates highest confidence) |
| `field_values[].references` | array | List of reference points in the document that support the extracted value (e.g., bounding boxes, page numbers, or text snippets where the value was found) |
| `line_items_item_code` | string | Code or SKU of the line item (if applicable) | 
| `line_items_description` | string | Description of the line item (if applicable) |
| `line_items_quantity` | string | Quantity of the line item (if applicable) |
| `line_items_unit_price` | string | Unit price of the line item (if applicable) |
| `line_items_total_amount` | string | Total amount of the line item (if applicable) |
| `line_items_tax_rate` | string | Tax rate for the line item (if applicable) |
| `line_items_tax` | string | Tax amount for the line item (if applicable) |


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

## security & compliance
Meanwhile, Laiye Technology, the parent company of ADP products, has obtained **ISO/IEC 27001:2022 Information Security Management System Certification** and **SOC 2 Independent Audit Certification**, providing end-to-end security and compliance assurance for your document data processing.

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
- **Issue Tracker:** [GitHub Issues](https://github.com/Laiye-ADP/adp-skills/issues)
- **Email:** global_product@laiye.com
- **Website:** [Laiye ADP](https://laiye.com/en/product/adp-platform)

Copyright 2026 [Laiye Technology (Beijing) Co., Ltd.] All rights reserved.
