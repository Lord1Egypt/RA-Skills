## Description:

Book flights to apartment hotels and extended stay suites, with support for related travel planning outputs powered by Fliggy and flyai.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dingtom336-gif](https://clawhub.ai/user/dingtom336-gif)

### License/Terms of Use:

MIT-0

## Use Case:

External travelers and travel-support agents use this skill to collect flight-search parameters, run flyai travel searches, and present apartment-hotel-oriented booking options with source links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may install an unpinned global flyai CLI package.

Mitigation: Install a pinned, verified CLI version in an isolated environment before use.

Risk: Travel prices and booking URLs are routed through a third-party CLI.

Mitigation: Review booking links and pricing details before relying on them for purchases.

## Reference(s):

- [Parameter Collection & Output Templates](artifact/references/templates.md)
- [Scenario Playbooks](artifact/references/playbooks.md)
- [Failure Recovery](artifact/references/fallbacks.md)
- [Execution Runbook](artifact/references/runbook.md)
- [Node.js](https://nodejs.org/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with comparison tables, booking links, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should be derived from flyai CLI results, include booking links when results are shown, and avoid raw JSON.]

## Skill Version(s):

3.2.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
