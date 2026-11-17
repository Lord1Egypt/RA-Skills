## Description:

Generates accessible, token-driven HTML/CSS and related interface, page, document, email, and asset content that follows the EDIC editorial olive-green design system.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cgartlab](https://clawhub.ai/user/cgartlab)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and designers use this skill to create or refactor EDIC interfaces and related materials with consistent design tokens, accessible patterns, and framework-agnostic styling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated pages may load external fonts or CDN assets, creating third-party requests from visitors' browsers.

Mitigation: Self-host reviewed assets or pin CDN resources with integrity checks, and assess external-font requests before publishing.

Risk: Toast messages that include untrusted text could be displayed as markup if inserted unsafely.

Mitigation: Render untrusted toast content as text with textContent rather than inserting it as HTML.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/cgartlab/skills/edic-design-system)
- [Publisher profile](https://clawhub.ai/user/cgartlab)
- [EDIC design system website](https://edic.cgartlab.com/)
- [EDIC documentation](https://edic.cgartlab.com/docs.html)
- [EDIC design tokens](https://edic.cgartlab.com/tokens.json)
- [Project repository (provenance unavailable)](https://github.com/cgartlab/edic-design-system)

## Skill Output:

**Output Type(s):** [Code, HTML/CSS, Markdown, Guidance]

**Output Format:** [Framework-agnostic HTML/CSS and supporting text, including token-based UI examples and compatible static email styles]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Accessible, dark-mode-ready, CJK-aware, and aligned with EDIC design tokens]

## Skill Version(s):

2.9.2 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
