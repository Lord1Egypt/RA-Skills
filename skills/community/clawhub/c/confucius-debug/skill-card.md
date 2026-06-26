## Description: <br>
Confucius Debug searches the YanHui Knowledge Base for instant debugging fixes or analyzes new errors with Confucius AI across OpenClaw, Claude Code, MCP, Telegram, Discord, Docker, and other platforms. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sstklen](https://clawhub.ai/user/sstklen) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineers use this skill to search a debugging knowledge base for existing fixes, request AI analysis for new errors, and prepare unresolved issues for follow-up research. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Debugging queries, identifiers, logs, environment details, or project structure may be sent to api.washinmura.jp. <br>
Mitigation: Redact tokens, API keys, customer data, internal URLs, private paths, stack traces with secrets, and proprietary code details before using search, analyze, escalate, or contribute. <br>
Risk: Escalation and contribution flows can submit additional context that may be stored for future knowledge-base use. <br>
Mitigation: Use a non-sensitive CONFUCIUS_LOBSTER_ID and review exactly what logs, environment details, and descriptions will be submitted before escalating or contributing. <br>


## Reference(s): <br>
- [Confucius Debug ClawHub Page](https://clawhub.ai/sstklen/confucius-debug) <br>
- [Confucius Debug Homepage](https://api.washinmura.jp/confucius) <br>
- [Confucius Debug API](https://api.washinmura.jp/api/v2/debug-ai) <br>
- [Confucius Debug MCP Endpoint](https://api.washinmura.jp/mcp/debug) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and terminal text with JSON API examples and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search and analysis results may include root-cause summaries, fix descriptions, patch text, confidence values, and setup guidance.] <br>

## Skill Version(s): <br>
2.0.2 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
