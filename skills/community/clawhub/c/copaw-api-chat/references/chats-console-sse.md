# Chats / Console Chat / SSE

## Core model
CoPaw chat flow is **session-centric**.

Correct sequence:
1. Create or select chat context
2. Reuse its `session_id / user_id / channel`
3. Send message through console chat endpoint
4. Read answer from SSE stream

## 1. Create chat
Endpoint:
- `POST /api/chats`

Minimal payload example:
```json
{
  "name": "neuromant-api-test",
  "session_id": "neuromant-api-session",
  "user_id": "neuromant",
  "channel": "console",
  "meta": {}
}
```

Server returns a `chat_id` and stores chat context.

## 2. Send message
Preferred endpoint:
- `POST /api/agents/{agentId}/console/chat`

Minimal payload pattern:
```json
{
  "channel": "console",
  "user_id": "api-user",
  "session_id": "api-session",
  "input": [
    {
      "role": "user",
      "content": [
        {"type": "text", "text": "Hello. Reply with one short sentence."}
      ]
    }
  ]
}
```

## 3. Read answer
This endpoint returns **SSE** (`text/event-stream`).
Expect `data: <json>` frames.
Typical object flow:
- `response`
- `message`
- `content`

## 4. Stop / control
There is a stop path for long-running chat work:
- `POST /api/console/chat/stop?chat_id=<chat_id>`

## Important caveats
- Do not assume a single stateless prompt request is enough.
- If you skip chat/session creation, the request may connect but not behave as expected.
- The most important context fields are:
  - `session_id`
  - `user_id`
  - `channel`

## Confirmed vs interpretation
Confirmed:
- `/api/chats` exists
- `/api/console/chat` exists
- SSE is used for response streaming
- chat-first flow is the safest integration pattern

Interpretation:
- for reliable automation, chat creation should be treated as mandatory, even if some UI paths may hide it implicitly
e UI paths may hide it implicitly
