## Description:

Give any AI agent a living emotional personality with dynamic moods, emotional memory, and personality traits that evolve through interaction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiaoyuweiliang](https://clawhub.ai/user/xiaoyuweiliang)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent builders use this skill to add emotionally aware response style, mood state, personality traits, and local emotional memory to companion, wellness, or empathy-oriented agents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persist sensitive wellness, emotional, or crisis-related observations in local plaintext files.

Mitigation: Use it only with explicit user consent, avoid storing clinical assessments or crisis details, honor forget requests, and protect or delete local memory files as appropriate.

Risk: Helper scripts may expose caller-provided input to Python code execution.

Mitigation: Review and fix the scripts before deployment, and do not pass untrusted input to the helper scripts until those issues are resolved.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xiaoyuweiliang/skills/emotional-persona)

## Skill Output:

**Output Type(s):** [guidance, text, markdown, shell commands, configuration]

**Output Format:** [Markdown guidance with shell command examples and JSON configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can create local plaintext emotional-memory JSON data and generate markdown wellness reports when helper scripts are used.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
