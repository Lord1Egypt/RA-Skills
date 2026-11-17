## Description:

An end-to-end delivery skill for Forward Deployed Engineers, solution architects, and enterprise AI POC teams. It combines one delivery router with eight independently runnable specialist modules to turn ambiguous customer needs into evidence, a POC charter, an acceptance-ready PRD, deployment architecture, an Agent Skill, POC evidence, adoption and value conclusions, and reusable delivery assets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xukun0821](https://clawhub.ai/user/xukun0821)

### License/Terms of Use:

MIT-0

## Use Case:

Forward Deployed Engineers, solution architects, and enterprise AI POC teams use this skill to route ambiguous customer work through discovery, chartering, PRD handoff, architecture, skill design, POC execution, adoption review, and productization. It is intended for delivery planning, audit, evidence tracking, and reusable asset creation rather than automatic customer commitments or production approval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The demo scaffold can turn untrusted project text into executable local JavaScript.

Mitigation: Use trusted or sanitized POC names, scenarios, and project IDs; inspect generated server.js and index.html before running them; and keep generated POC work in a disposable directory without secrets.

Risk: The delivery workflow can produce recommendations that may be mistaken for customer approval, production readiness, or business-value proof.

Mitigation: Require human review and explicit customer or risk-owner confirmation before treating POC success, production readiness, adoption, or business value as established.

## Reference(s):

- [FDE Delivery Loop](SKILL.md)
- [FDE Delivery Router](fde-delivery-router/MODULE.md)
- [FDE Problem Discovery](fde-problem-discovery/MODULE.md)
- [FDE POC Engagement Charter](fde-engagement-charter/MODULE.md)
- [FDE PRD Writer](fde-prd-writer/MODULE.md)
- [FDE Deployment Architecture](fde-deployment-architect/MODULE.md)
- [FDE Agent Skill Designer](fde-agent-skill-designer/MODULE.md)
- [FDE POC Run and Validation](fde-poc-runner/MODULE.md)
- [FDE Adoption and Value](fde-adoption-and-value/MODULE.md)
- [FDE Playbook Productizer](fde-playbook-productizer/MODULE.md)
- [ClawHub Skill Page](https://clawhub.ai/xukun0821/skills/fde-delivery-loop)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, structured delivery packages, optional code/configuration files, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are evidence-oriented and stage-specific; deterministic scripts provide structure checks but do not replace human review, customer authorization, or production governance.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
