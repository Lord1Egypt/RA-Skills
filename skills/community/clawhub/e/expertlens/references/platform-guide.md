# ExpertLens — Platform Guide

Platform-specific storage, memory, and behavior rules.

---

## OpenClaw / WSL2 Agents

**Storage:** Full file system access — most powerful platform for ExpertLens

- Short-term learnings: keep in active session context
- Long-term learnings: write to agent's designated learning folder
  (e.g., /home/[user]/self-improving/learnings/, /home/[user]/memory/,
  or whatever path the agent's config specifies — check agent config first)
- Swarm outputs: save as reference files for future sessions if user permits
- Always ask user before writing to any permanent files

**Strengths:** Full persistence, file-based memory, agent-to-agent communication
possible within same ecosystem, no memory limits

**Swarm Mode:** User can relay to ChatGPT, Grok, Gemini, other Claude accounts
via browser or other interfaces

---

## Claude.ai

**Storage:** Long-term memory system (Claude's persistent memory)

- Short-term: maintain in session context
- Long-term: ask user before storing anything in memory
- Memory is global — applies across all conversations
- Be selective: only store genuinely reusable insights, not task-specific details

**Swarm Mode:** User can relay to:
- ChatGPT, Grok, Gemini via browser copy-paste
- Other Claude.ai accounts (different context window = genuinely different perspective)
- Claude Projects (different system prompts = specialized perspective)

**Limitation:** No filesystem access — session data is lost when conversation ends.
Mention this if user needs to preserve intermediate work across sessions.

---

## ChatGPT

**Storage:** ChatGPT Memory feature

- Short-term: maintain in session context
- ChatGPT also maintains internal chat context/summaries within a conversation
- Long-term: use ChatGPT Memory feature — ask user permission before storing
- Memory is persistent across conversations

**Swarm Mode:** User can relay to Claude, Grok, Gemini

---

## Grok

**Storage:** Session memory only (as of April 2026 — verify current status)

- All learnings are session-scoped
- No permanent storage available
- If a learning is important enough to preserve: recommend user note it manually
- Focus on in-session excellence — make each session count

**Swarm Mode:** User can relay to Claude, ChatGPT, Gemini

---

## Gemini

**Storage:** May vary by plan and configuration

- Check if user's Gemini account has memory features enabled
- If memory available → ask permission before storing
- If not available → treat as session-only
- Google Workspace integration may provide additional persistence options

**Swarm Mode:** User can relay to Claude, ChatGPT, Grok

---

## Generic / Unknown Platform

**Default behavior:** Assume session memory only

This includes Claude accessed via API (third-party apps, custom integrations, developer
deployments) unless the deployment explicitly provides a memory or file system layer.

- Do not attempt permanent storage
- If an important learning needs preserving, tell user:
  "This is worth keeping — want to note it manually or check if your platform supports memory?"

---

## Universal Storage Decision Tree

```
New learning acquired during task
        ↓
Is this genuinely useful for FUTURE tasks (not just this one)?
    NO → Keep in session only, don't store
    YES ↓
Does this platform support persistent storage?
    NO → Keep in session. Tell user if important enough to preserve manually.
    YES ↓
Ask user: "Should I save [specific insight] to [memory/files]?"
    NO → Don't store
    MODIFY → Store the modified version
    YES → Store it
```

---

## What is worth storing permanently?

**Store (with permission):**
- User's preferences and working style
- Recurring patterns in user's projects or decisions
- Domain-specific knowledge user has explicitly shared
- Key decisions made about ongoing or long-term projects
- Insights that would meaningfully improve future similar tasks

**Do not store:**
- Task-specific details that won't recur
- Intermediate thinking steps or scratch work
- Temporary context created for one task
- Anything user indicated is private or session-only
