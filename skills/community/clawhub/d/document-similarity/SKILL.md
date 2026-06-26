---
name: document-similarity
description: "Compare two images or PDFs for visual similarity via the PDFAPIHub cloud API. Documents are uploaded to pdfapihub.com for comparison using feature matching, SSIM, or perceptual hashing. Requires a CLIENT-API-KEY header."
---

# Document Similarity

## What It Does
Compares two documents (images or PDFs) for visual similarity via the PDFAPIHub hosted API. Both documents are uploaded to PDFAPIHub servers where comparison is performed, and a similarity score (0–1) with confidence level is returned.

## When to Use
- Check if two documents are visually similar
- Detect duplicates or near-duplicates
- Compare image variations

## Comparison Methods
| Method | Description |
|--------|-------------|
| `auto` | Automatically selects best method (default) |
| `feature_match` | OpenCV feature matching |
| `ssim` | Structural Similarity Index |
| `phash` | Perceptual hashing |

## Supported Combinations
- image + image
- pdf + pdf
- image + pdf

## Required Inputs
Two files via one of:
- `url1` + `url2` — public URLs
- `image1_base64` + `image2_base64` — base64-encoded files
- Multipart upload with `file1` and `file2`

## Authentication
This skill calls the PDFAPIHub hosted API at `https://pdfapihub.com/api`. Both documents are uploaded to PDFAPIHub servers for comparison.

Send your API key in the `CLIENT-API-KEY` header.

Get your **free API key** at [https://pdfapihub.com](https://pdfapihub.com). Full API documentation is available at [https://pdfapihub.com/docs](https://pdfapihub.com/docs).

**Privacy note:** Both documents you compare are uploaded to PDFAPIHub's cloud service for processing. Do not send confidential documents unless you trust the service. Files are auto-deleted after 30 days.

## Use Cases
- **Duplicate Detection** — Identify duplicate or near-duplicate documents in a repository
- **Brand Consistency** — Compare generated documents against approved templates for visual consistency
- **QA Testing** — Compare rendered PDFs/images before and after code changes for regressions
- **Fraud Detection** — Compare submitted documents against known genuine samples
- **Document Versioning** — Quantify visual differences between document revisions
- **Container Inspection** — Compare shipping container photos for damage assessment

## Example Usage
```bash
curl -X POST https://pdfapihub.com/api/v1/document/similarity \
  -H "CLIENT-API-KEY: your_api_key" \
  -H "Content-Type: application/json" \
  -d '{
    "url1": "https://pdfapihub.com/sample-document-similarity-1.jpg",
    "url2": "https://pdfapihub.com/sample-document-similarity-2.jpg",
    "method": "auto"
  }'
```
