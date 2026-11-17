## Description:

Paste an agent job, cron, routing, or run summary and get an immediate read-only audit of possible routing, retry, fallback, or model-assignment waste.

This skill is ready for commercial/non-commercial use.

## Publisher:

[choosenobody](https://clawhub.ai/user/choosenobody)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to review agent routing, cron, retry, fallback, and model-assignment evidence for avoidable token or cost waste before making manual production changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may paste operational routing logs, cron evidence, or run summaries that contain secrets or sensitive payloads.

Mitigation: Redact secrets and sensitive payloads before using the skill; the release security guidance explicitly calls for redaction before installation or use.

Risk: Routing or cost-saving recommendations could be applied too quickly and disrupt production jobs.

Mitigation: Keep the audit read-only and require manual verification before modifying, disabling, rescheduling, or changing model routing policies.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/choosenobody/skills/agent-routing-waste-audit)
- [Hermes Cron List Examples](artifact/references/hermes-cron-examples.md)
- [Hermes Cron List Basic Example](artifact/references/hermes-cron-list-basic-example.md)
- [Hermes Cron List Basic Example Output](artifact/examples/hermes-cron-list-basic.md)

## Skill Output:

**Output Type(s):** [analysis, markdown, guidance]

**Output Format:** [Markdown audit with ranked findings, evidence used, missing evidence, manual verification steps, and a safe copy-paste prompt]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only by default; asks for the single most useful missing input when evidence is insufficient.]

## Skill Version(s):

1.2.2 (source: release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
