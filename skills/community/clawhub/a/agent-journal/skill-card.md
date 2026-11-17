## Description:

Gives AI agents a persistent journal backed by BlueColumn semantic memory for logging and recalling observations, decisions, user preferences, and notable events across sessions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bluecolumnconsulting-lgtm](https://clawhub.ai/user/bluecolumnconsulting-lgtm)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to persist selected session context, preferences, decisions, and follow-up information so agents can recall it in later sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: External persistent memory may store user and session details without clear consent, redaction, retention, or deletion controls.

Mitigation: Use explicit consent before storing entries, avoid secrets or regulated data, review summaries before submission, and confirm how memories can be inspected, corrected, deleted, and how the API key can be revoked.

## Reference(s):

- [BlueColumn API Reference](references/api.md)
- [BlueColumn official docs](https://bluecolumn.ai)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with curl command examples and JSON request/response shapes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a BlueColumn bc_live_* API key and sends selected journal content to BlueColumn's external service.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
