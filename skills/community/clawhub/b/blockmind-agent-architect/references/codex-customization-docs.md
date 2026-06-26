# OpenAI Codex Customization

## Source

- Canonical URL: https://openai.com/codex
- Related URL: https://platform.openai.com/docs/guides/codex

## Summary

OpenAI's Codex customization guidance is the main reference for making a repository legible to Codex over repeated sessions. The most visible mechanism is `AGENTS.md`. OpenAI describes it as the place to put persistent context that Codex cannot reliably infer from code alone: naming conventions, business rules, commands, known quirks, review expectations, and other repo-specific instructions. The practical point is that agent performance improves when important constraints live in a durable file rather than in one-off prompts.

Codex customization is broader than one markdown file. The official docs organize customization around repo guidance, rules, hooks, MCP, skills, and environment configuration. That matters because a well-structured agent repo separates stable policy from task-specific prompts. `AGENTS.md` carries the durable repo contract, while skills package repeatable workflows that need richer instructions, references, or scripts. This layered approach keeps the repository from turning into one giant prompt blob.

The docs and OpenAI guidance on real-world usage also emphasize how Codex reads and benefits from structured guidance files. Teams are encouraged to describe tasks as if they were well-scoped GitHub issues, to document canonical commands and module names, and to keep environment setup accurate so Codex can run builds and checks without guesswork. In practice, that means instructions should be concrete, file-path aware, and tied to the actual codebase instead of abstract principles alone.

The best practices that emerge are straightforward. Keep a single source of truth for business rules. Prefer explicit commands over implied workflows. Capture file paths, examples, and constraints where the agent will actually look. Use repo-local skills for recurring procedures that need more than a few bullet points. And keep the guidance current: stale agent instructions are just another form of bad data. For this repo, Codex customization is the basis for `AGENTS.md`, command discoverability, and the discipline of keeping knowledge artifacts in stable, agent-readable locations.
