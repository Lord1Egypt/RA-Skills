## Description:

Use when the user wants an E-E-A-T, credibility, authorship, or trust-signal review using TrustGrowth evidence when connected or observable public/repository evidence otherwise.

This skill is ready for commercial/non-commercial use.

## Publisher:

[trustgrowth](https://clawhub.ai/user/trustgrowth)

### License/Terms of Use:

MIT-0

## Use Case:

External users, site owners, and SEO practitioners use this skill to review E-E-A-T, credibility, authorship, and trust signals from TrustGrowth evidence when connected or from observable public and repository evidence otherwise.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may guide an agent toward optional paid or credentialed SEO, analytics, or TrustGrowth connectors.

Mitigation: Use Tier 1 public or exported evidence when API or MCP access is not desired, and enable only connectors already trusted and configured by the user.

Risk: E-E-A-T and trust-signal conclusions can become misleading if unsupported claims, missing measurements, or failed evidence validation are treated as facts.

Mitigation: Keep missing values unknown, validate normalized evidence before conclusions, label estimates explicitly, and avoid predicting score or ranking changes.

Risk: Recommended publishing or irreversible site changes could affect public-facing trust claims.

Mitigation: Require owner review for outward-facing or irreversible actions and keep fabricated identities, credentials, reviews, and experience out of recommendations.

## Reference(s):

- [Connectors and categories](references/connectors.md)
- [Reporting contract](references/reporting.md)
- [Groundcrew WHY-NOT-SLOP](https://github.com/techwright-lab/groundcrew-seo/blob/main/WHY-NOT-SLOP.md)
- [Groundcrew ETHICS](https://github.com/techwright-lab/groundcrew-seo/blob/main/ETHICS.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, shell commands]

**Output Format:** [Markdown review with evidence notes and optional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include code-fixable findings, content-fixable recommendations, structural recommendations, verdicts, and not-measured items.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
