---
name: ectoclaw
description: >
  Cryptographic audit ledger and AI firewall for OpenClaw agents.
  Records every agent action (messages, skills, tools, plugins, memory, models)
  in an immutable hash-chained ledger with Ed25519 signatures and Merkle proofs.
  Policy engine for defining block, redact, flag, and approval rules.
  Exports compliance bundles and verification reports.
  Protects against prompt injection, credential theft, and unauthorized agent behavior.
homepage: https://github.com/EctoSpace/EctoClaw
metadata:
  openclaw:
    requires:
      bins: []
    install:
      - id: node
        kind: node
        package: ectoclaw
        bins: ["ectoclaw"]
        label: "Install EctoClaw (npm)"
    primaryEnv: ECTOCLAW_URL
tags:
  - security
  - audit
  - compliance
  - cryptography
  - governance
  - firewall
  - policy
  - forensics
  - agent-security
  - audit-trail
---

# EctoClaw — Cryptographic Audit Ledger & AI Firewall for OpenClaw

## Configuration

- ECTOCLAW_URL: The EctoClaw server URL (default: http://localhost:3210)

> Source code and install scripts are fully open-source at https://github.com/EctoSpace/EctoClaw.

### Security / authentication

- EctoClaw is designed to run on localhost or a private network you control.
- If you expose ECTOCLAW_URL beyond localhost, put it behind your own authentication and access controls (for example, a reverse proxy with auth).
- Do not point ECTOCLAW_URL at an untrusted third-party host, since audit logs can contain sensitive prompts, tool outputs, and memory contents.

## Commands

### List Audit Sessions
When the user asks to see audit sessions, list recent sessions, or check audit history:
- Call GET {ECTOCLAW_URL}/api/sessions?limit=10
- Format the response as a readable list showing session ID, status, event count, and goal

### Create Audit Session
When the user asks to start a new audit, create a session, or begin tracking:
- Call POST {ECTOCLAW_URL}/api/sessions with JSON body: {"goal": "<user's stated goal>"}
- Optionally include "policy_name" to bind a policy: {"goal": "<goal>", "policy_name": "<n>"}
- Report the session ID, goal hash, and public key

### Append Event
When the user wants to log an action, record an event, or track an operation:
- Call POST {ECTOCLAW_URL}/api/sessions/{session_id}/events
- JSON body: {"type": "<EventType>", "payload": {<event data>}}
- Valid types: MessageReceived, MessageSent, SkillInvoked, SkillResult, ToolCall, ToolResult, PluginAction, PluginResult, ModelRequest, ModelResponse, MemoryStore, MemoryRecall, ApprovalRequired, ApprovalDecision
- Report the content hash, sequence number, and Ed25519 signature

### Verify Session Integrity
When the user asks to verify a session or check chain integrity:
- Call GET {ECTOCLAW_URL}/api/sessions/{session_id}/verify
- Report whether the hash chain is verified or broken and how many events were checked

### Get Session Details
When the user asks about a specific session:
- Call GET {ECTOCLAW_URL}/api/sessions/{session_id}
- Show full session details including goal, goal hash, status, policy, timestamps, event count, and public key

### Seal a Session
When the user asks to finalize, seal, or close an audit session:
- Call POST {ECTOCLAW_URL}/api/sessions/{session_id}/seal
- Report the sealed status and final Merkle root

### Get Audit Metrics
When the user asks for metrics, statistics, or a summary:
- Call GET {ECTOCLAW_URL}/api/metrics
- Display total sessions, active sessions, sealed sessions, total events, and event type breakdown

### Get Compliance Bundle
When the user asks for a compliance report or Merkle proof:
- Call GET {ECTOCLAW_URL}/api/sessions/{session_id}/compliance
- Show the Merkle root and event hashes

### Get Merkle Proof for Specific Event
When the user asks to prove a specific event exists in the chain:
- Call GET {ECTOCLAW_URL}/api/sessions/{session_id}/merkle?leaf={event_index}
- Show the Merkle root and inclusion proof path

### Verify a Merkle Proof
When the user provides a Merkle proof to verify:
- Call POST {ECTOCLAW_URL}/api/merkle/verify with the proof data
- Report whether the proof is valid

### Generate Audit Report
When the user asks for a full audit report:
- Call GET {ECTOCLAW_URL}/api/reports/{session_id}?format=json
- For HTML: GET {ECTOCLAW_URL}/api/reports/{session_id}?format=html
- Present the complete session report with events and verification status

### List Policies
When the user asks about active policies or what rules are configured:
- Call GET {ECTOCLAW_URL}/api/policies
- Show each policy name and its configuration

### Create or Update a Policy
When the user wants to set up audit rules:
- Call PUT {ECTOCLAW_URL}/api/policies/{name} with {"content": "<TOML policy>"}
- Report the saved status

### Stream Live Events
When the user wants real-time monitoring:
- Connect to GET {ECTOCLAW_URL}/api/stream (Server-Sent Events)
- Report events as they arrive

### Check Server Health
When the user asks if EctoClaw is running:
- Call GET {ECTOCLAW_URL}/health
- Report status, version, and name

## What EctoClaw records

Every OpenClaw lifecycle event is captured as a signed ledger entry:

| Event Type       | What it captures                                    |
|------------------|-----------------------------------------------------|
| MessageReceived  | Inbound messages from any channel                   |
| MessageSent      | Outbound agent responses                            |
| SkillInvoked     | Skill activation with parameters                    |
| SkillResult      | Skill execution output                              |
| ToolCall         | Tool invocations (shell, file, http, browser)       |
| ToolResult       | Tool execution results and observations             |
| PluginAction     | Plugin lifecycle events                             |
| ModelRequest     | LLM API calls with prompt context                   |
| ModelResponse    | LLM responses                                       |
| MemoryStore      | Memory write operations                             |
| MemoryRecall     | Memory read operations                              |
| PolicyViolation  | Blocked or flagged actions                          |
| ApprovalRequired | Human-in-the-loop gate triggered                    |
| ApprovalDecision | Human approval or denial recorded                   |
| SessionSeal      | Session finalized with Merkle root                  |
| KeyRotation      | Ed25519 signing key rotated                         |

> Only send data to an EctoClaw instance you operate and trust. Treat audit logs as highly sensitive and protect them accordingly.

## Cryptographic integrity

Every event is:
1. **SHA-256 hash-chained** — each event hash includes the previous event hash
2. **Ed25519 signed** — tamper-evident digital signatures per event and per session
3. **Merkle tree provable** — O(log n) inclusion proofs for any individual event

## Quick start (for users installing EctoClaw)

```bash
npm install ectoclaw
npx ectoclaw serve --dev
# Dashboard: http://localhost:3210/dashboard/
```

## Links

- GitHub: https://github.com/EctoSpace/EctoClaw
- NPM: https://www.npmjs.com/package/ectoclaw
- Website: https://ectospace.com/EctoClaw
- EctoLedger (Rust enterprise version): https://github.com/EctoSpace/EctoLedger