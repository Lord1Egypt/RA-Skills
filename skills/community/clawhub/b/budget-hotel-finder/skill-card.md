## Description:

Find clean, comfortable hotels under a user's budget by using flyai CLI hotel search output, sorting by price or rating, and formatting options with booking links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dingtom336-gif](https://clawhub.ai/user/dingtom336-gif)

### License/Terms of Use:

MIT

## Use Case:

External travel users and agents use this skill to search for budget hotels, compare real-time hotel options, and produce booking-link Markdown in the user's language.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks agents to install an unpinned global flyai CLI.

Mitigation: Pin and verify the CLI package before use, and require human approval before any global npm installation.

Risk: Hotel searches may be converted into shell commands from user-provided travel input.

Mitigation: Validate destination, date, price, and filter values and pass arguments safely instead of constructing shell commands from raw user text.

Risk: Raw travel queries may be persisted in a local execution log.

Mitigation: Disable the raw-query log or scrub sensitive user travel details before writing logs.

## Reference(s):

- [Templates](references/templates.md)
- [Playbooks](references/playbooks.md)
- [Fallbacks](references/fallbacks.md)
- [Runbook](references/runbook.md)
- [Parent flyai skill](https://github.com/alibaba-flyai/flyai-skill/tree/main/skills/flyai)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Markdown tables with inline booking links and flyai CLI command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires flyai CLI output for hotel names, prices, ratings, and booking detail URLs.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata; artifact frontmatter lists 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
