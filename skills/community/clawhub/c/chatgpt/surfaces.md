# ChatGPT Surface Routing

Pick the lightest surface that fits the job. Most ChatGPT problems are routing problems before they are prompting problems.

## Decision Table

| Surface | Best For | Avoid When | Strong Signal |
|---------|----------|------------|---------------|
| Standard chat | Fast one-off asks, short iterations, casual drafting | Long projects with many files or decisions | User needs speed more than memory |
| Temporary Chat | Sensitive work, one-off experiments, contamination recovery | Ongoing work that should persist | User wants clean context and low carryover |
| Projects | Multi-turn work with shared files, repeated revisions, durable context | Tiny tasks that will end in one or two turns | There is a file set, a brief, and a decision trail |
| Custom instructions | Stable preferences that should affect many future chats | Temporary goals, single projects, or volatile requirements | Same preference keeps being repeated across sessions |
| GPTs | Narrow recurring jobs with a fixed role, instructions, and optional tools | Broad general-purpose help or rapidly changing needs | The workflow can be packaged and reused by name |

## Routing Heuristics

- Start with standard chat unless memory or files clearly matter.
- Move to Temporary Chat when stale context, privacy, or experimentation make persistence a liability.
- Move to Projects when the user says "keep these files together," "continue this later," or "stop losing decisions."
- Use custom instructions only for defaults that should survive unrelated tasks.
- Build or recommend a GPT only after the workflow is stable enough to package.

## Search and Freshness

- If the task needs current facts, tell the user to use ChatGPT's web-enabled workflow or to verify externally.
- Do not treat remembered Project context as proof of freshness.
- Separate "current facts" from "stable internal brief" in the prompt packet.

## Fast Recovery Rule

When a chat feels contaminated:
1. Stop continuing the same thread.
2. Rebuild the source of truth in a fresh surface.
3. Paste only the active brief, needed files, and output contract.

Switching surfaces is often faster than over-correcting a broken conversation.
