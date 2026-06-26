# Example: Extracting and continuing from a DeepSeek chat

## Sample input

User sends: "https://chat.deepseek.com/share/abc123 帮我继续开发这个 REST API"

## Step-by-step

### 1. Read the chat
```bash
cd ~/.openclaw/workspace/skills/browser && node -e "require('puppeteer')" 2>&1 || npm install puppeteer
cd ~/.openclaw/workspace/skills/browser && node index.js read "https://chat.deepseek.com/share/abc123" 2>/dev/null
```

### 2. Raw browser output (abbreviated)
```
DeepSeek

You:
Build a REST API for a todo app using Express and SQLite.
Create the server file first.

DeepSeek:
Here's the Express server setup:

```javascript
// server.js
const express = require('express');
const app = express();
app.use(express.json());
...
```

You:
Good. Now create the routes file at src/routes/todos.js

DeepSeek:
...

You:
Next step: create the database models at src/models/todo.js
```

### 3. Parse into categories

**Code files:**
- `server.js` — Express server setup (complete, 40 lines)
- `src/routes/todos.js` — Todo routes (complete, 60 lines)
- `src/models/todo.js` — Database model (**NOT YET CREATED** — this is the next task)

**Documents:** None

**Goals:**
- Build REST API for todo app ✅ (in progress)
- Express + SQLite stack
- CRUD endpoints for todos

**Status:** ~60% done. Server + routes exist. Models and controllers pending.

### 4. Next action
Create `src/models/todo.js` following the patterns established in server.js and routes/todos.js.

### 5. Report to user
```
📋 Extracted from DeepSeek chat:
   - 8 messages
   - 2 existing code files: server.js, src/routes/todos.js
   - 0 docs
   - Tech: Express + SQLite
   - Status: ~60% — server & routes done, models next

🔧 Creating src/models/todo.js based on your API spec...
```
