# Advanced Patterns — BBC MCP Tool v2.0

## HTTP Integration (add_http)

### GET Request
```
create_answer:
  type: "add_http"
  message: ""
  plugins:
    http:
      url: "https://api.example.com/status?order={capture}"
      method: "GET"
      rules: []   ← REQUIRED, even if empty
```

### POST Request
```
create_answer:
  type: "add_http"
  message: ""
  plugins:
    http:
      url: "https://api.example.com/webhook"
      method: "POST"
      headers:
        Content-Type: "application/json"
      body:
        name: "{capture}"
        source: "whatsapp"
      rules: []   ← REQUIRED
```

### Capture → HTTP Pattern
Common for collecting user data then sending to API:
```
Flow: registration
  Answer 1: add_text "¿Cuál es tu nombre?" + capture: true
  Answer 2: add_text "¿Tu email?" + capture: true
  Answer 3: add_http → POST captured data to CRM
```

**IMPORTANT**: Each capture only passes to the NEXT answer. For multi-field capture,
chain answers or use AI (add_chatpdf) to collect all fields then route.

---

## Multi-Flow Routing

### Using gotoFlow
Redirect user from one flow to another after an answer:
```
update_answer:
  options:
    gotoFlow:
      flowId: "<target-flow-uuid>"
```

### Using add_intent (AI Semantic Router)
Route based on user intent without exact keyword matching:
```
create_answer:
  type: "add_intent"
  plugins:
    intent:
      rules:
        - conditionRule: "The user wants to book an appointment"
          conditionFlowId: "<booking-flow-uuid>"
          condition: ""
          conditionValue: ""
        - conditionRule: "The user wants to talk to a human"
          conditionFlowId: "<escalation-flow-uuid>"
          condition: ""
          conditionValue: ""
        - conditionRule: "The user wants to know prices"
          conditionFlowId: "<pricing-flow-uuid>"
          condition: ""
          conditionValue: ""
```

**When to use intent vs keywords:**
- Keywords: exact match, fast, predictable (e.g., "menu", "precios")
- Intent: semantic match, handles natural language (e.g., "quiero saber cuánto cuesta")
- Best practice: Use EVENTS.WELCOME + add_chatpdf for most cases, reserve intent for complex routing

---

## Knowledge Base Management

### Scraping a Website
After creating an add_chatpdf answer, feed it website content:
```
update_answer:
  answerId: "<answer-uuid>"
  flowId: "<flow-uuid>"
  projectId: "<project-uuid>"
  assistant:
    scrapeUrl: "https://www.business-website.com"
```

### Setting AI Instructions
```
update_answer:
  assistant:
    instructions: "You are the assistant for [business]..."
```

### Listing Knowledge Base Files
```
update_answer:
  assistant:
    listFiles: true
```

### Deleting a File from Knowledge Base
```
update_answer:
  assistant:
    deleteFileId: "<file-uuid>"
```

### Changing AI Model
```
update_answer:
  assistant:
    model: "gpt-5.4-nano"  // or other supported model
```

---

## Human Handoff Pattern

### Basic Handoff
```
Flow: escalation (keywords: "agente", "humano", "persona")
  Answer 1: add_text "Te comunico con un agente. Espera un momento."
  Answer 2: add_mute { status: true, gapTime: 60 }
```

### Handoff with Context (Advanced)
```
Flow: escalation
  Answer 1: add_text "Transfiriendo a un agente..."
  Answer 2: add_http → POST conversation context to agent dashboard
  Answer 3: add_mute { status: true, gapTime: 120 }
```

### Auto-unmute
`gapTime` controls auto-unmute in minutes. After this period, the bot resumes.
- Short conversations: gapTime: 30
- Complex support: gapTime: 120
- Indefinite (agent unmutes manually): gapTime: 1440 (24h)

---

## Media Answers

### Sending an Image
```
create_answer:
  type: "add_image"
  message: ""
  options:
    media:
      url: "https://example.com/menu.jpg"
    gotoFlow: {}
```

### Sending a Document (PDF, etc.)
```
create_answer:
  type: "add_doc"
  message: ""
  options:
    media:
      url: "https://example.com/catalog.pdf"
    gotoFlow: {}
```

### Sending a Video
```
create_answer:
  type: "add_video"
  message: ""
  options:
    media:
      url: "https://example.com/tutorial.mp4"
    gotoFlow: {}
```

**IMPORTANT**: Media URLs must be publicly accessible. Private/authenticated URLs will fail silently.

---

## Deployment Lifecycle

### Full Deploy Sequence
```
1. validate_bot(projectId)           → Must pass (criticalCount = 0)
2. deploy(projectId, action: "create")  → Provision container
3. deploy(projectId, action: "status")  → Wait for READY_TO_SCAN
4. deploy(projectId, action: "qr")      → Get QR code image
5. User scans QR with WhatsApp
6. deploy(projectId, action: "status")  → Should show CONNECTED
```

### Status Values
| Status | Meaning |
|--------|---------|
| INITIALIZATION | Container starting up |
| READY_TO_SCAN | QR available, waiting for scan |
| CONNECTED | Bot is live and responding |
| FAILED | Something went wrong |

### Reboot
```
deploy(projectId, action: "reboot")  → Restart bot container
```
Use when bot stops responding but project is fine.

### Delete Deployment (GATE REQUIRED)
```
deploy(projectId, action: "delete")  → Tear down container
```
Does NOT delete project data — just stops the running bot.

---

## WhatsApp Message Limits

- **Text messages**: ≤ 160 characters recommended (longer messages may be truncated or split)
- **AI responses** (add_chatpdf): Include "keep responses under 150 characters" in instructions
- **Button labels**: ≤ 20 characters
- **List items**: ≤ 24 characters for title, ≤ 72 for description

Always run `validate_bot` to catch messages > 160 chars before deploying.

---

## Troubleshooting

### Bot not responding
1. Check deploy status: `deploy(projectId, action: "status")`
2. If FAILED → `deploy(projectId, action: "reboot")`
3. If still failing → `deploy(projectId, action: "delete")` then re-create

### Double responses
- Check if flow has both `add_chatpdf` and `add_text` → remove `add_text`
- Check if multiple flows have overlapping keywords → audit keywords

### Messages being truncated
- Run `validate_bot` → check for "long messages" warning
- Shorten to ≤ 160 chars
- For AI: add instruction "respuestas de máximo 3 líneas"

### Flow not triggering
- Verify keywords with `list_flows`
- Check if another flow has conflicting keywords
- Ensure `listenKeywords: false` (unless VOICE_NOTE)
- Verify flow has at least one answer (`list_answers`)