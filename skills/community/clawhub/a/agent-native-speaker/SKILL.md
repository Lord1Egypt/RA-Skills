---
name: agent-native-speaker
description: "Use when user asks about Agent architecture, design, or how an Agent works. Two-layer teaching: Layer 1 explains Agent concepts (agent loop, tool calling, memory, session, config), Layer 2 reads the Agent's own source code to explain specific architecture. Follows the Self-Explanation Protocol: always search code before answering architecture questions."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [agent-native-learning, harness-engineering, self-explanation, agent-architecture, teaching]
    related_skills: [hermes-agent, writing-plans]
---

# Agent Native Speaker

> Learn how an Agent works — from the Agent itself.

## Overview

When a user asks about Agent architecture or how a specific Agent works, **Agent Native Speaker** activates. It operates in two layers:

- **Layer 1 (Concepts):** Explains Harness Engineering concepts in plain terms — what is an agent loop, what is tool calling, how memory works. No code reading needed; uses analogy and clear explanation for learners new to the field.
- **Layer 2 (Architecture):** The user wants to know how *this* specific Agent implements something (e.g., "How does Hermes's memory system work?"). The Agent must search its own source code, read the relevant implementation, and explain based on real code with file and line references.

**Core discipline:** For Layer 2 questions, the Agent MUST NOT rely solely on training-data recall. It must locate, read, and reference actual source files before answering.

## When to Use

**Activate when the user asks about:**

| Topic | Examples |
|-------|----------|
| **Agent architecture** | "How does an agent loop work?", "What's the architecture of this system?" |
| **Tool calling** | "How does tool calling work?", "How are tool results handled?" |
| **Memory & State** | "How does memory work?", "How are sessions persisted?" |
| **Agent design** | "How is this Agent built?", "How does the system start up?" |
| **Specific framework** | "How does Hermes implement the agent loop?", "How does OpenCode handle tool calling?" |
| **Harness Engineering** | "What is harness engineering?", "How to build an Agent?" |

**Neutral — use judgment:**

| Situation | Recommended behavior |
|-----------|---------------------|
| User asks a generic concept question without naming a framework | Layer 1 — explain concepts |
| User mentions a specific framework (e.g., "Hermes", "OpenCode", "Claude Code") | Layer 2 — search source code |
| User asks "how does X work" in the middle of a general conversation | Check context: if they mean *your* implementation, go Layer 2 |

**Do NOT activate when:**

- User is doing normal work (writing code, asking about features, config, setup)
- User asks about prompt engineering or LLM usage patterns
- User asks about machine learning theory or model training
- User asks for operational advice (performance tuning, deployment)

## How It Works

### The Two-Layer Teaching Model

```
      User Question
           │
           ▼
    ┌──────────────┐
    │ Is this about │
    │ Agent arch?   │──── No ──→ Normal response (skill not active)
    └──────┬───────┘
           │ Yes
           ▼
    ┌──────────────────────────────┐
    │ Does the question name      │
    │ a *specific* framework?     │
    │ (Hermes, OpenCode, etc.)    │
    └──────┬──────────────┬───────┘
           │ No            │ Yes
           ▼               ▼
      ┌─────────┐   ┌────────────┐
      │ Layer 1 │   │  Layer 2   │
      │ Concepts│   │ Architecture│
      │ No code │   │ Read code! │
      │ reading │   │ Cite files │
      └────┬────┘   └──────┬─────┘
           │               │
           ▼               ▼
     Explain with      Search src/
     analogies         Read modules
                       Explain design
```

---

## Layer 1: Concept Teaching

Triggered when the user asks about Agent concepts **without** naming a specific framework.

### What It Does

1. Takes the user's question
2. Identifies which Harness Engineering concept they're asking about (agent loop, tool calling, memory, session, config, model routing, error handling, etc.)
3. Explains it in plain, accessible language with analogies
4. Keeps it accurate but non-technical — suitable for someone new to Agent internals

### Example Interactions

> **User:** What is an agent loop?
>
> **You:** An agent loop is the core heartbeat of an Agent. Imagine a restaurant:
> 1. Customer places an order (user sends a message)
> 2. Waiter takes it to the kitchen (LLM processes the message)
> 3. Kitchen might need ingredients from the pantry (tool calling)
> 4. Waiter brings food back (delivers response)
> 5. The loop starts over for the next customer
>
> This "receive → process → respond → repeat" cycle is an agent loop. Most Agents have a configurable max_turns to prevent infinite loops.

> **User:** What is tool calling?
>
> **You:** An Agent can't do everything itself — it can't run code, access your filesystem, or search the web natively. Tool calling is how the Agent says "I need help with this part" and hands off to a specialized function (a "tool").
>
> Think of it like a chef who has assistants: the chef decides what needs to happen (e.g., "chop the vegetables"), but an assistant does the actual chopping. The chef doesn't need to know how to chop — just that the task gets done and the result comes back.

> **User:** How does memory work in an Agent?
>
> **You:** Agent memory works in layers, like your own memory:
> - **Short-term (session context):** Everything said in the current conversation. It's held in the prompt but gets dropped when the conversation ends — like what you had for breakfast this morning (you'll forget it tomorrow).
> - **Long-term (persistent storage):** Important facts saved to disk (in a database or file) that survive across sessions — like your home address or your birthday. The Agent reads these at the start of every new conversation.
> - **Searchable (session history):** Past conversations stored for retrieval. The Agent doesn't load everything into context, but it can search when needed — like searching your chat history for "where did I put that recipe?"

### Layer 1 Teaching Principles

- **Accuracy first:** Never sacrifice correctness for simplicity. If a simplification would be misleading, explain the nuance.
- **Always compare to a "wrong" model:** After explaining the right way, briefly mention what people often get wrong about it.
- **Stay at the concept level:** Don't guess how the current Agent implements something unless asked.
- **End with an invitation to go deeper:** "That's the general concept. If you want, I can show you how *this* Agent implements it — just ask."

---

## Layer 2: Architecture Deep-Dive (Self-Explanation Protocol)

Triggered when the user asks about how **a specific Agent** (including this one) implements something.

### The Self-Explanation Protocol

This is the **core behavior constraint** of the skill. The Agent MUST follow this exact sequence:

#### Step 1: Recognize the Trigger

Is the question about how *this* specific Agent works? Signals:
- User names a framework: "Hermes", "OpenCode", "Claude Code"
- User says "you" or "your": "How does your memory system work?"
- Context clearly establishes we're talking about the current Agent's internal design

If yes → proceed to Step 2. If no → fall back to Layer 1.

#### Step 2: Locate Source Code

```python
# Strategy: find the entry point and core modules
search_files("main", target="files", path="<agent_home>/src/", file_glob="*.py")
search_files("agent_loop OR event_loop OR main_loop", target="content", path="<agent_home>/src/core/")
search_files("memory OR session OR state", target="content", path="<agent_home>/src/")

# If directory layout is unknown, probe common patterns:
ls <agent_home>/src/  # or core/, lib/, app/
```

**Search targets by topic:**

| Topic | What to search for |
|-------|-------------------|
| Agent Loop | `agent_loop`, `event_loop`, `main_loop`, `while True`, `run()` |
| Tool Calling | `tool_call`, `function_call`, `tool_handler`, `tool_executor` |
| Memory | `memory`, `session_store`, `persist`, `state_manager` |
| Entry Point | `main.py`, `cli.py`, `index.ts`, `bootstrap`, `startup` |
| Config | `config`, `settings`, `yaml.load`, `toml.load` |
| Model Routing | `model`, `provider`, `router`, `llm_client` |
| Error Handling | `retry`, `fallback`, `error_handler`, `exception` |
| Tool Result | `tool_result`, `tool_output`, `tool_to_message`, `result_handler` |

#### Step 3: Read the Code

Read at least 2-3 core files to understand the implementation:

```python
# Read the found files
read_file("<agent_home>/src/core/agent_loop.py", limit=100)    # first 100 lines
read_file("<agent_home>/src/core/agent_loop.py", offset=100)    # continue reading
```

**Reading strategy:**
1. Read the file header / class definition / imports (first 50 lines) → understand structure
2. Read the main function or entry method → understand flow
3. Read any critical helper functions → understand details

#### Step 4: Organize the Answer

Structure every Layer 2 answer as:

```
[Concept name] → [Code location] → [What the code does] → [Why it's designed this way]
```

**Template:**

> **How it works:** [2-3 sentence explanation based on what the code actually does]
>
> **Code location:** `path/to/file.py:15-42`
>
> **Key design decisions:**
> - [Decision 1 with code evidence]
> - [Decision 2 with code evidence]
>
> **Trade-offs visible in the code:**
> - [What the code chose and what it sacrificed]

#### Step 5: Be Transparent About Limits

If source code is not accessible or readable:

> "I cannot access this Agent's source code to give an accurate architecture explanation. The following answer is based on general knowledge of how such systems are typically designed."

Do NOT fabricate code references. If you can't find it, say so.

### Layer 2 Answer Examples

> **User:** How does Hermes's memory system work?
>
> **You:** Let me look at the source code.
>
> [Agent searches and reads memory-related files]
>
> Hermes uses a two-tier memory system:
>
> **1. Session-scoped memory (short-term)**
> Every conversation is stored as a SQLite `messages` table with role, content, and timestamp. The active session loads recent messages into the LLM context window. Old messages stay in the DB but aren't loaded — they're searchable via `session_search`.
>
> **Code:** `src/core/state.db` — `messages` table (id, session_id, role, content, timestamp)
>
> **2. Persistent memory (long-term)**
> Key-value pairs stored as plain markdown files in `memories/MEMORY.md` and `memories/USER.md`. Each file contains declarative facts separated by `§` markers. These files are read at session start and injected into the system prompt.
>
> **Code location:** `src/core/memory_manager.py:1-89`
>
> **Design decision:** The choice of markdown files over a database for long-term memory prioritizes transparency and editability — the user can open MEMORY.md and see/edit everything the Agent remembers, no special tools needed. The trade-off is no query capability (you can't say "find memories about X" without regex).

> **User:** What happens when a tool returns an error?
>
> **You:** Let me find the error handling path in the source.
>
> [Agent searches for error handling code]
>
> **Code location:** `src/core/tool_handler.py:42-78`
>
> **What happens:** When a tool returns a non-zero exit code or raises, the `ToolResult` object's `is_error` flag is set. The agent loop checks this flag in `post_tool_hook()`:
>
> ```python
> # Simplified from tool_handler.py:52
> if result.is_error:
>     # Format error as a system message
>     return {"role": "tool", "content": f"[Error] Tool {tool_name} failed: {result.stderr}"}
> ```
>
> The error is then fed back to the LLM as a tool message. The LLM can decide to retry, use a different tool, or apologize to the user. The Agent itself does **not** auto-retry — that decision is delegated to the model.
>
> **Design trade-off:** Delegating retry decisions to the LLM is more flexible but means error handling is non-deterministic. A model might retry 10 times on a permanent error (wasting tokens) instead of failing fast.

### The Iron Law of Self-Explanation

```
NO LAYER 2 ANSWER WITHOUT SOURCE CODE ACCESS
```

If you skip the search-and-read step for a Layer 2 question, you are violating this skill's core contract.

---

## Trigger Domain Reference

### Layer 1 Keywords (concept-level only, no code reading)

```
agent loop, main loop, event loop
tool calling, function calling
memory, session, state
model routing, provider
config, settings, configuration
error handling, retry, fallback
harness engineering, build an agent
architecture, system design (generic)
entry point, startup, bootstrap (generic)
```

### Layer 2 Keywords (specific framework → code reading required)

If the question contains **any** of these framework names OR explicitly refers to "this Agent" / "your [system component]":

```
Hermes, Hermes Agent
OpenCode, Codex CLI
Claude Code
"your memory", "your loop", "your tool system"
"this Agent's", "the Agent's" (in context of code/implementation)
```

### What if the User Asks Something Ambiguous?

If you're unsure whether the user wants Layer 1 or Layer 2:

1. **Ask:** "Do you want the general concept, or how *this specific Agent* implements it?"
2. OR: Default to Layer 1 and end with "... want me to show you how this is implemented in code?"

---

## Common Pitfalls

1. **Relying on training data instead of reading code.** The most common trap. For Layer 2 questions, you MUST search the codebase. Your training data knows how agents *generally* work — it doesn't know how *this specific Agent* implements things.

2. **Fabricating code references.** If you didn't find the code, don't guess at file paths or line numbers. Say "I couldn't find that component in the source."

3. **Being too technical in Layer 1.** Concepts should be accessible. If you're talking about "message protocol serialization" to a beginner, you've lost them. Start with "how messages are packed up to be sent."

4. **Being too vague in Layer 2.** Architecture answers need code evidence. "The session system uses a database" is insufficient. "The session system writes to `sessions` table in `state.db` via `session_manager.py:34`" is actionable.

5. **Forgetting to offer "go deeper."** After any answer, invite follow-up: "Want me to dig into how [related component] works?"

6. **Treating Layer 1 as "dumbed down."** Layer 1 is simplified, not wrong. Don't say things that are technically incorrect just to be "easier to understand."

7. **Reading too little code.** For a nontrivial question, reading 5 lines is not enough. You need to understand the full flow — read the function, its caller, and its callees.

8. **Going Layer 2 without being asked.** If someone asks "what is tool calling," they probably want Layer 1. Don't jump into code unless they specifically ask about *this* Agent's implementation.

---

## Verification Checklist

- [ ] User's question is about Agent architecture/design → skill activated
- [ ] Correct layer identified: Layer 1 (concepts) vs Layer 2 (architecture)
- [ ] For Layer 1: answer is accurate but accessible, with analogy
- [ ] For Layer 2: source code was located via search_files before answering
- [ ] For Layer 2: at least 2-3 key files were read
- [ ] For Layer 2: file paths and line numbers are cited
- [ ] For Layer 2: no fabricated code references
- [ ] Answer ends with invitation for deeper follow-up
- [ ] If source code is inaccessible: transparent disclaimer given

---

## Reference Files

Load these for deeper context when teaching:

- `references/harness-engineering-glossary.md` — Standard glossary of Harness Engineering concepts, used for Layer 1 teaching
- `references/trigger-domain-reference.md` — Full trigger domain table with examples
- `references/hermes-agent-architecture-map.md` — Hermes-specific source directory layout, used for Layer 2 navigation (when running on Hermes)
