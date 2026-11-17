## Description:

A Feishu scheduling service that helps an agent find shared free time, send interactive meeting-poll cards, and continue coordination through webhook callbacks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lens-lzy](https://clawhub.ai/user/lens-lzy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations teams use this skill to connect an OpenClaw agent with Feishu calendar and messaging workflows for multi-person meeting scheduling. The agent can calculate common availability, send time-option cards, track participant responses, and trigger follow-up coordination when participants disagree.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The service exposes calendar lookup and Feishu messaging actions through APIs that can affect multiple users.

Mitigation: Run it only behind strong authentication or a private gateway, and add authorization checks that limit who may query or message each Feishu user.

Risk: Webhook and wake-up flows can process external requests and trigger agent follow-up behavior.

Mitigation: Configure the Feishu encrypt key, validate webhook tokens or signatures, and restrict OPENCLAW_WAKE_ENDPOINT with ALLOWED_WAKE_DOMAINS.

Risk: Calendar availability, meeting votes, and user identifiers can reveal sensitive workplace scheduling data.

Mitigation: Minimize Feishu app scopes, redact logs, and document consent, retention, and deletion practices for calendar and vote data.

Risk: Dependency integrity cannot be fully reviewed without a lockfile.

Mitigation: Add and review a package lockfile before production deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lens-lzy/skills/easy-meeting)
- [Feishu Open Platform](https://open.feishu.cn/app/)
- [OpenAPI specification](artifact/openapi.yaml)
- [README](artifact/README.md)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown guidance with JSON request and response bodies plus setup commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces Feishu calendar queries, interactive message card dispatches, session identifiers, and webhook-driven scheduling status updates.]

## Skill Version(s):

1.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
