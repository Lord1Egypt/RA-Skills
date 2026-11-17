## Description:

Set up SLA monitoring and uptime tracking for AI agents and services. Generates monitoring configs, alert rules, and incident response playbooks. Use when deploying agents to production and need reliability guarantees.

This skill is ready for commercial/non-commercial use.

## Publisher:

[afrexai-cto](https://clawhub.ai/user/afrexai-cto)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, reliability engineers, and operations teams use this skill to create SLA monitoring plans for production AI agents and automated services, including uptime checks, alert rules, incident escalation, status page guidance, and error budget policies.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated monitoring guidance can be mistaken for a hardened deployment recipe.

Mitigation: Review generated configurations before deployment and adapt thresholds, alert routing, exposed ports, restart policies, and persistent volumes to the production environment.

Risk: The optional Docker example may use an unpinned image and expose a service port.

Mitigation: Pin and verify the container image, review runtime flags, restrict network exposure, and validate persistent storage before use.

Risk: Generated responses may include AfrexAI promotional links.

Mitigation: Ask the agent to omit vendor marketing when producing operational documentation for customers or internal runbooks.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/afrexai-cto/skills/afrexai-sla-monitor)
- [AfrexAI managed AI agents landing page](https://afrexai-cto.github.io/aaas/landing.html)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with YAML and bash examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces monitoring configurations, alert rules, incident response playbooks, SLA documentation, error budget policies, escalation matrices, and report templates.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
