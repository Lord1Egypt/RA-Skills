# Bytedance TOS Document Process Skill

This skill enables an agent to perform document processing tasks on files stored in Bytedance's TOS (TeraObjectStore) by using the Volcengine TOS Python SDK's `doc-preview` feature.

**Key Change**: The official TOS Python SDK's `get_object` method currently only supports a limited set of data processing parameters (e.g., `process`, `save_bucket`). Document-specific parameters like `doc_dest_type` or `doc_page` are **not** supported as direct keyword arguments.

Therefore, this skill now exclusively uses the SDK's **`pre_signed_url`** method to pass all `doc-preview` parameters as query strings.

## Overview

The skill provides scripts and documentation for common document preview and conversion tasks, allowing an agent to:

1.  **Preview Documents as PDF**: Convert office documents into a single PDF file.
2.  **Preview Pages as Images**: Convert specific pages into PNG or JPG images, with control over DPI and quality.
3.  **Preview as HTML**: Fetch an HTML representation and extract the final, usable preview URL.
4.  **Query Total Page Count**: Read the `x-tos-total-page` response header.
5.  **Batch Export Pages**: Use advanced parameters to export a range of pages.

All operations are performed via generating a pre-signed URL and then making an HTTP request.

## Skill Structure

```
byted-tos-doc-process/
├── SKILL.md
├── README.md
├── REFERENCE.md
├── WORKFLOWS.md
├── scripts/
│   ├── doc_preview_params.py   # NEW: Helper for building query parameters
│   ├── doc_preview_pdf.py
│   ├── doc_preview_png.py
│   ├── doc_preview_jpg.py
│   ├── doc_preview_html_url.py # Supports --direct-url
│   ├── doc_preview_process.py
│   └── doc_total_page.py
└── requirements.txt
```

## Setup and Configuration

### Requirements
- Python 3.7+
- `tos` Python SDK

### Installation

```bash
pip install -r requirements.txt
```

### Environment Variables

| Variable                 | Description                                                  | Example                                    |
| ------------------------ | ------------------------------------------------------------ | ------------------------------------------ |
| `TOS_ACCESS_KEY`         | Your Access Key ID for TOS authentication.                   | `AKL...`                                   |
| `TOS_SECRET_KEY`         | Your Secret Access Key for TOS authentication.               | `your-secret-key`                          |
| `TOS_SECURITY_TOKEN`     | (Optional) The session token for temporary STS credentials.  | `STS...`                                   |
| `TOS_ENDPOINT`           | The full URL of the TOS service endpoint.                    | `https://tos-cn-beijing.volces.com`        |
| `TOS_REGION`             | The region of the TOS service.                               | `cn-beijing`                               |
| `TOS_BUCKET`             | The name of the bucket where the target document is stored.    | `my-document-assets`                       |
| `TOS_OBJECT_KEY`         | The full path (key) of the document file within the bucket.  | `reports/quarterly-review.docx`            |
| `MAX_OBJECT_SIZE`        | (Optional) Safeguard for local file size, in bytes.          | `262144` (default)                         |

### **Important: Custom Domain Restriction**

For buckets created after **Jan 03, 2024**, you **must** use a custom domain when accessing previewed files. Using the default TOS domain will result in the file being downloaded directly rather than previewed online.

## Quick Start

### 1. Set Environment Variables

```bash
# --- Required ---
export TOS_ACCESS_KEY="YOUR_AK"
export TOS_SECRET_KEY="YOUR_SK"
export TOS_ENDPOINT="https://tos-cn-beijing.volces.com"
export TOS_REGION="cn-beijing"
export TOS_BUCKET="your-doc-bucket"
export TOS_OBJECT_KEY="path/to/your/document.docx"
```

### 2. Run Example Scripts

**Convert Document to PDF:**
This script now generates a pre-signed URL with `x-tos-doc-dst-type=pdf` and downloads the result.
```bash
python3 scripts/doc_preview_pdf.py --output "preview.pdf"
```

**Convert Page 2 to a PNG Image:**
```bash
python3 scripts/doc_preview_png.py --page 2 --output "page_2.png"
```

**Get the HTML Preview URL (via Pre-signed URL):**
```bash
python3 scripts/doc_preview_html_url.py
```

The HTML preview script will now directly extract the full HTML link from `window.open("<LINK>","_self")` in the returned page, and then parse and decode the `token` parameter. Typical output looks like:

```text
[OK] Extracted preview information:
  HTML Link   : https://doc-preview.tos-cn-beijing.volces.com/index.html?token=...
  Token       : aHR0cHM6Ly9kYXRhLXByb2Nlc3MtdGVzdC13Y2MudG9zLWNuLWJlaWppbmcudm9sY2VzLmNvbS9kYXRhLXByb2Nlc3MtdGVzdC13Y2NfMTMwMTcwNTYxOTIwMjc4MjUyNjZfJTIyMTA1MDM0ZGEwZmQ5YTA2YTg0N2MwMjM2MTI1MGM3MjAlMjIucGRmP1gtVG9zLUh0bWwtUHJldmlldz1YbzJ4X0s0alhkaUlCX3Ric0lNZjlsUDNfSDlHSDZGcXg0RHFkdjF6N0paOGtLSFpBUE5QbEZtdHotU3NqQ1E1eU5jaTJqY05QZ25pMXVvenVMampGSkZfX2JQdi02c1A0LUVvMEtwY2Jja1hrNWgtMy1zaE9tdnFyVTRBTmZLSmh1QjVhajdBUmJoWkU3RnQxOVBDYUxXdjZnNFRWVTJzejlXWXRxNG9YejR3dE8wR0JmNjVuRW5pUXBtQXlJYjVQQWpUTWdxZjNUbjlQTzMyLURhMXJnZlZSWHhJd1VITHlrekRxWGZReVZzcW9Bd0hYZkU1dnc0VThZek84Qndjd05DdjZFa2EzeWZ5c1lQZzNHckNQQVZ5Mk5qSlRrTmhBdEFkOTBpUlRCWUV0OWl4bXhVU2dqQnE1TnE2VUdaVnhJN2loVnNZaGxMOUZxOUtNRm5uUHhKbnlXcjNacEZpWS1NOVRLbmx3dV94cVBKZ3lwRDdTNlllcWhncGtoVTJJTmhqWW5UenRVMTl1b0pjVVBiOWFsT2ZEbnlwMDc5aWhOejMtVlNuRmdTN2N1U0REYmkyeUlCTUF4QTdRVnphQ3ZkdTFQLTZULVRVUjZDa3MzRzIwM3VYWHhzekZsbk9EVjFrU0xES3UzZlMwWi14MTRxb0d5MUJWdFZ2eWR6bTN2VlkweE5CUV8yQnZqSVMwRWdrZWclM0QlM0Q=
  Preview URL : https://data-process-wcc-cq.tos-cn-chongqing-sdv.volces.com/data-process-wcc-cq_13017056192027825266_0d636579368e234ba0137e51d5b4f244.pdf?X-Tos-Html-Preview=...
```

**Get the HTML Preview URL (from a direct sample link):**
This new mode allows parsing an existing HTML preview URL without needing credentials.
```bash
python3 scripts/doc_preview_html_url.py --direct-url "https://your-bucket.tos-cn-beijing.volces.com/doc.docx?x-tos-process=doc-preview&x-tos-doc-dst-type=html"
```

**Get the Total Page Count:**
This script now reads the `x-tos-total-page` header from a pre-signed URL response.
```bash
python3 scripts/doc_total_page.py --dest-type pdf
```

**Use the Generic Processor to Batch Export Pages 1-3 as JPG:**
```bash
python3 scripts/doc_preview_process.py \
  --dest-type jpg \
  --img-mode 1 \
  --start-page 1 \
  --end-page 3 \
  --saveas-bucket "your-output-bucket" \
  --saveas-object "export/page_{Page}.jpg"
```

## Note on Implementation

The `doc-preview` feature is invoked by generating a pre-signed URL with all processing parameters in the query string. The `scripts/doc_preview_params.py` helper constructs this query dict. Always refer to the official Volcengine TOS documentation for the most up-to-date list of parameters.
