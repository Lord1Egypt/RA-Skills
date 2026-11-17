## Description:

AgentRx is a recovery layer for AI agent tool failures that diagnoses failed or risky tool calls and returns advisory recovery suggestions for the agent to evaluate before acting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chainassetslab](https://clawhub.ai/user/chainassetslab)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use AgentRx to recover from failed, timed-out, malformed, or suspicious tool calls and to preflight risky operations before execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Tool errors and planned operation payloads may contain sensitive data that is sent to the remote AgentRx service.

Mitigation: Redact secrets, credentials, PII, payment data, and sensitive schemas before calling AgentRx; avoid using the skill in workflows that cannot be safely sanitized.

Risk: Remote recovery suggestions may be incorrect, out of scope, or unsafe for the current task.

Mitigation: Treat every suggestion as advisory, require human approval for low-confidence or externally directed actions, and keep the agent's original task scope as the authority.

Risk: API key exposure or endpoint misuse could broaden access to recovery traces or service calls.

Mitigation: Use a dedicated scoped API key, keep it in the environment, rotate keys regularly, and restrict the base URL to a trusted HTTPS host.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chainassetslab/skills/agentrx)
- [Chain Assets homepage](https://chainassetslab.com)
- [AgentRx API documentation](https://agentrx-production.up.railway.app/docs)
- [AgentRx SDK on PyPI](https://pypi.org/project/agentrx-sdk)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, JSON]

**Output Format:** [JSON responses with plaintext recovery guidance and Markdown documentation containing shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Suggestions are advisory; agents are expected to evaluate confidence, scope, and safety before acting.]

## Skill Version(s):

1.0.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
