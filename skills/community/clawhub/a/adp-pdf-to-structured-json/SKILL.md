---
name: pdf-to-structured-json
description: A universal document parsing Skill powered by Laiye ADP (Agentic Document Processing) platform, outputting structured JSON. ADP leverages large model capabilities to intelligently parse 10+ document formats including PDF, images, scanned documents, and Office files, automatically recognizing document content and outputting key fields and structured data in standard JSON format. Zero-configuration and ready to use out of the box — ideal for structured document storage & retrieval, automated data pipelines, document quality inspection, and cross-system document integration.
---

# PDF to Structured JSON Skill

Powered by Laiye [ADP (Agentic Document Processing)](https://adp-global.laiye.com/?utm_source=clawhub) intelligent document processing platform. ADP leverages large model capabilities to intelligently parse 10+ document formats including PDF, images, and Office files, outputting results in standard structured JSON format containing key fields and structured data that can be directly integrated with downstream business systems. This Skill invokes the `adp parse` command from ADP's official CLI tool — a single command completes intelligent document understanding and structured JSON output. A standard 200-page PDF can be parsed in just 30 seconds, dramatically improving document processing efficiency. ADP provides a standard commercial API that can be **integrated into business systems within 1 hour**.

> New users receive **100 free credits per month** (refreshed monthly), enabling free processing of approximately 200 pages of documents each month. ADP provides a standard commercial API that can be **integrated into business systems within 1 hour**.
</br> Register now: [Global](https://adp-global.laiye.com/?utm_source=clawhub) | [Mainland China](https://adp.laiye.com/?utm_source=clawhub)

---

## Quick Start Guide

### Core Workflow

1. **Install dependencies**: Install the ADP CLI tool on first run.
2. **Authentication setup**: On first run, execute `adp config get` to check credentials. If not configured, prompt the user for their API Key.
3. **Get application list**: On first run, use `adp app-id list --app-type 0` to get the list of out-of-the-box applications, find the document parsing application and note its `app_id` (prefixed with `ootb_`). For subsequent runs, prefer `adp app-id cache`.
4. **Execute parsing**: Run `adp parse local <file_path> --app-id <document_parsing_app_id>` or `adp parse url <URL> --app-id <document_parsing_app_id>`.
5. **Process results**: Parse the returned JSON. The system automatically identifies the document type and outputs structured JSON data with key fields.
6. **Error handling**: When a command fails, parse the stderr JSON to determine the error type and recovery action.

### Typical Use Cases

| Scenario | Description |
| --- | --- |
| **Structured Document Storage & Retrieval** | Parse PDF, images, and Office documents into structured JSON for import into databases or content management systems, enabling precise retrieval and systematic management |
| **Automated Data Pipeline Construction** | Use standardized JSON output as unified input for downstream data processing pipelines and ETL workflows, automating document processing |
| **Document Content Auditing & Quality Inspection** | Leverage structured information such as OCR confidence scores and element positions from parsing results to automate document quality assessment and review |
| **Cross-System Document Integration** | Parse documents in multiple formats into a unified JSON structure, enabling seamless document data exchange and integration across different business systems |

### Supported Input Formats

| Format Type | Supported File Extensions |
| --- | --- |
| PDF Documents | .pdf |
| Image Files | .jpg, .jpeg, .png, .bmp, .tiff, .tif |
| Office Documents | .doc, .docx, .xls, .xlsx |

### Scenario → Command Mapping

**Single File Parsing**

| User Intent | Recommended Command |
| :--- | :--- |
| Parse key information from a local PDF/image to JSON | `adp parse local <file_path> --app-id <document_parsing_app_id>` |
| Parse key information from a remote URL document to JSON | `adp parse url <URL> --app-id <document_parsing_app_id>` |
| Parse key information from a Base64-encoded document | `adp parse base64 <base64> --app-id <document_parsing_app_id> --file-name <filename.ext>` |

**Batch Parsing**

| User Intent | Recommended Command |
| :--- | :--- |
| Batch parse documents in a local folder | `adp parse local <folder_path> --app-id <document_parsing_app_id>` |
| Batch parse multiple URL documents | `adp parse url <url_list_file> --app-id <document_parsing_app_id>` |

**Async Processing**

| User Intent | Recommended Command |
| :--- | :--- |
| Async submit a large file | `adp parse local <file_path> --app-id <document_parsing_app_id> --async` |
| Async batch processing | `adp parse local <folder_path> --app-id <document_parsing_app_id> --async` |
| Query async task results | `adp parse query <task_id>` |

> Concurrency limit: Free users support up to 2 concurrent document processing; paid users support up to 10
---

## Step 1: Install ADP CLI

```bash
# Method 1: npm (Recommended, cross-platform)
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
We provide separate public cloud access URLs for international and domestic users. Using the nearest region ensures faster and more stable API calls.

| Region | Login URL | API Base URL |
|-----|----------|--------------|
| International | [https://adp-global.laiye.com/](https://adp-global.laiye.com/?utm_source=clawhub) | `https://adp-global.laiye.com/` |
| Mainland China | [https://adp.laiye.com/](https://adp.laiye.com/?utm_source=clawhub) | `https://adp.laiye.com/` |

### 2. Get API Key After Registration/Login
New users need to register for an ADP account first. Upon registration, you'll receive 100 free credits per month.
- After logging in, click your profile avatar to access the `API_Key` entry.

### 3. Complete Authentication Setup
```bash
adp config set --api-key <your-api-key>
adp config set --api-base-url https://adp-global.laiye.com
```

### 4. Verify Configuration
```bash
adp config get
```

**Notes**:
1. If API Key and API Base URL are already configured, it's recommended to store the configuration in environment variables to avoid repeated setup.
2. If API Key and API Base URL are not yet configured, follow the steps above to complete the setup.


---

## Step 3: Get the Document Parsing Application ID

ADP provides **out-of-the-box** built-in parsing applications for various document types — no additional configuration required.

### Application Types

ADP applications are divided into two types, distinguished by the `app_type` field:

| `app_type` | Type | Description |
| --- | --- | --- |
| `0` | Out-of-the-box (OOTB) | Platform built-in, `app_id` prefixed with `ootb_`, ready to use without creation |
| `1` | Custom Application | User-created parsing applications with custom `app_id` |

### Query and Filter Parsing Applications

```bash
# Query only out-of-the-box applications (Recommended)
adp app-id list --app-type 0

# Or query all applications
adp app-id list
```
Find the application with `app_label` containing **"Document Parsing"** in the returned list, and note its `app_id`:

```json
[
  {
    "app_id": "ootb_*********y2b4",
    "app_label": ["Document Parsing", "Image Extraction", "OCR", "Structured Parsing", "Batch Parsing"],
    "app_name": "Document Parse",
    "app_type": 0
  }
]
```

> In the example above, `"app_id": "ootb_******y2b4"` is the document parsing application. `app_type` of `0` indicates an out-of-the-box application; `1` indicates a custom application.

### Cache Application ID (Recommended)

After the first query, prefer using the cache to avoid repeated requests:

```bash
# Use cache for subsequent queries
adp app-id cache
```

**Important**: Each account's `app_id` is unique and fixed. Unless the user manually deletes the application, the `app_id` will not change. It's recommended to save commonly used parsing application `app_id` in context for direct reuse.

---

## Step 4: Execute Document Parsing (JSON Output)

### Single File Parsing (Local File)

```bash
adp parse local ./invoice.pdf --app-id <document_parsing_app_id>
```

### Single File Parsing (URL)

```bash
adp parse url https://example.com/invoice.pdf --app-id <document_parsing_app_id>
```

### Single File Parsing (Base64)

```bash
adp parse base64 <base64_string> --app-id <document_parsing_app_id> --file-name <filename.ext>
```

### Response Example

ADP document parsing returns unified structured JSON. The system automatically identifies the document type and outputs corresponding key fields. The following example demonstrates a **purchase order** result:

```json
{
  "success": true,
  "status": 4,
  "task_id": "94fe9b74e0e311f091505e345594c618",
  "file_url": "",
  "doc_recognize_result": [
    {
      "page_num": 1,
      "document_content": "example...",
      "document_details": [
        {
          "type": "Picture",
          "text": "http://test-adp.laiye.com/web/agentic_doc_processor/laiye/file/7bc821dee0e311f091505e345594c618",
          "position": [
            {
              "points": [
                {
                  "x": 34,
                  "y": 26
                },
                {
                  "x": 93,
                  "y": 26
                },
                {
                  "x": 93,
                  "y": 93
                },
                {
                  "x": 34,
                  "y": 93
                }
              ]
            }
          ],
          "ocr_confidence": {
            "ocr_mean_confidence": 0.9948742372110055,
            "ocr_min_confidence": 0.6224551745238371,
            "is_overall_confidence": 0
          }
        },
        {
          "type": "Title",
          "text": "中山市蚂蚁照明光电有限公司\n采购订单",
          "position": [
            {
              "points": [
                {
                  "x": 234,
                  "y": 28
                },
                {
                  "x": 577,
                  "y": 28
                },
                {
                  "x": 577,
                  "y": 81
                },
                {
                  "x": 234,
                  "y": 81
                }
              ]
            }
          ],
          "ocr_confidence": {
            "ocr_mean_confidence": 0.9649929892499949,
            "ocr_min_confidence": 0.7520648420779353,
            "is_overall_confidence": 1
          }
        },
        {
          "type": "Text",
          "text": "采购单号: P020250304012",
          "position": [
            {
              "points": [
                {
                  "x": 587,
                  "y": 72
                },
                {
                  "x": 770,
                  "y": 72
                },
                {
                  "x": 770,
                  "y": 89
                },
                {
                  "x": 587,
                  "y": 89
                }
              ]
            }
          ],
          "ocr_confidence": {
            "ocr_mean_confidence": 0.9999092513136395,
            "ocr_min_confidence": 0.9986503483477672,
            "is_overall_confidence": 1
          }
        },
        {
          "type": "Text",
          "text": "example text...",
          "position": [
            {
              "points": [
                {
                  "x": 30,
                  "y": 109
                },
                {
                  "x": 676,
                  "y": 109
                },
                {
                  "x": 676,
                  "y": 125
                },
                {
                  "x": 30,
                  "y": 125
                }
              ]
            }
          ],
          "ocr_confidence": {
            "ocr_mean_confidence": 0.9907980751407313,
            "ocr_min_confidence": 0.9479157610236068,
            "is_overall_confidence": 1
          }
        },
        {
          "type": "Table",
          "text": "<table><tr><td>订货日期:</td><td>2025-03-04</td><td>订货方:</td><td colspan=\"4\">中山市蚂蚁照明光电有限公司</td></tr><tr><td>供应商名称:</td><td>深圳市唯特偶新材料股份有限公司</td><td>联系人:</td><td colspan=\"4\"></td></tr><tr><td>联系人:</td><td>马国银</td><td>联系电话:</td><td colspan=\"4\">0760-28188088</td></tr><tr><td>电话:</td><td>0755-61813001</td><td>企业传真:</td><td colspan=\"4\">0760-28188089</td></tr><tr><td>传真:</td><td></td><td>企业地址:</td><td colspan=\"4\">中山市横栏镇永兴工业区富庆一路21号2栋</td></tr><tr><td>序号</td><td>物料编号</td><td>物料名称</td><td>规格型号</td><td>单位</td><td>数量</td><td>交货日期</td><td>备注</td></tr><tr><td>1</td><td>C.FL.0003</td><td>有铅锡膏</td><td>GW9068C-6</td><td>克</td><td>100000</td><td>2025-03-04</td><td>50瓶</td></tr><tr><td>2</td><td>C.FL.0001</td><td>锡丝</td><td>YF-12 φ1.1mm 55%</td><td>pcs</td><td>80</td><td>2025-03-04</td><td>80卷</td></tr></table>",
          "position": [
            {
              "points": [
                {
                  "x": 27,
                  "y": 125
                },
                {
                  "x": 772,
                  "y": 125
                },
                {
                  "x": 772,
                  "y": 393
                },
                {
                  "x": 27,
                  "y": 393
                }
              ]
            }
          ],
          "ocr_confidence": {
            "ocr_mean_confidence": 0.9989620051858402,
            "ocr_min_confidence": 0.8928787142723804,
            "is_overall_confidence": 1
          }
        }
      ]
    }
  ]
}
```

### Response Field Structure

**Top-Level Fields**

| Field | Type | Description |
| --- | --- | --- |
| `success` | boolean | Whether parsing was successful |
| `status` | number | Task status code |
| `task_id` | string | Unique task identifier |
| `file_url` | string | File URL (empty for local file parsing) |
| `doc_recognize_result` | array | Document recognition result array, returned per page |

**Page-Level Fields (`doc_recognize_result[]`)**

| Field | Type | Description |
| --- | --- | --- |
| `page_num` | number | Page number (starting from 1) |
| `document_content` | string | Full text content of the page |
| `document_details` | array | Array of document element details for the page |

**Element-Level Fields (`document_details[]`)**

| Field | Type | Description |
| --- | --- | --- |
| `type` | string | Element type: `Picture`, `Title`, `Text`, `Table` |
| `text` | string | Recognized text content (tables returned as HTML `<table>` format, images as URLs) |
| `position` | array | Element position coordinates on the page |
| `position[].points` | array | Polygon vertex coordinate array (4 `{x, y}` points) |
| `ocr_confidence` | object | OCR confidence information |
| `ocr_confidence.ocr_mean_confidence` | number | Mean confidence (0–1) |
| `ocr_confidence.ocr_min_confidence` | number | Minimum confidence (0–1) |
| `ocr_confidence.is_overall_confidence` | number | Whether this is an overall confidence score (0 or 1) |

---

## Step 5: Batch Processing & Async Mode

### Batch Processing (Local Folder)

```bash
adp parse local ./documents/ --app-id <document_parsing_app_id> --export ./results/
```

Returns a summary:
```json
{
  "total": 10,
  "success": 9,
  "failed": 1,
  "output_dir": "/absolute/path/to/results",
  "files": [
    {"input": "invoice-001.pdf", "output": "invoice-001.pdf.json", "status": "success"},
    {"input": "order-002.jpg", "output": "order-002.jpg.json", "status": "success"},
    {"input": "damaged.pdf", "output": "damaged.pdf.error.json", "status": "failed", "error": "..."}
  ]
}
```

### Async (Batch + Resume)

```bash
# Phase 1: Submit tasks without waiting for results
adp parse local ./documents/ --app-id <document_parsing_app_id> --async --no-wait --export tasks.json

# Phase 2: Query results
adp parse query --watch --file tasks.json --export ./results/
```

---

## Command Quick Reference

```bash
# Check installation
adp version

# View configuration
adp config get

# Query all application list
adp app-id list

# Query only out-of-the-box applications (app_type=0)
adp app-id list --app-type 0

# Use cached applications
adp app-id cache

# Check credit balance
adp credit

# Parse document to JSON (local file)
adp parse local <file_path> --app-id <document_parsing_app_id>

# Parse document to JSON (URL)
adp parse url <file_url> --app-id <document_parsing_app_id>

# Parse document to JSON (Base64)
adp parse base64 <base64_string> --app-id <document_parsing_app_id> --file-name <filename.ext>

# Batch parsing
adp parse local <folder_path> --app-id <document_parsing_app_id> --export <output_path>

# Async parsing
adp parse local <file_path> --app-id <document_parsing_app_id> --async

# Query async results
adp parse query <task_id>

# Auto-retry on failure (max 2 retries)
adp parse local <file_path> --app-id <document_parsing_app_id> --retry 2

# AI-recommended parsing fields
adp custom-app ai-generate --file <sample_file_path>
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
  "details": {"context": "parse"}
}
```

### Exit Code Reference

| Exit Code | Meaning |
| --- | --- |
| 0 | Success |
| 1 | General error |
| 2 | Argument error |
| 3 | Resource not found |
| 4 | Permission/authentication error |
| 5 | Conflict |
| 6 | Partial failure (some succeeded, some failed in batch processing) |

---

## Credits & Billing

| Item | Description |
| --- | --- |
| Document parsing cost | **0.5 credits/page** |
| New user free quota | **100 credits** per month, reset at the beginning of each month |
| Check balance | `adp credit` |
| Top-up | Log in to the ADP portal: [International](https://adp-global.laiye.com/?utm_source=clawhub) \| [Mainland China & HK/Macau/Taiwan](https://adp.laiye.com/?utm_source=clawhub) |

---

## More Laiye ADP Document Processing Capabilities

PDF/Image to JSON is just one of many out-of-the-box capabilities from Laiye ADP platform. ADP leverages large model capabilities to provide intelligent document processing solutions covering all document categories:

| Capability | Description | Typical Scenarios |
| --- | --- | --- |
| **Global Invoice/Receipt Extraction** | Automatically identifies and extracts 10+ key fields including invoice number, date, amount, tax, line items; supports multi-language and multi-currency invoices | Cross-border settlement automation, expense reimbursement management |
| **Domestic Ticket Extraction** | Recognizes 30+ common Chinese tickets including VAT invoices, taxi receipts, train tickets, flight itineraries, fiscal invoices; supports multi-page/multi-ticket recognition and verification | Domestic ticket recognition, invoice verification |
| **Order Extraction** | Supports various purchase order formats; extracts order number, products, quantities, prices, logistics info | Procurement automation, supply chain integration |
| **ID Card & Certificate Extraction** | ADP supports 11 types of commonly used Chinese documents: ID card, HK/Macau/Taiwan travel permit, Chinese passport, bank card, household register, driver's license, vehicle registration, vehicle qualification certificate, bank account permit, business license | Account opening review, compliance checks, batch certificate data entry |
| **Document Parsing** | Converts PDF, images, and Office documents into structured data while preserving layout and hierarchy | Long document analysis, contract review, knowledge extraction |
| **Custom Extraction** | Create custom extraction applications with dedicated fields and recognition logic for non-standard documents | Enterprise-specific forms, industry-customized documents |

All capabilities above can be invoked through the same ADP CLI tool, sharing the ADP API Key and credit system.

For full capabilities, visit:
- ADP Global: [https://adp-global.laiye.com/](https://adp-global.laiye.com/?utm_source=clawhub)
- ADP Mainland China: [https://adp.laiye.com/](https://adp.laiye.com/?utm_source=clawhub)

---

## Important Notes

1. **Data Integrity**: When using ADP output, present the returned data as-is. Do not modify, add, or remove any fields during the parsing process.
2. **API Key Security**: Keep your API Key secure and avoid exposing it to unauthorized third parties.
3. **File Size Limit**: Maximum 50MB per file.
4. **Supported Formats**: .jpg, .jpeg, .png, .bmp, .tiff, .tif, .pdf, .doc, .docx, .xls, .xlsx
5. **Application ID Reuse**: The parsing application's `app_id` is unique and fixed per account. It's recommended to save it for direct reuse without querying each time.
6. **Choose the Right Application**: Select the corresponding out-of-the-box application based on document type, or create a custom application for optimal parsing results.

---

## Support & Contact
- **CLI User Guide:** [ADP CLI User Guide](https://laiye-tech.feishu.cn/wiki/YIaawiK2DimisZk5KfDc8a8cnLh)
- **API Documentation:** [Open API User Guide](https://laiye-tech.feishu.cn/wiki/S1t2wYR04ivndKkMDxxcp2SFnKd)
- **ADP Product Manual:** [Public Cloud Manual](https://laiye-tech.feishu.cn/wiki/OfexwgVUQiOpEek4kO7c7NEJnAe)
- **Issue Tracker:** [GitHub Issues](https://github.com/laiye-ai/adp-cli/issues)
- **Email:** global_product@laiye.com
- **Website:** [Laiye ADP](https://laiye.com/en/product/adp-platform)

Copyright © 2026 [Laiye Technology (Beijing) Co., Ltd.] All rights reserved.
