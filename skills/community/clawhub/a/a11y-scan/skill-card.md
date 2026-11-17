## Description:

Scan any public web page for WCAG 2.2 (ADA) accessibility issues and clearly explain what automated testing can and cannot catch.

This skill is ready for commercial/non-commercial use.

## Publisher:

[foomworks](https://clawhub.ai/user/foomworks)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, site owners, and accessibility reviewers use this skill to scan a public URL for static HTML accessibility issues, WCAG success-criterion mappings, issue counts, fixes, and coverage limitations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The hosted service receives the URL being audited.

Mitigation: Use the skill only with public, non-confidential URLs that you are authorized to scan.

Risk: Static automated scanning cannot determine full WCAG conformance or legal compliance.

Mitigation: Treat results as triage and follow up with browser-based testing, assistive-technology checks, and human accessibility review.

Risk: JavaScript-rendered content, keyboard behavior, focus management, color contrast, and semantic meaning may be missed.

Mitigation: Use complementary manual and browser-based accessibility tests for those areas before relying on remediation decisions.

## Reference(s):

- [A11y Scan ClawHub release](https://clawhub.ai/foomworks/skills/a11y-scan)
- [A11y Scan service homepage](https://a11y-scan.foomworks.workers.dev)
- [A11y Scan MCP endpoint](https://a11y-scan.foomworks.workers.dev/mcp)
- [A11y Scan OpenAPI manifest](https://a11y-scan.foomworks.workers.dev/openapi.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown guidance with optional curl examples and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include WCAG success criteria, impact, issue counts, suggested fixes, summaries, coverage notes, and disclaimers.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
