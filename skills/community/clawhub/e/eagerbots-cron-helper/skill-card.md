## Description:

Explain, generate, and validate cron expressions. Convert plain English schedules to cron syntax and back. Show next run times. Works with standard 5-field and 6-field cron.

This skill is ready for commercial/non-commercial use.

## Publisher:

[josephflu](https://clawhub.ai/user/josephflu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to explain, generate, validate, and preview cron schedules from plain English descriptions or raw cron syntax.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Six-field cron expressions with seconds may not behave consistently across schedulers.

Mitigation: Confirm that the target scheduler accepts seconds fields, and prefer standard 5-field cron where scheduler compatibility is uncertain.

Risk: Unpinned Python dependencies can change cron parsing or terminal rendering behavior over time.

Mitigation: Pin rich and croniter or use a committed lockfile before automated or production use.

Risk: Generated or explained schedules can be wrong for the target runtime if scheduler semantics differ.

Mitigation: Review generated cron expressions against the deployment scheduler and preview next run times before installation.

## Reference(s):

- [Cron Syntax Quick Reference](references/cron-syntax.md)
- [OpenClaw cron scheduler documentation](https://docs.openclaw.com/cron)
- [Project homepage](https://github.com/josephflu/clawhub-skills)
- [ClawHub skill page](https://clawhub.ai/josephflu/skills/eagerbots-cron-helper)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown or terminal text with cron expressions, explanations, validation results, next-run previews, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local Python execution for cron parsing and preview; no API keys or MCP tools were detected.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
