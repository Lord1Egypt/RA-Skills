## Description:

Generate a tailored incident response plan for AI agent deployments and SaaS operations, covering detection, triage, containment, recovery, and post-mortem.

This skill is ready for commercial/non-commercial use.

## Publisher:

[afrexai-cto](https://clawhub.ai/user/afrexai-cto)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, security operators, and SaaS teams use this skill to draft incident response playbooks for production AI agent services, including severity classification, alerting, containment, recovery, customer communication, and post-mortem procedures.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Incident response plans may recommend high-impact operational actions such as credential rotation, failover, or customer notification.

Mitigation: Have a qualified operator review and approve high-impact actions before using the plan in production.

Risk: Planning prompts may include sensitive operational context or incident details.

Mitigation: Provide only the context needed to draft the plan, and avoid pasting real API keys, credentials, or confidential incident details.

## Reference(s):

- [Skill README](artifact/README.md)
- [ClawHub skill page](https://clawhub.ai/afrexai-cto/skills/afrexai-incident-response-plan)
- [AfrexAI](https://afrexai.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown incident response plan with checklists, matrices, templates, and runbook guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Tailored to user-provided service, environment, data sensitivity, team, SLA, integrations, and compliance context.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
