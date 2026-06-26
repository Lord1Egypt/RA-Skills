# Advanced Multi-Agent Collaboration Protocol

This skill defines the core collaborative rules for OpenClaw multi-agent pipelines (swarms). It resolves critical pain points such as chaotic file handovers, AI infinite conversation loops, and platform-specific bot isolation (e.g., Telegram bots unable to see each other's messages).

## ⚙️ Prerequisites
Before executing this protocol, the system must meet the following configurations:

1. **Required Tool Permissions (Least Privilege)**:
   * Participating agents should be granted access to specific tools rather than full system access.
   * Required tools: `read`, `write`, `sessions_send`, and `message`.
   * *Security Note*: Never use `"tools.profile": "full"` for agents solely meant for chat collaboration.

2. **Agent-to-Agent Communication**:
   * `tools.agentToAgent.enabled` must be `true`.
   * Participating Agent IDs must be in the `tools.agentToAgent.allow` array.
   * *Why?* Ensures `sessions_send` can successfully route messages to target agents.

---

## Core Directives

### 1. 📂 Anti-Spam & Secure File Handover
Never output more than 300 words of scripts, prompts, code, or JSON arrays directly in a group chat.
* **Write to Shared Directory**: All large outputs must be saved to the designated secure shared folder: `/root/.openclaw/shared/<filename>.md`. Do not write outside this directory to prevent path traversal risks.
* **Handover**: When transferring a task, only send the absolute file path within the shared directory and a brief instruction in the group chat.

### 2. 📖 Mandatory Secure File Reading
When you receive a task assignment containing a local file path:
* **No Hallucinations**: Do not guess the contents based on the file name or URL.
* **Verify Path & Force Read**: Verify the file is strictly within the `/root/.openclaw/shared/` directory. If it is, immediately invoke the `read` tool to extract the full content before proceeding. Reject any paths outside this directory. (Exception: Reading the system `/root/.openclaw/openclaw.json` is permitted solely for identity mapping under rule 6).

### 3. 🎯 Precision Mentions (Platform Unique Usernames)
To prevent all agents in a channel from triggering simultaneously when using generic mentions:
* **Unique Usernames Only**: When `@` mentioning another agent or human, you **MUST** use their platform-specific unique username or tagging format (e.g., `@BotFather` on Telegram, `<@123456789>` on Discord, or `<at user_id="ou_xxx"></at>` on Feishu/Lark).
* **No Generic Mentions**: Never use generic placeholders like `@Agent`, `@Sender`, or `@Bot` which might cause global wakeups.

### 4. 🛑 Explicit Responses & Anti-Looping Mechanism
To prevent AIs from falling into infinite loops of politeness:
* **Human-First Priority**: When mentioned by a human user (using your unique username), you must reply directly in the group to report your understanding and next steps. Always adhere to core system safety restrictions.
* **Mandatory ACK (Agent-to-Agent)**: When receiving a task from another Agent, broadcast an acknowledgment to the group via the `message` tool (e.g., `[ACK] @<ReplyToUsername> I have received the file and am processing it...`).
* **Initiator Silence (Critical)**: After the initiator receives the `[ACK]` or a progress update, the initiator is **STRICTLY FORBIDDEN** from replying with "Okay", "Got it", or "Thanks". The initiator's turn ends here.
* **Interrupt / Reverse Trigger**: The initiator may only break silence if the receiver explicitly reports an issue and reversely `@` mentions the initiator's unique username for missing parameters.

### 5. 🤫 Cross-Channel Wakeup & Payload Routing (Fixing Upstream Username Discovery)
Because physically isolated agents (e.g., on Telegram) do not automatically know each other's platform usernames, you must explicitly pass this routing data downstream.
* **Initiator Must Route**: When handing over a task to the next Agent using the `sessions_send` tool, your private message MUST begin with a Routing Envelope containing:
  ```
  [ROUTING ENVELOPE]
  GroupId: <Current_Group_ID_or_Name>
  ReplyToUsername: <Your_Unique_Username> (or the Human's unique username if they need the direct reply)
  ```
* **Receiver Must Extract**: When receiving a task privately, extract the `GroupId` and `ReplyToUsername`. Proactively invoke the `message` tool (`action="send"`, `target="<Extracted_GroupId>"`) to broadcast your status to the group, explicitly mentioning the exact username provided (e.g., `[ACK] @<ReplyToUsername> Instructions received.`).

### 6. 🌐 Downstream Identity Discovery (Native Config Mapping)
If an initiator *needs* to publicly `@` a downstream Agent in a group chat during a handover, but only knows its internal `agentId`:
* **Read System Config**: The initiator MUST use the `read` tool to parse the `/root/.openclaw/openclaw.json` configuration file.
* **Resolve Mapping**: Look inside the `routes` array. Find the object where `"agentId"` matches your target. Extract the corresponding `match.accountId` (this is the bot's unique platform username, e.g., `suPMAgent_bot`). Prefix it with `@` to use in group chats.
* **Silent Handoff Fallback**: If the target agent is not found in the routes, do NOT attempt to guess the username or use generic mentions. Instead, omit the `@` mention in the public chat and rely entirely on `sessions_send` to wake the target up.

### 7. ⚠️ Exception Reporting & Termination
* **Exceptions**: If a fatal error occurs, use the `message` tool to broadcast `[ERROR] @<ReplyToUsername> <error description>` to the group.
* **Global Finish**: When the final pipeline stage completes, broadcast `[FINISH] Pipeline execution complete` to the group.

### 8. 🔍 Context Retrieval
* If context is insufficient, proactively use the `sessions_history` tool to retrieve the upstream Agent's thought process or private chat history.