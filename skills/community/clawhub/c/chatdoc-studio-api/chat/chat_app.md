# Chat App API

The Chat App API allows you to create document-based Q&A chat applications with multi-turn conversations and source tracing.

## Base Path

```
/chat/apps
```

## App Management

### 1. Create App

Create a new chat application.

**Endpoint:** `POST /chat/apps/`

**Request:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | Yes | App name (1-30 characters) |
| `instruction` | string | Yes | System prompt/instruction for the AI |
| `use_case` | string | No | Use case: `customer_service` (default) or `knowledge_base_qa` |
| `show_history` | boolean | No | Show conversation history (default: true) |
| `temperature` | float | No | Temperature 0-1 (default: 0.7) |
| `welcome_message` | string | No | Welcome message shown to users |
| `input_placeholder` | string | No | Placeholder text for input field |
| `primary_color` | string | No | Primary color in hex format (default: `#5971ED`) |
| `icon_primary_color` | string | No | Icon color in hex format (default: `#5971ED`) |
| `position` | integer | No | Icon position: `1` (right) or `3` (left), default: `1` |
| `source_traceable` | boolean | No | Enable source tracing (default: true) |
| `support_new_conversation` | boolean | No | Allow new conversations (default: true) |
| `suggested_messages_enabled` | boolean | No | Whether to show suggested starter messages (default: `false`) |
| `suggested_messages` | array[string] | No | Suggested starter messages, max 3 items, each item max 50 characters |
| `retrieval_mode` | string | No | Retrieval mode: `basic` (default), `contextual`, or `expanded` |
| `sources` | array | No* | Array of `{"id": "upload_id"}` objects |

*Required when `use_case` is `knowledge_base_qa`

**Retrieval Modes:**

| Mode | Description |
|------|-------------|
| `basic` | Fast and efficient. Combines Embedding and BM25 hybrid retrieval, followed by a non-contextual reranker to reorder the results |
| `contextual` | More precise. Combines Embedding and BM25 hybrid retrieval, followed by a contextual reranker to reorder the results for better accuracy |
| `expanded` | More comprehensive and highly accurate, with increased latency. After the initial contextual reranking, surrounding context from the top relevant segments is added to the candidate set for a second round of reranking |

**Response:**

| Field | Type | Nullable | Description |
|-------|------|----------|-------------|
| `app_type` | integer | No | App type |
| `documents` | array | Yes | Connected documents |
| `documents[].id` | string | Yes | Document ID |
| `documents[].name` | string | Yes | Document name |
| `icon_primary_color` | string | Yes | Icon color in hex format |
| `id` | string | No | App ID |
| `input_placeholder` | string | Yes | Placeholder text for input field |
| `instruction` | string | Yes | System prompt/instruction for the AI |
| `name` | string | No | App name |
| `position` | integer | Yes | Icon position: `1` (right) or `3` (left) |
| `primary_color` | string | Yes | Primary color in hex format |
| `retrieval_mode` | string | No | Retrieval mode used when the app searches bound documents |
| `show_history` | boolean | Yes | Show conversation history |
| `source_traceable` | boolean | Yes | Enable source tracing |
| `status` | boolean | No | App status |
| `suggested_messages` | array[string] | No | Suggested starter messages |
| `suggested_messages_enabled` | boolean | No | Whether suggested starter messages are enabled |
| `support_new_conversation` | boolean | Yes | Allow new conversations |
| `team_id` | string | No | Team ID |
| `temperature` | float | Yes | Temperature setting |
| `use_case` | string | Yes | Use case of the app |
| `welcome_message` | string | Yes | Welcome message shown to users |

**Response Example:**

```json
{
  "app_type": 0,
  "documents": [
    {
      "id": "string",
      "name": "string"
    }
  ],
  "icon_primary_color": "#5971ED",
  "id": "string",
  "input_placeholder": "string",
  "instruction": "string",
  "name": "string",
  "position": 1,
  "primary_color": "#5971ED",
  "retrieval_mode": "contextual",
  "show_history": true,
  "source_traceable": true,
  "status": true,
  "suggested_messages": [
    "What does this document cover?",
    "Summarize the key points."
  ],
  "suggested_messages_enabled": true,
  "support_new_conversation": true,
  "team_id": "string",
  "temperature": 0.7,
  "use_case": "knowledge_base_qa",
  "welcome_message": "string"
}
```

**Status Codes:**

| HTTP Code | Error Code | Description |
|-----------|------------|-------------|
| 201 | - | Success |
| 400 | `upload_ids_not_found` | One or more upload IDs not found |
| 400 | `maximum_document_count_exceeded` | Too many documents connected |
| 400 | `bind_invalid_file_id` | Invalid file ID for binding |
| 402 | - | Insufficient credits |
| 404 | `not_found_knowledge` | Knowledge not found |

### 2. Get App

Retrieve app details by app_id. Returns the latest draft and published versions.

**Endpoint:** `GET /chat/apps/{app_id}`

**Path Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `app_id` | string | App ID |

**Response:** Array of app objects (draft and/or published versions)

| Field | Type | Nullable | Description |
|-------|------|----------|-------------|
| `app_type` | integer | No | App type |
| `documents` | array | Yes | Connected documents |
| `documents[].id` | string | Yes | Document ID |
| `documents[].name` | string | Yes | Document name |
| `icon_primary_color` | string | Yes | Icon color in hex format |
| `id` | string | No | App ID |
| `input_placeholder` | string | Yes | Placeholder text for input field |
| `instruction` | string | Yes | System prompt/instruction for the AI |
| `name` | string | No | App name |
| `position` | integer | Yes | Icon position: `1` (right) or `3` (left) |
| `primary_color` | string | Yes | Primary color in hex format |
| `retrieval_mode` | string | No | Retrieval mode used when the app searches bound documents |
| `show_history` | boolean | Yes | Show conversation history |
| `source_traceable` | boolean | Yes | Enable source tracing |
| `status` | boolean | No | App status |
| `suggested_messages` | array[string] | No | Suggested starter messages |
| `suggested_messages_enabled` | boolean | No | Whether suggested starter messages are enabled |
| `support_new_conversation` | boolean | Yes | Allow new conversations |
| `team_id` | string | No | Team ID |
| `temperature` | float | Yes | Temperature setting |
| `type` | string | No | Version type, e.g. `Draft` |
| `use_case` | string | Yes | Use case of the app |
| `welcome_message` | string | Yes | Welcome message shown to users |

**Response Example:**

```json
[
  {
    "app_type": 0,
    "documents": [
      {
        "id": "string",
        "name": "string"
      }
    ],
    "icon_primary_color": "#5971ED",
    "id": "string",
    "input_placeholder": "string",
    "instruction": "string",
    "name": "string",
    "position": 1,
    "primary_color": "#5971ED",
    "retrieval_mode": "contextual",
    "show_history": true,
    "source_traceable": true,
    "status": true,
    "suggested_messages": [
      "What does this document cover?",
      "Summarize the key points."
    ],
    "suggested_messages_enabled": true,
    "support_new_conversation": true,
    "team_id": "string",
    "temperature": 0.7,
    "type": "Draft",
    "use_case": "knowledge_base_qa",
    "welcome_message": "string"
  }
]
```

**Status Codes:**

| HTTP Code | Error Code | Description |
|-----------|------------|-------------|
| 200 | - | Success |
| 404 | `not_found` | App not found |

### 3. Update App

Update the latest draft app.

**Endpoint:** `PUT /chat/apps/{app_id}`

**Path Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `app_id` | string | App ID |

**Request:** Same fields as Create App (all optional except when updating `sources`)

**Response:** Updated app object

**Status Codes:**

| HTTP Code | Error Code | Description |
|-----------|------------|-------------|
| 200 | - | Success |
| 400 | `upload_ids_not_found` | One or more upload IDs not found |
| 400 | `maximum_document_count_exceeded` | Too many documents connected |
| 400 | `bind_invalid_file_id` | Invalid file ID for binding |
| 404 | `not_found` | App not found |

### 4. Publish App

Publish the latest draft version.

**Endpoint:** `POST /chat/apps/{app_id}/publish`

**Path Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `app_id` | string | App ID |

**Response:** Empty data field on success

**Status Codes:**

| HTTP Code | Error Code | Description |
|-----------|------------|-------------|
| 201 | - | Successfully published |
| 400 | `already_published` | App is already published (no-op) |
| 400 | `training` | App is still processing, continue polling |
| 404 | `not_found` | App not found |

**Important Notes**:
- Publishing is an **async operation** when the app contains documents
- The endpoint processes documents in the background
- You need to **poll** this endpoint until it returns `201` (published successfully)
- During processing, the endpoint may return `400` with error code `training`; keep polling
- If you call publish again after successful publication, you'll get `already_published` error
- An app must be published before you can send messages to it

**Create/Update Notes**:
- `suggested_messages` can contain at most 3 items, and each item must be 50 characters or fewer.
- When `use_case` is `customer_service` and no `sources` are provided, set `source_traceable` to `false`.
- When `use_case` is `customer_service` and no `sources` are provided, `retrieval_mode` must remain `basic`.

## Conversation Management

### 5. Create Conversation

Create a new conversation thread for the app.

**Endpoint:** `POST /chat/apps/{app_id}/conversations`

**Path Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `app_id` | string | App ID |

**Response:**

| Field | Type | Nullable | Description |
|-------|------|----------|-------------|
| `id` | string | No | Conversation ID |
| `created_at` | integer | No | Creation timestamp |

**Status Codes:**

| HTTP Code | Error Code | Description |
|-----------|------------|-------------|
| 201 | - | Success |
| 400 | `not_ready` | Documents not ready (document status is not "indexed") |
| 404 | `not_found` | App not found |

### 6. Get Conversations

List all conversation threads for the app.

**Endpoint:** `GET /chat/apps/{app_id}/conversations`

**Path Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `app_id` | string | App ID |

**Query Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `start_at` | integer | Start timestamp filter |
| `end_at` | integer | End timestamp filter |

**Response:** Array of conversation objects

| Field | Type | Nullable | Description |
|-------|------|----------|-------------|
| `id` | string | No | Conversation ID |
| `name` | string | No | Conversation name |
| `created_at` | integer | No | Creation timestamp |

**Status Codes:**

| HTTP Code | Error Code | Description |
|-----------|------------|-------------|
| 200 | - | Success |
| 404 | `not_found` | App not found |

### 7. Get Messages

Get all messages in a conversation.

**Endpoint:** `GET /chat/apps/{app_id}/conversations/{conversation_id}`

**Path Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `app_id` | string | App ID |
| `conversation_id` | string | Conversation ID |

**Response:**

| Field | Type | Nullable | Description |
|-------|------|----------|-------------|
| `created_at` | integer | No | Conversation creation timestamp |
| `dialogues` | array | No | Array of dialogue objects |
| `id` | string | No | Conversation ID |
| `name` | string | No | Conversation name |

**Dialogue Object (`dialogues[]`):**

| Field | Type | Nullable | Description |
|-------|------|----------|-------------|
| `conversation_id` | string | No | Conversation ID |
| `created_at` | integer | No | Dialogue creation timestamp |
| `id` | integer | No | Dialogue ID |
| `message` | object | No | Message payload |
| `parent_id` | string | No | Parent dialogue/message ID |
| `round_id` | string | No | Round ID |

**Message Object (`dialogues[].message`):**

| Field | Type | Nullable | Description |
|-------|------|----------|-------------|
| `content` | string | No | Message content |
| `role` | string | No | Message role |

**Response Example:**

```json
{
  "created_at": 1757320181,
  "dialogues": [
    {
      "conversation_id": "string",
      "created_at": 1757320181,
      "id": 1,
      "message": {
        "content": "string",
        "role": "string"
      },
      "parent_id": "string",
      "round_id": "string"
    }
  ],
  "id": "string",
  "name": "string"
}
```

**Status Codes:**

| HTTP Code | Error Code | Description |
|-----------|------------|-------------|
| 200 | - | Success |
| 400 | `conversation_not_match_app` | Conversation doesn't belong to app |
| 400 | `no_published_version` | No published version of app |
| 404 | `not_found` | App or conversation not found |

### 8. Send Message

Send a message to a conversation.

**Endpoint:** `POST /chat/apps/{app_id}/messages`

**Path Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `app_id` | string | App ID |

**Request:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `conversation_id` | string | No | Conversation ID (creates new if omitted) |
| `question` | string | Yes | User message content (max 3000 characters) |

**Query Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `stream` | boolean | Enable streaming response (default: false) |

**Response:** (non-streaming)

| Field | Type | Nullable | Description |
|-------|------|----------|-------------|
| `name` | string | No | Conversation name (summary of the chat) |
| `conversation_id` | string | No | Conversation ID |
| `answer` | string | No | AI response content |

**Streaming Response:** Server-Sent Events (SSE) format

Each SSE event contains a JSON object with the following fields:

| Field | Type | Nullable | Description |
|-------|------|----------|-------------|
| `msg_id` | string | No | Message ID |
| `round_id` | string | No | Round ID for this conversation |
| `role` | string | No | Message role: `system`, `user`, `assistant`, `tool`, `function` |
| `content` | string | Yes | Message content |
| `reasoning_content` | string/null | Yes | Reasoning content (if available) |
| `conversation_id` | string | No | Conversation ID |
| `name` | string | Yes | App name |

**SSE Format:**
```
data: {"msg_id": "...", "content": "...", ...}

data: {"msg_id": "...", "content": "...", ...}
```

**Status Codes:**

| HTTP Code | Error Code | Description |
|-----------|------------|-------------|
| 201 | - | Success |
| 400 | `no_published_version` | **App must be published before sending messages** |
| 400 | `conversation_not_match_app` | Conversation doesn't belong to app |
| 404 | `not_found` | App or conversation not found |

**Important**: You must publish the app before sending messages. If you try to send messages to an unpublished app, you will receive a `400` error with error code `no_published_version`. Call `POST /chat/apps/{app_id}/publish` first.

## Use Case Behavior

### Customer Service (`customer_service`)

- Floating chat widget on website
- UI customization: icon, color, position
- No document source required
- General purpose chatbot

### Knowledge Base Q&A (`knowledge_base_qa`)

- Document-based Q&A
- Requires at least one document source
- All documents must be parsed and in `indexed` status
- Source tracing enabled by default

## Important Notes

1. **App Publishing Required**: The app MUST be published (`POST /chat/apps/{app_id}/publish`) before sending messages. Attempting to send messages to an unpublished app will return error code `no_published_version` (400 error).

2. **App ID**: Use the `id` field from Create App response for all subsequent API operations.

3. **Publishing Flow**: Create/Update operations affect the draft version. You must explicitly publish to make changes live for end users.

4. **Conversation Flow**:
   - You can send messages without creating a conversation first (one will be created automatically)
   - For multi-turn conversations, pass the `conversation_id` from the first response
   - Each conversation is independent and maintains its own context

5. **Streaming**: Set `stream=true` query parameter for real-time streaming responses via Server-Sent Events (SSE)
