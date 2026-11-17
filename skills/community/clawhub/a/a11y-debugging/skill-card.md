## Description:

Uses Chrome DevTools MCP for accessibility (a11y) debugging and auditing based on web.dev guidelines.

This skill is ready for commercial/non-commercial use.

## Publisher:

[poiuy1318](https://clawhub.ai/user/poiuy1318)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to audit web pages and components for accessibility issues, including semantic structure, labels, focus behavior, keyboard navigation, tap target size, and color contrast.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Browser audits and page-inspection snippets can expose page URLs, selectors, snippets, or tested-page data in reports and agent context.

Mitigation: Use the skill only on authorized sites and handle generated reports according to the data sensitivity of the audited page.

Risk: The color-contrast snippet uses a simplified calculation and may miss transparency, gradients, or image backgrounds.

Mitigation: Treat simplified contrast results as a screening signal and confirm ambiguous findings with browser issues, Lighthouse, screenshots, or production-grade accessibility tooling.

## Reference(s):

- [Accessibility Debugging Snippets](references/a11y-snippets.md)
- [Accessible tap targets](https://web.dev/articles/accessible-tap-targets)
- [ClawHub skill page](https://clawhub.ai/poiuy1318/skills/a11y-debugging)
- [Publisher profile](https://clawhub.ai/user/poiuy1318)

## Skill Output:

**Output Type(s):** [Analysis, Code, Shell commands, Guidance]

**Output Format:** [Markdown with inline code blocks and tool-use guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference Lighthouse reports, accessibility tree snapshots, Chrome issue output, screenshots, and small read-only JavaScript snippets.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
