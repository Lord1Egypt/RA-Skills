## Description:

Generates an interactive HTML feasibility report for AI Agent product ideas across technical fit, competition, market outlook, industry fit, development feasibility, reliability, cost, and go-to-market strategy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bettermen](https://clawhub.ai/user/bettermen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, product teams, and founders use this skill to assess whether an AI Agent product idea is practical to build and launch. It helps compare model and framework choices, market conditions, reliability risks, cost assumptions, and rollout strategy before committing to development.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated HTML may include unescaped user-provided or web-sourced content.

Mitigation: Escape or sanitize report fields before opening reports in a browser, and avoid opening reports generated from untrusted inputs.

Risk: The skill writes local HTML reports based on supplied output paths.

Mitigation: Constrain report output paths to expected working directories before running the generator.

Risk: Market, model, and API pricing inputs can change quickly.

Mitigation: Verify current pricing, market figures, and regulatory assumptions before using a report for business decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bettermen/skills/agent-decision)
- [Project homepage from metadata](https://github.com/bettermen/agent-decision)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with shell commands and generated interactive HTML reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python for local report generation; generated reports should be reviewed before opening or sharing.]

## Skill Version(s):

1.0.0 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
