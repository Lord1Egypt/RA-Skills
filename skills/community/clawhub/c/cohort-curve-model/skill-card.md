## Description:

Fits a retention power curve to observed cohort data and projects lifetime periods, LTV, and long-run retention behavior from real cohort inputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mohitagw15856](https://clawhub.ai/user/mohitagw15856)

### License/Terms of Use:

MIT-0

## Use Case:

External users, analysts, and developers use this skill to fit retention curves from observed cohort retention data and project LTV over a stated horizon. It is intended for transparent cohort analysis with reported fit quality, parameter interpretation, and caveats.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The artifact references scripts/cohort_model.py, but the inspected artifact does not include that file.

Mitigation: Confirm the helper script is present and reviewed before relying on generated calculations or workbook output.

Risk: A poor curve fit can produce misleading LTV projections beyond the observed cohort tail.

Mitigation: Report R-squared with the projection, warn when R-squared is below 0.9, and state the LTV horizon explicitly.

Risk: Fitting too few periods can make a power curve appear meaningful when the evidence is insufficient.

Mitigation: Require at least four retention periods and normalize period 0 to 100% before fitting.

## Reference(s):

- [Cohort Curve Model on ClawHub](https://clawhub.ai/mohitagw15856/skills/cohort-curve-model)
- [Cohort Curve Model homepage](https://mohitagw15856.github.io/pm-claude-skills/skill/cohort-curve-model.html)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, code, files, guidance]

**Output Format:** [Markdown analysis with inline shell commands and spreadsheet output when the helper script is available.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports fitted curve parameters, R-squared, retention floor, projection horizon, lifetime periods, LTV when ARPU is provided, and caveats for poor fits.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
