## Description:

Reviews generated HTML/CSS pages against a user-provided Markdown design specification and returns a structured design compliance report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[asz2864](https://clawhub.ai/user/asz2864)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and designers use this skill to check an HTML/CSS page against a specified design-spec Markdown file, identify mismatches in visual rules and component styling, and receive prioritized fixes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads user-selected design-spec Markdown and target HTML/CSS files, and may inspect broader project content if the target files are not clearly scoped.

Mitigation: Confirm the design specification and page paths before running, and limit review to the files needed for the design walk-through.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/asz2864/skills/design-compliance-check)
- [Publisher profile](https://clawhub.ai/user/asz2864)

## Skill Output:

**Output Type(s):** [analysis, markdown, code, guidance]

**Output Format:** [Markdown report with prioritized findings, summary tables, and CSS fix snippets when needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads the selected design specification and target HTML/CSS files before reporting pass, warning, error, and not-applicable items.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
