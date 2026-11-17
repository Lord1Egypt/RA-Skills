## Description:

Run a structured two-agent debate loop between ChatGPT and the user's own thoughts retrieved from Supabase Open Brain via MCP, iterating up to three rounds or until semantic agreement, then writing the final outcome back to Open Brain.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tvaloki](https://clawhub.ai/user/tvaloki)

### License/Terms of Use:


## Use Case:

Developers and power users use this skill to pressure-test decisions against recent Open Brain thoughts and context, then capture a structured debate outcome in memory.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads and persists Open Brain memory data through MCP and SQL access, which may expose private, business, or credential-like notes.

Mitigation: Use a least-privileged MCP or SQL role, review the data scope before installation, and disable persistence or runtime table creation if stored debate records are not needed.

Risk: When direct OpenAI API mode is enabled, retrieved memory content can be sent to an external model provider.

Mitigation: Avoid setting OPENAI_API_KEY unless external processing of memory content is acceptable, and prefer explicit --thoughts input when the debate should use a narrow context.

Risk: Debate outputs can contain incorrect or misleading reasoning that is then written back into memory.

Mitigation: Review generated outcomes before relying on them for decisions, and treat stored debate results as advisory context rather than authoritative conclusions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tvaloki/skills/dual-agent-debate)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [JSON command output with structured debate rounds, similarity scores, storage status, and setup guidance in Markdown documentation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call Open Brain MCP, OpenAI APIs, or an OAuth-backed local agent depending on environment configuration.]

## Skill Version(s):

0.3.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
