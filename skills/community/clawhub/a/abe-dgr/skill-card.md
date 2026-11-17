## Description:

Audit-ready decision artifacts for LLM outputs: assumptions, risks, recommendation, and review gating in schema-valid JSON.

This skill is ready for commercial/non-commercial use.

## Publisher:

[abeltennyson](https://clawhub.ai/user/abeltennyson)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, auditors, and decision makers use this skill to produce structured decision records for high-stakes or review-required scenarios. It captures assumptions, risks, clarifications, a recommendation, and consistency checks for storage in tickets, incidents, or audit logs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may treat the generated decision artifact as guaranteed correct or as professional advice.

Mitigation: Treat the output as a reasoning and documentation aid; validate assumptions, source documents, and conclusions with responsible human reviewers for legal, medical, financial, safety, access-control, or production-impacting decisions.

Risk: Missing or ambiguous decision inputs can lead to overconfident recommendations.

Mitigation: Use the skill's clarification and review_required fields to block or escalate decisions when critical inputs are absent or uncertainty is high.

Risk: Generated artifacts may cite or rely on evidence the model did not actually receive.

Mitigation: Follow the skill boundary requiring no fabricated evidence, and record unavailable sources as assumptions or risks instead of treating them as facts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/abeltennyson/skills/abe-dgr)
- [DGR homepage](https://www.heybossai.com/skills/dgr)
- [DGR output schema](artifact/schema.json)
- [DGR field guide](artifact/field_guide.md)

## Skill Output:

**Output Type(s):** [text, JSON, guidance]

**Output Format:** [Schema-valid JSON decision artifact]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes artifact metadata, input summary, optional clarifications, assumptions, risks, recommendation, next steps, and consistency checks.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
