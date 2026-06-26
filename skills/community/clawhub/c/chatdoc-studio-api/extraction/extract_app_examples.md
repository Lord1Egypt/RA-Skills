# Extract App API - Code Examples

This page contains code examples for the Extract App API in Python, TypeScript (server-side), Rust, and cURL.

## Environment Setup

Set up your environment variables:

```bash
export CHATDOC_STUDIO_BASE_URL="https://api.chatdoc.studio/v1"
export CHATDOC_STUDIO_API_KEY="your-api-key-here"
```

## Create App

### Python

```python
import os
import requests

BASE_URL = os.getenv("CHATDOC_STUDIO_BASE_URL", "https://api.chatdoc.studio/v1")
API_KEY = os.getenv("CHATDOC_STUDIO_API_KEY")

def create_extract_app(name: str, schema: dict) -> dict:
    """Create a new extraction app with JSON schema."""
    url = f"{BASE_URL}/extract/apps"
    headers = {"Authorization": f"Bearer {API_KEY}"}

    data = {
        "name": name,
        "schema": schema,
    }

    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    return response.json()["data"]

# Example: Invoice extraction schema
invoice_schema = {
    "schemas": {
        "type": "object",
        "properties": {
            "Invoice Number": {
                "type": "string",
                "description": "The invoice number",
                "propertyOrder": 0
            },
            "Invoice Date": {
                "type": "string",
                "description": "The date when the invoice was issued",
                "propertyOrder": 1
            },
            "Vendor Name": {
                "type": "string",
                "description": "Name of the vendor or company issuing the invoice",
                "propertyOrder": 2
            },
            "Total Amount": {
                "type": "string",
                "description": "Total amount to be paid",
                "propertyOrder": 3
            },
            "Due Date": {
                "type": "string",
                "description": "Payment due date",
                "propertyOrder": 4
            }
        }
    }
}

app = create_extract_app("Invoice Extractor", invoice_schema)
print(f"App ID: {app['id']}")
```

### TypeScript (Server-side)

```typescript
import axios from 'axios';

const BASE_URL = process.env.CHATDOC_STUDIO_BASE_URL || 'https://api.chatdoc.studio/v1';
const API_KEY = process.env.CHATDOC_STUDIO_API_KEY || '';

interface CreateExtractAppRequest {
  name: string;
  schema: Record<string, any>;
}

interface ExtractAppResponse {
  id: string;
  name: string;
  schema_data: {
    schemas: Record<string, any>;
  };
}

async function createExtractApp(
  name: string,
  schema: CreateExtractAppRequest['schema']
): Promise<ExtractAppResponse> {
  const response = await axios.post<{ data: ExtractAppResponse }>(
    `${BASE_URL}/extract/apps`,
    { name, schema },
    {
      headers: {
        Authorization: `Bearer ${API_KEY}`,
      },
    }
  );
  return response.data.data;
}

// Example: Invoice extraction schema
const invoiceSchema = {
  schemas: {
    type: 'object',
    properties: {
      'Invoice Number': {
        type: 'string',
        description: 'The invoice number',
        propertyOrder: 0,
      },
      'Invoice Date': {
        type: 'string',
        description: 'The date when the invoice was issued',
        propertyOrder: 1,
      },
      'Vendor Name': {
        type: 'string',
        description: 'Name of the vendor or company issuing the invoice',
        propertyOrder: 2,
      },
      'Total Amount': {
        type: 'string',
        description: 'Total amount to be paid',
        propertyOrder: 3,
      },
      'Due Date': {
        type: 'string',
        description: 'Payment due date',
        propertyOrder: 4,
      },
    },
  },
};

const app = await createExtractApp('Invoice Extractor', invoiceSchema);
console.log(`App ID: ${app.id}`);
```

### Rust

```rust
use reqwest::Client;
use serde::{Deserialize, Serialize};

const BASE_URL: &str = "https://api.chatdoc.studio/v1";

#[derive(Debug, Deserialize)]
struct ExtractAppResponse {
    id: String,
    name: String,
    schema_data: serde_json::Value,
}

#[derive(Debug, Deserialize)]
struct ApiResponse<T> {
    data: T,
}

#[derive(Debug, Serialize)]
struct CreateExtractAppRequest<'a> {
    name: &'a str,
    schema: serde_json::Value,
}

async fn create_extract_app(
    name: &str,
    schema: serde_json::Value,
) -> Result<ExtractAppResponse, Box<dyn std::error::Error>> {
    let api_key = std::env::var("CHATDOC_STUDIO_API_KEY")?;
    let client = Client::new();

    let request = CreateExtractAppRequest {
        name,
        schema,
    };

    let response = client
        .post(&format!("{}/extract/apps", BASE_URL))
        .header("Authorization", format!("Bearer {}", api_key))
        .json(&request)
        .send()
        .await?;

    let api_response: ApiResponse<ExtractAppResponse> = response.json().await?;
    Ok(api_response.data)
}
```

### cURL

```bash
curl -X POST "${CHATDOC_STUDIO_BASE_URL}/extract/apps" \
  -H "Authorization: Bearer ${CHATDOC_STUDIO_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Invoice Extractor",
    "schema": {
      "schemas": {
        "type": "object",
        "properties": {
          "Invoice Number": {
            "type": "string",
            "description": "The invoice number",
            "propertyOrder": 0
          },
          "Invoice Date": {
            "type": "string",
            "description": "The date when the invoice was issued",
            "propertyOrder": 1
          },
          "Vendor Name": {
            "type": "string",
            "description": "Name of the vendor or company issuing the invoice",
            "propertyOrder": 2
          },
          "Total Amount": {
            "type": "string",
            "description": "Total amount to be paid",
            "propertyOrder": 3
          },
          "Due Date": {
            "type": "string",
            "description": "Payment due date",
            "propertyOrder": 4
          }
        }
      }
    }
  }'
```

## Get App

### Python

```python
def get_extract_app(app_id: str) -> dict:
    """Get app details."""
    url = f"{BASE_URL}/extract/apps/{app_id}"
    headers = {"Authorization": f"Bearer {API_KEY}"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()["data"]

# Usage
app = get_extract_app("abc123")
print(f"App: {app['name']}")
print(f"Schema: {app['schema_data']}")
```

### TypeScript

```typescript
async function getExtractApp(appId: string): Promise<ExtractAppResponse> {
  const response = await axios.get<{ data: ExtractAppResponse }>(
    `${BASE_URL}/extract/apps/${appId}`,
    {
      headers: {
        Authorization: `Bearer ${API_KEY}`,
      },
    }
  );
  return response.data.data;
}

// Usage
const app = await getExtractApp('abc123');
console.log(`App: ${app.name}`);
console.log(`Schema:`, app.schema_data);
```

### cURL

```bash
curl -X GET "${CHATDOC_STUDIO_BASE_URL}/extract/apps/abc123" \
  -H "Authorization: Bearer ${CHATDOC_STUDIO_API_KEY}"
```

## Update App

### Python

```python
def update_extract_app(app_id: str, name: str, schema: dict) -> dict:
    """Update extraction app configuration."""
    url = f"{BASE_URL}/extract/apps/{app_id}"
    headers = {"Authorization": f"Bearer {API_KEY}"}

    data = {
        "name": name,
        "schema": schema,
    }

    response = requests.put(url, headers=headers, json=data)
    response.raise_for_status()
    return response.json()["data"]

# Usage
updated_app = update_extract_app("abc123", "Updated Invoice Extractor", invoice_schema)
print(f"Updated App ID: {updated_app['id']}")
print(f"Updated App Name: {updated_app['name']}")
```

### TypeScript

```typescript
async function updateExtractApp(
  appId: string,
  name: string,
  schema: CreateExtractAppRequest['schema']
): Promise<ExtractAppResponse> {
  const response = await axios.put<{ data: ExtractAppResponse }>(
    `${BASE_URL}/extract/apps/${appId}`,
    { name, schema },
    {
      headers: {
        Authorization: `Bearer ${API_KEY}`,
      },
    }
  );
  return response.data.data;
}

// Usage
const updatedApp = await updateExtractApp('abc123', 'Updated Invoice Extractor', invoiceSchema);
console.log(`Updated App ID: ${updatedApp.id}`);
console.log(`Updated App Name: ${updatedApp.name}`);
```

### Rust

```rust
use reqwest::Client;
use serde::{Deserialize, Serialize};

const BASE_URL: &str = "https://api.chatdoc.studio/v1";

#[derive(Debug, Deserialize)]
struct ExtractAppResponse {
    id: String,
    name: String,
    schema_data: serde_json::Value,
}

#[derive(Debug, Deserialize)]
struct ApiResponse<T> {
    data: T,
}

#[derive(Debug, Serialize)]
struct UpdateExtractAppRequest<'a> {
    name: &'a str,
    schema: serde_json::Value,
}

async fn update_extract_app(
    app_id: &str,
    name: &str,
    schema: serde_json::Value,
) -> Result<ExtractAppResponse, Box<dyn std::error::Error>> {
    let api_key = std::env::var("CHATDOC_STUDIO_API_KEY")?;
    let client = Client::new();

    let request = UpdateExtractAppRequest { name, schema };

    let response = client
        .put(&format!("{}/extract/apps/{}", BASE_URL, app_id))
        .header("Authorization", format!("Bearer {}", api_key))
        .json(&request)
        .send()
        .await?;

    let api_response: ApiResponse<ExtractAppResponse> = response.json().await?;
    Ok(api_response.data)
}
```

### cURL

```bash
curl -X PUT "${CHATDOC_STUDIO_BASE_URL}/extract/apps/abc123" \
  -H "Authorization: Bearer ${CHATDOC_STUDIO_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Updated Invoice Extractor",
    "schema": {
      "schemas": {
        "type": "object",
        "properties": {
          "Invoice Number": {
            "type": "string",
            "description": "The invoice number",
            "propertyOrder": 0
          },
          "Invoice Date": {
            "type": "string",
            "description": "The date when the invoice was issued",
            "propertyOrder": 1
          },
          "Vendor Name": {
            "type": "string",
            "description": "Name of the vendor or company issuing the invoice",
            "propertyOrder": 2
          },
          "Total Amount": {
            "type": "string",
            "description": "Total amount to be paid",
            "propertyOrder": 3
          },
          "Due Date": {
            "type": "string",
            "description": "Payment due date",
            "propertyOrder": 4
          }
        }
      }
    }
  }'
```

## Upload and Extract

### Python

```python
def upload_and_extract(app_id: str, file_path: str) -> str:
    """Upload a file and trigger extraction."""
    url = f"{BASE_URL}/extract/apps/{app_id}/upload"
    headers = {"Authorization": f"Bearer {API_KEY}"}

    with open(file_path, "rb") as f:
        files = {"file": f}
        response = requests.post(url, headers=headers, files=files)
        response.raise_for_status()
        return response.json()["data"]["upload_id"]

# Usage
upload_id = upload_and_extract("abc123", "invoice.pdf")
print(f"Upload ID: {upload_id}")
```

### TypeScript

```typescript
import fs from 'fs';
import FormData from 'form-data';
import axios from 'axios';

async function uploadAndExtract(
  appId: string,
  filePath: string
): Promise<string> {
  const form = new FormData();
  form.append('file', fs.createReadStream(filePath));

  const response = await axios.post<{ data: { upload_id: string } }>(
    `${BASE_URL}/extract/apps/${appId}/upload`,
    form,
    {
      headers: {
        ...form.getHeaders(),
        Authorization: `Bearer ${API_KEY}`,
      },
    }
  );

  return response.data.data.upload_id;
}

// Usage
const uploadId = await uploadAndExtract('abc123', 'invoice.pdf');
console.log(`Upload ID: ${uploadId}`);
```

### Rust

```rust
use reqwest::multipart::{Form, Part};
use reqwest::Client;
use serde::Deserialize;

const BASE_URL: &str = "https://api.chatdoc.studio/v1";

#[derive(Debug, Deserialize)]
struct UploadData {
    upload_id: String,
}

#[derive(Debug, Deserialize)]
struct ApiResponse<T> {
    data: T,
}

async fn upload_and_extract(
    app_id: &str,
    file_path: &str,
) -> Result<String, Box<dyn std::error::Error>> {
    let api_key = std::env::var("CHATDOC_STUDIO_API_KEY")?;
    let client = Client::new();

    let file_bytes = std::fs::read(file_path)?;
    let mime = match std::path::Path::new(file_path)
        .extension()
        .and_then(|ext| ext.to_str())
        .map(|ext| ext.to_lowercase())
        .as_deref()
    {
        Some("pdf") => "application/pdf",
        Some("doc") => "application/msword",
        Some("docx") => "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        _ => "application/octet-stream",
    };

    let file_part = Part::bytes(file_bytes)
        .file_name(std::path::Path::new(file_path).file_name().unwrap().to_string_lossy().to_string())
        .mime_str(mime)?;

    let form = Form::new().part("file", file_part);

    let response = client
        .post(&format!("{}/extract/apps/{}/upload", BASE_URL, app_id))
        .header("Authorization", format!("Bearer {}", api_key))
        .multipart(form)
        .send()
        .await?;

    let api_response: ApiResponse<UploadData> = response.json().await?;
    Ok(api_response.data.upload_id)
}
```

### cURL

```bash
curl -X POST "${CHATDOC_STUDIO_BASE_URL}/extract/apps/abc123/upload" \
  -H "Authorization: Bearer ${CHATDOC_STUDIO_API_KEY}" \
  -F "file=@invoice.pdf"
```

## Get Extraction Result

### Python

```python
import time

def get_extraction_result(app_id: str, upload_id: str, wait: bool = True) -> dict:
    """Get extraction result, optionally waiting for completion."""
    url = f"{BASE_URL}/extract/apps/{app_id}/uploads/{upload_id}/extraction"
    headers = {"Authorization": f"Bearer {API_KEY}"}

    if wait:
        while True:
            response = requests.get(url, headers=headers)

            if response.status_code == 400:
                error_data = response.json()
                if error_data.get("code") == "upload_still_extracting":
                    # Still processing, wait and retry
                    print("Still extracting, waiting...")
                    time.sleep(3)
                    continue
                else:
                    response.raise_for_status()

            # Extraction completed
            response.raise_for_status()
            result = response.json()["data"]

            if result["status"] < 0:
                # Extraction failed
                raise Exception(f"Extraction failed: {result.get('detail', 'Unknown error')}")
            return result
    else:
        response = requests.get(url, headers=headers)

        if response.status_code == 400:
            error_data = response.json()
            if error_data.get("code") == "upload_still_extracting":
                raise Exception("Extraction still in progress")

        response.raise_for_status()
        return response.json()["data"]

# Usage - wait for completion
result = get_extraction_result("abc123", "F1CMSW", wait=True)
print(f"Extracted data: {result['data']}")

# Usage - single check
try:
    result = get_extraction_result("abc123", "F1CMSW", wait=False)
    if result["status"] == 100:
        print(f"Extracted data: {result['data']}")
    elif result["status"] < 0:
        print(f"Error: {result.get('detail', 'Unknown error')}")
except Exception as e:
    if "still in progress" in str(e):
        print("Still processing...")
    else:
        raise
```

### TypeScript

```typescript
interface ExtractionResult {
  id: string;
  upload_id: string;
  status: number;
  data: Record<string, any> | null;
  detail: string | null;
}

interface ApiErrorResponse {
  code: string;
  detail?: string;
}

async function getExtractionResult(
  appId: string,
  uploadId: string,
  wait = true
): Promise<ExtractionResult> {
  const url = `${BASE_URL}/extract/apps/${appId}/uploads/${uploadId}/extraction`;

  if (wait) {
    while (true) {
      try {
        const response = await axios.get<{ data: ExtractionResult }>(url, {
          headers: {
            Authorization: `Bearer ${API_KEY}`,
          },
        });
        const result = response.data.data;

        if (result.status < 0) {
          throw new Error(result.detail || 'Unknown error');
        }
        return result;
      } catch (error) {
        if (axios.isAxiosError(error) && error.response?.status === 400) {
          const errorData = error.response.data as ApiErrorResponse;
          if (errorData.code === 'upload_still_extracting') {
            console.log('Still extracting, waiting...');
            await new Promise(resolve => setTimeout(resolve, 3000));
            continue;
          }
        }
        throw error;
      }
    }
  } else {
    try {
      const response = await axios.get<{ data: ExtractionResult }>(url, {
        headers: {
          Authorization: `Bearer ${API_KEY}`,
        },
      });
      return response.data.data;
    } catch (error) {
      if (axios.isAxiosError(error) && error.response?.status === 400) {
        const errorData = error.response.data as ApiErrorResponse;
        if (errorData.code === 'upload_still_extracting') {
          throw new Error('Extraction still in progress');
        }
      }
      throw error;
    }
  }
}

// Usage - wait for completion
const result = await getExtractionResult('abc123', 'F1CMSW', true);
console.log('Extracted data:', result.data);

// Usage - single check
try {
  const result2 = await getExtractionResult('abc123', 'F1CMSW', false);
  if (result2.status === 100) {
    console.log('Extracted data:', result2.data);
  } else if (result2.status < 0) {
    console.log('Error:', result2.detail);
  }
} catch (error) {
  if (error instanceof Error && error.message === 'Extraction still in progress') {
    console.log('Still processing...');
  } else {
    throw error;
  }
}
```

### Rust

```rust
use reqwest::Client;
use serde::Deserialize;
use std::time::Duration;
use tokio::time::sleep;

const BASE_URL: &str = "https://api.chatdoc.studio/v1";

#[derive(Debug, Deserialize)]
struct ExtractionResult {
    id: String,
    upload_id: String,
    status: i32,
    data: Option<serde_json::Value>,
    detail: Option<String>,
}

#[derive(Debug, Deserialize)]
struct ApiErrorResponse {
    code: String,
    detail: Option<String>,
}

#[derive(Debug, Deserialize)]
struct ApiResponse<T> {
    data: T,
}

async fn get_extraction_result(
    app_id: &str,
    upload_id: &str,
    wait: bool,
) -> Result<ExtractionResult, Box<dyn std::error::Error>> {
    let api_key = std::env::var("CHATDOC_STUDIO_API_KEY")?;
    let client = Client::new();
    let url = format!("{}/extract/apps/{}/uploads/{}/extraction", BASE_URL, app_id, upload_id);

    if wait {
        loop {
            let response = client
                .get(&url)
                .header("Authorization", format!("Bearer {}", api_key))
                .send()
                .await?;

            if response.status() == 400 {
                let error_data: ApiErrorResponse = response.json().await?;
                if error_data.code == "upload_still_extracting" {
                    println!("Still extracting, waiting...");
                    sleep(Duration::from_secs(3)).await;
                    continue;
                }
                return Err(
                    format!(
                        "Failed to get extraction result: {} ({})",
                        error_data.code,
                        error_data.detail.unwrap_or_else(|| "Unknown error".to_string())
                    )
                    .into(),
                );
            }

            if !response.status().is_success() {
                return Err(format!("Request failed with status: {}", response.status()).into());
            }

            let result: ApiResponse<ExtractionResult> = response.json().await?;

            if result.data.status < 0 {
                return Err(format!(
                    "Extraction failed: {}",
                    result.data.detail.unwrap_or_else(|| "Unknown error".to_string())
                )
                .into());
            }
            return Ok(result.data);
        }
    } else {
        let response = client
            .get(&url)
            .header("Authorization", format!("Bearer {}", api_key))
            .send()
            .await?;

        if response.status() == 400 {
            let error_data: ApiErrorResponse = response.json().await?;
            if error_data.code == "upload_still_extracting" {
                return Err("Extraction still in progress".into());
            }
            return Err(
                format!(
                    "Failed to get extraction result: {} ({})",
                    error_data.code,
                    error_data.detail.unwrap_or_else(|| "Unknown error".to_string())
                )
                .into(),
            );
        }

        if !response.status().is_success() {
            return Err(format!("Request failed with status: {}", response.status()).into());
        }

        let api_response: ApiResponse<ExtractionResult> = response.json().await?;
        Ok(api_response.data)
    }
}
```

### cURL

```bash
# Check extraction result
curl -X GET "${CHATDOC_STUDIO_BASE_URL}/extract/apps/abc123/uploads/F1CMSW/extraction" \
  -H "Authorization: Bearer ${CHATDOC_STUDIO_API_KEY}"

# Response example:
# {
#   "data": {
#     "id": "xxx",
#     "upload_id": "F1CMSW",
#     "status": 100,
#     "data": {
#       "Invoice Number": "INV-2024-001",
#       "Invoice Date": "2024-01-15",
#       "Vendor Name": "Acme Corp",
#       "Total Amount": "$1,234.56",
#       "Due Date": "2024-02-15"
#     }
#   }
# }
```

## Extract Again

### Python

```python
def extract_again(app_id: str, upload_id: str) -> None:
    """Re-extract a document using the current app schema."""
    url = f"{BASE_URL}/extract/apps/{app_id}/uploads/{upload_id}/extract-again"
    headers = {"Authorization": f"Bearer {API_KEY}"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()

# Usage
extract_again("abc123", "F1CMSW")
print("Re-extraction triggered")
```

### TypeScript

```typescript
async function extractAgain(appId: string, uploadId: string): Promise<void> {
  await axios.get(
    `${BASE_URL}/extract/apps/${appId}/uploads/${uploadId}/extract-again`,
    {
      headers: {
        Authorization: `Bearer ${API_KEY}`,
      },
    }
  );
}

// Usage
await extractAgain('abc123', 'F1CMSW');
console.log('Re-extraction triggered');
```

### cURL

```bash
curl -X GET "${CHATDOC_STUDIO_BASE_URL}/extract/apps/abc123/uploads/F1CMSW/extract-again" \
  -H "Authorization: Bearer ${CHATDOC_STUDIO_API_KEY}"
```

## Complete Workflow Example

### Python

```python
# Complete workflow for extraction

# 1. Create the app
app = create_extract_app("Invoice Extractor", invoice_schema)
app_id = app["id"]
print(f"Created app: {app_id}")

# 2. Upload file and trigger extraction
upload_id = upload_and_extract(app_id, "invoice.pdf")
print(f"Upload ID: {upload_id}")

# 3. Wait for extraction to complete
result = get_extraction_result(app_id, upload_id, wait=True)
print("Extraction complete!")
print("Extracted data:")
for key, value in result["data"].items():
    print(f"  {key}: {value}")
```

### TypeScript

```typescript
// Complete workflow for extraction

async function completeWorkflow() {
  // 1. Create the app
  const app = await createExtractApp('Invoice Extractor', invoiceSchema);
  const appId = app.id;
  console.log(`Created app: ${appId}`);

  // 2. Upload file and trigger extraction
  const uploadId = await uploadAndExtract(appId, 'invoice.pdf');
  console.log(`Upload ID: ${uploadId}`);

  // 3. Wait for extraction to complete
  const result = await getExtractionResult(appId, uploadId, true);
  console.log('Extraction complete!');
  console.log('Extracted data:');
  for (const [key, value] of Object.entries(result.data || {})) {
    console.log(`  ${key}: ${value}`);
  }
}

completeWorkflow();
```
