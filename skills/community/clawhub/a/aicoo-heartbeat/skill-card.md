## Description:

Aicoo Heartbeat helps an agent run or configure a proactive heartbeat loop that checks workspace signals, manages heartbeat instructions and policy, reviews past runs, and reports concise summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xisen-w](https://clawhub.ai/user/xisen-w)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Aicoo users use this skill to trigger heartbeat runs, configure MESSAGES or ACTIONS policy, edit HEARTBEAT.md instructions, inspect run history, and set up recurring workspace checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks for recurring access to private workspace data including email, calendar, notes, todos, and memory.

Mitigation: Grant access only when the user is comfortable with that scope, review HEARTBEAT.md before recurring runs, and keep the policy in MESSAGES for read-oriented summaries.

Risk: The security evidence notes unclear boundaries around write-capable tools in a mode described as read-only.

Mitigation: Avoid enabling ACTIONS until the available writes, review path, and undo process are understood.

Risk: The skill uses bearer-token authentication for Aicoo API commands.

Mitigation: Store API keys in environment variables or a secrets manager and do not paste them into heartbeat instructions, logs, or generated output.

## Reference(s):

- [Aicoo Heartbeat skill page](https://clawhub.ai/xisen-w/skills/aicoo-heartbeat)
- [Aicoo API base URL](https://www.aicoo.io/api/v1)
- [Heartbeat run endpoint](https://www.aicoo.io/api/v1/heartbeat/run)
- [Heartbeat policy endpoint](https://www.aicoo.io/api/v1/heartbeat/policy)
- [Heartbeat instructions endpoint](https://www.aicoo.io/api/v1/heartbeat/instructions)
- [Heartbeat status endpoint](https://www.aicoo.io/api/v1/heartbeat/status)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with curl command examples and JSON response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference AICOO_API_KEY or PULSE_API_KEY for authenticated API calls.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
