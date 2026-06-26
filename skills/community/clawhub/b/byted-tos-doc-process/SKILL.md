---
name: byted-tos-doc-process
description: Generates pre-signed URLs for Bytedance TOS `doc-preview` processing to preview and convert documents to PDF, images (PNG/JPG), or HTML, and to export page ranges. Use when the user needs TOS document preview/conversion, page count/export, or mentions doc-preview, x-tos-process, or x-tos-doc-* parameters.
version: 1.1.0
---

# Bytedance TOS Document Process Skill

This skill provides document processing functions for files in Bytedance's TOS via the `doc-preview` feature, implemented by generating **pre-signed URLs** with the Volcengine TOS SDK.

**Note**: This approach is necessary because the SDK's `get_object` method does not directly support `doc_*` keyword arguments. All document processing parameters must be passed as query parameters in a pre-signed URL.

## Quick Start

### 1. Client Initialization

```python
import os
import tos
from tos.enum import HttpMethodType
from urllib.request import urlopen

def create_client() -> tos.TosClientV2:
    """Initializes a TosClientV2 from environment variables."""
    try:
        # ... (full implementation in scripts)
        return tos.TosClientV2(
            ak=os.getenv('TOS_ACCESS_KEY'),
            sk=os.getenv('TOS_SECRET_KEY'),
            endpoint=os.getenv('TOS_ENDPOINT'),
            region=os.getenv('TOS_REGION'),
            security_token=os.getenv('TOS_SECURITY_TOKEN'),
        )
    except Exception as e:
        print(f"Error initializing client: {e}")
        return None

client = create_client()
```

### 2. Basic Workflow (Pre-signed URL)

```python
# (Assumes 'client' is initialized and 'bucket_name', 'object_key' are set)

# 1. Preview document as a PDF and save locally
try:
    # Build query params for doc-preview
    pdf_params = {
        "x-tos-process": "doc-preview",
        "x-tos-doc-dst-type": "pdf"
    }
    presigned_pdf = client.pre_signed_url(
        HttpMethodType.Http_Method_Get,
        bucket_name,
        object_key,
        query=pdf_params
    )
    
    # Download the content from the pre-signed URL
    with urlopen(presigned_pdf.signed_url) as response, open("local_preview.pdf", "wb") as f_out:
        f_out.write(response.read())
    print("PDF preview saved to local_preview.pdf")

except Exception as e:
    print(f"Error converting to PDF: {e}")

# 2. Preview page 3 as a PNG image
try:
    png_params = {
        "x-tos-process": "doc-preview",
        "x-tos-doc-dst-type": "png",
        "x-tos-doc-page": "3",
        "x-tos-doc-image-dpi": "150"
    }
    presigned_png = client.pre_signed_url(
        HttpMethodType.Http_Method_Get,
        bucket_name,
        object_key,
        query=png_params
    )
    with urlopen(presigned_png.signed_url) as response, open("page_3.png", "wb") as f_out:
        f_out.write(response.read())
    print("Page 3 saved as page_3.png")

except Exception as e:
    print(f"Error converting to PNG: {e}")

# 3. Get total page count from response headers
try:
    presigned_head = client.pre_signed_url(
        HttpMethodType.Http_Method_Get,
        bucket_name,
        object_key,
        query={"x-tos-process": "doc-preview", "x-tos-doc-dst-type": "pdf"}
    )
    with urlopen(presigned_head.signed_url) as response:
        total_pages = response.headers.get("x-tos-total-page")
        print(f"Document has {total_pages} pages.")
except Exception as e:
    print(f"Error getting page count: {e}")
```

## Core Operations

All document processing is achieved by generating a pre-signed URL with `process=\"doc-preview\"` and other `x-tos-doc-*` parameters in the query string.

### 1. Convert to PDF (`x-tos-doc-dst-type='pdf'`)

Converts an entire document into a single PDF file.

```python
# See Quick Start example
```

### 2. Convert to Image (`x-tos-doc-dst-type='png' or 'jpg'`)

Converts a specific page of a document into an image.

```python
# See Quick Start example
# Use query params like "x-tos-doc-page", "x-tos-doc-image-dpi", etc.
```

### 3. Convert to HTML (`x-tos-doc-dst-type='html'`)

Fetches a temporary HTML page containing a token for the final preview URL. This requires a second step to parse the HTML and decode the token.

```python
# Step 1: Get the HTML content via a pre-signed URL
html_params = {"x-tos-process": "doc-preview", "x-tos-doc-dst-type": "html"}
presigned_html = client.pre_signed_url(HttpMethodType.Http_Method_Get, bucket_name, object_key, query=html_params)

with urlopen(presigned_html.signed_url) as response:
    html_content = response.read().decode('utf-8')

# Step 2: Parse and decode (see scripts/doc_preview_html_url.py for full logic)
# ... logic to extract and base64-decode the token ...
# final_url = decode_preview_url(token)
```

### 4. Batch Export Pages (`image-mode=1`)

Exports a range of pages as images directly to a TOS bucket.

```python
# Use query params: "image-mode", "start-page", "end-page", "x-tos-save-bucket", "x-tos-save-object"
batch_params = {
    "x-tos-process": "doc-preview",
    "x-tos-doc-dst-type": "jpg",
    "image-mode": "1",
    "start-page": "2",
    "end-page": "5",
    "x-tos-save-bucket": "output-bucket",
    "x-tos-save-object": "exported/page_{Page}.jpg" # {Page} is a placeholder
}
presigned_batch = client.pre_signed_url(HttpMethodType.Http_Method_Get, bucket_name, object_key, query=batch_params)
# The response body (from urlopen) contains JSON metadata about the batch job
```

## Authorization

Authentication is handled by `tos.TosClientV2`. Provide credentials via environment variables.

### Required Environment Variables
- `TOS_ACCESS_KEY`
- `TOS_SECRET_KEY`
- `TOS_ENDPOINT`
- `TOS_REGION`

### Optional for STS
- `TOS_SECURITY_TOKEN`

## Best Practices
- **Error Handling**: Always wrap HTTP requests in `try...except` blocks for `HTTPError` and `URLError`.
- **Parameter Reference**: Refer to `REFERENCE.md` for a mapping of `doc_preview_params.py` arguments to `x-tos-*` query keys and to the official TOS documentation for authoritative details.
- **HTML Preview**: Be aware of the two-step process and the custom domain requirement for recent buckets.
- **Total Pages Header**: The `x-tos-total-page` header is a convenient way to get the page count.

## Additional Resources
- For detailed parameters, see [REFERENCE.md](REFERENCE.md).
- For end-to-end examples, see [WORKFLOWS.md](WORKFLOWS.md).
- For executable Python examples, see the `scripts/` directory.
- **For the definitive list of all processing parameters, always consult the official Volcengine TOS Document Preview documentation.**
