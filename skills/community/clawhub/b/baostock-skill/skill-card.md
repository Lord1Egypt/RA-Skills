## Description:

Baostock Skill helps agents query BaoStock for Chinese A-share quotes, historical K-line data, fundamentals, index data, and stock lists.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liyico](https://clawhub.ai/user/liyico)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to retrieve Chinese A-share market data for finance workflows, including quotes, historical bars, stock lists, index history, and basic market analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The server security verdict reports that ordinary queries can run unsafe local commands.

Mitigation: Review before installation, run in a contained environment, and replace shell execution with argument-array process execution and strict input validation before deployment.

Risk: The server security summary reports broad workspace filesystem access.

Mitigation: Restrict read and write permissions to the minimum required paths and limit file exports to approved destinations.

Risk: The scanner guidance notes dependency and manifest alignment concerns.

Mitigation: Pin dependencies and confirm the manifest points to the packaged entry points before release or use.

## Reference(s):

- [BaoStock](http://baostock.com)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration, guidance]

**Output Format:** [JSON responses and Markdown guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write JSON query results to a user-specified output file when invoked through the bundled CLI.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
