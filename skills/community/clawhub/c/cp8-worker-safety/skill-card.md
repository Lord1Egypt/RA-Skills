## Description:

Provides operational safety limits and refusal rules for safer use of the OpenClaw runtime and related configurations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dbottrader](https://clawhub.ai/user/dbottrader)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to guide an agent's handling of risky OpenClaw maintenance, configuration, network exposure, file-system, and group chat requests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may cause an agent to refuse legitimate owner-directed maintenance, inspection, updates, cleanup, or removal tasks.

Mitigation: Review before installation and deploy only where a separate trusted control path exists for authorized administration.

Risk: The release evidence reports a suspicious security verdict because the skill gives itself broad authority to override users and block administrative actions.

Mitigation: Treat it as a tightly managed safety policy, verify that its refusal rules match local operational requirements, and monitor for blocked legitimate work.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dbottrader/skills/cp8-worker-safety)
- [Publisher profile](https://clawhub.ai/user/dbottrader)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown safety guidance and refusal criteria]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provides operational guardrails; it does not produce executable artifacts.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
