# FactoriaGo API Reference

Base URL: `https://editor.factoriago.com/api`
Note: Landing page is at factoriago.com; App & API are at editor.factoriago.com
Auth: Session cookie (`connect.sid`) obtained via POST `/auth/login`

## Auth

```
POST /auth/register        { username, email, password, captchaToken }
POST /auth/login           { email, password }
GET  /auth/me              → { id, email, username, plan, ... }
POST /auth/logout
POST /auth/forgot-password { email }
```

## Papers (Projects)

```
GET  /paper/list           → [{ id, title, status, createdAt, ... }]
POST /paper/upload         multipart: paper(file), title
POST /paper/new-submission { title }   # blank project
GET  /paper/:id            → project detail
POST /paper/:id/analyze    { reviewText }  # submit reviewer comments for AI analysis
GET  /paper/:paperId/reviews → [review objects]
```

## Chat (AI Assistant)

```
GET  /chat/:paperId        → chat history
POST /chat                 { paperId, message, model }  → { reply }
```

Available models (from settings): `claude-3-5-sonnet`, `gpt-4o`, `gemini-2.0-flash`, `kimi`, `glm-4`, `minimax`

## Tasks (Revision Tasks)

```
GET  /paper/tasks/list                     → all tasks
GET  /paper/tasks/by-paper/:paperId        → tasks for a project
POST /paper/tasks                          { paperId, title, description, priority }
PUT  /tasks/:taskId/rename           { title }
DELETE /tasks/:taskId
```

## Project Files (LaTeX)

```
GET  /paper/:paperId/files           → file tree
GET  /paper/:paperId/files/:fileId/content → file text content
PUT  /paper/:paperId/files/:fileId   { content }  # save file
POST /paper/:paperId/files/compile   → compile LaTeX → PDF
GET  /paper/:paperId/files/download-zip → download all files
```

## Comments & Collaboration

```
POST /paper/:paperId/comments        { content, fileId, line, type }
GET  /paper/:paperId/comments        → [comments]
GET  /paper/:paperId/collaborators   → [collaborators]
```

## LLM Settings (API Key Management)

```
GET  /settings/llm              → { primary_model, primary_key_saved, fallback_model, fallback_key_saved }
POST /settings/llm              { primary_provider, primary_model, primary_api_key,
                                  fallback_provider?, fallback_model?, fallback_api_key? }
GET  /settings/llm-providers    → [{ id, label, models: [{ id, name }] }]
```

**Provider IDs:** `anthropic` | `openai` | `google` | `moonshot` | `zhipu` | `minimax`

**Model IDs (examples):**
- anthropic: `claude-3-5-sonnet-20241022`
- openai: `gpt-4o`
- google: `gemini-2.0-flash`
- moonshot: `moonshot-v1-8k`
- zhipu: `glm-4`
- minimax: `abab6.5s-chat`

> API keys are encrypted server-side. GET returns masked key + `primary_key_saved: bool`.
> Always check `primary_key_saved` before attempting AI operations.

## Auth Flow (for scripts)

```js
// Login and save cookie
const res = await fetch('https://factoriago.com/api/auth/login', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ email, password }),
  credentials: 'include'
});
// All subsequent requests need the session cookie
```
