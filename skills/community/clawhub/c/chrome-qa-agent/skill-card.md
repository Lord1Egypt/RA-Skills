## Description:

An adversarial UI testing agent that uses chrome-devtools MCP to test changes from a git diff or explore an application for bugs, covering functionality, accessibility, responsive layouts, and UX heuristics in local or live Chrome.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yzfly](https://clawhub.ai/user/yzfly)

### License/Terms of Use:

MIT

## Use Case:

Developers use this skill to QA UI changes and pull requests, audit accessibility, or explore a web application for bugs with a real Chrome session.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The guidance includes potentially consequential or destructive browser actions, broad browser-tool preapproval, and remote scripts running in authenticated pages.

Mitigation: Review actions before running, avoid broad browser-tool preapproval, and do not load remote scripts into authenticated pages without explicit review.

Risk: The security analysis was partial: 10 of 12 components were fully inspected and two were partially inspected.

Mitigation: Review the partially inspected content before installation or use.

## Reference(s):

- [Chrome QA Agent on ClawHub](https://clawhub.ai/yzfly/skills/chrome-qa-agent)
- [Adversarial testing patterns](artifact/references/adversarial-patterns.md)
- [Browser check recipes](artifact/references/browser-recipes.md)
- [Design consistency checks](artifact/references/design-consistency.md)
- [Exploratory testing guide](artifact/references/exploratory-testing.md)
- [Sequential browser testing](artifact/references/parallel-testing.md)
- [UX heuristics](artifact/references/ux-heuristics.md)
- [HTML report template](artifact/references/report-template.html)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, HTML report, Screenshots]

**Output Format:** [Structured Markdown test findings and a self-contained HTML report with embedded screenshots]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Screenshots are captured for failed checks; use depends on an available Chrome DevTools MCP connection and target application.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata; artifact frontmatter declares 0.5.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
