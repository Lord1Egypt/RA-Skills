## Description:

Performs 12-Factor App compliance analysis on a codebase.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anderskev](https://clawhub.ai/user/anderskev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to evaluate a codebase against the 12-Factor App methodology, identify compliance gaps, and produce evidence-backed recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill guides an agent to inspect the selected codebase and cite files and lines in its report.

Mitigation: Use it only on repositories you are comfortable having analyzed.

Risk: The workflow references a separate 12-factor-apps helper skill when present.

Mitigation: Ensure the referenced helper skill is trusted before relying on its search patterns.

## Reference(s):

- [The Twelve-Factor App](https://12factor.net)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown report with an executive summary table, detailed findings, evidence references, and priority recommendations.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Accepts a target codebase path and defaults to the current working directory.]

## Skill Version(s):

1.1.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
