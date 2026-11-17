## Description:

COPPA Guard is a local Chinese-language compliance guardrail that helps agents scan draft copy, privacy policies, and app store descriptions for COPPA-triggering or child privacy risk terms before release.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wwumit](https://clawhub.ai/user/wwumit)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, product teams, and agents preparing U.S. children's apps, games, e-commerce, or education releases use this skill to screen text before publication and receive risk-graded findings with remediation suggestions. It is a triage aid, not legal advice or a full COPPA audit.

### Deployment Geography for Use:

Global, with checks focused on United States COPPA contexts.

## Known Risks and Mitigations:

Risk: Keyword-based compliance checks can miss context-specific COPPA obligations or flag benign text.

Mitigation: Use the skill as pre-publication triage and route flagged, ambiguous, or high-impact releases to qualified U.S. privacy or legal review.

Risk: Users may treat the output as legal advice or a complete COPPA audit.

Mitigation: Keep the disclaimer visible and require final compliance decisions to rely on documented review processes rather than this skill alone.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wwumit/skills/coppa-guard)

## Skill Output:

**Output Type(s):** [text, JSON, guidance]

**Output Format:** [Plain text or JSON risk report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes decision, risk level, finding count, matched terms, categories, severity, offsets, and remediation suggestions.]

## Skill Version(s):

1.0.0 (source: server release, package.json, CHANGELOG, released 2026-08-09)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
