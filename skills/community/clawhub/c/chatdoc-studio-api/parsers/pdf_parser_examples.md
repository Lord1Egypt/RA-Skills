# PDF Parser API - Code Examples

This page contains code examples for the PDF Parser API in Python, TypeScript (server-side), Rust, and cURL.

## Environment Setup

Set up your environment variables:

```bash
export CHATDOC_STUDIO_BASE_URL="https://api.chatdoc.studio/v1"
export CHATDOC_STUDIO_API_KEY="your-api-key-here"
```

## Upload PDF

### Python

```python
import os
import requests

BASE_URL = os.getenv("CHATDOC_STUDIO_BASE_URL", "https://api.chatdoc.studio/v1")
API_KEY = os.getenv("CHATDOC_STUDIO_API_KEY")

def upload_pdf(file_path: str, wait: bool = False) -> dict:
    """Upload a PDF file for parsing."""
    url = f"{BASE_URL}/pdf/parser/upload"
    headers = {"Authorization": f"Bearer {API_KEY}"}

    with open(file_path, "rb") as f:
        files = {"file": f}
        data = {"wait": str(wait).lower()}
        response = requests.post(url, headers=headers, files=files, data=data)
        response.raise_for_status()
        return response.json()["data"]

# Usage
result = upload_pdf("document.pdf")
print(
    f"Upload ID: {result['upload_id']}, "
    f"Type: {result['file_type']}, "
    f"Status: {result['status']}, "
    f"Created At: {result['created_at']}"
)
```

### TypeScript (Server-side)

```typescript
// npm i axios form-data
import * as fs from 'node:fs';
import FormData from 'form-data';
import axios from 'axios';

const BASE_URL = process.env.CHATDOC_STUDIO_BASE_URL || 'https://api.chatdoc.studio/v1';
const API_KEY = process.env.CHATDOC_STUDIO_API_KEY || '';

interface UploadResponse {
  data: {
    created_at: number;
    file_type: string;
    upload_id: string;
    name: string;
    status: string;
    markdown: string;
  };
}

async function uploadPDF(
  filePath: string,
  wait: boolean = false
): Promise<UploadResponse['data']> {
  const form = new FormData();
  form.append('file', fs.createReadStream(filePath));
  form.append('wait', wait.toString());

  const response = await axios.post<UploadResponse>(
    `${BASE_URL}/pdf/parser/upload`,
    form,
    {
      headers: {
        ...form.getHeaders(),
        Authorization: `Bearer ${API_KEY}`,
      },
    }
  );

  return response.data.data;
}

// Usage
async function main(): Promise<void> {
  const result = await uploadPDF('document.pdf');
  console.log(
    `Upload ID: ${result.upload_id}, Type: ${result.file_type}, Status: ${result.status}, Created At: ${result.created_at}`
  );
}

main().catch(console.error);
```

### Rust

```rust
use std::env;
use reqwest::multipart::{Form, Part};
use reqwest::Client;
use serde::Deserialize;

const BASE_URL: &str = "https://api.chatdoc.studio/v1";

#[derive(Debug, Deserialize)]
struct UploadData {
    created_at: i64,
    file_type: String,
    upload_id: String,
    name: String,
    status: String,
    markdown: String,
}

#[derive(Debug, Deserialize)]
struct ApiResponse<T> {
    data: T,
}

async fn upload_pdf(
    file_path: &str,
    wait: bool,
) -> Result<UploadData, Box<dyn std::error::Error>> {
    let api_key = env::var("CHATDOC_STUDIO_API_KEY")?;

    let client = Client::new();
    let file_bytes = std::fs::read(file_path)?;
    let file_part = Part::bytes(file_bytes)
        .file_name(std::path::Path::new(file_path).file_name().unwrap().to_string_lossy().to_string())
        .mime_str("application/pdf")?;

    let form = Form::new()
        .part("file", file_part)
        .text("wait", wait.to_string());

    let response = client
        .post(&format!("{}/pdf/parser/upload", BASE_URL))
        .header("Authorization", format!("Bearer {}", api_key))
        .multipart(form)
        .send()
        .await?;

    let api_response: ApiResponse<UploadData> = response.json().await?;
    Ok(api_response.data)
}

// Usage
#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let result = upload_pdf("document.pdf", false).await?;
    println!(
        "Upload ID: {}, Type: {}, Status: {}, Created At: {}",
        result.upload_id, result.file_type, result.status, result.created_at
    );
    Ok(())
}
```

### cURL

```bash
curl -X POST "${CHATDOC_STUDIO_BASE_URL}/pdf/parser/upload" \
  -H "Authorization: Bearer ${CHATDOC_STUDIO_API_KEY}" \
  -F "file=@document.pdf" \
  -F "wait=false"
```

## Get JSON

### Python

```python
import os
import time
import requests

BASE_URL = os.getenv("CHATDOC_STUDIO_BASE_URL", "https://api.chatdoc.studio/v1")
API_KEY = os.getenv("CHATDOC_STUDIO_API_KEY")

def get_pdf_json(upload_id: str, wait: bool = True) -> dict:
    """Get parsed PDF as JSON."""
    url = f"{BASE_URL}/pdf/parser/{upload_id}/json"
    headers = {"Authorization": f"Bearer {API_KEY}"}

    if wait:
        while True:
            response = requests.get(url, headers=headers)

            if response.status_code == 400:
                error_data = response.json()
                if error_data.get("code") == "not_parsed":
                    print("Still parsing, waiting...")
                    time.sleep(3)
                    continue
                else:
                    response.raise_for_status()

            response.raise_for_status()
            return response.json()["data"]
    else:
        response = requests.get(url, headers=headers)

        if response.status_code == 400:
            error_data = response.json()
            if error_data.get("code") == "not_parsed":
                raise Exception("Document parsing not completed")

        response.raise_for_status()
        return response.json()["data"]

# Usage - wait for completion
data = get_pdf_json("F1CMSW", wait=True)
print(f"Document: {data['document']['name']}")
print(f"Elements: {len(data['elements'])}")
```

### TypeScript

```typescript
import axios from 'axios';

const BASE_URL = process.env.CHATDOC_STUDIO_BASE_URL || 'https://api.chatdoc.studio/v1';
const API_KEY = process.env.CHATDOC_STUDIO_API_KEY || '';

interface Element {
  type: string;
  content: any;
  page: number[];
  index: number;
}

interface JsonResponse {
  document: {
    id: string;
    name: string;
    create_time: number;
  };
  elements: Element[];
}

interface ApiErrorResponse {
  code: string;
  detail?: string;
}

async function getPdfJson(uploadId: string, wait = true): Promise<JsonResponse> {
  const url = `${BASE_URL}/pdf/parser/${uploadId}/json`;

  if (wait) {
    while (true) {
      try {
        const response = await axios.get<{ data: JsonResponse }>(url, {
          headers: {
            Authorization: `Bearer ${API_KEY}`,
          },
        });
        return response.data.data;
      } catch (error) {
        if (axios.isAxiosError(error) && error.response?.status === 400) {
          const errorData = error.response.data as ApiErrorResponse;
          if (errorData.code === 'not_parsed') {
            console.log('Still parsing, waiting...');
            await new Promise(resolve => setTimeout(resolve, 3000));
            continue;
          }
        }
        throw error;
      }
    }
  } else {
    try {
      const response = await axios.get<{ data: JsonResponse }>(url, {
        headers: {
          Authorization: `Bearer ${API_KEY}`,
        },
      });
      return response.data.data;
    } catch (error) {
      if (axios.isAxiosError(error) && error.response?.status === 400) {
        const errorData = error.response.data as ApiErrorResponse;
        if (errorData.code === 'not_parsed') {
          throw new Error('Document parsing not completed');
        }
      }
      throw error;
    }
  }
}

// Usage - wait for completion
async function main(): Promise<void> {
  const data = await getPdfJson('F1CMSW', true);
  console.log(`Document: ${data.document.name}`);
  console.log(`Elements: ${data.elements.length}`);
}

main().catch(console.error);
```

### Rust

```rust
use reqwest::{Client, StatusCode};
use serde::Deserialize;
use std::time::Duration;
use tokio::time::sleep;

const BASE_URL: &str = "https://api.chatdoc.studio/v1";

#[derive(Debug, Deserialize)]
struct Document {
    id: String,
    name: String,
    create_time: i64,
}

#[derive(Debug, Deserialize)]
struct Element {
    #[serde(rename = "type")]
    element_type: String,
    content: serde_json::Value,
    page: Vec<i32>,
    index: i32,
}

#[derive(Debug, Deserialize)]
struct JsonResponse {
    document: Document,
    elements: Vec<Element>,
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

async fn get_pdf_json(upload_id: &str, wait: bool) -> Result<JsonResponse, Box<dyn std::error::Error>> {
    let api_key = std::env::var("CHATDOC_STUDIO_API_KEY")?;
    let client = Client::new();
    let url = format!("{}/pdf/parser/{}/json", BASE_URL, upload_id);

    if wait {
        loop {
            let response = client
                .get(&url)
                .header("Authorization", format!("Bearer {}", api_key))
                .send()
                .await?;

            if response.status() == StatusCode::BAD_REQUEST {
                let error_data: ApiErrorResponse = response.json().await?;
                if error_data.code == "not_parsed" {
                    println!("Still parsing, waiting...");
                    sleep(Duration::from_secs(3)).await;
                    continue;
                }
                return Err(
                    format!(
                        "Failed to get PDF JSON: {} ({})",
                        error_data.code,
                        error_data.detail.unwrap_or_else(|| "Unknown error".to_string())
                    )
                    .into(),
                );
            }

            if !response.status().is_success() {
                return Err(format!("Request failed with status: {}", response.status()).into());
            }

            let api_response: ApiResponse<JsonResponse> = response.json().await?;
            return Ok(api_response.data);
        }
    } else {
        let response = client
            .get(&url)
            .header("Authorization", format!("Bearer {}", api_key))
            .send()
            .await?;

        if response.status() == StatusCode::BAD_REQUEST {
            let error_data: ApiErrorResponse = response.json().await?;
            if error_data.code == "not_parsed" {
                return Err("Document parsing not completed".into());
            }
            return Err(
                format!(
                    "Failed to get PDF JSON: {} ({})",
                    error_data.code,
                    error_data.detail.unwrap_or_else(|| "Unknown error".to_string())
                )
                .into(),
            );
        }

        if !response.status().is_success() {
            return Err(format!("Request failed with status: {}", response.status()).into());
        }

        let api_response: ApiResponse<JsonResponse> = response.json().await?;
        Ok(api_response.data)
    }
}
```

### cURL

```bash
curl -X GET "${CHATDOC_STUDIO_BASE_URL}/pdf/parser/F1CMSW/json" \
  -H "Authorization: Bearer ${CHATDOC_STUDIO_API_KEY}"
```

## Get Markdown

### Python

```python
import os
import time
import requests

BASE_URL = os.getenv("CHATDOC_STUDIO_BASE_URL", "https://api.chatdoc.studio/v1")
API_KEY = os.getenv("CHATDOC_STUDIO_API_KEY")

def get_pdf_markdown(upload_id: str, output_path: str, wait: bool = True) -> None:
    """Download parsed PDF as Markdown file."""
    url = f"{BASE_URL}/pdf/parser/{upload_id}/markdown"
    headers = {"Authorization": f"Bearer {API_KEY}"}

    if wait:
        while True:
            response = requests.get(url, headers=headers)

            if response.status_code == 400:
                error_data = response.json()
                if error_data.get("code") == "not_parsed":
                    print("Still parsing, waiting...")
                    time.sleep(3)
                    continue
                else:
                    response.raise_for_status()

            response.raise_for_status()
            break

        with open(output_path, 'wb') as f:
            f.write(response.content)
    else:
        response = requests.get(url, headers=headers)

        if response.status_code == 400:
            error_data = response.json()
            if error_data.get("code") == "not_parsed":
                raise Exception("Document parsing not completed")

        response.raise_for_status()
        with open(output_path, 'wb') as f:
            f.write(response.content)

# Usage - wait for completion
get_pdf_markdown("F1CMSW", "output.md", wait=True)
```

### TypeScript

```typescript
import axios from 'axios';
import { Buffer } from 'node:buffer';
import * as fs from 'node:fs';

const BASE_URL = process.env.CHATDOC_STUDIO_BASE_URL || 'https://api.chatdoc.studio/v1';
const API_KEY = process.env.CHATDOC_STUDIO_API_KEY || '';

interface ApiErrorResponse {
  code: string;
  detail?: string;
}

function parseAxiosApiError(data: unknown): ApiErrorResponse | null {
  if (!data) return null;

  if (typeof data === 'object' && 'code' in (data as Record<string, unknown>)) {
    return data as ApiErrorResponse;
  }

  try {
    const text = Buffer.from(data as ArrayBuffer).toString('utf-8');
    return JSON.parse(text) as ApiErrorResponse;
  } catch {
    return null;
  }
}

async function getPdfMarkdown(uploadId: string, outputPath: string, wait = true): Promise<void> {
  const url = `${BASE_URL}/pdf/parser/${uploadId}/markdown`;

  if (wait) {
    while (true) {
      try {
        const response = await axios.get(url, {
          headers: {
            Authorization: `Bearer ${API_KEY}`,
          },
          responseType: 'arraybuffer',
        });
        fs.writeFileSync(outputPath, response.data);
        return;
      } catch (error) {
        if (axios.isAxiosError(error) && error.response?.status === 400) {
          const errorData = parseAxiosApiError(error.response.data);
          if (errorData?.code === 'not_parsed') {
            console.log('Still parsing, waiting...');
            await new Promise(resolve => setTimeout(resolve, 3000));
            continue;
          }
        }
        throw error;
      }
    }
  } else {
    try {
      const response = await axios.get(url, {
        headers: {
          Authorization: `Bearer ${API_KEY}`,
        },
        responseType: 'arraybuffer',
      });
      fs.writeFileSync(outputPath, response.data);
    } catch (error) {
      if (axios.isAxiosError(error) && error.response?.status === 400) {
        const errorData = parseAxiosApiError(error.response.data);
        if (errorData?.code === 'not_parsed') {
          throw new Error('Document parsing not completed');
        }
      }
      throw error;
    }
  }
}

// Usage - wait for completion
async function main(): Promise<void> {
  await getPdfMarkdown('F1CMSW', 'output.md', true);
}

main().catch(console.error);
```

### cURL

```bash
curl -X GET "${CHATDOC_STUDIO_BASE_URL}/pdf/parser/F1CMSW/markdown" \
  -H "Authorization: Bearer ${CHATDOC_STUDIO_API_KEY}" \
  -o output.md
```

## Get Excel

### Python

```python
import os
import time
import requests

BASE_URL = os.getenv("CHATDOC_STUDIO_BASE_URL", "https://api.chatdoc.studio/v1")
API_KEY = os.getenv("CHATDOC_STUDIO_API_KEY")

def get_pdf_excel(upload_id: str, output_path: str, wait: bool = True) -> None:
    """Download parsed PDF as Excel file (tables only)."""
    url = f"{BASE_URL}/pdf/parser/{upload_id}/excel"
    headers = {"Authorization": f"Bearer {API_KEY}"}

    if wait:
        while True:
            response = requests.get(url, headers=headers)

            if response.status_code == 400:
                error_data = response.json()
                if error_data.get("code") == "not_parsed":
                    print("Still parsing, waiting...")
                    time.sleep(3)
                    continue
                else:
                    response.raise_for_status()

            response.raise_for_status()
            break

        with open(output_path, 'wb') as f:
            f.write(response.content)
    else:
        response = requests.get(url, headers=headers)

        if response.status_code == 400:
            error_data = response.json()
            if error_data.get("code") == "not_parsed":
                raise Exception("Document parsing not completed")

        response.raise_for_status()
        with open(output_path, 'wb') as f:
            f.write(response.content)

# Usage - wait for completion
get_pdf_excel("F1CMSW", "output.xlsx", wait=True)
```

### TypeScript

```typescript
import axios from 'axios';
import { Buffer } from 'node:buffer';
import * as fs from 'node:fs';

const BASE_URL = process.env.CHATDOC_STUDIO_BASE_URL || 'https://api.chatdoc.studio/v1';
const API_KEY = process.env.CHATDOC_STUDIO_API_KEY || '';

interface ApiErrorResponse {
  code: string;
  detail?: string;
}

function parseAxiosApiError(data: unknown): ApiErrorResponse | null {
  if (!data) return null;

  if (typeof data === 'object' && 'code' in (data as Record<string, unknown>)) {
    return data as ApiErrorResponse;
  }

  try {
    const text = Buffer.from(data as ArrayBuffer).toString('utf-8');
    return JSON.parse(text) as ApiErrorResponse;
  } catch {
    return null;
  }
}

async function getPdfExcel(uploadId: string, outputPath: string, wait = true): Promise<void> {
  const url = `${BASE_URL}/pdf/parser/${uploadId}/excel`;

  if (wait) {
    while (true) {
      try {
        const response = await axios.get(url, {
          headers: {
            Authorization: `Bearer ${API_KEY}`,
          },
          responseType: 'arraybuffer',
        });
        fs.writeFileSync(outputPath, response.data);
        return;
      } catch (error) {
        if (axios.isAxiosError(error) && error.response?.status === 400) {
          const errorData = parseAxiosApiError(error.response.data);
          if (errorData?.code === 'not_parsed') {
            console.log('Still parsing, waiting...');
            await new Promise(resolve => setTimeout(resolve, 3000));
            continue;
          }
        }
        throw error;
      }
    }
  } else {
    try {
      const response = await axios.get(url, {
        headers: {
          Authorization: `Bearer ${API_KEY}`,
        },
        responseType: 'arraybuffer',
      });
      fs.writeFileSync(outputPath, response.data);
    } catch (error) {
      if (axios.isAxiosError(error) && error.response?.status === 400) {
        const errorData = parseAxiosApiError(error.response.data);
        if (errorData?.code === 'not_parsed') {
          throw new Error('Document parsing not completed');
        }
      }
      throw error;
    }
  }
}

// Usage - wait for completion
async function main(): Promise<void> {
  await getPdfExcel('F1CMSW', 'output.xlsx', true);
}

main().catch(console.error);
```

### cURL

```bash
curl -X GET "${CHATDOC_STUDIO_BASE_URL}/pdf/parser/F1CMSW/excel" \
  -H "Authorization: Bearer ${CHATDOC_STUDIO_API_KEY}" \
  -o output.xlsx
```
