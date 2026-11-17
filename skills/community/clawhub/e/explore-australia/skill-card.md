## Description:

Book flights to Australia including Sydney, Melbourne, and Brisbane, with support for related travel booking and planning tasks powered by Fliggy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiejinsong](https://clawhub.ai/user/xiejinsong)

### License/Terms of Use:

MIT-0

## Use Case:

External users and travel agents use this skill to search Australia-bound flights, collect required route parameters, run the flyai CLI, and present bookable flight options with links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks agents to install and run an unpinned global npm CLI package.

Mitigation: Review the package before installation, prefer a pinned local or isolated installation, and verify the CLI version before use.

Risk: The skill uses shell command templates populated with user-supplied travel fields.

Mitigation: Validate and safely quote route, date, and preference values before execution; avoid passing untrusted free-form text into command templates.

## Reference(s):

- [Parameter Collection & Output Templates](references/templates.md)
- [Scenario Playbooks](references/playbooks.md)
- [Failure Recovery](references/fallbacks.md)
- [Execution Runbook](references/runbook.md)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Markdown travel results with booking links and inline shell commands when setup or execution is needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires CLI-derived results and booking detail URLs; raw JSON should not be returned to the user.]

## Skill Version(s):

3.2.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
