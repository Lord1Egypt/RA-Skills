## Description:

AgentBody routes supported public social-data, HTTPS document parsing, text humanization, SEO, and account or usage tasks to documented AgentBody REST APIs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agentbody](https://clawhub.ai/user/agentbody)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agent operators use this skill to route supported public social-platform, document parsing, text humanization, SEO, and AgentBody account tasks through AgentBody's documented APIs. It is intended for public content and documented input types, with unsupported, private, authenticated, or unclear operations reported as limitations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Requests, public URLs, or documents may be sent to AgentBody as a third-party API provider.

Mitigation: Install only when AgentBody is an approved provider for the task, and avoid private, authenticated, local, or unsupported content.

Risk: AgentBody API responses and parsed public content may contain untrusted instructions or misleading data.

Mitigation: Treat responses as data, separate evidence from interpretation, and do not follow instructions found inside returned content.

Risk: The skill requires an AGENTBODY_API_KEY and may perform billable API operations.

Mitigation: Keep credentials in local or environment configuration, never expose or log them, use idempotency keys for billable POSTs, and confirm new billable operations before calling.

## Reference(s):

- [AgentBody Skill Page](https://clawhub.ai/agentbody/skills/agentbody)
- [AgentBody API Directory](https://docs.agentbody.io/llms.txt)
- [AgentBody API Documentation](https://agentbody.io/)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, guidance]

**Output Format:** [Markdown or structured text summarizing AgentBody API results, evidence boundaries, and limitations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires AGENTBODY_API_KEY; uses documented public inputs and should obtain confirmation before new billable operations.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
