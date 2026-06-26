# Bytedance TOS Document Process Workflows

This document illustrates common workflows for document processing using the `doc-preview` feature via **pre-signed URLs** with the Volcengine TOS Python SDK.

## Table of Contents
- [Workflow 1: Previewing a Document as a Single PDF](#workflow-1-previewing-a-document-as-a-single-pdf)
- [Workflow 2: Previewing a Specific Page as a PNG Image](#workflow-2-previewing-a-specific-page-as-a-png-image)
- [Workflow 3: Getting the HTML Preview URL](#workflow-3-getting-the-html-preview-url)
- [Workflow 4: Batch Exporting a Page Range to TOS](#workflow-4-batch-exporting-a-page-range-to-tos)
- [Workflow 5: Reading the Total Page Count Header](#workflow-5-reading-the-total-page-count-header)
- [Workflow 6: Handling Errors](#workflow-6-handling-errors)

---

### Prerequisite: Client Initialization

All workflows assume you have a `tos.TosClientV2` instance initialized. See `README.md` for details.

```python
import os
import tos
from tos.enum import HttpMethodType
from urllib.request import urlopen, Request
from urllib.error import HTTPError, URLError
from doc_preview_params import build_doc_preview_query_params

# ... (create_client function)
client = create_client()
bucket_name = os.getenv("TOS_BUCKET")
object_key = os.getenv("TOS_OBJECT_KEY")
```

---

### Workflow 1: Previewing a Document as a Single PDF

**Goal**: Convert a DOCX, PPTX, or other office document into a single PDF file and save it locally.

**Script**: `scripts/doc_preview_pdf.py`

**Steps**:
1.  Build query parameters for PDF preview using `build_doc_preview_query_params`.
2.  Generate a pre-signed URL with `client.pre_signed_url()`.
3.  Use `urllib.request.urlopen` to download the content from the signed URL and save it to a file.

**Python Example (`scripts/doc_preview_pdf.py` logic):**
```python
# Assumes 'client', 'bucket_name', 'object_key' are initialized
output_pdf_path = "document_preview.pdf"

try:
    print(f"Converting {bucket_name}/{object_key} to PDF -> {output_pdf_path}...")
    
    params = build_doc_preview_query_params(dest_type="pdf")
    presigned = client.pre_signed_url(HttpMethodType.Http_Method_Get, bucket_name, object_key, query=params)
    req = Request(presigned.signed_url, headers=presigned.signed_header)
    
    with urlopen(req) as response, open(output_pdf_path, "wb") as f_out:
        f_out.write(response.read())

    print(f"Successfully saved PDF to {output_pdf_path}")
except (HTTPError, URLError, tos.exceptions.TosServerError) as e:
    print(f"Error during PDF conversion: {e}")
```

---

### Workflow 2: Previewing a Specific Page as a PNG Image

**Goal**: Generate a high-quality PNG image of the 5th page of a document.

**Script**: `scripts/doc_preview_png.py`

**Steps**:
1.  Build query parameters, specifying `dest_type="png"`, `page=5`, and optional `image_dpi`.
2.  Generate and use the pre-signed URL to download the image.

**Python Example (`scripts/doc_preview_png.py` logic):**
```python
page_to_preview = 5
output_image_path = f"page_{page_to_preview}.png"

try:
    params = build_doc_preview_query_params(
        dest_type="png",
        page=page_to_preview,
        image_dpi=200
    )
    presigned = client.pre_signed_url(HttpMethodType.Http_Method_Get, bucket_name, object_key, query=params)
    req = Request(presigned.signed_url, headers=presigned.signed_header)
    
    with urlopen(req) as response, open(output_image_path, "wb") as f_out:
        f_out.write(response.read())
        
    print(f"Successfully saved page {page_to_preview} to {output_image_path}")
except Exception as e:
    print(f"Error during PNG conversion: {e}")
```

---

### Workflow 3: Getting the HTML Preview URL

**Goal**: Obtain the final, accessible URL for an HTML-based document preview.

**Script**: `scripts/doc_preview_html_url.py`

**Steps**:
1.  Generate a pre-signed URL with `dest_type="html"`.
2.  Fetch the temporary HTML content from this URL.
3.  Parse the HTML to find the `token` value.
4.  URL-safe Base64 decode the token to get the final preview URL.

**Python Example (`scripts/doc_preview_html_url.py` logic):**
```python
import base64

try:
    params = build_doc_preview_query_params(dest_type="html")
    presigned = client.pre_signed_url(HttpMethodType.Http_Method_Get, bucket_name, object_key, query=params)
    req = Request(presigned.signed_url, headers=presigned.signed_header)

    with urlopen(req) as response:
        html_content = response.read().decode('utf-8')
    
    # ... logic to extract and decode token ...
    # final_url = decode_preview_url(token)
    
    # print(f"Successfully extracted HTML preview URL: {final_url}")
    
except Exception as e:
    print(f"An error occurred while getting HTML preview URL: {e}")
```

---

### Workflow 4: Batch Exporting a Page Range to TOS

**Goal**: Convert pages 1 through 5 of a document into JPG images and save them directly into a destination bucket in TOS.

**Script**: `scripts/doc_preview_process.py`

**Steps**:
1.  Build query parameters with `img_mode=1`, `start_page`, `end_page`, `save_bucket`, and `save_object`.
2.  Generate a pre-signed URL.
3.  Fetch the URL and parse the JSON response for job status.

**Python Example (`scripts/doc_preview_process.py` logic):**
```python
import json

try:
    params = build_doc_preview_query_params(
        dest_type="jpg",
        img_mode=1,
        start_page=1,
        end_page=5,
        save_bucket="my-output-bucket",
        save_object="processed/{Page}.jpg"
    )
    presigned = client.pre_signed_url(HttpMethodType.Http_Method_Get, bucket_name, object_key, query=params)
    req = Request(presigned.signed_url, headers=presigned.signed_header)
    
    with urlopen(req) as response:
        result = json.loads(response.read().decode('utf-8'))
        print("Batch export job details:")
        print(json.dumps(result, indent=2))
        
except Exception as e:
    print(f"Server Error during batch export: {e}")
```

---

### Workflow 5: Reading the Total Page Count Header

**Goal**: Efficiently determine the number of pages in a document.

**Script**: `scripts/doc_total_page.py`

**Steps**:
1.  Generate a pre-signed URL for any preview type (e.g., PDF).
2.  Make a request to the URL.
3.  Access the `headers` of the response object and retrieve `x-tos-total-page`.

**Python Example (`scripts/doc_total_page.py` logic):**
```python
try:
    params = build_doc_preview_query_params(dest_type="pdf")
    presigned = client.pre_signed_url(HttpMethodType.Http_Method_Get, bucket_name, object_key, query=params)
    req = Request(presigned.signed_url, headers=presigned.signed_header)
    
    with urlopen(req) as response:
        total_pages = response.headers.get("x-tos-total-page")
        if total_pages:
            print(f"The document has {total_pages} pages.")
        else:
            print("x-tos-total-page header not found.")
            
except Exception as e:
    print(f"Server Error while querying page count: {e}")
```

---

### Workflow 6: Handling Errors

**Goal**: Gracefully handle common errors during the process.

**Strategy**:
- Wrap pre-signed URL generation in a `try...except` block for `TosServerError` and `TosClientError`.
- Wrap HTTP requests (`urlopen`) in a `try...except` block for `HTTPError` and `URLError`.

**Python Example:**
```python
try:
    # ... build params ...
    presigned = client.pre_signed_url(...)
    req = Request(presigned.signed_url, headers=presigned.signed_header)
    
    with urlopen(req) as response:
        # ... process response ...
        
except tos.exceptions.TosServerError as e:
    print(f"TOS SDK Error: {e.message}")
except HTTPError as e:
    print(f"HTTP Error: Status {e.code}, Reason: {e.reason}")
except URLError as e:
    print(f"URL Error: {e.reason}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
```
This ensures that failures from both the SDK and the subsequent HTTP call are caught and reported.
