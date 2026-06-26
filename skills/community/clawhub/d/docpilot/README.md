# DocPilot — Intelligent Document Processing Expert

> OpenClaw Skill - Document Parsing, Information Extraction, and Classification

Extract structured data from PDF, images, Word, and Excel documents. Perform field extraction and document classification.

## Why Choose DocPilot?

### Three-Layer Capabilities + Six Core Advantages

**Three-Layer Capabilities**
1. **Parse** — High-precision document content recognition with layout preservation
2. **Extract** — Extract key fields with evidence tracing back to original positions
3. **Classify** — Auto-identify document types, split mixed documents automatically

**Six Core Advantages**

#### 1. Evidence Tracing — Every Field Has an "ID Card" ⭐ Exclusive
```json
{
  "key": "Contract Amount",
  "value": "¥1,200,000",
  "confidence": "high",
  "evidence": [{
    "text": "Total Contract Amount: ¥1,200,000",
    "page": 2,
    "quad": [[120, 350], [480, 350], [480, 380], [120, 380]]
  }]
}
```
> Essential for audit, legal, and finance — know where data comes from to trust it.

#### 2. Mixed Document Splitting — One File, Multiple Types ⭐ Exclusive
Upload a mixed file containing "contract + invoice + quotation", auto-identify boundaries and classify segment by segment.

#### 3. Seal Detection — Official/Signature/Cross-page Seals ⭐ Exclusive
Auto-detect seals and stamps in documents, return position and type info. Ideal for contract review and qualification verification.

#### 4. Cross-page Table Merging — Smart Reconstruction ⭐ Exclusive
Auto-identify tables split across pages, intelligently merge headers and bodies, output complete structures.

#### 5. Handwriting Recognition — Print + Handwriting Mixed ⭐ Exclusive
Support mixed recognition of printed and handwritten text. Covers form filling, handwritten annotations, and signature confirmation.

#### 6. Full Format Support — One Skill Does It All
PDF · Images · Word · Excel · CSV — No need to combine multiple tools.

---

## Features

- ✅ **Multi-format Support**: PDF, Images (JPG/PNG), Word, Excel, CSV
- ✅ **Layout Analysis**: Automatically detect and structure document elements
- ✅ **Table Recognition**: Extract tables with HTML and Markdown outputs, cross-page merge
- ✅ **Information Extraction**: Extract structured fields with evidence tracing
- ✅ **Document Classification**: Single document or mixed document classification & splitting
- ✅ **Seal Detection**: Detect stamps and seals in documents
- ✅ **Handwriting Recognition**: Print + handwriting mixed recognition
- ✅ **Multiple Output Formats**: structured JSON, markdown, plain text

---

## Quick Start

### Installation

```bash
# Install via ClawHub
openclaw skills install DocPilot

# Or manual installation (local development)
cd E:\skills\document-parser
pip install -r requirements.txt
```

### Configuration

**Option 1: Environment Variables**
```bash
# Windows PowerShell
$env:DOCPilot_BASE_URL="https://docpilot.token-ai.com.cn"
$env:DOCPilot_API_KEY="your_api_key"
```

**Option 2: Configuration File**
```bash
cd E:\skills\DocPilot
copy config.example.json config.json
# Edit config.json with your API endpoint and API key
```

**Option 2: Configuration File**
```bash
cd E:\skills\document-parser
copy config.example.json config.json
# Edit config.json with your API endpoint
```

### Usage

#### Parse a Document
```bash
# Basic parsing
DocPilot parse "C:\docs\report.pdf"

# Markdown output
DocPilot parse "C:\docs\scan.jpg" --output markdown

# Enable seal detection and bbox
DocPilot parse "C:\docs\contract.pdf" --seal --bbox

# Parse Excel
DocPilot parse "C:\docs\data.xlsx"
```

#### Extract Information
```bash
# Extract fields with schema
DocPilot extract "C:\docs\contract.pdf" --schema "{\"fields\":[{\"key\":\"Party A\",\"type\":\"string\"},{\"key\":\"Party B\",\"type\":\"string\"}]}"

# Extract with schema file
DocPilot extract "C:\docs\invoice.pdf" --schema schema.json
```

#### Classify Document
```bash
# Single document classification
DocPilot classify "C:\docs\doc.pdf"

# Mixed document classification and splitting
DocPilot classify "C:\docs\mixed.pdf" --mode classify_and_split --categories "[{\"name\":\"Contract\",\"description\":\"Contract agreement\"},{\"name\":\"Invoice\",\"description\":\"Invoice document\"}]"
```

---

## Parameters

### parse Command

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| file | string | Yes | PDF/Image/Word/Excel file path |
| --output | string | No | Output format: structured/markdown/text |
| --layout | flag | No | Enable layout analysis |
| --table | flag | No | Enable table recognition (incl. cross-page merge) |
| --seal | flag | No | Enable seal recognition |
| --dpi | int | No | DPI: 72/144/200/216 |
| --pages | string | No | Page range, e.g., "1-5,8,10-12" |
| --bbox | flag | No | Include bbox coordinates |
| --normalize | flag | No | Return formatted parsed data (default: on) |
| --raw | flag | No | Return raw parsed format |
| --include-image | flag | No | Include images in markdown |
| --image-format | string | No | Image format: url/base64 |

### extract Command

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| file | string | Yes | Document file path |
| --schema | JSON | Yes | Field schema definition |
| --prompt | JSON | No | Prompt mode schema |
| --schema-ref | string | No | Schema reference template |
| --options | JSON | No | Extended options |

### classify Command

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| file | string | Yes | Document file path |
| --mode | string | No | classify_only / classify_and_split |
| --categories | JSON | No | Category schema definition |

---

## Output Format

### parse Response
```json
{
  "code": 10000,
  "message": "Success",
  "data": {
    "document_id": "dp-8a3f-xxxx",
    "page_count": 25,
    "file_type": "pdf",
    "pages": [...],
    "markdown": "..."
  }
}
```

### extract Response
```json
{
  "code": 10000,
  "message": "Success",
  "data": {
    "extraction_id": "ext-xxxx",
    "fields": [
      {
        "key": "Party A",
        "value": "ABC Company",
        "confidence": "high",
        "evidence": [...]
      }
    ],
    "unfound_fields": [],
    "metadata": {...}
  }
}
```

### classify Response
```json
{
  "code": 10000,
  "message": "Success",
  "data": {
    "mode": "classify_only",
    "classification": {
      "category": "Contract",
      "confidence": 0.95,
      "reasoning": "..."
    },
    "metadata": {...}
  }
}
```

---

## Supported Document Elements

| Type | Description |
|------|-------------|
| DocumentTitle | Document title |
| LevelTitle | Section heading |
| Paragraph | Text paragraph |
| Table | Table (with cross-page merge) |
| Image | Image |
| Seal | Seal/Stamp |
| FigureTitle | Figure title |
| Handwriting | Handwritten text |

---

## Typical Use Cases

| Scenario | Usage | Core Capability |
|----------|-------|-----------------|
| **Contract Review** | Extract key fields + seal detection | Evidence tracing + Seal recognition |
| **Financial Audit** | Cross-page table merge + field extraction | Cross-page merge + Tracing |
| **Archive Organization** | Mixed document auto-classification & splitting | Document classification |
| **Bidding Documents** | Identify quotations/qualifications/proposals separately | Classification + Parsing |
| **Form Processing** | Handwriting recognition + structured extraction | Handwriting + Extraction |
| **Compliance Check** | Detect seals, verify document integrity | Seal detection |

---

## Error Codes

| Code | Message | Description |
|------|---------|-------------|
| 10000 | Success | Successful |
| 10001 | Missing parameter | Missing required parameter |
| 10002 | Invalid parameter | Invalid parameter value |
| 10003 | Invalid file | Unsupported file format |
| 10004 | Failed to recognize | Recognition failed |
| 10005 | Internal error | Internal server error |

---

## Dependencies

- Python 3.8+
- requests>=2.28.0

---

## License

MIT License

---

## Support

File an issue or contact TokenAI for help.
