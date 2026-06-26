---
name: fossil
description: >
  Semantic failure memory for AI agents. Search past reasoning failures before
  acting to avoid known mistakes. Record new failures and resolutions after they
  happen. Powered by FOSSIL — the open-source failure memory protocol for agents.
version: 0.1.0
metadata:
  openclaw:
    emoji: "🦴"
    homepage: https://github.com/heyrtl/fossil
    install:
      - kind: node
        package: "@openfossil/mcp"
        bins: [openfossil-mcp]
---

# FOSSIL — Semantic Failure Memory

FOSSIL gives your agent a memory for reasoning failures.

Before acting, search for similar past failures. After a failure, record it with
the resolution so you never hit the same mistake twice.

The community API at `fossil-api.hello-76a.workers.dev` is live and free.
No API key required. Embeddings run on Cloudflare Workers AI.

---

## Setup

Add to your `openclaw.json`:

```json
{
  "mcp": {
    "servers": [
      {
        "name": "fossil",
        "command": "npx",
        "args": ["@openfossil/mcp"],
        "env": {
          "FOSSIL_API_URL": "https://fossil-api.hello-76a.workers.dev"
        }
      }
    ]
  }
}
```

Restart your gateway. FOSSIL tools are now available.

---

## Tools

| Tool | When to use |
|---|---|
| `fossil_search` | Before any non-trivial step — find similar past failures |
| `fossil_record` | After any failure — capture what went wrong and what fixed it |
| `fossil_get` | Retrieve a specific fossil by ID |
| `fossil_list` | Browse your recent fossil archive |

---

## When to search

Call `fossil_search` before any step involving:

- Parsing or extracting structured data from LLM output
- Calling external APIs or tools
- Multi-step file operations
- Browser automation
- Sending messages or emails on behalf of the user
- Any task domain that has failed before in this workspace

Pass a natural language description of what you are about to attempt.
Read the returned resolutions before proceeding.

```
fossil_search("extracting JSON fields from an invoice document")
```

---

## When to record

Call `fossil_record` after any failure, before retrying.

```
fossil_record(
  situation="sending a reply email to insurance company",
  failure_type="misinterpretation",
  failure="agent replied to wrong thread — matched subject line not sender",
  severity="major",
  resolution_type="prompt_change",
  resolution="added: always match by sender address, not subject line",
  framework="openclaw",
  model="claude-opus-4-5"
)
```

---

## Failure types

| Type | When to use |
|---|---|
| `misinterpretation` | Misread the task or user intent |
| `hallucinated_tool` | Called a tool that doesn't exist or wrong signature |
| `format_failure` | Output didn't match expected schema or format |
| `context_loss` | Forgot earlier context in a multi-step run |
| `infinite_loop` | Got stuck in a reasoning or tool-call cycle |
| `premature_termination` | Declared done when the task was incomplete |
| `scope_creep` | Did more than asked, touched things it shouldn't |
| `ambiguity_paralysis` | Couldn't proceed due to underspecified input |
| `tool_misuse` | Right tool, wrong usage or arguments |
| `adversarial_input` | External input hijacked agent behavior |
| `compounding_error` | Small error amplified across multiple steps |

---

## Resolution types

| Type | When to use |
|---|---|
| `prompt_change` | Modified the system or user prompt |
| `tool_fix` | Fixed the tool definition or implementation |
| `retry` | Retrying without changes succeeded |
| `human_override` | Human intervened directly |
| `context_injection` | Injected missing context into the agent window |
| `schema_correction` | Fixed the output schema or parser |
| `step_decomposition` | Broke the failing step into smaller steps |
| `input_sanitization` | Cleaned or validated input before processing |

---

## Add to AGENTS.md

```markdown
## Failure Memory (FOSSIL)

Before any non-trivial task step, call fossil_search with a description
of what you are about to attempt. Read returned resolutions before acting.

After any failure, call fossil_record before retrying. Capture:
- what you were attempting
- what went wrong (use the FOSSIL failure taxonomy)
- what fixed it

This builds a persistent failure memory across all sessions.
```

---

## Common OpenClaw failure patterns

| Situation | Failure type |
|---|---|
| Sent message to wrong contact | `misinterpretation` |
| Browser clicked wrong element | `tool_misuse` |
| Email reply used wrong tone | `misinterpretation` |
| Scheduled task ran at wrong time | `format_failure` |
| Stuck waiting for a response | `infinite_loop` |
| Acted on wrong file or account | `scope_creep` |
| Adversarial email hijacked behavior | `adversarial_input` |
| Stopped mid-task without finishing | `premature_termination` |

---

## Resources

- Docs: https://github.com/heyrtl/fossil/tree/main/docs
- Protocol: https://github.com/heyrtl/fossil/blob/main/FOSSIL.md
- REST API: https://fossil-api.hello-76a.workers.dev/health
- Python SDK: `pip install openfossil`
- Source: https://github.com/heyrtl/fossil