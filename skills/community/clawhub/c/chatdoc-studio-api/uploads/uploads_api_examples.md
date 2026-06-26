# Uploads API - Code Examples

This page contains code examples for the Uploads API in Python, TypeScript (server-side), Rust, and cURL.

## Environment Setup

Set up your environment variables:

```bash
export CHATDOC_STUDIO_BASE_URL="https://api.chatdoc.studio/v1"
export CHATDOC_STUDIO_API_KEY="your-api-key-here"
```

## Upload File

### Python

```python
import os
import requests
import time

BASE_URL = os.getenv("CHATDOC_STUDIO_BASE_URL", "https://api.chatdoc.studio/v1")
API_KEY = os.getenv("CHATDOC_STUDIO_API_KEY")

def upload_file(file_path: str) -> dict:
    """Upload a file to the team."""
    url = f"{BASE_URL}/uploads/"
    headers = {"Authorization": f"Bearer {API_KEY}"}

    with open(file_path, "rb") as f:
        files = {"file": f}
        response = requests.post(url, headers=headers, files=files)
        response.raise_for_status()
        return response.json()["data"]

# Usage
result = upload_file("document.pdf")
upload_id = result["upload_id"]
print(f"Upload ID: {upload_id}")
print(f"Status: {result['status']}")
print(f"Name: {result['name']}")
```

### TypeScript (Server-side)

```typescript
import fs from 'fs';
import FormData from 'form-data';
import axios from 'axios';

const BASE_URL = process.env.CHATDOC_STUDIO_BASE_URL || 'https://api.chatdoc.studio/v1';
const API_KEY = process.env.CHATDOC_STUDIO_API_KEY || '';

interface UploadResponse {
  upload_id: string;
  name: string;
  file_type: string;
  status: string;
  created_at: number;
}

async function uploadFile(filePath: string): Promise<UploadResponse> {
  const form = new FormData();
  form.append('file', fs.createReadStream(filePath));

  const response = await axios.post<{ data: UploadResponse }>(
    `${BASE_URL}/uploads/`,
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
const result = await uploadFile('document.pdf');
const uploadId = result.upload_id;
console.log(`Upload ID: ${uploadId}`);
console.log(`Status: ${result.status}`);
console.log(`Name: ${result.name}`);
```

### Rust

```rust
use reqwest::multipart::{Form, Part};
use reqwest::Client;
use serde::Deserialize;

const BASE_URL: &str = "https://api.chatdoc.studio/v1";

#[derive(Debug, Deserialize)]
struct UploadResponse {
    #[serde(rename = "upload_id")]
    upload_id: String,
    name: String,
    #[serde(rename = "file_type")]
    file_type: String,
    status: String,
    #[serde(rename = "created_at")]
    created_at: i64,
}

#[derive(Debug, Deserialize)]
struct ApiResponse<T> {
    data: T,
}

async fn upload_file(file_path: &str) -> Result<UploadResponse, Box<dyn std::error::Error>> {
    let api_key = std::env::var("CHATDOC_STUDIO_API_KEY")?;
    let client = Client::new();

    let file_bytes = std::fs::read(file_path)?;
    let file_name = std::path::Path::new(file_path)
        .file_name()
        .unwrap()
        .to_string_lossy()
        .to_string();

    let mime = match std::path::Path::new(file_path)
        .extension()
        .and_then(|ext| ext.to_str())
        .map(|ext| ext.to_lowercase())
        .as_deref()
    {
        Some("pdf") => "application/pdf",
        Some("doc") => "application/msword",
        Some("docx") => "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        Some("md") => "text/markdown",
        Some("txt") => "text/plain",
        _ => "application/octet-stream",
    };

    let file_part = Part::bytes(file_bytes)
        .file_name(file_name.clone())
        .mime_str(mime)?;

    let form = Form::new().part("file", file_part);

    let response = client
        .post(&format!("{}/uploads/", BASE_URL))
        .header("Authorization", format!("Bearer {}", api_key))
        .multipart(form)
        .send()
        .await?;

    let api_response: ApiResponse<UploadResponse> = response.json().await?;
    Ok(api_response.data)
}

// Usage
#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let result = upload_file("document.pdf").await?;
    println!("Upload ID: {}", result.upload_id);
    println!("Status: {}", result.status);
    println!("Name: {}", result.name);
    Ok(())
}
```

### cURL

```bash
# Upload a PDF file
curl -X POST "${CHATDOC_STUDIO_BASE_URL}/uploads/" \
  -H "Authorization: Bearer ${CHATDOC_STUDIO_API_KEY}" \
  -F "file=@document.pdf"

# Upload a DOCX file
curl -X POST "${CHATDOC_STUDIO_BASE_URL}/uploads/" \
  -H "Authorization: Bearer ${CHATDOC_STUDIO_API_KEY}" \
  -F "file=@document.docx"

# Upload a Markdown file
curl -X POST "${CHATDOC_STUDIO_BASE_URL}/uploads/" \
  -H "Authorization: Bearer ${CHATDOC_STUDIO_API_KEY}" \
  -F "file=@document.md"
```

## Upload Multiple Files

### Python

```python
from typing import List

def upload_files(file_paths: List[str]) -> List[str]:
    """Upload multiple files and return their upload IDs."""
    upload_ids = []

    for file_path in file_paths:
        print(f"Uploading {file_path}...")
        result = upload_file(file_path)
        upload_id = result["upload_id"]
        upload_ids.append(upload_id)
        print(f"  Upload ID: {upload_id}")

    return upload_ids

# Usage
files = ["doc1.pdf", "doc2.pdf", "doc3.pdf"]
upload_ids = upload_files(files)

print("All files uploaded:")
for upload_id in upload_ids:
    print(f"  - {upload_id}")

# Now you can use these IDs when creating an app
sources = [{"id": uid} for uid in upload_ids]
print(f"Sources for app: {sources}")
```

### TypeScript

```typescript
async function uploadFiles(filePaths: string[]): Promise<string[]> {
  const uploadIds: string[] = [];

  for (const filePath of filePaths) {
    console.log(`Uploading ${filePath}...`);
    const result = await uploadFile(filePath);
    const uploadId = result.upload_id;
    uploadIds.push(uploadId);
    console.log(`  Upload ID: ${uploadId}`);
  }

  return uploadIds;
}

// Usage
const files = ['doc1.pdf', 'doc2.pdf', 'doc3.pdf'];
const uploadIds = await uploadFiles(files);

console.log('All files uploaded:');
for (const id of uploadIds) {
  console.log(`  - ${id}`);
}

// Now you can use these IDs when creating an app
const sources = uploadIds.map(id => ({ id }));
console.log(`Sources for app:`, sources);
```

## Complete Workflow Example

### Python

```python
# Simplified workflow: Upload files -> Create Chat App -> Wait for app ready
# Note: Parsing is triggered automatically when documents are referenced in the app!

# 1. Upload multiple documents
files = ["handbook.pdf", "policy.pdf", "faq.pdf"]
upload_ids = upload_files(files)
print(f"Uploaded {len(upload_ids)} files")

# 2. Create Chat App immediately (parsing will be triggered automatically)
def create_chat_app(name: str, instruction: str, sources: list) -> dict:
    url = f"{BASE_URL}/chat/apps/"
    headers = {"Authorization": f"Bearer {API_KEY}"}

    data = {
        "name": name,
        "instruction": instruction,
        "use_case": "knowledge_base_qa",
        "sources": sources,
        "suggested_messages_enabled": True,
        "suggested_messages": [
            "What topics are covered?",
            "Summarize this knowledge base.",
        ],
        "retrieval_mode": "contextual",
    }

    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    return response.json()["data"]

sources = [{"id": uid} for uid in upload_ids]
app = create_chat_app(
    "Company Knowledge Base",
    "You are a helpful assistant that answers questions about company policies and procedures.",
    sources,
)

print(f"Chat App created: {app['id']}")
print("Documents are being parsed in the background...")

# 3. Wait for app to be ready (all documents processed)
app_id = app['id']
def publish_app_with_retry(app_id: str, max_retries: int = 60, delay: int = 2):
    """Publish app and poll for completion.

    The publish endpoint processes documents in the background.
    You need to poll until it returns success (usually 201).
    If you call it again after successful publication, you'll get
    error code `already_published` (400 error). During processing,
    it may return `training` (400 error), which means keep polling.
    """
    url = f"{BASE_URL}/chat/apps/{app_id}/publish"
    headers = {"Authorization": f"Bearer {API_KEY}"}
    for attempt in range(max_retries):
        response = requests.post(url, headers=headers)

        if response.status_code in (200, 201):
            print(f"✓ App published successfully!")
            return True

        if response.status_code == 400:
            error_data = response.json()
            error_code = error_data.get("code")

            if error_code == "already_published":
                print(f"✓ App already published!")
                return True
            if error_code == "training":
                print(f"Publishing... ({attempt + 1}/{max_retries})")
                time.sleep(delay)
                continue
            # Other errors - raise
            response.raise_for_status()

        if response.status_code >= 400:
            response.raise_for_status()

        # Still processing (202 or other status), wait and retry
        print(f"Publishing... ({attempt + 1}/{max_retries})")
        time.sleep(delay)

    return False  # timeout

ready = publish_app_with_retry(app_id)
if ready:
    print("You can now start using the chat app!")
```

### TypeScript

```typescript
// Simplified workflow: Upload files -> Create Chat App -> Wait for app ready
// Note: Parsing is triggered automatically when documents are referenced in the app!

import axios from 'axios';

interface CreateChatAppRequest {
  name: string;
  instruction: string;
  use_case: 'knowledge_base_qa' | 'customer_service';
  sources: Array<{ id: string }>;
  suggested_messages_enabled?: boolean;
  suggested_messages?: string[];
  retrieval_mode?: 'basic' | 'contextual' | 'expanded';
}

interface ChatAppDocument {
  id: string | null;
  name: string | null;
}

interface CreateChatAppResponse {
  app_type: number;
  documents: ChatAppDocument[] | null;
  icon_primary_color: string | null;
  id: string;
  input_placeholder: string | null;
  instruction: string | null;
  name: string;
  position: number | null;
  primary_color: string | null;
  retrieval_mode: 'basic' | 'contextual' | 'expanded';
  show_history: boolean | null;
  source_traceable: boolean | null;
  status: boolean;
  suggested_messages: string[];
  suggested_messages_enabled: boolean;
  support_new_conversation: boolean | null;
  team_id: string;
  temperature: number | null;
  use_case: string | null;
  welcome_message: string | null;
}

interface ApiResponse<T> {
  data: T;
}

async function createChatApp(data: CreateChatAppRequest): Promise<CreateChatAppResponse> {
  const response = await axios.post<ApiResponse<CreateChatAppResponse>>(
    `${BASE_URL}/chat/apps/`,
    data,
    {
      headers: {
        Authorization: `Bearer ${API_KEY}`,
      },
    }
  );
  return response.data.data;
}

async function completeWorkflow() {
  // 1. Upload multiple documents
  const files = ['handbook.pdf', 'policy.pdf', 'faq.pdf'];
  const uploadIds = await uploadFiles(files);
  console.log(`Uploaded ${uploadIds.length} files`);

  // 2. Create Chat App immediately (parsing will be triggered automatically)
  const sources = uploadIds.map(id => ({ id }));
  const app = await createChatApp({
    name: 'Company Knowledge Base',
    instruction: 'You are a helpful assistant that answers questions about company policies and procedures.',
    use_case: 'knowledge_base_qa',
    sources,
    suggested_messages_enabled: true,
    suggested_messages: [
      'What topics are covered?',
      'Summarize this knowledge base.',
    ],
    retrieval_mode: 'contextual',
  });

  console.log(`Chat App created: ${app.id}`);
  console.log('Documents are being parsed in the background...');

  // 3. Wait for app to be ready (all documents processed)
  const appId = app.id;
  await waitForAppReady(appId);
}

async function waitForAppReady(appId: string, timeout = 600000): Promise<boolean> {
  const startTime = Date.now();
  const pollIntervalMs = 5000;
  const url = `${BASE_URL}/chat/apps/${appId}/publish`;

  while (Date.now() - startTime < timeout) {
    try {
      const response = await axios.post(
        url,
        {},
        {
          headers: {
            Authorization: `Bearer ${API_KEY}`,
          },
        }
      );

      if (response.status === 200 || response.status === 201) {
        console.log('App is ready! All documents processed.');
        return true;
      }
    } catch (error: unknown) {
      if (axios.isAxiosError(error) && error.response?.status === 400) {
        const code = (error.response.data as { code?: string } | undefined)?.code;
        if (code === 'already_published') {
          console.log('App is ready! All documents processed.');
          return true;
        }
        if (code === 'training') {
          console.log(`App is still training... (${Math.floor((Date.now() - startTime) / 1000)}s elapsed)`);
          await new Promise(resolve => setTimeout(resolve, pollIntervalMs));
          continue;
        }
        throw new Error(`Unexpected publish error code: ${code ?? 'unknown_error'}`);
      } else {
        throw error;
      }
    }

    console.log(`App processing... (${Math.floor((Date.now() - startTime) / 1000)}s elapsed)`);
    await new Promise(resolve => setTimeout(resolve, pollIntervalMs));
  }

  console.log('Timeout waiting for app to be ready');
  return false;
}

completeWorkflow();
```

**Key Points:**
1. Upload files and get `upload_id` values (initial status is `chunking`)
2. Create app immediately with the `upload_id` values
3. Parsing is triggered automatically when documents are referenced
4. Wait for app status before using chat/retrieval features

## Error Handling

### Python

```python
import requests

def upload_file_safe(file_path: str) -> dict | None:
    """Upload file with error handling."""
    try:
        result = upload_file(file_path)
        return result
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 400:
            error_data = e.response.json()
            error_code = error_data.get("code")
            if error_code == "not_support_file_format":
                print(f"Error: Unsupported file format for {file_path}")
            elif error_code == "file_too_large":
                print(f"Error: File {file_path} is too large")
            elif error_code == "empty_file":
                print(f"Error: File {file_path} is empty")
            else:
                print(f"Error: {error_data}")
        elif e.response.status_code == 402:
            print("Error: Insufficient credits. Please top up your account.")
        else:
            print(f"Unexpected error: {e}")
        return None
    except Exception as e:
        print(f"Error uploading file: {e}")
        return None

# Usage
result = upload_file_safe("document.pdf")
if result:
    print(f"Success: {result['upload_id']}")
else:
    print("Upload failed")
```

### TypeScript

```typescript
async function uploadFileSafe(filePath: string): Promise<UploadResponse | null> {
  try {
    return await uploadFile(filePath);
  } catch (error) {
    if (axios.isAxiosError(error)) {
      const e = error;

      if (e.response?.status === 400) {
        const errorCode = e.response.data?.code;
        if (errorCode === 'not_support_file_format') {
          console.log(`Error: Unsupported file format for ${filePath}`);
        } else if (errorCode === 'file_too_large') {
          console.log(`Error: File ${filePath} is too large`);
        } else if (errorCode === 'empty_file') {
          console.log(`Error: File ${filePath} is empty`);
        } else {
          console.log(`Error: ${e.response.data}`);
        }
      } else if (e.response?.status === 402) {
        console.log('Error: Insufficient credits. Please top up your account.');
      } else {
        console.log(`Unexpected error: ${e.message}`);
      }
    } else {
      console.log(`Error uploading file: ${error}`);
    }
    return null;
  }
}

// Usage
const result = await uploadFileSafe('document.pdf');
if (result) {
  console.log(`Success: ${result.upload_id}`);
} else {
  console.log('Upload failed');
}
```
