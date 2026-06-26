---
name: codemend
version: 1.1.0
description: AI-powered error monitoring — report errors, get AI fixes, and list recent errors
requires:
  env:
    - CODEMEND_API_KEY
tools:
  - name: report_error
    description: Report a production error to Codemend for AI analysis and fix generation
    parameters:
      message:
        type: string
        required: true
        description: The error message (e.g. "TypeError: Cannot read properties of undefined")
      stack:
        type: string
        description: Full stack trace
      source_url:
        type: string
        description: URL where the error occurred
    returns:
      error_id: string
      status: string
  - name: get_fix
    description: Get the AI-generated fix for a reported error (includes explanation, root cause, fix prompt, and PR URL if applicable)
    parameters:
      error_id:
        type: string
        required: true
        description: The error ID returned from report_error
    returns:
      error: object
      fix: object
      dashboard_url: string
  - name: list_errors
    description: List recent errors for this project with optional status filter
    parameters:
      limit:
        type: number
        description: Number of errors to return (default 10, max 50)
      status:
        type: string
        description: "Filter by status: new, analyzing, analyzed, fix_applied, ignored"
    returns:
      errors: array
      total: number
---

# Codemend AI Skill

Codemend captures production JavaScript/TypeScript errors, analyzes them with AI, and generates fixes — either as GitHub PRs or paste-back prompts for AI coding tools like Lovable, Replit, and Cursor.

## Tools

### report_error

Report a production error to Codemend. The error will be analyzed by AI within seconds.

```bash
curl -X POST "https://codemend.ai/api/errors/ingest" \
  -H "Content-Type: application/json" \
  -d '{
    "key": "'$CODEMEND_API_KEY'",
    "message": "TypeError: Cannot read properties of undefined (reading '\''map'\'')",
    "stack": "TypeError: Cannot read properties of undefined\n    at renderList (src/components/List.tsx:15:23)",
    "source_url": "https://myapp.com/dashboard",
    "source_type": "openclaw"
  }'
```

Response:
```json
{ "status": "queued", "error_id": "uuid-here" }
```

### get_fix

Get the AI-generated fix for a reported error. Includes explanation, root cause, confidence score, and a fix prompt you can paste into your AI coding tool.

```bash
curl -s "https://codemend.ai/api/errors/{ERROR_ID}/fix" \
  -H "x-api-key: $CODEMEND_API_KEY"
```

Response:
```json
{
  "error": {
    "id": "uuid",
    "status": "analyzed",
    "message": "TypeError: Cannot read properties of undefined",
    "stack_trace": "...",
    "source_url": "https://myapp.com/dashboard"
  },
  "fix": {
    "id": "uuid",
    "explanation": "The map() call fails because data is undefined on first render",
    "root_cause": "Missing null check before array operation",
    "confidence": 0.92,
    "fix_prompt": "In src/components/List.tsx, add an early return if data is undefined...",
    "pr_url": "https://github.com/user/repo/pull/42"
  },
  "dashboard_url": "https://codemend.ai/errors/uuid"
}
```

If the error is still being analyzed, the `fix` field will be `null`. Poll with `check_status` first.

### check_status

Check if an error has been analyzed yet.

```bash
curl -s "https://codemend.ai/api/errors/{ERROR_ID}/status" \
  -H "x-api-key: $CODEMEND_API_KEY"
```

Response:
```json
{
  "status": "analyzed",
  "message": "TypeError: Cannot read properties of undefined",
  "has_fix": true,
  "fix_id": "uuid-here",
  "dashboard_url": "https://codemend.ai/dashboard/errors/uuid"
}
```

Statuses: `new` → `analyzing` → `analyzed` / `fix_applied` / `ignored`

### list_errors

List recent errors for this project.

```bash
curl -s "https://codemend.ai/api/errors?limit=10&status=analyzed" \
  -H "x-api-key: $CODEMEND_API_KEY"
```

Response:
```json
{
  "errors": [
    {
      "id": "uuid",
      "status": "analyzed",
      "message": "TypeError: Cannot read properties of undefined",
      "source_type": "openclaw",
      "has_fix": true,
      "fix_id": "uuid",
      "created_at": "2026-03-11T12:00:00Z"
    }
  ],
  "total": 42
}
```

## Setup in a Project

### Browser (React, Next.js, Vue, etc.)

Add to your HTML `<head>`:

```html
<script src="https://codemend.ai/s.js" data-key="YOUR_API_KEY"></script>
```

Or if using an AI coding tool (Lovable, Replit, Bolt, etc.), paste this prompt:

> Add this error monitoring script to my app. Put it in the `<head>` section of index.html:
> `<script src="https://codemend.ai/s.js" data-key="YOUR_API_KEY"></script>`

### Node.js / Backend

```bash
npm install codemend
```

```javascript
const codemend = require('codemend');
codemend.init({ apiKey: process.env.CODEMEND_API_KEY });
codemend.setupProcessHandlers();
```

### Express

```javascript
const codemend = require('codemend');
codemend.init({ apiKey: process.env.CODEMEND_API_KEY });
app.use(codemend.expressErrorHandler());
```

### React Native

```javascript
import codemend from 'codemend/react-native';
codemend.init({ apiKey: 'YOUR_API_KEY' });
codemend.setupErrorHandler();
```

## Typical Workflow

1. Set up error monitoring in your project (above)
2. Errors are automatically captured and sent to Codemend
3. Use `list_errors` to see recent errors
4. Use `get_fix` to get the AI-generated fix
5. Apply the fix: paste the `fix_prompt` into your AI tool, or review the PR on GitHub
