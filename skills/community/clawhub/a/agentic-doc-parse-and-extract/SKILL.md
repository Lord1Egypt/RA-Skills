---
name: agentic-doc-parse-and-extract
description: Enables AI-powered parsing and key information extraction from high-frequency documents including invoices, orders, receipts, long texts, and common Chinese identity & credential documents. Supports reusable custom templates for non-standard business files. Features batch concurrent processing to automate document workflows for finance, administration, HR data entry and other departments.
---
# agentic-doc-parse-and-extract Skill

agentic-doc-parse-and-extract is an official command-line tool released by Laiye Technology's ADP (Agentic Document Processing) product, enabling both humans and AI agents to invoke ADP capabilities in the terminal for document parsing and extraction.

## Quick Start Guide for AI Agents

### Core Workflow
1. **Install dependencies**: On first execution, install the ADP CLI tool and dependencies by following the instructions in [references/examples.md](references/examples.md).
2. **Discover commands**: Run `adp schema` to get the machine-readable JSON spec of all commands, parameters, types, and defaults.
3. **Authentication**: On first execution, run `adp config get` to verify credentials. If no valid configuration exists, prompt the user to provide an API Key.
4. **Check Application**: On first execution, retrieve the application list via `adp app-id list`. For subsequent executions, prioritize `adp app-id cache` (cached in context). If the cache is unavailable, refresh it by calling `adp app-id list` again.
5. **Execute**: Run `adp extract url <URL> --app-id <ID>` or `adp parse url <URL> --app-id <ID>`.
6. **Query**: Check results asynchronously with `adp extract query <task_id>` or `adp parse query <task_id>`.
7. **Error handling**: When a command fails, parse the stderr JSON to determine error type and recovery action. See [references/error-handling.md](references/error-handling.md).

### Common Scenarios → Command Mapping
| User Intent | Recommended Command | Handling Rules |
| :---------- | :------------------ | :------------- |
| - Read full document content<br>- Parse layout & structure<br>- Convert document to text<br>- Process / analyze full document | `adp parse` | - Sync processing for small files<br>- Async processing (`--async` parameter) for files >20MB or >200 pages |
| - Extract key fields (amount, date, name, ID, etc.)<br>- Output structured results (JSON/table) | `adp extract` | - Use Extract directly, **no need to parse first**<br>- Use matched existing app<br>- Create a custom extraction app if the document type is not in the known app list |
| Batch processing of local files | `adp extract local <folder path>` <br> `adp parse local <folder path> `  | Batch processing can accept files from the local folder. |
| Batch processing of URL files | `adp extract url <URL list file path>` <br> `adp parse url <URL list file path> `  | If you need to process multiple URLs in a batch, you can first save the list of URLs in a text file, and then input the corresponding URL of this text file to achieve batch processing at once. |

Note:
- The `adp extract` command has built-in document parsing capabilities. After ADP automatically parses the document, it performs structured extraction. Therefore, when users need to extract the structured content of the document, there is no need to use apd for parsing.
- URL list file format: A plain text file where each line is a URL pointing to a document to be processed.


### Quick Reference for Common Commands

```bash
# Command Discovery (for Agent introspection)
adp schema

# Configuration Check
adp config get

# Query Applications (First Use)
adp app-id list

# Document Extraction (Invoice/Receipt)
adp extract url <file URL> --app-id <app_id>

# Document Parsing (Long Document)
adp parse url <file URL> --app-id <app_id>

# Base64 Input
adp extract base64 <base64_string> --app-id <app_id> --file-name invoice.pdf
adp parse base64 <base64_string> --app-id <app_id> --file-name document.pdf

# Asynchronous Query
adp extract query <task_id>
adp parse query <task_id>
adp parse query <task_id1> <task_id2> --watch  # batch query with auto-poll

# Batch Processing
adp extract local <folder path> --app-id <app_id> --export <folder path> --concurrency 2
adp parse local <folder path> --app-id <app_id> --export <folder path> --concurrency 2
```

## Performance Optimization Suggestions
- **Reuse APP_ID**: Cache it in the context after one query to avoid calling `app-id list` every time.
- **Sync First**: For small files (<20MB), prioritize using synchronous calls to avoid asynchronous polling.
- **Batch Processing**: Processes multiple documents via `url <URL list file path>` or `local <folder path>` in a single run, without looped invocations. Default `--concurrency 2`.
- **Local Cache**: Store commonly used APP_IDs in environment variables or configuration files.
- **Priority Extraction**: If only key information needs to be extracted, use `extract` instead of `parse` (faster).
- **Use --retry for batch**: Set `--retry 2` for batch processing to auto-recover from transient failures.
- **Use --timeout for large files**: Increase `--timeout` for files >20MB. Default is 900s.

---

## Detailed Product Introduction

### Core Function Definition
- **parse**: Parses the entire document to retrieve full text, layout, structure, and content.
- **extract**: Extracts specific structured fields from the document, such as amount, date, company name, and order number.

### Application Scenarios
- **Long Document Parsing**: Efficiently process long documents with fast parsing speed, accurately extract multiple elements such as text, tables and images, replace manual extraction, and improve efficiency.
- **Structured Extraction for Scanned/Photographed Documents**: For scanned documents and photos, complete structured extraction in reading order, generate clear and editable electronic documents, and eliminate manual entry errors.
- **Intelligent Invoice Extraction**: After uploading invoice images/documents, AI automatically invokes preset applications to accurately extract 10+ key fields such as invoice number and amount, suitable for financial filing scenarios.
- **Intelligent Order Extraction**: Support batch upload of orders from multiple distributors, AI extracts 10+ key fields such as order number and buyer-seller information, automatically identifies currencies, and reduces manual verification costs.
- **Domestic ID Document Extraction**: Process in seconds, supporting the identification and extraction of more than 10 common types of documents in China; for example, core information such as name and ID number can be quickly extracted from ID card scans.
- **Automatic Splitting and Extraction of Mixed Documents**: Batch upload mixed documents such as contracts and invoices, AI automatically classifies, splits and completes structured extraction to improve processing efficiency.
- **Batch Document Processing**: Support batch upload of various business documents, extract information and output standardized structured data, reducing repetitive manual operations.

## Detailed Usage Steps

### Step 1: Obtain the Installation Package
For details, see [references/examples.md](references/examples.md)

### Step 2: Obtain and Configure API Key

   #### 1. Access the ADP Portal to Obtain Credentials

   We provide independent Public Cloud access addresses for domestic and international users, which need to be configured separately by region. Accessing nearby can better ensure high-speed and stable calls across the network.

   | Region | Login Address | API Base URL |
   |-----|----------|--------------|
   | Chinese Mainland | [https://adp.laiye.com/](https://adp.laiye.com/?utm_source=clawhub) | `https://adp.laiye.com/` |
   | Overseas Region | [https://adp-global.laiye.com/](https://adp-global.laiye.com/?utm_source=clawhub) | `https://adp-global.laiye.com/` |

   #### 2. Get API Key after registration/login
   New users need to register an ADP account first, and after registration, they can get 100 free credits/month
   - After logging in, click on the personal avatar, and you can directly access the `API_Key` entry.
   
   #### 3. Complete the authentication configuration
   For details, see [references/examples.md](references/examples.md)
   
   #### 4. Verify the configuration
   For details, see [references/examples.md](references/examples.md)
   
   **Notes**:
   1. If API Key and API Base URL have been configured, the configuration information needs to be stored in environment variables to avoid uploading configuration items every time they are used.
   2. If API Key and API Base URL have not been configured yet, they need to be configured according to the above steps.

### Step 3: Upload Documents
After completing the authentication of the API Key, guide the user to upload local files or specify the file URL. After the user uploads the document, they can query the supported application scope of ADP and select the appropriate application for document parsing and extraction. If no suitable application is found, they can choose to create a custom extraction application, configure exclusive fields and parsing modes to meet the personalized document processing requirements.

### Step 4: Query Available Applications 
This function is used to query the built-in applications under the user's account (such as invoices/receipts, orders, common cards and certificates in China region, etc. which are standardized documents). Based on the `app-label`, you can assist in filtering the suitable application IDs. If no suitable application is found, you can choose to create a custom extraction application, configure specific fields and parsing modes to meet the personalized document processing requirements.

**Notes**:
1. For the first execution, use `adp app-id list`. For subsequent executions, prefer to use `adp app-id cache` (cache the application ID in the context). If the cache becomes invalid or there are no suitable applications in the cache, call `adp app-id list` again to update the cache.

For detailed examples of commands and responses, see [references/examples.md](references/examples.md).


### Step 5: Add custom extraction application

Support creating custom extraction applications, and independently add business-specific extraction fields as needed, and improve the detailed description of each field; the system will accurately identify the document content based on the configured fields and definitions, and complete customized information extraction for personalized documents and non-standard forms.

For example commands, responses, and detailed parameter descriptions, please refer to [references/examples.md](references/examples.md) 

### Step 6: Execute Document Processing

### Single Document Parsing

Perform document parsing based on the selected application ID, which will return a formatted JSON result containing information such as document content, element position coordinates, OCR Confidence Level, etc.

For examples of commands and responses, please refer to [references/examples.md](references/examples.md)

### Single Document Extraction

Perform document extraction based on the selected application ID, which will return a formatted JSON result containing information such as extraction fields, extraction results, and Confidence Level.

For examples of commands and responses, please refer to [references/examples.md](references/examples.md)


### Batch Document Processing

ADP supports batch processing capabilities. Users can upload multiple file URLs or local folder paths at once, and the system will automatically identify each document type and match the most suitable application for processing, greatly improving the efficiency of batch document processing.

For detailed command examples, see [references/examples.md](references/examples.md)

**Note**: The number of concurrent requests is limited to 1 for free users, while enterprise users can adjust it according to their needs, with a maximum support of 2.

### Asynchronous Processing (Suitable for Large Documents)

ADP provides asynchronous processing capabilities, allowing users to choose asynchronous mode to perform document parsing and extraction. The system will return a task ID, and users can periodically query the task status and results through the query interface, which is suitable for processing complex documents or batch documents with long processing times. If the document uploaded by the user is larger than 20MB or contains more than 200 pages, it is recommended to use the asynchronous processing mode.

For examples of commands and responses, see [references/examples.md](references/examples.md)

---

## Complete Command List

For a complete list of all available commands with full parameter specs, see [references/commands.md](references/commands.md)

## Response Schema Reference

For the output structure of each command (including batch processing output mechanism), see [references/response-schema.md](references/response-schema.md)

## Error Handling Guide

For error codes, types, and Agent auto-recovery strategies, see [references/error-handling.md](references/error-handling.md)

---

## Precautions

When using ADP output, always present the returned data as-is. Do not modify, add, or remove any fields during extraction or parsing to ensure data integrity.

1. **API Key Security**: Please keep your API Key secure and avoid disclosing it to unauthorized third parties.
2. **API Base URL Configuration**: Select the corresponding address based on the region. For Chinese Mainland, use `https://adp.laiye.com/`, and for overseas regions, use `https://adp-global.laiye.com/`
3. **File Size Limit**: The maximum size of a single file is 50MB
4. **Supported Formats**: .jpg, .jpeg, .png, .bmp, .tiff, .tif, .pdf, .doc, .docx, .xls, .xlsx
5. **Free Quota**: New users receive 100 free credits per month, which are reset at the beginning of each month. Credits can be used for document parsing and extraction processing.
6. **Check Balance**: Run `adp credit` to check the current account's credit balance.
7. **Billing Rules**:
   - Document parsing: 0.5 credits per page
   - Invoice/receipt extraction: 1.5 credits per page
   - Order extraction: 1.5 credits per page
   - Custom extraction: 1 credit per page
8. **App ID Reuse**: The app ID used by the user can be remembered for direct use next time, eliminating the need to enter the app_id after each query. The app ID under each user is unique and fixed; unless the user deletes the app, the app_id will not change, and the previously queried app_id can be directly used for document processing calls.

---

## Related Resources
- **CLI Documentation**: [ADP CLI User Guide](https://laiye-tech.feishu.cn/wiki/YIaawiK2DimisZk5KfDc8a8cnLh)
- **API Documentation**: [OpenAPI User Guide](https://laiye-tech.feishu.cn/wiki/S1t2wYR04ivndKkMDxxcp2SFnKd)
- **User Guide**: [Public Cloud Operation Manual](https://laiye-tech.feishu.cn/wiki/OfexwgVUQiOpEek4kO7c7NEJnAe)
- **Problem Feedback**: [GitHub Issues](https://github.com/laiye-ai/adp-cli/issues) | global_product@laiye.com
- **Official Website**: [Laiye Technology](https://laiye.com)

---

Copyright © 2026 [Laiye Technology (Beijing) Co., Ltd.] All rights reserved.
