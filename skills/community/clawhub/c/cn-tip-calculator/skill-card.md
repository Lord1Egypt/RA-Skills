## Description:

Calculate tips and split bills with custom tip percentages and optional bill splitting using a local Python script.

This skill is ready for commercial/non-commercial use.

## Publisher:

[freedompixels](https://clawhub.ai/user/freedompixels)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to calculate restaurant tip amounts, total bills, common tip alternatives, and per-person shares for split bills.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Documentation claims currency formatting, but the artifact behavior returns numeric JSON amounts without locale or currency-symbol formatting.

Mitigation: Confirm presentation requirements before relying on currency-specific formatting, or document the output as numeric JSON amounts.

Risk: The artifact documentation includes an unrelated offsite promotional link.

Mitigation: Review external links before distribution and remove links that are not needed to understand or operate the calculator.

## Reference(s):


## Skill Output:

**Output Type(s):** [Shell commands, Text]

**Output Format:** [JSON output from a Python command-line script, with concise usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Pure Python standard library; no API keys or external dependencies required]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
