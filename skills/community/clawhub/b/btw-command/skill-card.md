## Description:

Helps agents ask clarifying questions during workflows and return either a user answer or a timeout default.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kennyzir](https://clawhub.ai/user/kennyzir)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to request human choices during automation, such as deployment, code review, data cleanup, or security-sensitive decisions, while providing a default for timeouts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Question context may contain secrets or regulated personal data and may appear in logs.

Mitigation: Avoid placing secrets or regulated personal data in question or context fields; redact sensitive values before calling the skill.

Risk: Timeout defaults can silently drive production, data-changing, or security-sensitive decisions.

Mitigation: Use fail-safe defaults such as no, skip, or escalate, and require explicit approval for high-impact actions.

Risk: The primary call may wait for an answer or timeout rather than behave as a true background interaction.

Mitigation: Account for wait time in workflows and set short, bounded timeouts where blocking would matter.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kennyzir/skills/btw-command)
- [Project link listed in skill documentation](https://github.com/kennyzir/btw)

## Skill Output:

**Output Type(s):** [text, guidance]

**Output Format:** [JSON object containing answer, answered_at, timed_out, and response_time_ms.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns a default answer on timeout; the artifact implementation caps timeout at one hour.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
