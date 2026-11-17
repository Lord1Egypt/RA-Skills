## Description:

Call management system with preparation, real-time capture, and follow-up tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pratilsudra](https://clawhub.ai/user/pratilsudra)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to prepare for calls, capture notes and decisions, track commitments, and draft follow-up messages while keeping call data local.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores and reads sensitive call notes, contact context, commitments, and follow-ups in local memory files.

Mitigation: Install only when local storage of this information is acceptable, and periodically review or delete stored call records that are no longer needed.

Risk: Some advertised workflows reference scripts that are not present in the reviewed artifact.

Mitigation: Confirm required workflow scripts are available before relying on capture, call closing, follow-up, history, or commitment-status workflows.

## Reference(s):

- [ClawHub skill page for call-pro](https://clawhub.ai/pratilsudra/skills/call-pro)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown and terminal-style text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference or summarize locally stored call notes, contacts, commitments, and follow-ups.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
