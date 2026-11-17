## Description:

Book flights to beach hotels and seaside resort destinations, with support for related travel booking tasks such as hotels, trains, attractions, visa information, insurance, and car rental.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dingtom336-gif](https://clawhub.ai/user/dingtom336-gif)

### License/Terms of Use:

MIT-0

## Use Case:

External travelers use this skill through an agent to collect route and date details, execute flyai travel searches, and return beach-hotel flight options with booking links. It is intended for booking-oriented travel assistance rather than general travel knowledge answers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires installation and use of an unpinned third-party travel CLI.

Mitigation: Use a sandboxed or project-local install, pin and verify the CLI version, and ask the user before installing dependencies.

Risk: The workflow depends on third-party booking links as the mandatory source of travel results.

Mitigation: Validate that each result came from CLI output and clearly preserve booking links without substituting unsourced travel data.

Risk: Route and date inputs can affect commands sent to the travel CLI.

Mitigation: Validate city, airport, route, and date values before command execution and ask clarifying questions for missing or ambiguous parameters.

## Reference(s):

- [Parameter Collection and Output Templates](artifact/references/templates.md)
- [Scenario Playbooks](artifact/references/playbooks.md)
- [Failure Recovery](artifact/references/fallbacks.md)
- [Execution Runbook](artifact/references/runbook.md)

## Skill Output:

**Output Type(s):** [markdown, shell commands, guidance]

**Output Format:** [Markdown with booking links and inline shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires flyai CLI results for booking data; listed options must include detailUrl booking links.]

## Skill Version(s):

3.2.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
