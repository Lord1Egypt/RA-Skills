---
name: bbc-skill-tool
description: >-
  Builds, manages, and troubleshoots WhatsApp bots using the BuilderBot Cloud (BBC) MCP Tool v2.0.
  Covers bot creation for businesses needing appointment booking, citas, escalation, and conversational AI.
  Enforces verification after every mutation, destructive action gates, error recovery, and pre-deploy validation.
  USE FOR: BuilderBot, BBC, WhatsApp bot, bot para WhatsApp, MCP tool, builderbot, flow, deploy bot,
  QR code, crear bot, chatbot, bot creation for businesses (restaurant, salon, store, services, rental,
  creators, forum, tech support), debugging bot behavior, voice/image/document handling, notifications,
  structured data capture, managing BBC projects, BBC scaffolding files.
  Pattern 2 (AI-powered) is the DEFAULT for 80% of real-world cases.
---

# BBC MCP Tool v2.0 — Safe-by-Default WhatsApp Bot Builder

## CORE PHILOSOPHY

v2.0 = v1 + Safety. Same tools, same BBC API, but with **mandatory patterns** that prevent
the silent failures, accidental deletions, and unvalidated deploys that plagued v1.

**Three pillars:**
1. **VERIFY** — After every mutating operation, call the corresponding `list_*` to confirm
2. **GATE** — Before every destructive operation, show impact and require explicit "yes"
3. **RECOVER** — When something fails, diagnose why and propose a fix, never just stop

---

## TOOL REFERENCE (Quick)

| Tool | Purpose | Mutating? |
|------|---------|-----------|
| `builderbot_list_projects` | List all projects | No |
| `builderbot_create_project` | Create project | Yes |
| `builderbot_list_flows` | List flows in project | No |
| `builderbot_create_flow` | Create flow with keywords | Yes |
| `builderbot_update_flow` | Update flow config | Yes |
| `builderbot_delete_flow` | Delete flow + all answers | Yes (DESTRUCTIVE) |
| `builderbot_list_answers` | List answers in flow | No |
| `builderbot_create_answer` | Add answer to flow | Yes |
| `builderbot_update_answer` | Update answer content | Yes |
| `builderbot_delete_answer` | Delete single answer | Yes (DESTRUCTIVE) |
| `builderbot_validate_bot` | Health check before deploy | No |
| `builderbot_deploy` | Deploy/status/QR/reboot/delete | Yes (some actions) |

---

## MANDATORY PATTERNS

### Pattern 1: VERIFY after every mutation

After ANY create/update/delete, call the corresponding `list_*` tool to confirm:

```
create_flow(projectId, ...) → list_flows(projectId) → search for the new flow
create_answer(...)          → list_answers(projectId, flowId) → search for new answer
update_answer(...)          → list_answers(projectId, flowId) → confirm content changed
delete_flow(...)            → list_flows(projectId) → confirm flow is gone
```

If verification fails: STOP, report the discrepancy, diagnose, and propose recovery.

### Pattern 2: GATE before destructive actions

Before `delete_flow`, `delete_answer`, or `deploy(action='delete')`:

1. Show what will be affected (flow name, answer count, references)
2. Show a clear warning: "⚠️ This cannot be undone"
3. Wait for explicit user confirmation
4. After execution, VERIFY the deletion
5. Run `validate_bot` to check for broken references

### Pattern 3: RECOVER on failure

When any operation fails or verification shows a discrepancy:

1. **Diagnose**: Check limits (flow count), conflicts (duplicate keywords), permissions
2. **Report**: Tell user exactly what went wrong
3. **Propose**: Offer concrete fix (delete unused flow, rename keyword, retry)
4. **Execute**: Fix with user approval, then VERIFY

---

## FLOW CREATION RULES

### create_flow parameters

```
projectId:        UUID (from list_projects)
name:             "Human Readable Name" (Title Case, user's language)
label:            "snake_case_slug" (lowercase, no spaces)
keywords:         ["keyword1", "keyword2"] or ["EVENTS.WELCOME"]
listenKeywords:   false (ALWAYS false unless EVENTS.VOICE_NOTE)
transcribeAudio:  true only for EVENTS.VOICE_NOTE
interpretImage:   true only for EVENTS.MEDIA
analyzeDocument:  true only for EVENTS.DOCUMENT
```

### CRITICAL RULES

- `listenKeywords` MUST be `false` for ALL flows EXCEPT `EVENTS.VOICE_NOTE`
- A new flow has 0 answers — the bot will NOT respond until you add answers
- Always add answers IMMEDIATELY after creating a flow
- Text keywords must be UNIQUE across all flows
- System events (EVENTS.*) must not be mixed with text keywords
- Each EVENTS.* can appear in only ONE flow

### System Events Reference

| Event | Use case | Required flags |
|-------|----------|----------------|
| `EVENTS.WELCOME` | Catch-all / fallback | listenKeywords: false |
| `EVENTS.VOICE_NOTE` | Voice message handler | listenKeywords: true, transcribeAudio: true |
| `EVENTS.MEDIA` | Image handler | interpretImage: true |
| `EVENTS.DOCUMENT` | Document handler | analyzeDocument: true |
| `EVENTS.LOCATION` | Location shared | — |
| `EVENTS.ACTION` | Button/list response | — |

---

## ANSWER TYPES REFERENCE

### add_text — Simple text message
```
type: "add_text"
message: "Your text here"  ← MAX 160 chars for WhatsApp
```

### add_chatpdf — AI-powered assistant (Pattern 2)
```
type: "add_chatpdf"
message: ""  ← MUST be empty string
```
**CRITICAL**: NEVER mix `add_chatpdf` with `add_text` in the same flow.
Both fire on every message → broken double-response loop.
A flow with `add_chatpdf` must contain ONLY the `add_chatpdf` answer.

After creating, configure via `update_answer` with `assistant` field:
```
assistant: {
  instructions: "You are a helpful assistant for [business]...",
  model: "gpt-5.4-nano"  (optional)
}
```

### add_image / add_video / add_doc / add_voice_note — Media
```
type: "add_image"
message: ""
options: { media: { url: "https://public-url.com/image.jpg" }, gotoFlow: {} }
```

### add_http — HTTP webhook/API call
```
type: "add_http"
message: ""
plugins: {
  http: {
    url: "https://api.example.com/endpoint",
    method: "GET" | "POST",
    headers: { "Content-Type": "application/json" },  // optional
    body: { key: "value" },  // optional, for POST
    rules: []  // REQUIRED — always include, even if empty
  }
}
```
**CRITICAL**: `plugins.http.rules` is REQUIRED. Omitting it causes backend rejection.

### add_mute — Mute contact (human handoff)
```
type: "add_mute"
plugins: { mute: { status: true, gapTime: 60 } }
options: { gotoFlow: { flowId: "farewell-flow-uuid" } }
```
Mutes the INDIVIDUAL contact, not the whole bot. `gapTime` = minutes until auto-unmute.

### add_intent — AI semantic routing
```
type: "add_intent"
plugins: {
  intent: {
    rules: [{
      conditionRule: "The user wants to talk to a human",
      conditionFlowId: "<target-flow-uuid>",
      condition: "",
      conditionValue: ""
    }]
  }
}
```

### Capture rule
`options.capture = true` → bot waits for user reply, passes it to NEXT answer.
**NEVER set capture=true on the LAST answer** of a flow — value is silently lost.

### Redirect
`options.gotoFlow = { flowId: "<target-flow-uuid>" }` → redirect after this answer.

---

## DECISION TREE: Which Pattern to Use

```
User request → What type of business?
├── Needs appointments/citas/availability → Pattern 2 (AI) ★ RECOMMENDED
├── Needs Q&A about products/services    → Pattern 2 (AI)
├── Needs order tracking/status          → Pattern 2 (AI) + HTTP
├── Simple info (hours, location, menu)  → Pattern 1 (keyword-based) OK
├── Lead generation / qualification      → Pattern 2 (AI) + capture
└── Human handoff / escalation           → Pattern 2 (AI) + mute
```

**DEFAULT**: Pattern 2 (AI-powered with `add_chatpdf`) for 80% of real cases.
Only use pure keyword → text flows for very simple, static information.

---

## PATTERN TEMPLATES BY VERTICAL

### Salon / Beauty / Services
- WELCOME: `add_chatpdf` with instructions about services, prices, availability
- AI instructions must include: services list, hours, booking guidance, escalation trigger
- Escalation flow: `add_mute` + human handoff
- Knowledge base: scrape website with `assistant.scrapeUrl`

### Restaurant / Food
- WELCOME: `add_chatpdf` with menu, hours, delivery info
- Order flow: capture address + items via AI
- Location flow: `add_text` with Google Maps link

### E-commerce / Store
- WELCOME: `add_chatpdf` with catalog, pricing, shipping
- Order status: `add_http` to check order API
- Support escalation: `add_mute`

### Content Creator / Digital Products
- WELCOME: `add_chatpdf` with product catalog, pricing
- Purchase flow: redirect to payment link
- Support: AI handles FAQ, escalates complex issues

### Forum / Event
- WELCOME: `add_chatpdf` with event details, schedule, registration
- Registration: capture data + `add_http` to registration API

---

## COMPLETE WORKFLOW: Building a Bot

### Step 1: Get or Create Project

```
list_projects()
├── Project exists → use its projectId
└── Need new → create_project(name) → list_projects() → VERIFY
```

### Step 2: Plan Flows

Before creating anything, plan all flows and share the plan with user:
```
📋 Bot Plan: [Business Name]
├── welcome (EVENTS.WELCOME) — AI assistant with business context
├── escalation (keyword: "agente", "humano") — Human handoff
├── [additional flows based on business needs]
└── Total: N flows
```

### Step 3: Create Flows (one at a time)

For EACH flow:
```
1. create_flow(projectId, name, label, keywords, ...)
2. list_flows(projectId) → VERIFY flow exists, get flow_id
3. create_answer(projectId, flowId, type, message, ...)
4. list_answers(projectId, flowId) → VERIFY answer exists
5. [If add_chatpdf] update_answer(answerId, assistant: { instructions: "..." })
6. list_answers(projectId, flowId) → VERIFY instructions set
```

**NEVER create all flows first then add answers. Create flow → add answers → verify → next flow.**

### Step 4: Validate

```
validate_bot(projectId)
├── criticalCount = 0 → Ready to deploy
└── criticalCount > 0 → Fix issues first
    ├── Dead ends → add answers to empty flows
    ├── Long messages → shorten to ≤160 chars
    ├── Dangling capture → remove capture from last answer
    └── Missing WELCOME → create welcome flow
```

### Step 5: Deploy (with GATE)

```
1. validate_bot(projectId) → MUST pass (criticalCount = 0)
2. Show deployment summary to user:
   ┌─────────────────────────────┐
   │ 📤 DEPLOY SUMMARY          │
   │ Project: [name]            │
   │ Flows: N                    │
   │ Answers: M                  │
   │ Validation: ✅ PASS        │
   │ Confirm? [yes/no]          │
   └─────────────────────────────┘
3. Wait for user confirmation
4. deploy(projectId, action: "create")
5. deploy(projectId, action: "status") → check status
6. If READY_TO_SCAN → deploy(projectId, action: "qr") → show QR
```

---

## ERROR HANDLING FRAMEWORK

### Common Failures & Recovery

| Error | Diagnosis | Recovery |
|-------|-----------|----------|
| Flow created but not in list | Silent failure / API lag | Retry create, verify again |
| "Limit reached" | 50/50 flows used | List flows, find unused, offer to delete |
| Duplicate keyword | Keyword conflict | list_flows to find conflict, rename |
| Answer > 160 chars | WhatsApp truncation | Shorten message, verify |
| Deploy fails | Validation issues | Run validate_bot, fix all criticals |
| add_chatpdf + add_text in same flow | Double-response bug | Delete the add_text answer |
| capture=true on last answer | Dangling capture | Remove capture or add follow-up answer |

### Batch Operations: Sequential with Verification

When creating multiple flows, ALWAYS do them sequentially:
```
FOR EACH flow in plan:
  1. create_flow → VERIFY
  2. create_answer(s) → VERIFY each
  3. [configure AI if needed] → VERIFY
  THEN next flow
```

NEVER batch-create all flows then batch-add answers. This hides partial failures.

---

## FINAL REPORT FORMAT

After completing bot creation, always provide:

```
📊 BOT REPORT: [Project Name]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Project ID: [uuid]

✅ Flows Created:
  1. [flow_name] (id: [uuid]) — [N] answers — [type summary]
  2. ...

⚠️ Issues Fixed:
  • [description of any issues encountered and resolved]

🔍 Validation: [PASS/FAIL]
  • Criticals: 0
  • Warnings: [N]

📤 Deploy Status: [DEPLOYED / NOT YET / READY_TO_SCAN]

🔗 Tool Call Trace:
  [list of all tool calls made in order]
```

---

## ANTI-PATTERNS (Never Do These)

1. ❌ Creating a flow without immediately adding answers
2. ❌ Reporting success without verification (`list_*`)
3. ❌ Deleting without showing impact and getting confirmation
4. ❌ Deploying without running `validate_bot` first
5. ❌ Mixing `add_chatpdf` and `add_text` in the same flow
6. ❌ Setting `listenKeywords: true` on non-VOICE_NOTE flows
7. ❌ Setting `capture: true` on the last answer of a flow
8. ❌ Batch-creating all flows before adding answers
9. ❌ Ignoring validation warnings about message length (>160 chars)
10. ❌ Creating `add_http` answers without `plugins.http.rules: []`

---

## REFERENCES

For vertical-specific templates and advanced patterns, read:
- `references/verticals.md` — Detailed bot templates per business type
- `references/advanced-patterns.md` — HTTP integrations, multi-flow routing, knowledge base setup