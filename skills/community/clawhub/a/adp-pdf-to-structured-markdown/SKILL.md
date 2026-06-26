---
name: pdf-to-structured-markdown
description: A universal document parsing Skill powered by Laiye ADP (Agentic Document Processing) platform, outputting high-quality Markdown. ADP leverages large model capabilities to intelligently parse 10+ document formats including PDF, images, scanned documents, and Office files, automatically converting unstructured documents into Markdown format while fully preserving heading hierarchy, tables, lists, paragraph structure, and more. Zero-configuration and ready to use out of the box — ideal for structured document reading, content migration, technical documentation organization, and LLM context preparation.
---

# PDF to Structured Markdown Skill

Powered by Laiye [ADP (Agentic Document Processing)](https://adp-global.laiye.com/?utm_source=clawhub) intelligent document processing platform. ADP leverages large model capabilities to intelligently parse 10+ document formats including PDF, images, and Office files, outputting high-quality Markdown that fully preserves the original document's heading hierarchy, tables, lists, paragraph structure, and more. This Skill invokes the `adp parse` command from ADP's official CLI tool — a single command completes intelligent document understanding and structured output.

> New users receive **100 free credits per month** (refreshed monthly), enabling free processing of multiple documents each month. ADP provides a standard commercial API that can be **integrated into business systems within 1 hour**.
</br> Register now: [Global](https://adp-global.laiye.com/?utm_source=clawhub) | [Mainland China](https://adp.laiye.com/?utm_source=clawhub)

---

## Quick Start Guide

### Core Workflow

1. **Install dependencies**: Install the ADP CLI tool on first run.
2. **Authentication setup**: On first run, execute `adp config get` to check credentials. If not configured, prompt the user for their API Key.
3. **Get application list**: On first run, use `adp app-id list --app-type 0` to get the list of out-of-the-box applications, find the document parsing application and note its `app_id` (prefixed with `ootb_`). For subsequent runs, prefer `adp app-id cache`.
4. **Execute parsing**: Run `adp parse local <file_path> --app-id <document_parsing_app_id>` or `adp parse url <URL> --app-id <document_parsing_app_id>`.
5. **Process results**: The parsing result is returned as Markdown-formatted text, preserving the original document's headings, tables, lists, paragraphs, and other structural elements.
6. **Error handling**: When a command fails, parse the stderr JSON to determine the error type and recovery action.

### Supported Input Formats

| Format Type | Supported File Extensions |
| --- | --- |
| PDF Documents | .pdf |
| Image Files | .jpg, .jpeg, .png, .bmp, .tiff, .tif |
| Office Documents | .doc, .docx, .xls, .xlsx, .ppt, .pptx |

### Typical Use Cases

| Scenario | Description |
| --- | --- |
| **Technical Documentation Migration & Organization** | Parse PDF-format technical manuals, API docs, and product specifications into Markdown for easy import into Wiki, GitBook, Notion, and other knowledge management platforms |
| **LLM Context Preparation** | Parse unstructured documents into Markdown text as input context for large language models, improving AI comprehension and Q&A quality |
| **Content Publishing & Format Conversion** | Parse Word, PPT, and PDF reports into Markdown for direct use in blog publishing, documentation site generation, or CMS content entry |
| **Historical Archive Digitization** | Parse scanned documents and image-format historical materials via OCR into editable Markdown text for easy retrieval and reuse |

### Scenario → Command Mapping

**Single File Parsing**

| User Intent | Recommended Command |
| :--- | :--- |
| Convert a local PDF to Markdown | `adp parse local <file_path> --app-id <document_parsing_app_id>` |
| Convert a remote PDF/image to Markdown | `adp parse url <URL> --app-id <document_parsing_app_id>` |
| Convert a Base64-encoded document to Markdown | `adp parse base64 <base64> --app-id <document_parsing_app_id> --file-name <filename.ext>` |

**Batch Parsing**

| User Intent | Recommended Command |
| :--- | :--- |
| Batch convert documents in a local folder | `adp parse local <folder_path> --app-id <document_parsing_app_id>` |
| Batch convert multiple remote URL documents | `adp parse url <url_list_file> --app-id <document_parsing_app_id>` |

**Async Processing**

| User Intent | Recommended Command |
| :--- | :--- |
| Async parse a large file | `adp parse local <file_path> --app-id <document_parsing_app_id> --async` |
| Async batch parse | `adp parse local <folder_path> --app-id <document_parsing_app_id> --async` |
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
We provide separate public cloud access URLs for domestic and international users. Using the nearest region ensures faster and more stable API calls.

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

ADP provides **out-of-the-box** built-in applications for document parsing — no additional configuration required.

### Application Types

ADP applications are divided into two types, distinguished by the `app_type` field:

| `app_type` | Type | Description |
| --- | --- | --- |
| `0` | Out-of-the-box (OOTB) | Platform built-in, `app_id` prefixed with `ootb_`, ready to use without creation |
| `1` | Custom Application | User-created extraction applications with custom `app_id` |

Document parsing is an **out-of-the-box application** and can be queried with `--app-type 0`.

### Query and Filter Document Parsing Applications

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

> In the example above, `"app_id": "ootb_******xx"` is the document parsing application. `app_type` of `0` indicates an out-of-the-box application; `1` indicates a custom application.

### Cache Application ID (Recommended)

After the first query, prefer using the cache to avoid repeated requests:

```bash
# Use cache for subsequent queries
adp app-id cache
```

**Important**: Each account's `app_id` is unique and fixed. Unless the user manually deletes the application, the `app_id` will not change. It's recommended to save the document parsing `app_id` in context for direct reuse.

---

## Step 4: Execute PDF/Image to Markdown Conversion

### Single File Parsing (Local File)

```bash
adp parse local ./document.pdf --app-id <document_parsing_app_id>
```

### Single File Parsing (URL)

```bash
adp parse url https://example.com/document.pdf --app-id <document_parsing_app_id>
```

### Single File Parsing (Base64)

```bash
adp parse base64 <base64_string> --app-id <document_parsing_app_id> --file-name <filename.ext>
```

### Output Description

ADP document parsing returns Markdown-formatted text that fully preserves the original document's layout structure:

- **Heading Hierarchy**: Automatically identifies H1-H6 heading levels and converts them to corresponding `#` markers
- **Tables**: Automatically identifies tables and converts them to Markdown table syntax
- **Lists**: Both ordered and unordered lists preserve their original format
- **Paragraphs**: Body paragraphs preserve original segmentation and line breaks
- **Image Regions**: Image positions are annotated (with OCR text if available)
- **Page Numbers**: Multi-page documents are automatically annotated with page separators

### Output Example

```markdown
# Contract Agreement

## Chapter 1: General Provisions

**Party A**: Beijing XX Technology Co., Ltd.
**Party B**: Shanghai XX Trading Co., Ltd.

### 1.1 Purpose of Contract

This contract aims to clarify the rights and obligations of both parties in the software development project...

## Chapter 2: Service Scope

| No. | Service Item | Delivery Date | Amount (10K CNY) |
| --- | --- | --- | --- |
| 1 | Requirements Analysis | 2025-03-01 | 10.0 |
| 2 | System Design | 2025-04-01 | 15.0 |
| 3 | Development & Implementation | 2025-06-01 | 50.0 |
```

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
    {"input": "contract.pdf", "output": "contract.pdf.json", "status": "success"},
    {"input": "report.docx", "output": "report.docx.json", "status": "success"},
    {"input": "damaged.pdf", "output": "damaged.pdf.error.json", "status": "failed", "error": "..."}
  ]
}
```

### Async Processing

```bash
# Submit async task
adp parse local ./large-document.pdf --app-id <document_parsing_app_id> --async

# Query task results
adp parse query <task_id>
```

### Two-Phase Async (Batch + Resume)

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

# PDF/Image to Markdown (local file)
adp parse local <file_path> --app-id <document_parsing_app_id>

# PDF/Image to Markdown (URL)
adp parse url <file_url> --app-id <document_parsing_app_id>

# PDF/Image to Markdown (Base64)
adp parse base64 <base64_string> --app-id <document_parsing_app_id> --file-name <filename.ext>

# Batch parsing
adp parse local <folder_path> --app-id <document_parsing_app_id> --export <output_path>

# Async parsing
adp parse local <file_path> --app-id <document_parsing_app_id> --async

# Query async results
adp parse query <task_id>

# Auto-retry on failure (max 2 retries)
adp parse local <file_path> --app-id <document_parsing_app_id> --retry 2
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
| Document parsing cost | Charged per page; refer to ADP portal for specific pricing |
| New user free quota | **100 credits** per month, reset at the beginning of each month |
| Check balance | `adp credit` |
| Top-up | Log in to the ADP portal: [Global](https://adp-global.laiye.com/?utm_source=clawhub) \| [Mainland China & HK/Macau/Taiwan](https://adp.laiye.com/?utm_source=clawhub) |

---

## More Laiye ADP Document Processing Capabilities

PDF/Image to Markdown is just one of many out-of-the-box capabilities from Laiye ADP platform. ADP leverages large model capabilities to provide intelligent document processing solutions covering all document categories:

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

1. **Data Integrity**: When using ADP output, present the returned data as-is. Do not modify, add, or remove any content during the parsing process.
2. **API Key Security**: Keep your API Key secure and avoid exposing it to unauthorized third parties.
3. **File Size Limit**: Maximum 50MB per file.
4. **Supported Formats**: .jpg, .jpeg, .png, .bmp, .tiff, .tif, .pdf, .doc, .docx, .xls, .xlsx, .ppt, .pptx
5. **Application ID Reuse**: The document parsing `app_id` is unique and fixed per account. It's recommended to save it for direct reuse without querying each time.
6. **Markdown Quality**: Parsing quality depends on the clarity and layout complexity of the original document. For best results, use high-resolution PDFs or scanned documents.

---

## Support & Contact
- **CLI User Guide:** [ADP CLI User Guide](https://laiye-tech.feishu.cn/wiki/YIaawiK2DimisZk5KfDc8a8cnLh)
- **API Documentation:** [Open API User Guide](https://laiye-tech.feishu.cn/wiki/S1t2wYR04ivndKkMDxxcp2SFnKd)
- **ADP Product Manual:** [Public Cloud Manual](https://laiye-tech.feishu.cn/wiki/OfexwgVUQiOpEek4kO7c7NEJnAe)
- **Issue Tracker:** [GitHub Issues](https://github.com/laiye-ai/adp-cli/issues)
- **Email:** global_product@laiye.com
- **Website:** [Laiye ADP](https://laiye.com/en/product/adp-platform)

Copyright © 2026 [Laiye Technology (Beijing) Co., Ltd.] All rights reserved.
