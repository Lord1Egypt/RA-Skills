# Extract App API

The Extract App API enables structured data extraction from documents using JSON Schema definitions.

## Base Path

```
/extract/apps
```

## App Management

### 1. Create App

Create a new extraction application with a JSON Schema.

**Endpoint:** `POST /extract/apps`

**Request:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | Yes | App name (1-30 characters) |
| `schema` | object | Yes | JSON Schema definition for extraction |

**Schema Format:**

The schema must be a valid JSON Schema with a `schemas` property containing the schema definition.

```json
{
  "schemas": {
    "type": "object",
    "properties": {
      "field_name": {
        "type": "string",
        "description": "Field description",
        "propertyOrder": 0
      }
    }
  }
}
```

**Response:**

| Field | Type | Nullable | Description |
|-------|------|----------|-------------|
| `id` | string | No | App ID |
| `name` | string | No | App name |
| `schema_data` | object | No | JSON Schema definition |

**Status Codes:**

| HTTP Code | Error Code | Description |
|-----------|------------|-------------|
| 201 | - | Success |
| 400 | - | Invalid schema format |

### 2. Get App

Retrieve app details.

**Endpoint:** `GET /extract/apps/{app_id}`

**Path Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `app_id` | string | App ID |

**Response:**

| Field | Type | Nullable | Description |
|-------|------|----------|------------|
| `id` | string | No | App ID |
| `name` | string | No | App name |
| `schema_data` | object | No | JSON Schema definition |

**Status Codes:**

| HTTP Code | Error Code | Description |
|-----------|------------|-------------|
| 200 | - | Success |
| 400 | `not_authorized` | "Unauthorized" |

### 3. Update App

Update app configuration.

**Endpoint:** `PUT /extract/apps/{app_id}`

**Path Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `app_id` | string | App ID |

**Request:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | Yes | App name (1-30 characters) |
| `schema` | object | Yes | JSON Schema definition |

**Response:** Updated app object

| Field | Type | Nullable | Description |
|-------|------|----------|-------------|
| `id` | string | No | App ID |
| `name` | string | No | App name |
| `schema_data` | object | No | JSON Schema definition |

**Status Codes:**

| HTTP Code | Error Code | Description |
|-----------|------------|-------------|
| 200 | - | Success |
| 400 | - | Invalid schema format |
| 400 | `forbid_from_updating` | Cannot update app with active extractions |
| 404 | `not_found` | App not found |

## Document Extraction

### 4. Upload and Extract

Upload a document to the app and trigger extraction.

**Endpoint:** `POST /extract/apps/{app_id}/upload`

**Path Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `app_id` | string | App ID |

**Request:** (multipart/form-data)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `file` | File | Yes | PDF, DOC, or DOCX file |

**Response:**

| Field | Type | Nullable | Description |
|-------|------|----------|-------------|
| `upload_id` | string | No | Upload ID |

**Status Codes:**

| HTTP Code | Error Code | Description |
|-----------|------------|-------------|
| 201 | - | Success (extraction started) |
| 400 | - | Invalid file type |
| 400 | `file_exists` | File already exists in app |
| 404 | `not_found` | App not found |

### 5. Get Extraction Result

Get the extraction results for a processed document.

**Endpoint:** `GET /extract/apps/{app_id}/uploads/{upload_id}/extraction`

**Path Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `app_id` | string | App ID |
| `upload_id` | string | Upload ID |

**Response:**

| Field | Type | Nullable | Description |
|-------|------|----------|-------------|
| `id` | string | No | Extraction ID |
| `upload_id` | string | No |  Upload ID |
| `status` | integer | No | Extraction status (100 = completed, < 0 = error) |
| `data` | object/null | Yes | Extracted data matching schema |
| `detail` | string | Yes | Error detail (only for failed status) |

**Extraction Status Codes:**

| Status | Description |
|--------|-------------|
| 100 | Extraction completed successfully |
| 1 | Preprocessing |
| 2 | Extracting |
| -1 | Parse result error |
| -2 | Extract error |
| -3 | Embedding error |
| -4 | File parse error |
| -5 | Credit insufficient |

**Status Codes:**

| HTTP Code | Error Code | Description |
|-----------|------------|-------------|
| 200 | - | Success |
| 400 | `upload_still_extracting` | Extraction still in progress |
| 404 | `not_found` | App or upload not found |
| 404 | `upload_not_found` | Upload not found |

### 6. Extract Again

Re-extract a document using the app's current schema.

**Endpoint:** `GET /extract/apps/{app_id}/uploads/{upload_id}/extract-again`

**Path Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `app_id` | string | App ID |
| `upload_id` | string | Upload ID |

**Response:** Empty data field on success

**Status Codes:**

| HTTP Code | Error Code | Description |
|-----------|------------|-------------|
| 200 | - | Success (extraction started) |
| 400 | `upload_still_extracting` | Extraction still in progress |
| 404 | `not_found` | App or upload not found |

## Important Notes

1. **Document Status**: Documents need a non-failed status (`status != "failed"`) for upload; the system will automatically trigger parsing if needed
2. **Supported File Types**: PDF, DOC, and DOCX files are supported
3. **Asynchronous Processing**: Extraction is asynchronous; poll the extraction endpoint for results
4. **Schema Validation**: The schema must be a valid JSON Schema; use validation tools before creating the app
5. **Re-extraction**: Use `extract-again` to re-extract with updated schema or for failed extractions
6. **Error Handling**: Check the extraction `status` field; negative values indicate errors (see status codes above)
