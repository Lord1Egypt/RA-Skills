---
name: file-to-json-parsing
description: "File To JSON Parsing: Parse files to JSON: CSV, HTML, JSON, ICS calendars. Use when an agent needs file to json parsing, parsing uploaded csv files into structured records for database import or api submission, extracting tabular data from html reports or web page snapshots for analysis, converting calendar ics files into event objects for scheduling integrations, processing excel spreadsheets from user uploads into json for data transformation pipelines, extract csv, input base64, file id."
version: 1.0.0
homepage: https://www.agentpmt.com/marketplace/file-to-json-parsing
compatibility: "Agent instructions for AgentPMT-hosted remote tool calls. Follow this skill body for supported account, wallet, and setup routes. No local command runtime is declared."
metadata: {"author":"agentpmt","openclaw":{"homepage":"https://www.agentpmt.com/marketplace/file-to-json-parsing"}}
---
# File To JSON Parsing

## Freshness
Last updated: `2026-06-10`.

If the current date is more than 7 days after the last updated date, reinstall this skill from skills.sh or ClawHub before relying on endpoints, schemas, setup steps, or examples.

## What This Tool Does
A powerful data extraction tool that converts a wide variety of binary file formats into structured JSON output for seamless processing in automated workflows. This function supports eleven extraction actions covering the most common document and data formats: CSV for tabular data parsing, HTML for extracting text content and table structures using BeautifulSoup, JSON for direct parsing, ICS for calendar event extraction, ODS and XLSX/XLS for spreadsheet processing across LibreOffice and Microsoft Excel formats, PDF for page-by-page text and table extraction using pdfplumber, RTF for rich text conversion, and plain text for basic content retrieval. Users can provide input via base64-encoded content or cloud storage file ID, with support for files up to 100MB and inline base64 returns up to 10MB. Configurable parameters allow fine-tuning of extraction behavior including maximum row limits up to 100,000 for spreadsheets, maximum page counts up to 1,000 for PDFs, and toggles for text and table inclusion in applicable formats. The function automatically handles character encoding detection and returns consistently structured JSON with customizable output field names, making it an essential bridge between raw file uploads and downstream data processing pipelines.

## Product Instructions
### File To JSON Parsing - Instructions

#### Overview
Extract structured JSON data from a wide range of file formats. Provide a file via base64-encoded content or a cloud storage file ID, and receive parsed, structured output. Supports CSV, HTML, JSON, ICS (calendar), ODS, PDF, RTF, plain text, XLS, and XLSX files. Also supports converting any file to base64.

#### File Input
Every action (except get_instructions) requires **one** of the following:
- **input_base64** (string) - Base64-encoded file content (up to 100 MB raw; 10 MB for file-to-base64 return)
- **file_id** (string) - File ID from cloud storage

#### Actions

##### extract-csv
Parse a CSV file into structured row data.

**Required:** `action`, plus `input_base64` or `file_id`
**Optional:**
- `max_rows` (integer, default 1000, max 100000) - Maximum rows to extract
- `output_field` (string, default "data") - Key name for the extracted data in the response

**Example:**
```json
{
  "action": "extract-csv",
  "input_base64": "bmFtZSxhZ2UKQWxpY2UsMzAKQm9iLDI1"
}
```

---

##### extract-html
Parse an HTML file, extracting text content and/or table data.

**Required:** `action`, plus `input_base64` or `file_id`
**Optional:**
- `include_text` (boolean, default true) - Include extracted text content
- `include_tables` (boolean, default true) - Include extracted table data
- `max_rows` (integer, default 1000) - Maximum rows per table
- `output_field` (string, default "data")

**Example:**
```json
{
  "action": "extract-html",
  "file_id": "abc123",
  "include_text": true,
  "include_tables": true
}
```

---

##### extract-json
Parse a JSON file and return its contents as structured data.

**Required:** `action`, plus `input_base64` or `file_id`
**Optional:**
- `output_field` (string, default "data")

**Example:**
```json
{
  "action": "extract-json",
  "input_base64": "eyJrZXkiOiAidmFsdWUifQ=="
}
```

---

##### extract-ics
Parse an ICS calendar file and extract events with summary, start, end, location, and description.

**Required:** `action`, plus `input_base64` or `file_id`
**Optional:**
- `output_field` (string, default "data")

**Example:**
```json
{
  "action": "extract-ics",
  "file_id": "calendar_file_id"
}
```

---

##### extract-ods
Parse an OpenDocument Spreadsheet (.ods) file, returning sheets with row data.

**Required:** `action`, plus `input_base64` or `file_id`
**Optional:**
- `max_rows` (integer, default 1000, max 100000) - Maximum rows per sheet
- `output_field` (string, default "data")

**Example:**
```json
{
  "action": "extract-ods",
  "file_id": "spreadsheet_file_id",
  "max_rows": 500
}
```

---

##### extract-pdf
Extract text and/or tables from a PDF document, page by page.

**Required:** `action`, plus `input_base64` or `file_id`
**Optional:**
- `include_text` (boolean, default true) - Include text extraction per page
- `include_tables` (boolean, default true) - Include table extraction per page
- `max_pages` (integer, default 50, max 1000) - Maximum pages to process
- `output_field` (string, default "data")

**Example:**
```json
{
  "action": "extract-pdf",
  "file_id": "report_pdf_id",
  "max_pages": 10,
  "include_text": true,
  "include_tables": false
}
```

---

##### extract-rtf
Parse an RTF (Rich Text Format) file and extract plain text.

**Required:** `action`, plus `input_base64` or `file_id`
**Optional:**
- `output_field` (string, default "data")

**Example:**
```json
{
  "action": "extract-rtf",
  "input_base64": "e1xydGYxIEhlbGxvIFdvcmxkfQ=="
}
```

---

##### extract-text
Read a plain text file and return its contents.

**Required:** `action`, plus `input_base64` or `file_id`
**Optional:**
- `output_field` (string, default "data")

**Example:**
```json
{
  "action": "extract-text",
  "file_id": "text_file_id"
}
```

---

##### extract-xls
Parse a legacy Excel (.xls) file, returning sheets with row data.

**Required:** `action`, plus `input_base64` or `file_id`
**Optional:**
- `max_rows` (integer, default 1000, max 100000) - Maximum rows per sheet
- `output_field` (string, default "data")

**Example:**
```json
{
  "action": "extract-xls",
  "file_id": "legacy_excel_id",
  "max_rows": 2000
}
```

---

##### extract-xlsx
Parse a modern Excel (.xlsx) file, returning sheets with row data.

**Required:** `action`, plus `input_base64` or `file_id`
**Optional:**
- `max_rows` (integer, default 1000, max 100000) - Maximum rows per sheet
- `output_field` (string, default "data")

**Example:**
```json
{
  "action": "extract-xlsx",
  "input_base64": "<base64_encoded_xlsx>",
  "max_rows": 5000
}
```

---

##### file-to-base64
Convert a cloud-stored file to base64 for inline use. The file must be 10 MB or smaller.

**Required:** `action`, plus `input_base64` or `file_id`

**Example:**
```json
{
  "action": "file-to-base64",
  "file_id": "image_file_id"
}
```

---

#### Common Workflows

1. **Parse an uploaded spreadsheet:** Use `extract-xlsx` or `extract-xls` with a `file_id` to get structured row data from each sheet.
2. **Extract text from a PDF report:** Use `extract-pdf` with `include_text: true` and `include_tables: false` for text-only extraction.
3. **Convert HTML to structured data:** Use `extract-html` to pull both readable text and any embedded tables from an HTML file.
4. **Read calendar events:** Use `extract-ics` to get a list of events from an ICS calendar export.
5. **Retrieve a file as base64:** Use `file-to-base64` with a `file_id` to get the raw file content encoded for inline transfer.

#### Important Notes
- Every extraction action requires either `input_base64` or `file_id` -- at least one must be provided.
- Maximum file size is 100 MB. The `file-to-base64` action has a stricter 10 MB limit for the returned content.
- The `max_rows` parameter applies to CSV, HTML tables, ODS, XLS, and XLSX extractions.
- The `max_pages` parameter applies only to PDF extraction.
- The `include_text` and `include_tables` options apply to HTML and PDF extraction.
- The `output_field` parameter lets you customize the key name in the response (default is "data").
- Text files are decoded as UTF-8, falling back to Latin-1 if needed.
- Spreadsheet actions (ODS, XLS, XLSX) return data organized by sheet, each with a name and rows array.

## When To Use
- Use this skill for `File To JSON Parsing` on AgentPMT.
- Use it when an agent needs this specific tool's behavior, schema, inputs, outputs, and invocation shape.
- Search and activation keywords: file to json parsing, parsing uploaded csv files into structured records for database import or api submission, extracting tabular data from html reports or web page snapshots for analysis, converting calendar ics files into event objects for scheduling integrations, processing excel spreadsheets from user uploads into json for data transformation pipelines, extract csv, input base64, file id.
- Supported action names: `extract-csv`, `extract-html`, `extract-ics`, `extract-json`, `extract-ods`, `extract-pdf`, `extract-rtf`, `extract-text`, `extract-xls`, `extract-xlsx`, `file-to-base64`.

## Use Cases
- Parsing uploaded CSV files into structured records for database import or API submission
- extracting tabular data from HTML reports or web page snapshots for analysis
- converting calendar ICS files into event objects for scheduling integrations
- processing Excel spreadsheets from user uploads into JSON for data transformation pipelines
- extracting text and tables from PDF invoices or contracts for automated document processing
- converting legacy XLS files from enterprise systems into modern JSON formats
- parsing RTF documents from email attachments into plaintext for content indexing
- scraping structured table data from HTML exports for reporting dashboards
- extracting event details from shared calendar files for synchronization workflows
- converting uploaded spreadsheet data into API-compatible payloads for third-party service integrations

## Related Product Skills
- File Management: ../file-management (ClawHub: `file-management`, page: https://clawhub.ai/agentpmt/file-management; skills.sh: `npx skills add AgentPMT/agent-skills --skill file-management`)

## Categories And Industries
No categories or industry tags are published for this tool.

## Actions And Schema
Complete generated action schema: `./schema.md`.
Supported action count: `11`.
x402 availability: not enabled for this product.

- `extract-csv` (action slug: `extract-csv`): Parse a CSV file into structured row data. Price: `5` credits. Parameters: `file_id`, `input_base64`, `max_rows`, `output_field`.
- `extract-html` (action slug: `extract-html`): Parse an HTML file, extracting text content and/or table data. Price: `5` credits. Parameters: `file_id`, `include_tables`, `include_text`, `input_base64`, `max_rows`, `output_field`.
- `extract-ics` (action slug: `extract-ics`): Parse an ICS calendar file and extract events with summary, start, end, location, and description. Price: `5` credits. Parameters: `file_id`, `input_base64`, `output_field`.
- `extract-json` (action slug: `extract-json`): Parse a JSON file and return its contents as structured data. Price: `5` credits. Parameters: `file_id`, `input_base64`, `output_field`.
- `extract-ods` (action slug: `extract-ods`): Parse an OpenDocument Spreadsheet (.ods) file, returning sheets with row data. Price: `5` credits. Parameters: `file_id`, `input_base64`, `max_rows`, `output_field`.
- `extract-pdf` (action slug: `extract-pdf`): Extract text and/or tables from a PDF document, page by page. Price: `5` credits. Parameters: `file_id`, `include_tables`, `include_text`, `input_base64`, `max_pages`, `output_field`.
- `extract-rtf` (action slug: `extract-rtf`): Parse an RTF (Rich Text Format) file and extract plain text. Price: `5` credits. Parameters: `file_id`, `input_base64`, `output_field`.
- `extract-text` (action slug: `extract-text`): Read a plain text file and return its contents. Price: `5` credits. Parameters: `file_id`, `input_base64`, `output_field`.
- `extract-xls` (action slug: `extract-xls`): Parse a legacy Excel (.xls) file, returning sheets with row data. Price: `5` credits. Parameters: `file_id`, `input_base64`, `max_rows`, `output_field`.
- `extract-xlsx` (action slug: `extract-xlsx`): Parse a modern Excel (.xlsx) file, returning sheets with row data. Price: `5` credits. Parameters: `file_id`, `input_base64`, `max_rows`, `output_field`.
- `file-to-base64` (action slug: `file-to-base64`): Convert a file to base64-encoded string. File must be 10 MB or smaller for inline return. Price: `5` credits. Parameters: `file_id`, `input_base64`.

## Live Schema And Examples
Use the compact schema above for ordinary calls. Before a new production integration, or whenever parameters, enum values, nested objects, outputs, or examples are unclear, fetch live details first.

- Exact schema: call `agentpmt-tool-search-and-execution` with `action: "get_schema"`, and `tool_id: "file-to-json-parsing"`.
- Detailed examples: call `agentpmt-tool-search-and-execution` with `action: "get_instructions"` and `tool_id: "file-to-json-parsing"`, or call this product with `action: "get_instructions"` when the product tool is already selected.
- Treat returned live schema and instructions as more specific than this generated summary.

MCP schema lookup through the main AgentPMT MCP server:

```json
{
  "method": "tools/call",
  "params": {
    "name": "AgentPMT-Tool-Search-and-Execution",
    "arguments": {
      "action": "get_schema",
      "tool_id": "file-to-json-parsing"
    }
  }
}
```

For live examples, keep the same MCP tool and use these arguments:

```json
{
  "action": "get_instructions",
  "tool_id": "file-to-json-parsing"
}
```

Authenticated AgentPMT REST schema lookup body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_schema",
    "tool_id": "file-to-json-parsing"
  }
}
```

Authenticated AgentPMT REST live examples body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_instructions",
    "tool_id": "file-to-json-parsing"
  }
}
```

## Call This Tool
Product slug: `file-to-json-parsing`

Marketplace page: https://www.agentpmt.com/marketplace/file-to-json-parsing

- AgentPMT account route: first use `../agentpmt-account-mcp-rest-api-setup` to connect the main MCP server or REST API for an Agent Group where this tool is enabled.
- x402 route: not enabled for this product.
- AgentPMT overview: use `../what-is-agentpmt` for marketplace, Agent Group, workflow, MCP, REST, and payment concepts.

If those setup skills are not installed beside this product skill, use the downloads below.

Core AgentPMT setup skills:
- What AgentPMT is: ../what-is-agentpmt
  - ClawHub page: https://clawhub.ai/agentpmt/what-is-agentpmt
  - OpenClaw install: `openclaw skills install what-is-agentpmt`
  - skills.sh install: `npx skills add AgentPMT/agent-skills --skill what-is-agentpmt`
- AgentPMT account MCP/REST setup: ../agentpmt-account-mcp-rest-api-setup
  - ClawHub page: https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup
  - OpenClaw install: `openclaw skills install agentpmt-account-mcp-rest-api-setup`
  - skills.sh install: `npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup`

skills.sh install script:

```bash
npx skills add AgentPMT/agent-skills --skill what-is-agentpmt
npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup
```

MCP call shape after the main AgentPMT MCP server is connected:

```json
{
  "method": "tools/call",
  "params": {
    "name": "File-To-JSON-Parsing",
    "arguments": {
      "action": "extract-csv",
      "file_id": "example file id",
      "input_base64": "example input base64",
      "max_rows": 1000,
      "output_field": "data"
    }
  }
}
```

Use the exact tool name returned by `tools/list`; the name above is the expected readable form.

Authenticated AgentPMT REST call body:

```json
{
  "name": "file-to-json-parsing",
  "parameters": {
    "action": "extract-csv",
    "file_id": "example file id",
    "input_base64": "example input base64",
    "max_rows": 1000,
    "output_field": "data"
  }
}
```

Use the setup skill for the account connection details before making REST calls.

## Response Handling
- Treat the returned JSON as the source of truth for this tool call.
- If the response includes warnings or correction targets, apply them before retrying.
- If the response includes a `passed` or success-style boolean, use it as the workflow gate.
- If validation fails or the response shape is unclear, call `get_schema` or `get_instructions` before retrying.
- If `extract-csv` fails, preserve the request parameters and retry only after fixing schema, auth, or payment errors.

## Security
- Do not place account secrets, wallet private keys, mnemonics, signatures, or payment headers in prompts or logs.
- Keep tool inputs scoped to the minimum content needed for the task.
- Use the setup skills for credential handling; this product skill only defines product-specific behavior.

## AgentPMT Reference
- What AgentPMT is: ../what-is-agentpmt (ClawHub: `what-is-agentpmt`, page: https://clawhub.ai/agentpmt/what-is-agentpmt; skills.sh: `npx skills add AgentPMT/agent-skills --skill what-is-agentpmt`)
- AgentPMT account MCP/REST setup: ../agentpmt-account-mcp-rest-api-setup (ClawHub: `agentpmt-account-mcp-rest-api-setup`, page: https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup; skills.sh: `npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup`)
- Marketplace product: https://www.agentpmt.com/marketplace/file-to-json-parsing
- AgentPMT main MCP server: https://api.agentpmt.com/mcp/
- AgentPMT REST invoke endpoint: https://api.agentpmt.com/products/purchase
