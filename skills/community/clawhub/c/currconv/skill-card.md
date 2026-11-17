## Description:

Convert currencies using the frankfurter.app free API for amount conversion, exchange-rate lookup, and rate history.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bytesagain-lab](https://clawhub.ai/user/bytesagain-lab)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, agents, and end users can use this skill to convert currency amounts, inspect current exchange rates, list supported currencies, and retrieve historical exchange rates. It requires curl, python3, and network access to frankfurter.app.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Release security evidence reports an unsafe code-construction bug where live API data can be inserted into locally executed Python code.

Mitigation: Review before installing; pass API values to Python as data, validate rates as finite positive numbers, and avoid building executable code from remote responses.

Risk: The bundled shell script reports VERSION="3.0.0" while server release metadata and SKILL.md report version 3.0.1.

Mitigation: Confirm the installed script version matches the release before publishing or running it in production workflows.

## Reference(s):

- [Currconv on ClawHub](https://clawhub.ai/bytesagain-lab/skills/currconv)
- [BytesAgain](https://bytesagain.com)
- [frankfurter.app](https://frankfurter.app)
- [European Central Bank euro foreign exchange reference rates](https://www.ecb.europa.eu/stats/policy_and_exchange_rates/euro_reference_exchange_rates/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands and terminal text output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The generated shell workflow calls frankfurter.app and may cache rate data under ~/.local/share/currconv/.]

## Skill Version(s):

3.0.1 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
