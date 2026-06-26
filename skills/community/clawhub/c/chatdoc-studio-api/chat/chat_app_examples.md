# Chat App API - Code Examples

This page contains code examples for the Chat App API in Python, TypeScript (server-side), Rust, and cURL.

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

def create_chat_app(
    name: str,
    instruction: str,
    use_case: str = "customer_service",
    sources: list[dict] | None = None,
    **kwargs
) -> dict:
    """Create a new chat application."""
    url = f"{BASE_URL}/chat/apps/"
    headers = {"Authorization": f"Bearer {API_KEY}"}

    data = {
        "name": name,
        "instruction": instruction,
        "use_case": use_case,
        **kwargs
    }

    if sources is not None:
        data["sources"] = sources

    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    return response.json()["data"]

# Usage - Customer Service
app = create_chat_app(
    name="Customer Support Bot",
    instruction="You are a helpful customer support assistant.",
    source_traceable=False,
)
print(f"App ID: {app['id']}")

# Usage - Knowledge Base Q&A
app = create_chat_app(
    name="Document QA",
    instruction="Answer questions based on the provided documents.",
    use_case="knowledge_base_qa",
    sources=[{"id": "F1CMSW"}],  # upload_id from document
    temperature=0.3,
    suggested_messages_enabled=True,
    suggested_messages=[
        "What topics are covered?",
        "Summarize this document.",
    ],
    retrieval_mode="contextual",
)
print(f"App ID: {app['id']}")
```

### TypeScript (Server-side)

```typescript
import axios from 'axios';

const BASE_URL = process.env.CHATDOC_STUDIO_BASE_URL || 'https://api.chatdoc.studio/v1';
const API_KEY = process.env.CHATDOC_STUDIO_API_KEY || '';

interface CreateAppRequest {
  name: string;
  instruction: string;
  use_case?: string;
  sources?: Array<{ id: string }>;
  temperature?: number;
  welcome_message?: string;
  input_placeholder?: string;
  show_history?: boolean;
  primary_color?: string;
  icon_primary_color?: string;
  position?: number;
  source_traceable?: boolean;
  support_new_conversation?: boolean;
  suggested_messages_enabled?: boolean;
  suggested_messages?: string[];
  retrieval_mode?: 'basic' | 'contextual' | 'expanded';
}

interface AppDocument {
  id: string | null;
  name: string | null;
}

interface CreateAppResponse {
  app_type: number;
  documents: AppDocument[] | null;
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

interface GetAppResponse {
  app_type: number;
  documents: AppDocument[] | null;
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
  type: string;
  use_case: string | null;
  welcome_message: string | null;
}

async function createChatApp(data: CreateAppRequest): Promise<CreateAppResponse> {
  const response = await axios.post<{ data: CreateAppResponse }>(
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

// Usage - Customer Service
const app = await createChatApp({
  name: 'Customer Support Bot',
  instruction: 'You are a helpful customer support assistant.',
  use_case: 'customer_service',
  source_traceable: false,
  welcome_message: 'Hello! How can I help you today?',
});
console.log(`App ID: ${app.id}`);

// Usage - Knowledge Base Q&A
const kbApp = await createChatApp({
  name: 'Document QA',
  instruction: 'Answer questions based on the provided documents.',
  use_case: 'knowledge_base_qa',
  sources: [{ id: 'F1CMSW' }], // upload_id from document
  temperature: 0.3,
  suggested_messages_enabled: true,
  suggested_messages: [
    'What topics are covered?',
    'Summarize this document.',
  ],
  retrieval_mode: 'contextual',
});
console.log(`App ID: ${kbApp.id}`);
```

### Rust

```rust
use reqwest::Client;
use serde::{Deserialize, Serialize};

const BASE_URL: &str = "https://api.chatdoc.studio/v1";

#[derive(Debug, Deserialize)]
struct AppDocument {
    id: Option<String>,
    name: Option<String>,
}

#[derive(Debug, Deserialize)]
struct CreateAppResponse {
    app_type: i32,
    documents: Option<Vec<AppDocument>>,
    icon_primary_color: Option<String>,
    id: String,
    input_placeholder: Option<String>,
    instruction: Option<String>,
    name: String,
    position: Option<i32>,
    primary_color: Option<String>,
    retrieval_mode: String,
    show_history: Option<bool>,
    source_traceable: Option<bool>,
    status: bool,
    suggested_messages: Vec<String>,
    suggested_messages_enabled: bool,
    support_new_conversation: Option<bool>,
    team_id: String,
    temperature: Option<f32>,
    use_case: Option<String>,
    welcome_message: Option<String>,
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
struct CreateAppRequest<'a> {
    name: &'a str,
    #[serde(rename = "instruction")]
    instruction: &'a str,
    #[serde(rename = "use_case")]
    use_case: &'a str,
    #[serde(skip_serializing_if = "Option::is_none")]
    sources: Option<Vec<Source>>,
    #[serde(skip_serializing_if = "Option::is_none")]
    temperature: Option<f32>,
    #[serde(rename = "suggested_messages_enabled", skip_serializing_if = "Option::is_none")]
    suggested_messages_enabled: Option<bool>,
    #[serde(rename = "suggested_messages", skip_serializing_if = "Option::is_none")]
    suggested_messages: Option<Vec<&'a str>>,
    #[serde(rename = "retrieval_mode", skip_serializing_if = "Option::is_none")]
    retrieval_mode: Option<&'a str>,
}

async fn create_chat_app(
    name: &str,
    instruction: &str,
    use_case: &str,
    sources: Option<Vec<String>>,
    suggested_messages: Option<Vec<&str>>,
    retrieval_mode: Option<&str>,
) -> Result<CreateAppResponse, Box<dyn std::error::Error>> {
    let api_key = std::env::var("CHATDOC_STUDIO_API_KEY")?;
    let client = Client::new();

    let sources = sources.map(|ids| ids.into_iter()
        .map(|id| Source { id })
        .collect());

    let request = CreateAppRequest {
        name,
        instruction,
        use_case,
        sources,
        temperature: None,
        suggested_messages_enabled: suggested_messages.as_ref().map(|_| true),
        suggested_messages,
        retrieval_mode,
    };

    let response = client
        .post(&format!("{}/chat/apps/", BASE_URL))
        .header("Authorization", format!("Bearer {}", api_key))
        .json(&request)
        .send()
        .await?;

    let api_response: ApiResponse<CreateAppResponse> = response.json().await?;
    Ok(api_response.data)
}
```

### cURL

```bash
# Customer Service App
curl -X POST "${CHATDOC_STUDIO_BASE_URL}/chat/apps/" \
  -H "Authorization: Bearer ${CHATDOC_STUDIO_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Customer Support Bot",
    "instruction": "You are a helpful customer support assistant.",
    "use_case": "customer_service",
    "source_traceable": false,
    "welcome_message": "Hello! How can I help you today?"
  }'

# Knowledge Base Q&A App
curl -X POST "${CHATDOC_STUDIO_BASE_URL}/chat/apps/" \
  -H "Authorization: Bearer ${CHATDOC_STUDIO_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Document QA",
    "instruction": "Answer questions based on the provided documents.",
    "use_case": "knowledge_base_qa",
    "sources": [{"id": "F1CMSW"}],
    "temperature": 0.3,
    "suggested_messages_enabled": true,
    "suggested_messages": [
      "What topics are covered?",
      "Summarize this document."
    ],
    "retrieval_mode": "contextual"
  }'
```

## Get App

### Python

```python
def get_chat_app(app_id: str) -> list[dict]:
    """Get app details (returns draft and published versions)."""
    url = f"{BASE_URL}/chat/apps/{app_id}"
    headers = {"Authorization": f"Bearer {API_KEY}"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()["data"]

# Usage
apps = get_chat_app("abc123")
for app in apps:
    print(f"App: {app['name']}, Type: {app['type']}, Status: {app['status']}")
```

### TypeScript

```typescript
async function getChatApp(appId: string): Promise<GetAppResponse[]> {
  const response = await axios.get<{ data: GetAppResponse[] }>(
    `${BASE_URL}/chat/apps/${appId}`,
    {
      headers: {
        Authorization: `Bearer ${API_KEY}`,
      },
    }
  );
  return response.data.data;
}

// Usage
const apps = await getChatApp('abc123');
for (const app of apps) {
  console.log(`App: ${app.name}, Type: ${app.type}, Status: ${app.status}`);
}
```

### cURL

```bash
curl -X GET "${CHATDOC_STUDIO_BASE_URL}/chat/apps/abc123" \
  -H "Authorization: Bearer ${CHATDOC_STUDIO_API_KEY}"
```

## Update App

### Python

```python
def update_chat_app(app_id: str, **kwargs) -> dict:
    """Update the latest draft app."""
    url = f"{BASE_URL}/chat/apps/{app_id}"
    headers = {"Authorization": f"Bearer {API_KEY}"}
    response = requests.put(url, headers=headers, json=kwargs)
    response.raise_for_status()
    return response.json()["data"]

# Usage
app = update_chat_app(
    "abc123",
    name="Updated Name",
    instruction="Updated instruction",
    temperature=0.5,
    suggested_messages_enabled=True,
    suggested_messages=[
        "Give me the highlights.",
        "What should I read first?",
    ],
    retrieval_mode="expanded",
)
```

### TypeScript

```typescript
async function updateChatApp(
  appId: string,
  updates: Partial<CreateAppRequest>
): Promise<CreateAppResponse> {
  const response = await axios.put<{ data: CreateAppResponse }>(
    `${BASE_URL}/chat/apps/${appId}`,
    updates,
    {
      headers: {
        Authorization: `Bearer ${API_KEY}`,
      },
    }
  );
  return response.data.data;
}

// Usage
const app = await updateChatApp('abc123', {
  name: 'Updated Name',
  instruction: 'Updated instruction',
  temperature: 0.5,
  suggested_messages_enabled: true,
  suggested_messages: [
    'Give me the highlights.',
    'What should I read first?',
  ],
  retrieval_mode: 'expanded',
});
```

### cURL

```bash
curl -X PUT "${CHATDOC_STUDIO_BASE_URL}/chat/apps/abc123" \
  -H "Authorization: Bearer ${CHATDOC_STUDIO_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Updated Name",
    "instruction": "Updated instruction",
    "temperature": 0.5,
    "suggested_messages_enabled": true,
    "suggested_messages": [
      "Give me the highlights.",
      "What should I read first?"
    ],
    "retrieval_mode": "expanded"
  }'
```

## Publish App

**Important**: Publishing is an async operation when the app contains documents. Keep polling until the request succeeds.

**Status Codes:**

| HTTP Code | Error Code | Description |
|-----------|------------|-------------|
| 201 | - | Successfully published |
| 400 | `already_published` | App is already published (no-op) |
| 400 | `training` | App is still processing, continue polling |
| 404 | `not_found` | App not found |

### Python

```python
import time

def publish_chat_app(
    app_id: str,
    max_retries: int = 60,
    delay: int = 2
) -> None:
    """Publish the latest draft version with polling.

    Args:
        app_id: App ID
        max_retries: Maximum polling attempts
        delay: Delay between attempts (seconds)
    """
    url = f"{BASE_URL}/chat/apps/{app_id}/publish"
    headers = {"Authorization": f"Bearer {API_KEY}"}

    for attempt in range(max_retries):
        response = requests.post(url, headers=headers)

        if response.status_code in (200, 201):
            print(f"✓ App published successfully!")
            return

        if response.status_code == 400:
            error_data = response.json()
            error_code = error_data.get("code")
            if error_code == "already_published":
                print(f"✓ App already published!")
                return
            if error_code == "training":
                print(f"Publishing... ({attempt + 1}/{max_retries})")
                time.sleep(delay)
                continue
            # Other errors - raise
            response.raise_for_status()

        if response.status_code >= 400:
            response.raise_for_status()

        # Still processing, wait and retry
        print(f"Publishing... ({attempt + 1}/{max_retries})")
        time.sleep(delay)

    raise TimeoutError(f"App did not publish within {max_retries * delay} seconds")

# Usage
publish_chat_app("abc123")
```

### TypeScript

```typescript
async function publishChatApp(
  appId: string,
  maxRetries: number = 60,
  delay: number = 2000
): Promise<void> {
  const url = `${BASE_URL}/chat/apps/${appId}/publish`;

  for (let attempt = 0; attempt < maxRetries; attempt++) {
    try {
      const response = await axios.post(url, {}, {
        headers: { Authorization: `Bearer ${API_KEY}` }
      });

      if (response.status === 200 || response.status === 201) {
        console.log('✓ App published successfully!');
        return;
      }

      // Still processing, wait and retry
      console.log(`Publishing... (${attempt + 1}/${maxRetries})`);
      await new Promise(resolve => setTimeout(resolve, delay));
    } catch (error: unknown) {
      if (axios.isAxiosError(error) && error.response?.status === 400) {
        const errorCode = (error.response.data as { code?: string } | undefined)?.code;
        if (errorCode === 'already_published') {
          console.log('✓ App already published!');
          return;
        }
        if (errorCode === 'training') {
          console.log(`Publishing... (${attempt + 1}/${maxRetries})`);
          await new Promise(resolve => setTimeout(resolve, delay));
          continue;
        }
        throw new Error(`Publish failed: ${errorCode ?? 'unknown_error'}`);
      }

      throw error;
    }
  }

  throw new Error('App did not publish in time');
}

// Usage
await publishChatApp('abc123');
```

### cURL

```bash
# Publish app
curl -X POST "${CHATDOC_STUDIO_BASE_URL}/chat/apps/abc123/publish" \
  -H "Authorization: Bearer ${CHATDOC_STUDIO_API_KEY}"

# Poll for completion (in a script)
for i in {1..30}; do
  HTTP_CODE=$(curl -s -o /tmp/publish_resp.json -w "%{http_code}" -X POST "${CHATDOC_STUDIO_BASE_URL}/chat/apps/abc123/publish" \
    -H "Authorization: Bearer ${CHATDOC_STUDIO_API_KEY}")
  ERROR_CODE=$(jq -r '.code // empty' /tmp/publish_resp.json)

  if [ "$HTTP_CODE" = "200" ] || [ "$HTTP_CODE" = "201" ]; then
    echo "✓ App published!"
    break
  fi

  if [ "$ERROR_CODE" = "already_published" ]; then
    echo "✓ App already published!"
    break
  fi

  if [ "$ERROR_CODE" = "training" ]; then
    echo "Publishing... ($i/30)"
    sleep 2
    continue
  fi

  echo "Publish failed: HTTP ${HTTP_CODE}, code=${ERROR_CODE:-unknown_error}"
  cat /tmp/publish_resp.json | jq '.'
  exit 1
done
```

## Create Conversation

### Python

```python
def create_conversation(app_id: str) -> dict:
    """Create a new conversation thread."""
    url = f"{BASE_URL}/chat/apps/{app_id}/conversations"
    headers = {"Authorization": f"Bearer {API_KEY}"}
    response = requests.post(url, headers=headers)
    response.raise_for_status()
    return response.json()["data"]

# Usage
conv = create_conversation("abc123")
print(f"Conversation ID: {conv['id']}")
print(f"Created At: {conv['created_at']}")
```

### TypeScript

```typescript
interface CreateConversationResponse {
  id: string;
  created_at: number;
}

async function createConversation(appId: string): Promise<CreateConversationResponse> {
  const response = await axios.post<{ data: CreateConversationResponse }>(
    `${BASE_URL}/chat/apps/${appId}/conversations`,
    {},
    {
      headers: {
        Authorization: `Bearer ${API_KEY}`,
      },
    }
  );
  return response.data.data;
}

// Usage
const conv = await createConversation('abc123');
console.log(`Conversation ID: ${conv.id}`);
console.log(`Created At: ${conv.created_at}`);
```

### cURL

```bash
curl -X POST "${CHATDOC_STUDIO_BASE_URL}/chat/apps/abc123/conversations" \
  -H "Authorization: Bearer ${CHATDOC_STUDIO_API_KEY}"
```

## Send Message

### Python

```python
import json
import time

def send_message(
    app_id: str,
    question: str,
    conversation_id: str | None = None,
    stream: bool = False
) -> dict | None:
    """Send a message to a conversation.

    Automatically handles app publishing if needed.
    """
    url = f"{BASE_URL}/chat/apps/{app_id}/messages"
    headers = {"Authorization": f"Bearer {API_KEY}"}

    data = {"question": question}
    if conversation_id:
        data["conversation_id"] = conversation_id

    # Try sending message first
    response = requests.post(url, headers=headers, json=data, params={"stream": stream})

    # Check if app needs to be published
    if response.status_code == 400:
        error_data = response.json()
        if error_data.get("code") == "no_published_version":
            print("App not published. Publishing...")
            publish_app_with_retry(app_id)
            # Retry sending message after publish
            response = requests.post(url, headers=headers, json=data, params={"stream": stream})

    response.raise_for_status()
    return response.json()["data"]

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
            return

        if response.status_code == 400:
            error_data = response.json()
            error_code = error_data.get("code")

            if error_code == "already_published":
                print(f"✓ App already published!")
                return
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

    raise TimeoutError(f"App did not publish within {max_retries * delay} seconds")

# Usage - auto-publish flow
result = send_message(
    "abc123",
    "What is the document about?",
)
print(f"Conversation ID: {result['conversation_id']}")
print(f"Answer: {result['answer']}")
```

### TypeScript

```typescript
interface SendMessageRequest {
  conversation_id?: string;
  question: string;
}

interface MessageResponse {
  name: string;
  conversation_id: string;
  answer: string;
}

async function sendMessage(
  appId: string,
  question: string,
  conversationId?: string
): Promise<MessageResponse> {
  const response = await axios.post<{ data: MessageResponse }>(
    `${BASE_URL}/chat/apps/${appId}/messages`,
    {
      conversation_id: conversationId,
      question,
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
const result = await sendMessage(
  'abc123',
  'What is the document about?',
  'conv-id'
);
console.log(`Conversation ID: ${result.conversation_id}`);
console.log(`Name: ${result.name}`);
console.log(`Answer: ${result.answer}`);
```

### cURL

```bash
# Send message with conversation_id
curl -X POST "${CHATDOC_STUDIO_BASE_URL}/chat/apps/abc123/messages" \
  -H "Authorization: Bearer ${CHATDOC_STUDIO_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "conversation_id": "conv-id",
    "question": "What is the document about?"
  }'

# Send message (creates new conversation)
curl -X POST "${CHATDOC_STUDIO_BASE_URL}/chat/apps/abc123/messages" \
  -H "Authorization: Bearer ${CHATDOC_STUDIO_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "Hello!"
  }'

# Send message with streaming
curl -X POST "${CHATDOC_STUDIO_BASE_URL}/chat/apps/abc123/messages?stream=true" \
  -H "Authorization: Bearer ${CHATDOC_STUDIO_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "conversation_id": "conv-id",
    "question": "Tell me more"
  }'
```

### Streaming Response (TypeScript)

```typescript
interface StreamingMessage {
  msg_id: string;
  round_id: string;
  role: string;
  content: string | null;
  reasoning_content: string | null;
  conversation_id: string;
  name: string | null;
}

async function sendMessageStream(
  appId: string,
  question: string,
  onChunk: (chunk: StreamingMessage) => void,
  conversationId?: string
): Promise<void> {
  const url = new URL(`${BASE_URL}/chat/apps/${appId}/messages`);
  url.searchParams.append('stream', 'true');

  const response = await fetch(url.toString(), {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${API_KEY}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      conversation_id: conversationId,
      question,
    }),
  });

  if (!response.ok) {
    const rawError = await response.text();
    let errorMessage = `Send message stream failed with status ${response.status}`;

    if (rawError.trim()) {
      try {
        const errorData = JSON.parse(rawError) as { code?: string; detail?: string };
        const errorCode = errorData.code ?? 'unknown_error';
        const errorDetail = errorData.detail ?? 'No detail';
        errorMessage = `Send message stream failed: ${errorCode} (${errorDetail})`;
      } catch {
        errorMessage = `Send message stream failed with status ${response.status}: ${rawError}`;
      }
    }

    throw new Error(errorMessage);
  }

  const reader = response.body?.getReader();
  const decoder = new TextDecoder();

  if (!reader) {
    throw new Error('No response body');
  }

  while (true) {
    const { done, value } = await reader.read();
    if (done) break;

    const chunk = decoder.decode(value);
    const lines = chunk.split('\n');

    for (const line of lines) {
      if (line.startsWith('data: ')) {
        const data = line.slice(6);
        if (data.trim()) {
          try {
            const parsed: StreamingMessage = JSON.parse(data);
            onChunk(parsed);
          } catch (e) {
            console.error('Failed to parse SSE data:', e);
          }
        }
      }
    }
  }
}

// Usage
await sendMessageStream(
  'abc123',
  'Tell me more',
  (chunk) => {
    console.log(`Role: ${chunk.role}`);
    console.log(`Content: ${chunk.content}`);
    console.log(`Conversation ID: ${chunk.conversation_id}`);
    console.log(`Name: ${chunk.name}`);
  },
  'conv-id'
);
```

## Get Conversations

### Python

```python
def get_conversations(
    app_id: str,
    start_at: int | None = None,
    end_at: int | None = None
) -> list[dict]:
    """List all conversations for an app."""
    url = f"{BASE_URL}/chat/apps/{app_id}/conversations"
    headers = {"Authorization": f"Bearer {API_KEY}"}

    params = {}
    if start_at:
        params["start_at"] = start_at
    if end_at:
        params["end_at"] = end_at

    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()["data"]

# Usage
conversations = get_conversations("abc123")
for conv in conversations:
    print(f"ID: {conv['id']}, Created: {conv['created_at']}")
```

### TypeScript

```typescript
interface ConversationSummary {
  id: string;
  name: string;
  created_at: number;
}

async function getConversations(
  appId: string,
  startAt?: number,
  endAt?: number
): Promise<ConversationSummary[]> {
  const params: Record<string, number> = {};
  if (startAt) params.start_at = startAt;
  if (endAt) params.end_at = endAt;

  const response = await axios.get<{ data: ConversationSummary[] }>(
    `${BASE_URL}/chat/apps/${appId}/conversations`,
    {
      params,
      headers: {
        Authorization: `Bearer ${API_KEY}`,
      },
    }
  );
  return response.data.data;
}

// Usage
const conversations = await getConversations('abc123');
for (const conv of conversations) {
  console.log(`ID: ${conv.id}, Created: ${conv.created_at}`);
}
```

### cURL

```bash
curl -X GET "${CHATDOC_STUDIO_BASE_URL}/chat/apps/abc123/conversations" \
  -H "Authorization: Bearer ${CHATDOC_STUDIO_API_KEY}"
```

## Get Messages

### Python

```python
def get_messages(app_id: str, conversation_id: str) -> dict:
    """Get all messages in a conversation."""
    url = f"{BASE_URL}/chat/apps/{app_id}/conversations/{conversation_id}"
    headers = {"Authorization": f"Bearer {API_KEY}"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()["data"]

# Usage
messages = get_messages("abc123", "conv-id")
for dialogue in messages["dialogues"]:
    message = dialogue["message"]
    print(f"{message['role']}: {message['content']}")
```

### TypeScript

```typescript
interface Dialogue {
  conversation_id: string;
  created_at: number;
  id: number;
  message: {
    content: string;
    role: string;
  };
  parent_id: string;
  round_id: string;
}

interface ConversationDetail {
  created_at: number;
  id: string;
  name: string;
  dialogues: Dialogue[];
}

async function getMessages(
  appId: string,
  conversationId: string
): Promise<ConversationDetail> {
  const response = await axios.get<{ data: ConversationDetail }>(
    `${BASE_URL}/chat/apps/${appId}/conversations/${conversationId}`,
    {
      headers: {
        Authorization: `Bearer ${API_KEY}`,
      },
    }
  );
  return response.data.data;
}

// Usage
const messages = await getMessages('abc123', 'conv-id');
for (const msg of messages.dialogues) {
  console.log(`${msg.message.role}: ${msg.message.content}`);
}
```

### cURL

```bash
curl -X GET "${CHATDOC_STUDIO_BASE_URL}/chat/apps/abc123/conversations/conv-id" \
  -H "Authorization: Bearer ${CHATDOC_STUDIO_API_KEY}"
```
