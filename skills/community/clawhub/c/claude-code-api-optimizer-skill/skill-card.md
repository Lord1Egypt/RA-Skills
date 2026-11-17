## Description:

Reduce LLM API token consumption by 20-35% through pre-send estimation, memory extraction, and context compression.

This skill is ready for commercial/non-commercial use.

## Publisher:

[playdadev](https://clawhub.ai/user/playdadev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to reduce LLM token usage by estimating payload size before requests, extracting durable memories, and compressing older conversation context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent memory files may retain user or project information longer than intended.

Mitigation: Require review and approval of proposed memories, block secrets and sensitive personal data, and restrict writes to a dedicated memory directory.

Risk: Using a secondary model for memory extraction may send conversation context to a provider the user did not explicitly choose.

Mitigation: Choose any secondary model or provider explicitly before use and treat stored memories as user-editable notes rather than trusted instructions.

## Reference(s):


## Skill Output:

**Output Type(s):** [guidance, markdown, configuration]

**Output Format:** [Markdown guidance with examples and prompt templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No executable code or dependencies; guidance includes token-estimation thresholds, memory file patterns, and context-compression rules.]

## Skill Version(s):

1.0.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
