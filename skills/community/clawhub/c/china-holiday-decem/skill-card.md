## Description:

Looks up China public holiday, make-up workday, next holiday, next workday, yearly holiday, and text-to-speech holiday information using the timor.tech holiday API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[decemjiang](https://clawhub.ai/user/decemjiang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users can use this skill to answer China holiday and workday questions, including whether a date is a holiday, whether a make-up workday applies, and what holidays are listed for a month or year.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Holiday queries require outbound requests to timor.tech, so results depend on external API availability and response quality.

Mitigation: Allow network access only to the disclosed API endpoint and review returned holiday information before using it for operational decisions.

Risk: The skill output is primarily Chinese, which may be unsuitable for users who cannot review Chinese-language responses.

Mitigation: Use with reviewers or downstream translation appropriate for the target audience.

## Reference(s):

- [timor.tech holiday API](https://timor.tech/api/holiday)
- [timor.tech](https://timor.tech)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Plain text and Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are primarily Chinese and depend on live responses from the timor.tech public API.]

## Skill Version(s):

1.0.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
