---
name: purchase-order-recognition-and-extract
description: Accurate extraction of all fields from purchase orders and sales orders in various formats — PO number, order date, seller name, buyer/customer name, buyer/customer address, receiver name, delivery address, currency, total amount, and line items (including material code, description, quantity, tax rate, unit price incl. tax, total amount incl. tax, delivery date). Outputs structured JSON, zero-configuration out-of-the-box, suitable for e-commerce order entry, supply chain reconciliation, and warehouse management automation.
---

# Global Purchase Order Recognition and Extraction Skill

Powered by [Laiye ADP (Agentic Document Processing)](https://adp-global.laiye.com/?utm_source=clawhub), this skill delivers intelligent recognition and key information extraction for various purchase orders (POs) and sales orders. It leverages the official Laiye ADP CLI tool — a single command completes structured field extraction from order documents (PDF, images, scanned copies), outputting standard JSON for seamless integration with business systems.

> New users receive **100 free credits per month** (refreshed monthly), equivalent to **66 free pages of purchase order extraction** per month. ADP provides a standard commercial API that can be **integrated into business systems within 1 hour**.
</br> Register now: [Global](https://adp-global.laiye.com/?utm_source=clawhub) | [China Mainland](https://adp.laiye.com/?utm_source=clawhub)

---

## Quick Start Guide

### Core Workflow

1. **Install dependencies**: On first run, install the ADP CLI tool.
2. **Authentication setup**: On first run, execute `adp config get` to check credentials. If not configured, prompt the user to provide an API Key.
3. **Get app list**: On first run, retrieve the out-of-the-box app list via `adp app-id list --app-type 0`, find the order extraction app, and record its `app_id` (prefixed with `ootb_`). For subsequent runs, prefer `adp app-id cache`.
4. **Execute extraction**: Run `adp extract url <URL> --app-id <order-app-id>` or `adp extract local <file-path> --app-id <order-app-id>`.
5. **Process results**: Parse the returned JSON to extract structured fields such as PO number, order date, seller name, buyer/customer name, buyer/customer address, receiver name, delivery address, currency, total amount, and line items (including material code, description, quantity, tax rate, unit price incl. tax, total amount incl. tax, delivery date).
6. **Error handling**: When a command fails, parse the stderr JSON to determine the error type and recovery action.

### Scenario-to-Command Mapping

**Single Order Recognition**

| User Intent | Recommended Command |
| :--- | :--- |
| Recognize an order file (URL) | `adp extract url <URL> --app-id <order-app-id>` |
| Recognize a local order file | `adp extract local <file-path> --app-id <order-app-id>` |
| Recognize a Base64-encoded order | `adp extract base64 <base64> --app-id <order-app-id> --file-name <filename.ext>` |

**Batch Recognition**

| User Intent | Recommended Command |
| :--- | :--- |
| Batch recognize orders in a local folder | `adp extract local <folder-path> --app-id <order-app-id>` |
| Batch recognize multiple URLs | `adp extract url <URL-list-file> --app-id <order-app-id>` |

**Async Processing**

| User Intent | Recommended Command |
| :--- | :--- |
| Async submit a large file | `adp extract url <URL> --app-id <order-app-id> --async` |
| Async batch processing | `adp extract local <folder-path> --app-id <order-app-id> --async` |
| Query async task result | `adp extract query <task_id>` |

> Concurrency Limit: Free users support a maximum of 2 documents for concurrent processing, while paid users support up to 10 documents concurrently.
---

## Step 1: Install ADP CLI

```bash
# Method 1: npm (recommended, cross-platform)
npm install -g @laiye-adp/agentic-doc-parse-and-extract-cli
```

```bash
# Method 2: Shell script (Linux / macOS, when npm is not available)
curl -fsSL https://raw.githubusercontent.com/laiye-ai/adp-cli/main/scripts/adp-init.sh | bash
```

```bash
# Method 3: PowerShell script (Windows, when npm is not available)
irm https://raw.githubusercontent.com/laiye-ai/adp-cli/main/scripts/adp-init.ps1 | iex
```

Or download pre-compiled binaries from [GitHub Releases](https://github.com/laiye-ai/adp-cli/releases).

---

## Step 2: Get API Key & Authentication Setup

### 1. Access the ADP Portal for Credentials
Separate public cloud URLs are provided for China Mainland and Global users. Using the nearest region ensures optimal network performance.

| Region | Login URL | API Base URL |
|-----|----------|--------------|
| Global | [https://adp-global.laiye.com/](https://adp-global.laiye.com/?utm_source=clawhub) | `https://adp-global.laiye.com/` |
| China Mainland | [https://adp.laiye.com/](https://adp.laiye.com/?utm_source=clawhub) | `https://adp.laiye.com/` |

### 2. Get API Key After Registration/Login
New users need to register an ADP account first; upon registration, you will receive 100 free credits per month.
- After logging in, click your profile avatar to access the `API_Key` entry.

### 3. Complete Authentication Setup
```bash
adp config set --api-key <your-api-key>
adp config set --api-base-url https://adp.laiye.com
```

### 4. Verify Configuration
```bash
adp config get
```

**Notes**:
1. If API Key and API Base URL are already configured, it is recommended to store the configuration in environment variables to avoid repeated setup.
2. If API Key and API Base URL are not yet configured, follow the steps above to complete the setup.


---

## Step 3: Get the Order Extraction App ID

ADP provides a **built-in, out-of-the-box** extraction app for purchase orders — no additional configuration required.

### App Type Description

ADP apps are divided into two types, distinguished by the `app_type` field:

| `app_type` | Type | Description |
| --- | --- | --- |
| `0` | Out-of-the-Box (OOTB) | Platform built-in, `app_id` prefixed with `ootb_`, ready to use without creation |
| `1` | Custom App | User-created extraction apps with user-defined `app_id` |

Order recognition is an **out-of-the-box app** and can be queried with `--app-type 0`.

### Query and Filter Order App

```bash
# Query OOTB apps only (recommended)
adp app-id list --app-type 0

# Or query all apps
adp app-id list
```

Find the app whose `app_name` contains **"order"** in the returned list and record its `app_id`:

```json
[
  {
    "app_id": "ootb_******a2b5",
    "app_label": ["Order", "E-commerce Logistics", "Warehouse Management", "Information Extraction"],
    "app_name": "Order",
    "app_type": 0
  }
]
```

> In the example above, `"app_id": "ootb_******a2b5"` is the order extraction app. `app_type` of `0` indicates an OOTB app, while `1` indicates a custom app.

### Cache App ID (Recommended)

After the first query, prefer using the cache to avoid repeated requests:

```bash
# Use cached apps for subsequent calls
adp app-id cache
```

**Important**: The `app_id` for each account is unique and fixed — it will not change unless the user explicitly deletes the app. It is recommended that agents save the order app's `app_id` in context for direct reuse.

---

## Step 4: Execute Purchase Order Extraction

### Single Order Extraction (URL)

```bash
adp extract url https://example.com/purchase-order.pdf --app-id <order-app-id>
```

### Single Order Extraction (Local File)

```bash
adp extract local ./purchase-order.pdf --app-id <order-app-id>
```

### Single Order Extraction (Base64)

```bash
adp extract base64 <base64-string> --app-id <order-app-id> --file-name <filename.ext>
```

### Response Example

ADP purchase order extraction returns unified structured JSON, accurately recognizing order header information (9 fields) and line item details table (7 columns), totaling **10** top-level fields.

```json
[
  {
    "field_key": "po_number",
    "field_name": "PO Number",
    "field_values": [
      {
        "field_value": "PO-2025-003721"
      }
    ]
  },
  {
    "field_key": "order_date",
    "field_name": "Order Date",
    "field_values": [
      {
        "field_value": "2025-11-20"
      }
    ]
  },
  {
    "field_key": "seller_name",
    "field_name": "Seller Name",
    "field_values": [
      {
        "field_value": "Global Supply Chain Co., Ltd."
      }
    ]
  },
  {
    "field_key": "buyer_name",
    "field_name": "Buyer/Customer Name",
    "field_values": [
      {
        "field_value": "TechNova Innovation Inc."
      }
    ]
  },
  {
    "field_key": "buyer_address",
    "field_name": "Buyer/Customer Address",
    "field_values": [
      {
        "field_value": "1 Innovation Drive, Suite 200, San Jose, CA 95134"
      }
    ]
  },
  {
    "field_key": "receiver_name",
    "field_name": "Receiver Name",
    "field_values": [
      {
        "field_value": "TechNova Innovation Inc. — Warehouse Dept."
      }
    ]
  },
  {
    "field_key": "delivery_address",
    "field_name": "Delivery Address",
    "field_values": [
      {
        "field_value": "1 Innovation Drive, Building A, San Jose, CA 95134"
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
    "field_key": "total_amount",
    "field_name": "Total Amount",
    "field_values": [
      {
        "field_value": "$87,623.00"
      }
    ]
  },
  {
    "field_key": "line_items",
    "field_name": "Line Items",
    "table_values": [
      [
        {
          "field_key": "line_items_material_code",
          "field_name": "Material Code",
          "field_values": [
            {
              "field_value": "MAT-A200-001"
            }
          ]
        },
        {
          "field_key": "line_items_description",
          "field_name": "Description",
          "field_values": [
            {
              "field_value": "Industrial Precision Sensor Module A-200"
            }
          ]
        },
        {
          "field_key": "line_items_quantity",
          "field_name": "Quantity",
          "field_values": [
            {
              "field_value": "500"
            }
          ]
        },
        {
          "field_key": "line_items_tax_rate",
          "field_name": "Tax Rate",
          "field_values": [
            {
              "field_value": "8%"
            }
          ]
        },
        {
          "field_key": "line_items_unit_price_inc_tax",
          "field_name": "Unit Price (Tax Incl.)",
          "field_values": [
            {
              "field_value": "$135.60"
            }
          ]
        },
        {
          "field_key": "line_items_total_amount_inc_tax",
          "field_name": "Total Amount (Tax Incl.)",
          "field_values": [
            {
              "field_value": "$67,800.00"
            }
          ]
        },
        {
          "field_key": "line_items_delivery_date",
          "field_name": "Delivery Date",
          "field_values": [
            {
              "field_value": "2025-12-20"
            }
          ]
        }
      ],
      [
        {
          "field_key": "line_items_material_code",
          "field_name": "Material Code",
          "field_values": [
            {
              "field_value": "MAT-B100-002"
            }
          ]
        },
        {
          "field_key": "line_items_description",
          "field_name": "Description",
          "field_values": [
            {
              "field_value": "High-Voltage Wiring Harness Assembly B-100"
            }
          ]
        },
        {
          "field_key": "line_items_quantity",
          "field_name": "Quantity",
          "field_values": [
            {
              "field_value": "200"
            }
          ]
        },
        {
          "field_key": "line_items_tax_rate",
          "field_name": "Tax Rate",
          "field_values": [
            {
              "field_value": "8%"
            }
          ]
        },
        {
          "field_key": "line_items_unit_price_inc_tax",
          "field_name": "Unit Price (Tax Incl.)",
          "field_values": [
            {
              "field_value": "$99.12"
            }
          ]
        },
        {
          "field_key": "line_items_total_amount_inc_tax",
          "field_name": "Total Amount (Tax Incl.)",
          "field_values": [
            {
              "field_value": "$19,823.00"
            }
          ]
        },
        {
          "field_key": "line_items_delivery_date",
          "field_name": "Delivery Date",
          "field_values": [
            {
              "field_value": "2025-12-25"
            }
          ]
        }
      ]
    ]
  }
]
```

### Extraction Field Reference

ADP purchase order extraction returns the following fields. Each field contains `field_key` (machine-readable identifier), `field_name` (human-readable name), and `field_values` (extraction result array; `field_value` is an empty string when not recognized).

**Order Header Fields**

| field_key | field_name | Description |
| --- | --- | --- |
| `po_number` | PO Number | Purchase order number |
| `order_date` | Order Date | Date the order was placed |
| `seller_name` | Seller Name | Seller / supplier name |
| `buyer_name` | Buyer/Customer Name | Buyer or customer name |
| `buyer_address` | Buyer/Customer Address | Buyer or customer address |
| `receiver_name` | Receiver Name | Goods receiver name |
| `delivery_address` | Delivery Address | Shipping / delivery address |
| `currency` | Currency | Currency code (e.g., USD, CNY) |
| `total_amount` | Total Amount | Order total amount |

**Line Item Table Fields (`line_items`)**

The `line_items` field uses a `table_values` (2D array) structure — the outer array represents rows, and the inner array represents columns for each row. Each column also contains `field_key`, `field_name`, and `field_values`.

| field_key | field_name | Description |
| --- | --- | --- |
| `line_items_material_code` | Material Code | Product / material code |
| `line_items_description` | Description | Product description / name |
| `line_items_quantity` | Quantity | Order quantity |
| `line_items_tax_rate` | Tax Rate | Applicable tax rate |
| `line_items_unit_price_inc_tax` | Unit Price (Tax Incl.) | Unit price including tax |
| `line_items_total_amount_inc_tax` | Total Amount (Tax Incl.) | Line total amount including tax |
| `line_items_delivery_date` | Delivery Date | Delivery date for this line item |

---

## Step 5: Batch Processing & Async Mode

### Batch Processing (Local Folder)

```bash
adp extract local ./purchase-orders/ --app-id <order-app-id> --export ./results/ 
```

Response summary:
```json
{
  "total": 10,
  "success": 9,
  "failed": 1,
  "output_dir": "/absolute/path/to/results",
  "files": [
    {"input": "po-001.pdf", "output": "po-001.pdf.json", "status": "success"},
    {"input": "po-002.pdf", "output": "po-002.pdf.json", "status": "success"},
    {"input": "damaged.pdf", "output": "damaged.pdf.error.json", "status": "failed", "error": "..."}
  ]
}
```

### Async Processing

```bash
# Submit async task
adp extract url https://example.com/purchase-order.pdf --app-id <order-app-id> --async

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

# Order extraction (URL)
adp extract url <file-URL> --app-id <order-app-id>

# Order extraction (local file)
adp extract local <file-path> --app-id <order-app-id>

# Order extraction (Base64)
adp extract base64 <base64-string> --app-id <order-app-id> --file-name <filename.ext>

# Batch extraction
adp extract local <folder-path> --app-id <order-app-id> --export <output-path> 

# Async extraction
adp extract url <file-URL> --app-id <order-app-id> --async

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

### Exit Code Reference

| Exit Code | Meaning |
| --- | --- |
| 0 | Success |
| 1 | General error |
| 2 | Argument error |
| 3 | Resource not found |
| 4 | Permission / authentication error |
| 5 | Conflict |
| 6 | Partial failure (some succeeded, some failed in batch processing) |

---

## Credits & Billing

| Item | Description |
| --- | --- |
| Order extraction cost | **1.5 credits/page** |
| Free monthly allowance | **100 credits per month** (equivalent to **66 pages of purchase order extraction**), reset at the beginning of each month |
| Check balance | `adp credit` |
| Top up | Log in to the ADP portal: [Global](https://adp-global.laiye.com/?utm_source=clawhub) \| [China Mainland & HK/Macau/TW](https://adp.laiye.com/?utm_source=clawhub) |

---

## More Laiye ADP Document Processing Capabilities

Order extraction is just one of many out-of-the-box capabilities on the Laiye ADP platform. Powered by large model general understanding, ADP provides intelligent document processing solutions covering all document categories:

| Capability | Description | Typical Scenarios |
| --- | --- | --- |
| **Global Invoice/Receipt Extraction** | Automatically recognizes and extracts 10+ key fields including invoice number, date, amount, tax, and line items; supports multi-language and multi-currency invoices | Cross-border accounts payable automation, expense reimbursement |
| **China Domestic Receipt Extraction** | Recognizes 30+ common receipt types including VAT invoices, taxi receipts, train tickets, flight itineraries, and fiscal invoices; supports multi-page/multi-receipt recognition and verification | Domestic receipt recognition, invoice verification |
| **Order Extraction** | Supports various purchase order formats; extracts order number, products, quantity, price, logistics info, etc. | Procurement automation, supply chain integration |
| **ID & Certificate Extraction** | ADP supports 11 types of Chinese certificates including ID cards, HK/Macau/TW travel permits, Chinese passports, bank cards, household registers, driver's licenses, vehicle licenses, vehicle certificates, account opening permits, and business licenses | Account opening reviews, compliance checks, batch certificate data entry |
| **Document Parsing** | Converts PDFs, images, and Office documents into structured data while preserving layout and hierarchy | Long document analysis, contract review, knowledge extraction |
| **Custom Extraction** | Create custom extraction apps with proprietary fields and recognition logic for non-standard documents | Enterprise-specific forms, industry-specific documents |

All capabilities above can be accessed through the same ADP CLI tool, sharing the same ADP API Key and credit system.

For the full range of capabilities, visit:
- ADP Global: [https://adp-global.laiye.com/](https://adp-global.laiye.com/?utm_source=clawhub)
- ADP China Mainland: [https://adp.laiye.com/](https://adp.laiye.com/?utm_source=clawhub)

---

## Important Notes

1. **Data integrity**: When using ADP output, present the returned data as-is — do not modify, add, or remove any fields during the extraction process.
2. **API Key security**: Keep your API Key secure and avoid sharing it with unauthorized third parties.
3. **File size limit**: Maximum 50 MB per file.
4. **Supported formats**: .jpg, .jpeg, .png, .bmp, .tiff, .tif, .pdf, .doc, .docx, .xls, .xlsx
5. **App ID reuse**: The order app's `app_id` is unique and fixed per account — save it for direct reuse without querying each time.
6. **Line item fields**: For line item fields such as product name, code, quantity, unit price, and line amount, each element in the `field_values` array corresponds to one product row, in sequential order.

---

## Support & Contact
- **CLI User Guide:** [ADP CLI User Guide](https://laiye-tech.feishu.cn/wiki/YIaawiK2DimisZk5KfDc8a8cnLh)
- **API Documentation:** [Open API User Guide](https://laiye-tech.feishu.cn/wiki/S1t2wYR04ivndKkMDxxcp2SFnKd)
- **ADP Product Manual:** [Public Cloud Manual](https://laiye-tech.feishu.cn/wiki/OfexwgVUQiOpEek4kO7c7NEJnAe)
- **Issue Tracker:** [GitHub Issues](https://github.com/laiye-ai/adp-cli/issues)
- **Email:** global_product@laiye.com
- **Website:** [Laiye](https://laiye.com/en/product/adp-platform)

Copyright © 2026 Laiye, Inc. All rights reserved.
