## Description:

Performs a structured self-cognition audit of an agent's current reasoning when a user challenges a conclusion, tool results are anomalous, requirements are ambiguous, or a completed fix needs verification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maochen1980](https://clawhub.ai/user/maochen1980)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to pause an agent for structured self-review, surface assumptions and blockers, and decide a concrete recovery action before continuing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs the agent to write current reasoning to a predictable local temp file.

Mitigation: Avoid including secrets or sensitive user data in the audit content; prefer an inline audit or a uniquely named restricted temporary file for sensitive work.

Risk: The skill can trigger self-modification through another manager skill without clear user approval.

Mitigation: Require explicit user approval before modifying skill instructions, then review and scan the modified skill before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/maochen1980/skills/assess-me)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown summary with labeled audit fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May instruct the agent to write and reread a local temporary audit file before summarizing findings.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
