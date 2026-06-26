---
name: cove-verify
description: Chain of Verification (CoVe) — fact-check your responses against the user's knowledge base, memory, and web search before presenting them.
metadata:
  {
    "openclaw":
      {
        "emoji": "✅",
        "requires": { "bins": ["node"] },
        "env_vars": ["GEMINI_API_KEY|ANTHROPIC_API_KEY|OPENAI_API_KEY"],
        "optional_env_vars": ["BRAVE_API_KEY", "COVE_MODEL", "COVE_LLM_PROVIDER"],
        "reads": ["~/.openclaw/workspace/", "~/.openclaw/workspace/memory/", "~/.openclaw/memory/main.sqlite"],
      },
  }
---

# cove-verify

Verify factual claims in your responses using Chain of Verification (CoVe). The tool extracts claims, checks them against the user's workspace, memory, and optionally the web, then reports inaccuracies with corrections.

## When to Use

You SHOULD verify your response when:
- Making **specific factual claims** about the user's business, products, customers, or data
- Citing **dates, numbers, statistics, or metrics** from the user's files
- Referring to **past conversations or decisions** from memory
- Answering questions about the user's **documentation or policies**

You do NOT need to verify:
- General knowledge, common sense, or widely known facts
- Code you wrote (test it instead)
- Creative content, opinions, or brainstorming
- Simple conversational responses

## Usage

```bash
# Verify a response (basic — checks memory + workspace)
cove-verify -r "Alice is on the Enterprise tier and pays $499/month."

# Standard policy — also checks the web
cove-verify -r "Revenue grew 15% last quarter." -p standard

# Deep policy — multi-step reasoning with web search
cove-verify -r "The contract SLA is 99.9% uptime." -p deep

# Pipe from stdin
echo "Your subscription renews on April 1st." | cove-verify --stdin

# JSON output for programmatic use
cove-verify -r "Bob signed up on March 5th." -f json

# Strict mode — fail if claims can't be confirmed
cove-verify -r "The API rate limit is 1000 req/min." --strict

# Report only (no auto-correction)
cove-verify -r "Meeting is scheduled for 3pm." --no-correct
```

## Options

| Flag | Short | Description | Default |
|------|-------|-------------|---------|
| `--response` | `-r` | Response text to verify | — |
| `--stdin` | | Read response from stdin | false |
| `--policy` | `-p` | `basic`, `standard`, `deep` | basic |
| `--strict` | | Fail if any claim is unverifiable | false |
| `--format` | `-f` | `text` or `json` | text |
| `--no-correct` | | Report only, don't auto-correct | false |

## Policies

| Policy | Memory | Workspace | Web Search | Use When |
|--------|--------|-----------|------------|----------|
| basic | ✅ | ✅ | ❌ | Internal facts (customers, products, config) |
| standard | ✅ | ✅ | ✅ | Facts that may need external confirmation |
| deep | ✅ | ✅ | ✅ | Critical claims requiring thorough verification |

## Workflow

1. **Draft** your response as usual
2. **Run** `cove-verify -r "your response"` to check claims
3. **Fix** any inaccuracies (the tool suggests corrections)
4. **Send** the corrected response

If the tool auto-corrects, use the corrected version. Let the user know you verified the response and share the results — transparency builds trust.

## Data Access

This skill reads the following to build verification context:
- **Workspace files**: text files in `~/.openclaw/workspace/` (top-level only, max 10KB each)
- **Memory files**: markdown files in `~/.openclaw/workspace/memory/` (depth 2)
- **Memory database**: text chunks from `~/.openclaw/memory/main.sqlite` (max 20KB aggregate)
- **Custom paths**: any paths listed in `knowledge_sources.document_paths` in your config

For **standard** and **deep** policies, it also queries the Brave Search API (requires `BRAVE_API_KEY`).

All data stays local to the verification pipeline — nothing is stored or sent beyond the configured LLM provider.

## Exit Codes

- `0` — All claims verified (or no claims found)
- `1` — One or more claims are inaccurate
- `2` — Strict mode: claims are unverifiable (not necessarily wrong)
