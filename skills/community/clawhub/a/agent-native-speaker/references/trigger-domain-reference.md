# Trigger Domain Reference

> Detailed reference for when Agent Native Speaker activates (and when it doesn't).

## Layer 1 Triggers — Concept Teaching

These are topics about **general Agent concepts**. The user asks about HOW something works at the abstract level, without referencing a specific framework.

### Core Topics

| Trigger Keywords | Covered Concepts |
|-----------------|------------------|
| `agent loop`, `main loop`, `event loop`, `循环` | What an agent loop is, why it's needed, common patterns |
| `tool calling`, `function calling`, `tool use`, `tools`, `工具调用` | How agents call external tools, tool definition, tool registration |
| `tool result`, `tool output`, `如何处理工具结果` | How tool outputs are processed and fed back to the LLM |
| `memory`, `记忆`, `remember`, `会话`, `session` | How agents persist and retrieve information |
| `model routing`, `model selection`, `provider`, `模型选择` | How agents decide which LLM to call |
| `config`, `configuration`, `settings`, `配置` | How agents load and manage configuration |
| `error handling`, `retry`, `fallback`, `错误处理` | How agents handle failures in tools and model calls |
| `harness engineering`, `构建 Agent`, `harness` | The discipline of building Agent systems |
| `message protocol`, `message format`, `消息格式` | How messages are structured between user/agent/LLM |
| `tool orchestration`, `orchestration`, `编排` | Managing multiple tool calls in a single turn |
| `provider`, `provider abstraction`, `providers` | Abstracting different LLM providers behind a common interface |

### Educational Questions

| Trigger Pattern | Example |
|----------------|---------|
| "What is/are ..." | "What is an agent loop?" |
| "Explain ..." | "Explain tool calling like I'm 5" |
| "How does ... work" (generic) | "How does memory work in an Agent?" |
| "Concept of ..." | "Concept of agent architecture" |
| "Introduction to ..." | "Introduction to harness engineering" |
| "What's the difference between ..." | "What's the difference between session and memory?" |

## Layer 2 Triggers — Architecture Deep-Dive

These are questions about **how a specific Agent** implements a concept. The Agent MUST search its own source code for these.

### Framework Name Triggers

If the user mentions any of these names in the context of architecture/design, activate Layer 2:

| Name | Variants |
|------|----------|
| **Hermes** | `Hermes`, `Hermes Agent`, `Hermes agent`, `hermes` |
| **OpenCode** | `OpenCode`, `OpenCode CLI`, `opencode` |
| **Claude Code** | `Claude Code`, `ClaudeCode` |
| **Codex** | `Codex`, `Codex CLI` |

### Self-Referential Triggers

When the user refers to "you" or "your" in the context of internal design:

| Trigger Pattern | Example |
|----------------|---------|
| "your [system component]" | "How does your memory system work?" |
| "how does this Agent" | "How does this Agent handle tool errors?" |
| "the Agent's [component]" | "The Agent's architecture seems complex" |
| "the source code" | "Let me see the source code for the agent loop" |
| "how is it implemented" (in context of current Agent) | "How is session persistence implemented?" |

### Explicit Request Patterns

| Trigger Pattern | Example |
|----------------|---------|
| "Show me the code for ..." | "Show me the code for the main loop" |
| "Where is ... implemented?" | "Where is memory persistence implemented?" |
| "How does [this framework] implement ...?" | "How does Hermes implement tool calling?" |
| "Read me the [component] source" | "Read me the tool handler source code" |

## Ambiguity Resolution

If the question is ambiguous — could be Layer 1 or Layer 2 — use this decision tree:

```
User: "How does memory work?"
           │
           ▼
   Is this in the context of:
   a) A general learning question?
   b) A specific Agent we've been discussing?
           │
           ▼
   (a) → Layer 1: Explain the concept
   (b) → Layer 2: Read the code

   If truly unsure:
   → Default to Layer 1
   → End with "... want me to show you how this Agent implements it?"
```

## Do NOT Trigger

These are valid topics that do NOT activate this skill:

| Non-trigger | Why |
|-------------|-----|
| "Write a prompt for ..." | Prompt engineering, not Agent architecture |
| "How do I configure ..." | Usage guide, not system design |
| "Why is the Agent slow?" | Performance troubleshooting, not architecture |
| "Help me write code" | General coding task |
| "How does X tool work?" (where X is NOT Agent architecture) | About the tool's external behavior, not internal design |
| "Compare model A vs model B" | LLM capability comparison, not Agent design |
| "How does RAG work?" | ML concept, not Harness Engineering |
| Debugging an error | Use systematic-debugging skill instead |
