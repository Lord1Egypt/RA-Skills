## Description:

Helps agents route medical and wellness questions with uncertainty, emergency routing, clinician referral, diagnosis and treatment boundaries, and private health data minimization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mindbomber](https://clawhub.ai/user/mindbomber)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and developers use this skill to classify, triage, summarize, draft, or route medical and wellness-related requests while staying within safer response boundaries. It is most relevant for workflows that need emergency escalation, clinician or pharmacist referral, diagnosis and treatment overclaim checks, and health-data minimization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A high-risk medical or crisis request could be handled as routine advice.

Mitigation: Route urgent warning signs, self-harm risk, or other emergency scenarios to emergency services, crisis support, or immediate medical care.

Risk: An agent could overstate diagnostic or treatment certainty from incomplete chat context.

Mitigation: Require uncertainty language, avoid definitive diagnosis or prescription claims, and defer high-risk decisions to a clinician or pharmacist.

Risk: Private health information could be exposed in review payloads or optional checker calls.

Mitigation: Use minimal redacted summaries and avoid raw records, images, full lab reports, insurance identifiers, clinician notes, credentials, or unrelated health data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mindbomber/skills/aana-medical-safety-router)
- [Skill README](artifact/README.md)
- [Medical safety review schema](artifact/schemas/medical-safety-review.schema.json)
- [Redacted medical safety review example](artifact/examples/redacted-medical-safety-review.json)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, guidance]

**Output Format:** [Markdown guidance and optional structured JSON review payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Instruction-only; optional checker payloads should use minimal redacted summaries.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
