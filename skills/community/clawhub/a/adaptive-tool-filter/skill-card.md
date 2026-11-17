## Description:

Adaptive Tool Filter helps agents identify task intent and prioritize a smaller set of relevant tools to reduce tool-list token overhead.

This skill is ready for commercial/non-commercial use.

## Publisher:

[paibwhgs](https://clawhub.ai/user/paibwhgs)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators can use this skill as guidance for configuring intent-based tool filtering, prioritizing relevant tools, and reducing prompt overhead during agent conversations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad keyword rules could make sensitive tools such as shell execution, messaging, subagents, or business-document actions available in contexts where they are not appropriate.

Mitigation: Review and tighten the intent-to-tool rules before deployment, and require explicit approval for sensitive actions such as command execution and file edits.

Risk: The artifact is guidance for influencing tool selection, so behavior depends on the host runtime implementing the filtering rules correctly.

Mitigation: Validate the runtime integration with representative requests before relying on the skill for production tool filtering.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/paibwhgs/skills/adaptive-tool-filter)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Configuration, Guidance]

**Output Format:** [Markdown guidance with Python and JSON snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language guidance; no executable payload, persistence, or hidden data flow found in security evidence.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
