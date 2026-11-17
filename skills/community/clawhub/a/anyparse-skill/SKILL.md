---
name: anyparse-skill
description:
  Use the AnyParse API to extract content from various documents. Supports PDF, Word, Excel, CSV, TSV, images, PPT, HTML, Markdown, Epub, ipynb, RST, EML,
  and many other formats. Supports document orientation classification, layout analysis, and layout preservation. Use this skill when users need to parse documents,
  extract document content, or convert documents into structured text.
version: 1.0.0
author: anyparse
metadata:
  openclaw:
    requires:
      env:
        - anyparse_api_url
        - anyparse_api_key
      bins:
        - python
---
# AnyParse Document Parsing and Extraction Skill

Use the AnyParse API to extract structured text content from multiple document formats.

## When to Use

- Extract text content from documents
- Convert scanned documents/images into structured text
- Preserve document page layout and identify content in different regions
- Automatically classify document orientation (landscape/portrait) to improve recognition accuracy
- The user mentions "document parsing", "OCR", "text extraction", "content extraction", or "document conversion"

## Key Features

- **Multi-format support**: Supports common document formats and image formats
- **Layout analysis**: Preserves information about the original document layout
- **Document orientation classification**: Automatically recognizes landscape/portrait documents to improve accuracy
- **Structured output**: Returns complete page layouts and full text
- **Local deployment**: Supports private local deployment, keeping data privacy under your control

## Prerequisites

- The AnyParse API service has been deployed, and its access URL and key have been configured

## Security Notes

- This skill does not perform any operations other than runtime package installation
- It only sends requests to the AnyParse API service you configured
- It only reads the API URL and key from environment variables or configuration files

**⛔ Mandatory Restrictions - Do Not Violate ⛔**

1. **Use only the AnyParse API** - Run `python scripts/api.py` to complete parsing
2. **Never parse documents yourself** - Do not attempt to extract text by yourself
3. **Do not provide alternatives** - Do not say things like "I can try to analyze it"
4. **If the API fails** - Show the error message and stop immediately
5. **Do not use fallback methods** - Do not attempt to extract text in any other way

## Installation and Configuration

1. Deploy the AnyParse service (see the official project documentation)
2. Install dependencies:

   ```bash
   pip install -r scripts/requirements.txt
   ```
3. Configure: edit `scripts/config.json` and enter your API URL and key:

   ```json
   {
     "anyparse_api_url": "http://your-api-host:port/anyparse/invoke/v1",
     "anyparse_api_key": "your-api-key-here"
   }
   ```

   Or configure them through environment variables:
   ```bash
   export anyparse_api_url=http://your-api-host:port/anyparse/invoke/v1
   export anyparse_api_key=your-api-key-here
   ```

## Usage

### Parse a Local File (layout analysis enabled by default)

```bash
python scripts/api.py --file /path/to/document.pdf
```

### Enable Document Orientation Classification

```bash
python scripts/api.py --file /path/to/image.jpg --use_doc_cls
```

### Enable Document Rectification
```bash
python scripts/api.py --file /path/to/image.jpg --use_doc_rectifier
```

### Disable Layout Analysis

```bash
python scripts/api.py --file /path/to/document.pdf --no_doc_layout
```

## CLI Reference

```
python {baseDir}/scripts/api.py --file PATH [--use_doc_cls] [--no_doc_layout]
```

| Parameter              | Required | Description                       |
| ---------------------- | -------- | --------------------------------- |
| `--file`               | Yes      | Local file path                   |
| `--use_doc_cls`        | No       | Use document orientation classification |
| `--use_doc_rectifier`  | No       | Use document rectification        |
| `--no_doc_layout`      | No       | Do not use document layout analysis |

## Response Format

```json
{
  "code": 2000,
  "msg": "success",
  "data": {
    "metadata": {
      "file_md5": "f484351567161df1e5e4d9d4b861c594",
      "file_type": "jpg",
      "file_name": "image.jpg",
      "file_size": "8.10/KB"
    },
    "pages": [
      {
        "id": 1,
        "content": "$10^{9}/L$",
        "layout": [
          {
            "order_id": 0,
            "label_name": "text",
            "box": [0, 0, 196, 80],
            "task": "text",
            "parse_text": "$10^{9}/L$"
          }
        ],
        "elapse_times": 1.9343271255493164
      }
    ],
    "content": "$10^{9}/L$",
    "elapse_times": 1.9524128437042236
  }
}
```

Key fields:

- `code` — API status code; 2000 means success
- `msg` — Status message
- `data.metadata` — File metadata
- `data.pages[].layout[]` — Layout information for each region, including position and parsing result
- `data.content` — Merged text result for the entire document

## Error Handling

**API URL not configured:**
→ Tell the user to configure `anyparse_api_url` in config.json or environment variables

**API key not configured:**
→ Tell the user to configure `anyparse_api_key` in config.json or environment variables

**File does not exist:**
→ Check whether the file path is correct

**Non-2000 status code:**
→ Show the API error message to the user

**Missing dependencies:**
→ Tell the user to run `pip install -r scripts/requirements.txt` to install dependencies
