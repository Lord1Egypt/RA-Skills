# 360 AI Translation API Reference

## Authentication

All requests require:
```
Authorization: Bearer <API_KEY>
Content-Type: application/json
```

API key is read from env var `TRANSLATE_360_API_KEY`.

## 1. Text Translation

**POST** `https://api.360.cn/v1/translate`

### Request Body (JSON)

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| input | array[string] | Yes | Texts to translate (max 50 per request) |
| tl | string | Yes | Target language code |
| sl | string | No | Source language (auto-detect if omitted) |
| content_filter | bool | No | Content filtering (default true) |
| split_enable | bool | No | Auto-split long text (default false) |

### Response

```json
{ "output": ["translated text"], "code": 0, "id": "..." }
```

Error: `{ "error": { "code": "1001", "message": "..." } }`

## 2. Image Translation

**POST** `https://api.360.cn/v1/images/translate`

### Request Body (JSON)

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| image_format | string | Yes | `url` or `base64` |
| init_image | string | Yes | Image URL or base64 (without data URI prefix) |
| model | string | Yes | Always `360/image-translate` |
| target_lang | string | Yes | Target language code |

### Supported formats
JPG, PNG, WEBP, BMP, GIF (first frame only). Max 10MB.

### Supported languages
zh, en, ja, fr, ru, ko, pt, th, es, it, hi, pl, vi, id

### Response

```json
{
  "code": "0", "message": "success",
  "data": {
    "res": {
      "img_res": ["https://...translated-image.png"],
      "word_res": ["extracted translated text"]
    },
    "size": "597x600",
    "time_cost_ms": 1260
  }
}
```

Image URLs in `img_res` expire in 6 months — download promptly.

## 3. Document Translation (Async)

### Step 1: Upload

**POST** `https://api.360.cn/v1/documents/translate/upload?target_lang=<code>`

- Content-Type: `multipart/form-data`
- Body: `file` field with the document
- `target_lang` query param (optional; defaults to foreign→zh or zh→en)

Supported formats: pdf, doc, docx, xls, xlsx, ppt, pptx, csv, epub, mobi, rtf, html, xhtml, md, txt
Max size: 100MB. Output: PDF only.

Response:
```json
{ "errno": 0, "data": { "taskId": "..." } }
```

### Step 2: Poll Result

**GET** `https://api.360.cn/v1/documents/translate/result?task_id=<taskId>`

Response:
```json
{
  "errno": 0,
  "data": {
    "state": "success",  // "process" | "success" | "fail"
    "output": {
      "progress": 100,
      "data": {
        "s3url": "https://...translated.pdf",
        "pageCount": 10,
        "transPageCount": 10
      }
    }
  }
}
```

## 4. Common Language Codes

| Language | Code | | Language | Code |
|----------|------|-|----------|------|
| Chinese | zh | | English | en |
| Japanese | ja | | Korean | ko |
| French | fr | | German | de |
| Spanish | es | | Portuguese | pt |
| Russian | ru | | Italian | it |
| Thai | th | | Vietnamese | vi |
| Indonesian | id | | Arabic | ar |
| Hindi | hi | | Turkish | tr |
| Polish | pl | | Dutch | nl |
| zh-TW (Traditional) | zh-TW | | zh-HK (Traditional HK) | zh-HK |
| Cantonese | yue | | Tibetan | bo |
| Uyghur | ug | | Mongolian | mn |

Full list: 100+ languages. See API doc for complete codes.

## 5. Pricing

| Service | Unit | Price |
|---------|------|-------|
| Text | per char | ¥30 / 1M chars |
| Image | per image | ¥0.04 / image |
| Document | per page | ¥0.2 / page |

## 6. Error Codes

| HTTP | Code | Description |
|------|------|-------------|
| 400 | 1001 | Bad params |
| 401 | 1002 | Auth failed (invalid key) |
| 401 | 1004 | Insufficient balance |
| 401 | 1006 | Daily limit exceeded |
| 429 | 1005 | Rate limited |
| 500 | 1003 | Server error |
| 500 | 10631 | No text detected in image |
| 500 | 10632 | Detected text needs no translation |
