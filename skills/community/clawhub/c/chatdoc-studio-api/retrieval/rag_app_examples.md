# Content Retrieval App API - Code Examples

This page contains code examples for the Content Retrieval App API in Python, TypeScript (server-side), Rust, and cURL.

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

def create_rag_app(name: str, sources: list[dict]) -> dict:
    """Create a new content retrieval app."""
    url = f"{BASE_URL}/rag/apps"
    headers = {"Authorization": f"Bearer {API_KEY}"}

    data = {
        "name": name,
        "sources": sources,  # [{"id": "upload_id"}, ...]
    }

    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    return response.json()["data"]

# Usage
app = create_rag_app(
    name="Document Search",
    sources=[{"id": "F1CMSW"}],
)
print(f"App ID: {app['id']}")
print(f"Documents: {len(app['documents'])}")
```

### TypeScript (Server-side)

```typescript
import axios from 'axios';

const BASE_URL = process.env.CHATDOC_STUDIO_BASE_URL || 'https://api.chatdoc.studio/v1';
const API_KEY = process.env.CHATDOC_STUDIO_API_KEY || '';

interface CreateRagAppRequest {
  name: string;
  sources: Array<{ id: string }>;
}

interface RagAppResponse {
  id: string;
  name: string;
  documents: Array<{
    id: string;
    name: string;
    status: string;
  }>;
}

async function createRagApp(
  name: string,
  sources: Array<{ id: string }>
): Promise<RagAppResponse> {
  const response = await axios.post<{ data: RagAppResponse }>(
    `${BASE_URL}/rag/apps`,
    { name, sources },
    {
      headers: {
        Authorization: `Bearer ${API_KEY}`,
      },
    }
  );
  return response.data.data;
}

// Usage
async function main(): Promise<void> {
  const app = await createRagApp('Document Search', [{ id: 'F1CMSW' }]);
  console.log(`App ID: ${app.id}`);
  console.log(`Documents: ${app.documents.length}`);
}

main().catch(console.error);
```

### Rust

```rust
use reqwest::Client;
use serde::{Deserialize, Serialize};

const BASE_URL: &str = "https://api.chatdoc.studio/v1";

#[derive(Debug, Deserialize)]
struct Document {
    id: String,
    name: String,
    status: String,
}

#[derive(Debug, Deserialize)]
struct RagAppResponse {
    id: String,
    name: String,
    documents: Vec<Document>,
}

#[derive(Debug, Deserialize)]
struct ApiResponse<T> {
    data: T,
}

#[derive(Debug, Serialize)]
struct Source {
    id: String,
}

#[derive(Debug, Serialize)]
struct CreateRagAppRequest<'a> {
    name: &'a str,
    sources: Vec<Source>,
}

async fn create_rag_app(
    name: &str,
    sources: Vec<String>,
) -> Result<RagAppResponse, Box<dyn std::error::Error>> {
    let api_key = std::env::var("CHATDOC_STUDIO_API_KEY")?;
    let client = Client::new();

    let sources = sources.into_iter()
        .map(|id| Source { id })
        .collect();

    let request = CreateRagAppRequest { name, sources };

    let response = client
        .post(&format!("{}/rag/apps", BASE_URL))
        .header("Authorization", format!("Bearer {}", api_key))
        .json(&request)
        .send()
        .await?;

    let api_response: ApiResponse<RagAppResponse> = response.json().await?;
    Ok(api_response.data)
}
```

### cURL

```bash
curl -X POST "${CHATDOC_STUDIO_BASE_URL}/rag/apps" \
  -H "Authorization: Bearer ${CHATDOC_STUDIO_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Document Search",
    "sources": [{"id": "F1CMSW"}]
  }'
```

## Get App

### Python

```python
import os
import requests

BASE_URL = os.getenv("CHATDOC_STUDIO_BASE_URL", "https://api.chatdoc.studio/v1")
API_KEY = os.getenv("CHATDOC_STUDIO_API_KEY")

def get_rag_app(app_id: str) -> dict:
    """Get app details."""
    url = f"{BASE_URL}/rag/apps/{app_id}"
    headers = {"Authorization": f"Bearer {API_KEY}"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()["data"]

# Usage
app = get_rag_app("abc123")
print(f"App: {app['name']}")
for doc in app["documents"]:
    print(f"  - {doc['name']} (status: {doc['status']})")
```

### TypeScript

```typescript
import axios from 'axios';

const BASE_URL = process.env.CHATDOC_STUDIO_BASE_URL || 'https://api.chatdoc.studio/v1';
const API_KEY = process.env.CHATDOC_STUDIO_API_KEY || '';

interface RagAppResponse {
  id: string;
  name: string;
  documents: Array<{
    id: string;
    name: string;
    status: string;
  }>;
}

async function getRagApp(appId: string): Promise<RagAppResponse> {
  const response = await axios.get<{ data: RagAppResponse }>(
    `${BASE_URL}/rag/apps/${appId}`,
    {
      headers: {
        Authorization: `Bearer ${API_KEY}`,
      },
    }
  );
  return response.data.data;
}

// Usage
async function main(): Promise<void> {
  const app = await getRagApp('abc123');
  console.log(`App: ${app.name}`);
  for (const doc of app.documents) {
    console.log(`  - ${doc.name} (status: ${doc.status})`);
  }
}

main().catch(console.error);
```

### cURL

```bash
curl -X GET "${CHATDOC_STUDIO_BASE_URL}/rag/apps/abc123" \
  -H "Authorization: Bearer ${CHATDOC_STUDIO_API_KEY}"
```

## Update App

### Python

```python
import os
import requests

BASE_URL = os.getenv("CHATDOC_STUDIO_BASE_URL", "https://api.chatdoc.studio/v1")
API_KEY = os.getenv("CHATDOC_STUDIO_API_KEY")

def update_rag_app(app_id: str, name: str, sources: list[dict]) -> dict:
    """Update app configuration and documents."""
    url = f"{BASE_URL}/rag/apps/{app_id}"
    headers = {"Authorization": f"Bearer {API_KEY}"}

    data = {
        "name": name,
        "sources": sources,
    }

    response = requests.put(url, headers=headers, json=data)
    response.raise_for_status()
    return response.json()["data"]

# Usage
app = update_rag_app(
    "abc123",
    name="Updated Document Search",
    sources=[{"id": "F1CMSW"}, {"id": "F2DNE9"}],
)
```

### TypeScript

```typescript
import axios from 'axios';

const BASE_URL = process.env.CHATDOC_STUDIO_BASE_URL || 'https://api.chatdoc.studio/v1';
const API_KEY = process.env.CHATDOC_STUDIO_API_KEY || '';

interface RagAppResponse {
  id: string;
  name: string;
  documents: Array<{
    id: string;
    name: string;
    status: string;
  }>;
}

async function updateRagApp(
  appId: string,
  name: string,
  sources: Array<{ id: string }>
): Promise<RagAppResponse> {
  const response = await axios.put<{ data: RagAppResponse }>(
    `${BASE_URL}/rag/apps/${appId}`,
    { name, sources },
    {
      headers: {
        Authorization: `Bearer ${API_KEY}`,
      },
    }
  );
  return response.data.data;
}

// Usage
async function main(): Promise<void> {
  const app = await updateRagApp(
    'abc123',
    'Updated Document Search',
    [{ id: 'F1CMSW' }, { id: 'F2DNE9' }]
  );
  console.log(`Updated app: ${app.id}`);
}

main().catch(console.error);
```

### cURL

```bash
curl -X PUT "${CHATDOC_STUDIO_BASE_URL}/rag/apps/abc123" \
  -H "Authorization: Bearer ${CHATDOC_STUDIO_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Updated Document Search",
    "sources": [{"id": "F1CMSW"}, {"id": "F2DNE9"}]
  }'
```

## Retrieval Query

### Python

```python
import os
import requests

BASE_URL = os.getenv("CHATDOC_STUDIO_BASE_URL", "https://api.chatdoc.studio/v1")
API_KEY = os.getenv("CHATDOC_STUDIO_API_KEY")

def retrieval_query(
    app_id: str,
    query: str,
    retrieval_mode: str = "contextual",
    retrieval_token_length: int = 6000
) -> list[dict]:
    """Execute a semantic search query."""
    url = f"{BASE_URL}/rag/apps/{app_id}/retrieval"
    headers = {"Authorization": f"Bearer {API_KEY}"}

    data = {
        "query": query,
        "retrieval_mode": retrieval_mode,
        "retrieval_token_length": retrieval_token_length,
    }

    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    return response.json()["data"]

# Usage
results = retrieval_query(
    "abc123",
    "What are the payment terms?",
    retrieval_mode="contextual",
)

for result in results:
    print(f"Document: {result['document_name']}")
    for element in result["elements"]:
        element_text = element.get("markdown") or element.get("text") or ""
        print(f"  [{element['type']}] {element_text[:100]}...")
```

### TypeScript

```typescript
import axios from 'axios';

const BASE_URL = process.env.CHATDOC_STUDIO_BASE_URL || 'https://api.chatdoc.studio/v1';
const API_KEY = process.env.CHATDOC_STUDIO_API_KEY || '';

interface RetrievalRequest {
  query: string;
  retrieval_mode?: 'basic' | 'contextual' | 'expanded';
  retrieval_token_length?: number;
}

interface Element {
  index: number;
  type: string;
  page: number[];
  outline: Record<string, number[][]>;
  is_chapter_title?: boolean;
  parent_chapter?: number;
  rotation?: number;
  text?: string;
  markdown?: string | null;
  cells?: Record<string, { text: string }>;
  grid?: Record<string, Array<{ rows?: number[]; columns?: number[] }>>;
  title?: string;
  title_index?: number;
  merged?: number[][][];
}

interface RetrievalResult {
  upload_id: string;
  document_name: string;
  elements: Element[];
}

async function retrievalQuery(
  appId: string,
  query: string,
  retrievalMode: 'basic' | 'contextual' | 'expanded' = 'contextual',
  retrievalTokenLength = 6000
): Promise<RetrievalResult[]> {
  const response = await axios.post<{ data: RetrievalResult[] }>(
    `${BASE_URL}/rag/apps/${appId}/retrieval`,
    {
      query,
      retrieval_mode: retrievalMode,
      retrieval_token_length: retrievalTokenLength,
    },
    {
      headers: {
        Authorization: `Bearer ${API_KEY}`,
      },
    }
  );
  return response.data.data;
}

// Usage
async function main(): Promise<void> {
  const results = await retrievalQuery(
    'abc123',
    'What are the payment terms?',
    'contextual'
  );

  for (const result of results) {
    console.log(`Document: ${result.document_name}`);
    for (const element of result.elements) {
      const elementText = element.markdown ?? element.text ?? '';
      console.log(`  [${element.type}] ${elementText.substring(0, 100)}...`);
    }
  }
}

main().catch(console.error);
```

### Rust

```rust
use reqwest::Client;
use serde::{Deserialize, Serialize};

const BASE_URL: &str = "https://api.chatdoc.studio/v1";

#[derive(Debug, Serialize)]
struct RetrievalRequest<'a> {
    query: &'a str,
    #[serde(rename = "retrieval_mode")]
    retrieval_mode: &'a str,
    #[serde(rename = "retrieval_token_length")]
    retrieval_token_length: i32,
}

#[derive(Debug, Deserialize)]
struct Element {
    index: i32,
    #[serde(rename = "type")]
    element_type: String,
    page: Vec<i32>,
    outline: serde_json::Value,
    is_chapter_title: Option<bool>,
    parent_chapter: Option<i32>,
    rotation: Option<f64>,
    text: Option<String>,
    markdown: Option<String>,
    cells: Option<serde_json::Value>,
    grid: Option<serde_json::Value>,
    title: Option<String>,
    title_index: Option<i32>,
    merged: Option<Vec<Vec<Vec<i32>>>>,
}

#[derive(Debug, Deserialize)]
struct RetrievalResult {
    #[serde(rename = "upload_id")]
    upload_id: String,
    #[serde(rename = "document_name")]
    document_name: String,
    elements: Vec<Element>,
}

#[derive(Debug, Deserialize)]
struct ApiResponse<T> {
    data: T,
}

async fn retrieval_query(
    app_id: &str,
    query: &str,
    retrieval_mode: &str,
) -> Result<Vec<RetrievalResult>, Box<dyn std::error::Error>> {
    let api_key = std::env::var("CHATDOC_STUDIO_API_KEY")?;
    let client = Client::new();

    let request = RetrievalRequest {
        query,
        retrieval_mode,
        retrieval_token_length: 6000,
    };

    let response = client
        .post(&format!("{}/rag/apps/{}/retrieval", BASE_URL, app_id))
        .header("Authorization", format!("Bearer {}", api_key))
        .json(&request)
        .send()
        .await?;

    let api_response: ApiResponse<Vec<RetrievalResult>> = response.json().await?;
    Ok(api_response.data)
}
```

### cURL

```bash
# Basic retrieval
curl -X POST "${CHATDOC_STUDIO_BASE_URL}/rag/apps/abc123/retrieval" \
  -H "Authorization: Bearer ${CHATDOC_STUDIO_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What are the payment terms?",
    "retrieval_mode": "contextual",
    "retrieval_token_length": 6000
  }'

# Fast retrieval (basic mode)
curl -X POST "${CHATDOC_STUDIO_BASE_URL}/rag/apps/abc123/retrieval" \
  -H "Authorization: Bearer ${CHATDOC_STUDIO_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What are the payment terms?",
    "retrieval_mode": "basic"
  }'

# Comprehensive retrieval (expanded mode)
curl -X POST "${CHATDOC_STUDIO_BASE_URL}/rag/apps/abc123/retrieval" \
  -H "Authorization: Bearer ${CHATDOC_STUDIO_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What are the payment terms?",
    "retrieval_mode": "expanded",
    "retrieval_token_length": 10000
  }'
```

## Complete Workflow Example

### Python

```python
# Complete workflow for creating and querying a content retrieval app

# 1. Create the app
app = create_rag_app(
    name="Contract Search",
    sources=[{"id": "F1CMSW"}, {"id": "F2DNE9"}],
)
app_id = app["id"]
print(f"Created app: {app_id}")

# 2. Wait for documents to be processed (poll status)
import time
timeout = 300  # 5 minutes
start_time = time.time()
while True:
    app = get_rag_app(app_id)
    if any(doc["status"] == "failed" for doc in app["documents"]):
        raise RuntimeError("One or more documents failed to process.")
    if all(doc["status"] == "indexed" for doc in app["documents"]):
        break
    if time.time() - start_time > timeout:
        raise TimeoutError("Timed out waiting for documents to be processed.")
    print("Waiting for documents to be processed...")
    time.sleep(5)

print("All documents ready!")

# 3. Execute retrieval queries
queries = [
    "What is the contract duration?",
    "What are the termination clauses?",
    "Who are the parties involved?",
]

for query in queries:
    print(f"\nQuery: {query}")
    results = retrieval_query(app_id, query)
    for result in results:
        print(f"  From: {result['document_name']}")
        for element in result["elements"]:
            element_text = element.get("markdown") or element.get("text") or ""
            print(f"    - {element_text[:80]}...")
```

### TypeScript

```typescript
// Complete workflow for creating and querying a content retrieval app

async function completeWorkflow() {
  // 1. Create the app
  const app = await createRagApp('Contract Search', [
    { id: 'F1CMSW' },
    { id: 'F2DNE9' },
  ]);
  const appId = app.id;
  console.log(`Created app: ${appId}`);

  // 2. Wait for documents to be processed (with timeout and failure handling)
  const pollIntervalMs = 5000;
  const maxWaitMs = 5 * 60 * 1000; // 5 minutes
  const startTime = Date.now();

  while (true) {
    const currentApp = await getRagApp(appId);

    if (currentApp.documents.some(doc => doc.status === 'failed')) {
      throw new Error('One or more documents failed to process.');
    }

    if (currentApp.documents.every(doc => doc.status === 'indexed')) {
      break;
    }

    if (Date.now() - startTime > maxWaitMs) {
      throw new Error('Timed out waiting for documents to be processed.');
    }

    console.log('Waiting for documents to be processed...');
    await new Promise(resolve => setTimeout(resolve, pollIntervalMs));
  }

  console.log('All documents ready!');

  // 3. Execute retrieval queries
  const queries = [
    'What is the contract duration?',
    'What are the termination clauses?',
    'Who are the parties involved?',
  ];

  for (const query of queries) {
    console.log(`\nQuery: ${query}`);
    const results = await retrievalQuery(appId, query);
    for (const result of results) {
      console.log(`  From: ${result.document_name}`);
      for (const element of result.elements) {
        const elementText = element.markdown ?? element.text ?? '';
        console.log(`    - ${elementText.substring(0, 80)}...`);
      }
    }
  }
}

completeWorkflow().catch(console.error);
```
