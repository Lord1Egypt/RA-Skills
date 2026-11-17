## Description:

Routes legal, regulatory, compliance, contract, immigration, criminal, family, employment, housing, court, dispute, and rights-related questions through legal-safety checks for jurisdiction, advice boundaries, unsupported claims, referral needs, and privacy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mindbomber](https://clawhub.ai/user/mindbomber)

### License/Terms of Use:

MIT-0

## Use Case:

Agents use this skill before responding to legal-sensitive requests to distinguish general legal information from legal advice, add jurisdiction caveats, avoid unsupported legal claims, minimize private legal data, and route high-impact matters to qualified legal help.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may mistake agent output for licensed legal advice.

Mitigation: The skill directs agents to provide general legal information, avoid attorney-client relationship language, and route high-impact or deadline-sensitive matters to qualified legal professionals.

Risk: Legal requests can expose sensitive legal, identity, financial, health, family, employment, or immigration data.

Mitigation: The skill requires minimized, redacted summaries for review payloads and warns against including raw legal records, full filings, identity documents, credentials, or unrelated private data.

Risk: Unsupported claims about statutes, deadlines, rights, enforceability, eligibility, penalties, or outcomes can mislead users.

Mitigation: The skill requires jurisdiction checks, source support, caveats, retrieval from trusted sources when current law is needed, or deferral when claims cannot be supported.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mindbomber/skills/aana-legal-safety-router)
- [README](artifact/README.md)
- [Legal safety review schema](artifact/schemas/legal-safety-review.schema.json)
- [Redacted legal safety review example](artifact/examples/redacted-legal-safety-review.json)

## Skill Output:

**Output Type(s):** [guidance, markdown, configuration]

**Output Format:** [Markdown instructions with optional JSON review payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Instruction-only; produces legal-safety review guidance and does not execute commands or call services by itself.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
