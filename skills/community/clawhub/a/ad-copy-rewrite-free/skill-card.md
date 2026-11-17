## Description:

Checks Chinese advertising copy locally and flags risky phrases with line numbers, matched terms, legal basis, and review guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

External e-commerce operators, brand marketers, and ad buyers use this skill before publishing Chinese ad copy to identify mechanically detectable wording risks under mainland China advertising-law concepts. It is intended as a pre-publication review aid, not as legal advice or a substitute for platform, factual, image, approval, or jurisdiction-specific review.

### Deployment Geography for Use:

Mainland China

## Known Risks and Mitigations:

Risk: Users may treat the report as a legal clearance decision.

Mitigation: Require manual review of findings and remind users that the skill is not legal advice and does not determine whether an advertisement is lawful.

Risk: The checker does not verify factual claims, platform rules, images, approvals, or non-mainland legal requirements.

Mitigation: Use it only as a China-ad-law-oriented text screen and route unsupported dimensions to the appropriate platform, legal, factual, or regulatory review.

Risk: Mechanical term matching can miss context or flag text that is quoted, ironic, or otherwise lawful in context.

Mitigation: Review every finding against the original line, surrounding context, and supporting evidence before changing or publishing copy.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/ad-copy-rewrite-free)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [Human-readable terminal text or structured JSON report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports verdict summary, line-level findings, exempted terms, legal bases, and checks withheld by the free version.]

## Skill Version(s):

1.0.63 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
