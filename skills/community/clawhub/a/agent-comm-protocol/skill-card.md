## Description:

Standard protocol for reliable task dispatch, status reporting, and result feedback with confirmation, retry, and logging between agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nancliu](https://clawhub.ai/user/nancliu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to standardize inter-agent task handoff, progress reporting, completion feedback, timeout handling, and exception reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Communication logs may persist sensitive task details, secrets, tokens, personal data, or confidential information if users include them in messages.

Mitigation: Configure file permissions, redaction, path validation, and retention controls before using the logging convention, and avoid including secrets or confidential data in agent messages.

Risk: Protocol timeouts and retries can create duplicate or stale task messages if recipients process delayed messages without checking status.

Mitigation: Use the confirmation, status tracking, retry limit, and exception-reporting steps together so operators can identify failed, delayed, or repeated handoffs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nancliu/skills/agent-comm-protocol)
- [Publisher profile](https://clawhub.ai/user/nancliu)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, configuration]

**Output Format:** [Markdown protocol templates and concise operating guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes message templates, timeout thresholds, retry counts, flow steps, and a local communication-log path convention.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
