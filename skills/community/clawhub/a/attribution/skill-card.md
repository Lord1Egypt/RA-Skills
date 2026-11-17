## Description:

Helps agents choose, interpret, and reconcile marketing attribution models and guide first-party attribution patterns for connecting marketing touches to conversions and revenue.

This skill is ready for commercial/non-commercial use.

## Publisher:

[coreyhaines31](https://clawhub.ai/user/coreyhaines31)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing, growth, analytics, and revenue teams use this skill to understand which channels are likely driving conversions and revenue, compare attribution approaches, and reconcile conflicting numbers across ad platforms, web analytics, CRM, and self-reported sources. Developers may also use it for guidance on first-party attribution patterns when they control the site or app.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: First-party attribution guidance can touch consent, privacy notices, data retention, and vendor agreements.

Mitigation: Confirm consent requirements, notice coverage, retention limits, and vendor agreements before implementing the tracking pattern.

Risk: Passing identified user values through third-party URLs can expose PII or corrupt identity merges.

Mitigation: Only pass anonymous IDs, reject PII-shaped values, fail closed when identity state is ambiguous, and avoid logging emails.

Risk: Webhook-based attribution stitching can fail or merge data incorrectly if inputs are not validated.

Mitigation: Verify webhook signatures, validate smuggled IDs, bound analytics calls with timeouts, make analytics failures non-fatal, and test with real conversion flows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/coreyhaines31/skills/attribution)
- [Attribution Models](references/attribution-models.md)
- [Measurement Paradigms](references/measurement-paradigms.md)
- [Attribution by Business Type](references/by-business-type.md)
- [First-Party Attribution](references/first-party-tracking.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown guidance with tables, attribution readouts, code snippets, and implementation checklists when relevant]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include model comparisons, source-of-truth recommendations, confidence notes, and privacy guardrails for first-party tracking.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
