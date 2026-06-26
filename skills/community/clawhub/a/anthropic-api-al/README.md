# Anthropic (Claude) API Skill

This skill teaches an agent **how and when** to use the Anthropic Claude API well — correctly, safely, and cost-consciously. It complements the **Anthropic MCP server**, which provides the actual callable tools.

> **Cost awareness.** Claude calls are **billed per token**. The skill's central guidance is: pick the cheapest capable model (default **Haiku**), always set `max_tokens`, cache repeated context, and batch bulk work.

---

## What's here

| File | Purpose |
|------|---------|
| [SKILL.md](SKILL.md) | The main skill (20 numbered sections). Start here. |
| [reference/models.md](reference/models.md) | Model families, cost/quality, context windows, when to use each. |
| [reference/endpoints.md](reference/endpoints.md) | The four MCP tools and the endpoints they map to. |
| [reference/parameters.md](reference/parameters.md) | Messages parameters (`max_tokens`, `system`, `tools`, `thinking`, …). |
| [reference/common-errors.md](reference/common-errors.md) | Error envelope, status codes, reactions. |
| [reference/best-practices.md](reference/best-practices.md) | Model choice, caching, batches, tool use, security. |
| [recipes/chat-completion.md](recipes/chat-completion.md) | Recipe: simple chat. |
| [recipes/tool-use.md](recipes/tool-use.md) | Recipe: tool/function calling loop. |
| [recipes/vision-analysis.md](recipes/vision-analysis.md) | Recipe: image analysis. |
| [prompts/model-selection.md](prompts/model-selection.md) | Reusable prompt: choose the cheapest viable model. |
| [prompts/cost-control.md](prompts/cost-control.md) | Reusable prompt: enforce cost discipline. |
| [tests/skill-evaluation.md](tests/skill-evaluation.md) | Evaluation checklist. |
| [tests/failure-cases.md](tests/failure-cases.md) | Bad behaviors + corrected versions. |

---

## Relationship to the MCP server

- **MCP server** = the runtime that exposes `anthropic_messages`, `anthropic_count_tokens`, `anthropic_models`, `anthropic_request`. See [../mcp/README.md](../mcp/README.md).
- **Skill** = the knowledge that makes the agent use those tools well.

Install both: the MCP gives the agent the ability to call Claude; this skill gives it the judgment.

---

## Quick start for an agent

1. Read [SKILL.md](SKILL.md).
2. Default to `claude-haiku-4-5`; escalate only when quality requires it.
3. Always set `max_tokens`.
4. Use [recipes/](recipes/) for concrete patterns.
5. Apply [reference/common-errors.md](reference/common-errors.md) on failures.

> Verification needed: confirm current models and pricing at https://docs.anthropic.com/en/api
