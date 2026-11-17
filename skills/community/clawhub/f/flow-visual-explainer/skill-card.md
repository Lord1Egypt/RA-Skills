## Description:

FlowVisualExplainer generates self-contained HTML diagrams, architecture overviews, comparison tables, reviews, recaps, and slide decks for visual explanations of technical concepts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[windseeker1111](https://clawhub.ai/user/windseeker1111)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and technical teams use this skill to turn system descriptions, code reviews, implementation plans, comparisons, and presentation requests into visual HTML artifacts for inspection or sharing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Public sharing can expose confidential code, architecture, business plans, customer data, or incident material.

Mitigation: Review generated pages before sharing and avoid the share or deploy workflow for sensitive material unless external publication is intentionally approved.

Risk: Generated pages may load CDN scripts or fonts, and slide workflows may use remote image generation paths.

Mitigation: Use local assets or offline templates for sensitive work, and disable remote image generation or CDN-backed templates when external services are not acceptable.

Risk: Visual explanations can misstate source code, plans, data relationships, or review findings.

Mitigation: Compare generated diagrams, tables, and slides against the source material before relying on them for decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/windseeker1111/skills/flow-visual-explainer)
- [Visual Explainer homepage](https://github.com/nicobailon/visual-explainer)
- [CSS Patterns for Diagrams](references/css-patterns.md)
- [External Libraries (CDN)](references/libraries.md)
- [Responsive Section Navigation](references/responsive-nav.md)
- [Slide Deck Patterns](references/slide-patterns.md)
- [Architecture Diagram Reference Template](templates/architecture.html)
- [Data Table Reference Template](templates/data-table.html)
- [Mermaid Flowchart Reference Template](templates/mermaid-flowchart.html)
- [Slide Deck Reference Template](templates/slide-deck.html)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Self-contained HTML files with optional Markdown guidance and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes HTML to ~/clawd/output/diagrams/, opens it in a browser, may load CDN libraries, and can optionally deploy pages through Vercel.]

## Skill Version(s):

1.0.2 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
