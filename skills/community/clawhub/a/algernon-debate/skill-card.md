## Description:

Designs a structured trade-off debate mode for OpenAlgernon that challenges a user's position and ends with a balanced technical synthesis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[antoniovfranco](https://clawhub.ai/user/antoniovfranco)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and technical learners use this skill to practice design trade-off debates, defend an implementation choice, respond to opposing arguments, and produce an interview-ready synthesis of when each option is appropriate.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can query a specific local study database.

Mitigation: Use it only in an environment where that database path is expected, validate material slugs before querying, and prefer read-only database access.

Risk: Debate summaries and critiques may be sent to a configured Notion page.

Mitigation: Require explicit user confirmation before export and confirm the destination page is appropriate for the content.

Risk: Session notes may be persisted locally without clear consent.

Mitigation: Tell users when logging is enabled and avoid recording sensitive or unnecessary details.

Risk: User-derived Markdown may be passed through a shell command string.

Mitigation: Avoid shell-string interpolation for user content; pass content through a safer input channel or quote and escape it rigorously.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/antoniovfranco/skills/algernon-debate)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with debate prompts, counter-arguments, synthesis text, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include a Notion append command and a conversation-log entry when the configured local workflow is used.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
