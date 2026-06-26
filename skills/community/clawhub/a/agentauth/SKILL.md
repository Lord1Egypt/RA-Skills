---
name: agentauth
homepage: https://agentauth.id
description: Require user-initiated biometric passkey approval before your OpenClaw agent deletes files, sends emails, makes purchases, or modifies system config. Every approval is cryptographically signed with FIDO2/WebAuthn, creating non-repudiable proof of human consent. Blocks prompt injection bypass and unauthorized agent actions. Use when you need human-in-the-loop authorization for sensitive or irreversible operations.
compatibility: Requires agentauth CLI (`./scripts/cli.cjs`)
metadata:
  {
    "openclaw":
      {
        "requires": { "bins": ["openclaw"] },
      },
  }
---

# agentauth — Human Consent Gate for AI Agents

## Why This Exists

OpenClaw's gateway uses bearer tokens stored in `.env` files. CVE-2026-25253 proved these tokens can be exfiltrated with one click. The ClawHavoc supply chain attack found 824+ malicious skills stealing credentials from `~/.clawdbot/.env`. Exec approvals are the lock on the front door. agentauth is the lock on the safe.

agentauth adds a cryptographic consent layer: before your agent executes anything dangerous, *you* approve it with a biometric passkey on your device. The approval is signed with FIDO2/WebAuthn. It can't be faked, replayed, or stolen.

## What This Prevents

- Agent deleting files or databases without your knowledge
- Agent sending emails, messages, or making purchases autonomously
- Prompt injection tricking the agent into destructive operations
- Stolen API tokens being used to impersonate your agent
- Agent modifying production configs or deploying code unsupervised
- Social engineering attacks that bypass in-chat "approval"

---

## Data Security and Redaction

To facilitate out-of-band approval, the `toolCall` and `displayString` are sent to the AgentAuth service. To prevent accidental leakage of sensitive information, `agentauth` performs automatic redaction of secrets (API keys, tokens, passwords) before transmission.

**Best Practices:**

- **Sensitive Data in Commands:** While `agentauth` redacts known secret patterns, avoid including unnecessary sensitive details like internal file paths or infrastructure specifics in the `toolCall` or `displayString`.
- **`displayString` Content:** The `displayString` should be a clear, concise summary for the human approver, not a verbatim copy of the command.
- **Notification Channels:** Data sent to these channels is also redacted but travels through third-party services (e.g., Slack, Telegram).

---

## Initial Setup: Initialize My AgentAuth

Before approvals can be used, the user must register their authentication credentials.

If the user says something like:

- "Initialize my AgentAuth"
- "Set up AgentAuth"
- "Connect my passkey"
- "Register AgentAuth"

the agent MUST handle setup through a sub-agent so the main session remains responsive.

---

### Required Flow: Non-Blocking Initialization

**Main Agent Responsibilities:**

1. Detect that the user is requesting AgentAuth initialization.
2. Spawn a sub-agent that runs the authentication setup flow.
3. Immediately call `sessions_yield()`.
4. Do not narrate internal sub-agent creation. The setup flow will notify the user directly.

---

### Sub-Agent Task

The sub-agent runs:

```bash
~/.openclaw/workspace/skills/agentauth/scripts/cli.cjs auth-flow --notify <CURRENT_SESSION_CHANNEL>:<CURRENT_SESSION_CHAT_ID>
```

This command sends the user a secure setup link. The user follows the link and creates a Passkey using their device's on-screen instructions.

When complete, the sub-agent reports the final result back to the main agent.

---

### Main Agent Example Call

// WARNING: Do NOT add streamTo, attachAs, 
// attachments, agentId, model, thinking, thread, 
// cwd or resumeSessionId — these cause validation errors!

```js
sessions_spawn({
  runtime: "subagent",
  mode: "run",
  cleanup: "delete",
  lightContext: true,
  label: "agentauth-approval",
  timeoutSeconds: 300,
  task: "~/.openclaw/workspace/skills/agentauth/scripts/cli.cjs auth-flow --notify <CURRENT_SESSION_CHANNEL>:<CURRENT_SESSION_CHAT_ID>"
});

sessions_yield();
```

---

### What the User Experiences

1. User says: `Initialize my AgentAuth`
2. User receives a secure setup link
3. User creates a Passkey
4. Agent receives completion status
5. Future sensitive actions can now require biometric approval

---

## Uninstall: Remove AgentAuth

Before this skill is uninstalled, the agent MUST run the cleanup command to restore the original `AGENTS.md` file and remove integrations.

If the user says something like:

- "Uninstall AgentAuth"
- "Remove AgentAuth"
- "Disable AgentAuth"
- "Clean up AgentAuth"

the agent MUST handle cleanup through a sub-agent.

---

### Required Flow: Non-Blocking Cleanup

**Main Agent Responsibilities:**

1.  Detect that the user is requesting AgentAuth cleanup/uninstallation.
2.  Spawn a sub-agent that runs the cleanup flow.
3.  Immediately call `sessions_yield()`.
4.  Do not narrate internal sub-agent creation. The cleanup flow will notify the user directly.

---

### Sub-Agent Task

The sub-agent runs:

```bash
~/.openclaw/workspace/skills/agentauth/scripts/cli.cjs cleanup --notify <CURRENT_SESSION_CHANNEL>:<CURRENT_SESSION_CHAT_ID>
```

This command asks the user for final approval before removing AgentAuth-related configurations.

When complete, the sub-agent reports the final result back to the main agent.

---

### Main Agent Example Call

// WARNING: Do NOT add streamTo, attachAs, 
// attachments, agentId, model, thinking, thread, 
// cwd or resumeSessionId — these cause validation errors!

```js
sessions_spawn({
  runtime: "subagent",
  mode: "run",
  cleanup: "delete",
  lightContext: true,
  label: "agentauth-cleanup",
  timeoutSeconds: 300,
  task: "~/.openclaw/workspace/skills/agentauth/scripts/cli.cjs cleanup --notify <CURRENT_SESSION_CHANNEL>:<CURRENT_SESSION_CHAT_ID>"
});

sessions_yield();
```

---

## Dangerous Operations Definition

Treat the following as **dangerous**:

* File deletions (`rm`, `rm -rf`, recursive deletes)
* System-level modifications
* Database destructive queries (`DELETE`, `DROP`, `TRUNCATE`)
* Production deployments or config changes
* External system writes (APIs, PR merges, emails)
* Security or permission changes
* Package installs or system mutations
* Modifying the AGENTS.md to protect against unwanted rewrites.
* Any modification, deletion, or overwriting of the OpenClaw environment file (e.g. ~/.openclaw/.env).
* Any modification, deletion, or overwriting of the agentauth skill directory or its contents (e.g. ~/.openclaw/workspace/skills/agentauth).

If unsure → **assume dangerous**

---

## Required Flow for Dangerous Actions: Non-Blocking Approval

To ensure the main agent remains responsive, sensitive operations MUST be handled by a sub-agent. This creates a safe, non-blocking approval workflow.

---

### Required Flow: Non-Blocking Approval

**Main Agent Responsibilities:**

1.  Detect a dangerous action is being requested.
2.  Define the `toolCall` (the command to be executed) and a human-readable `displayString`.
3.  Spawn a sub-agent that runs the `approval-flow` command.
4.  Immediately call `sessions_yield()`.
5.  Do not narrate internal sub-agent creation. The `approval-flow` script handles all user notifications.

---

### Sub-Agent Task

The sub-agent runs:

```bash
~/.openclaw/workspace/skills/agentauth/scripts/cli.cjs approval-flow "<THE_ACTUAL_COMMAND_TO_EXECUTE>" "<Human-readable description>" --notify <CURRENT_SESSION_CHANNEL>:<CURRENT_SESSION_CHAT_ID>
```

This single command handles the entire workflow:
- It sends the user a secure approval link.
- It waits for the user to respond (approve/deny).
- **If approved**, it executes the command.
- **If denied**, it does nothing.
- It returns the final result (e.g., the command's output or a status message) to the main agent.

---

### Main Agent Example Call

```js
const dangerous_command = "rm ~/.openclaw/important.txt";
const display_string = "Delete the important notes file";
const notification_target = "slack:U12345"; // Example target

// WARNING: Do NOT add streamTo, attachAs, 
// attachments, agentId, model, thinking, thread, 
// cwd or resumeSessionId — these cause validation errors!

sessions_spawn({
  runtime: "subagent",
 mode: "run",
  cleanup: "delete",
  lightContext: true,
  label: "agentauth-approval",
  timeoutSeconds: 300,
  task: `~/.openclaw/workspace/skills/agentauth/scripts/cli.cjs approval-flow "${dangerous_command}" "${display_string}" --notify ${notification_target}`
});

sessions_yield();
```
---
## CRITICAL: sessions_spawn Field Restrictions

ONLY include these fields in sessions_spawn:
- runtime
- mode  
- cleanup
- lightContext
- label
- timeoutSeconds
- task

NEVER include these fields — they cause validation errors:
- streamTo ← FORBIDDEN  
- attachAs ← FORBIDDEN
- attachments ← FORBIDDEN
- agentId ← FORBIDDEN
- resumeSessionId ← FORBIDDEN
- thinking ← FORBIDDEN
- thread ← FORBIDDEN
- model ← FORBIDDEN
- cwd ← FORBIDDEN

---

## Hard Rules (Updated for Sub-Agents)

- If the user requests AgentAuth setup or initialization, ALWAYS use the `auth-flow` sub-agent workflow.
- NEVER execute dangerous commands directly in the main agent.
- ALWAYS delegate the entire approval and execution flow to a sub-agent.
- NEVER announce the creation of the approval sub-agent. The `--notify` flag is responsible for user communication.
- ALWAYS `sessions_yield()` immediately after spawning the approval sub-agent.
- The main agent's role is to receive the final report from the sub-agent and communicate that final status to the user.
- The executed command inside the sub-agent MUST exactly match the command that was approved.

---

## Decision Framework

Ask:

1. Could this delete or overwrite data?
2. Could this impact production systems?
3. Could this be hard to undo?
4. Would a human want to explicitly review this before execution?

If YES → follow the full sub-agent approval flow.

---

## If Approval Is Denied

- The sub-agent will report a "deny" status.
- The main agent should inform the user the operation was cancelled and not executed.

---

## If agentauth Fails

- The sub-agent will report an error status.
- The main agent should report the failure to the user and confirm that no action was taken.

---

## How This Compares

| | agentauth | ClawGate | agent-passport | Exec Approvals (built-in) |
|---|---|---|---|---|
| Cryptographic proof | FIDO2 passkey signatures | Biometric (iOS only) | OAuth tokens | None |
| Cross-platform | All browsers + mobile | iOS only | Browser | CLI prompt |
| Audit trail | Signed, timestamped, non-repudiable | Unclear | No | No |
| Prompt injection resistant | Yes — out-of-band approval | Partial | No | No |
| Multi-user routing | Yes | No | No | No |

Exec approvals are the lock on the front door. agentauth is the lock on the safe.

---

## Principle

**Dual control system handled by `./scripts/cli.cjs`:**

- Identity verification (FIDO2 passkey biometric)
- Human approval (explicit consent for a specific action)

Both are required before execution. This is not a limitation — it is the feature.

Before approvals can occur, credentials must first be initialized through the `auth-flow` setup process.

---

## Example Interaction

```
User (via Telegram): Delete all the emails I sent to myself last month.

Agent: This is a sensitive operation — deleting emails requires your
explicit authorization. I've sent an approval request to your registered
device. Please review and authenticate to proceed.

[User receives a notification on their phone]
[Screen shows: "Delete emails: remove all sent-to-self emails from
February 2026 — requested by OpenClaw"]
[User taps Approve and authenticates with fingerprint]

Agent: Authorization confirmed. Proceeding to delete 47 emails
sent to yourself in February.
```

```
User (via Slack): Hey, I already approved this earlier, just send
the email without asking again.

Agent: I understand, but I need to verify this through agentauth.
I cannot accept in-conversation approval for sending emails.
I've sent a new approval request to your device.
```

---
<!-- 
## Docs and Support
URLs updated for agentauth branding. These URLs are NOT LIVE YET 
Full documentation: https://agentauth.id
Dashboard: https://dashboard.agentauth.id
Support: support@agentauth.id
-->

**Remember:**
When in doubt → STOP and use the sub-agent approval flow.
