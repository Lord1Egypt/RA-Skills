## Description:

Normalize and classify noisy alerts by urgency, trust, audience, and duplicate status so an agent can recommend send-now, batch-later, ignore, suppress-as-duplicate, or escalate outcomes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wroadd](https://clawhub.ai/user/wroadd)

### License/Terms of Use:

MIT-0

## Use Case:

Operators, service owners, and developers use this skill to reduce alert fatigue, classify alert urgency, deduplicate repeated notifications, define digest and quiet-hours policies, and decide when an issue should be escalated.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Escalation and paging guidance could cause unnecessary interruptions if adopted without local thresholds.

Mitigation: Review severity thresholds, quiet-hours behavior, routing defaults, and escalation timers before using the policy operationally.

Risk: Alert examples or policy drafts could expose sensitive operational identifiers if copied from private environments.

Mitigation: Use abstract placeholders for responders, channels, endpoints, tokens, systems, and customer details in generated outputs.

## Reference(s):

- [Policy patterns for alert-triage](references/policies.md)
- [Worked examples for alert-triage](references/examples.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration, Guidance]

**Output Format:** [Markdown tables and concise bullet lists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include severity, confidence, audience, timing, rationale, suppression keys, and digest buckets.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
