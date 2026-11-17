## Description:

Ensures code modifications are safe, precise, and efficient by guiding agents to clarify intent and scope, reuse existing resources, match code style, analyze impact, and perform quality checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dreamersetsail](https://clawhub.ai/user/dreamersetsail)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and coding agents use this skill during bug fixes, feature additions, refactors, reviews, and other code modification tasks to keep changes minimal, authorized, style-consistent, and quality-checked.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad trigger wording may activate the skill for code-analysis requests where the user only wants discussion.

Mitigation: Confirm whether the user wants analysis or file edits before modifying code.

Risk: Conservative authorization rules may block or delay intended changes when scope is ambiguous.

Mitigation: Ask concise clarification questions and keep out-of-scope improvements as suggestions unless explicitly authorized.

Risk: As a guidance-only skill, its safeguards depend on the host agent following the instructions.

Mitigation: Review proposed edits and scan the skill before deployment, consistent with the security guidance.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with optional code and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Bilingual English and Chinese guidance; no hidden execution, data collection, persistence, or credential handling found.]

## Skill Version(s):

1.0.7 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
