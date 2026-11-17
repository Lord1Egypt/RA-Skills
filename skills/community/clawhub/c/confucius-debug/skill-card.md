## Description:

AI debugging assistant that never repeats a mistake. Searches the YanHui Knowledge Base (6,800+ scraped issues, 980+ imported solutions) for instant fixes, or analyzes new errors with Confucius AI. Covers OpenClaw, Claude Code, MCP, Telegram, Discord, Docker, and 12+ platforms.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sstklen](https://clawhub.ai/user/sstklen)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to search a debugging knowledge base, request AI analysis for unresolved errors, and contribute fixes for future reuse. It is aimed at agent and integration debugging across OpenClaw, Claude Code, MCP, Codex, Docker, Telegram, Discord, and related platforms.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send debugging text, identifiers, logs, environment details, and project structure to api.washinmura.jp during analysis or escalation.

Mitigation: Use it only where that external sharing is acceptable; redact confidential, production, regulated, or secret-bearing information before submitting payloads.

Risk: The release security verdict is suspicious because the workflow promotes broad automatic third-party debugging requests and understates diagnostic context sharing.

Mitigation: Review before installing, avoid automatic use on sensitive errors, and explicitly approve the exact payload before analysis or escalation.

## Reference(s):

- [Confucius Debug API Homepage](https://api.washinmura.jp/confucius)
- [Confucius Debug ClawHub Page](https://clawhub.ai/sstklen/skills/confucius-debug)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and terminal text with JSON API responses, shell commands, configuration snippets, and optional patch text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and jq for bundled shell scripts; CONFUCIUS_LOBSTER_ID is required for analysis and contribution workflows and optional for search attribution.]

## Skill Version(s):

2.0.2 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
