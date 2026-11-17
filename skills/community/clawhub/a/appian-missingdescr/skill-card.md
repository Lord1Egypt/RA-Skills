## Description:

Audit Appian application objects for missing descriptions. Given an application UUID, reports every object whose description field is empty or absent.

This skill is ready for commercial/non-commercial use.

## Publisher:

[solarspiker](https://clawhub.ai/user/solarspiker)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Appian administrators use this skill to audit an Appian application for objects whose description field is empty or absent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs a configured APPIAN_RUNNER against a target Appian environment.

Mitigation: Install and run it only when the APPIAN_RUNNER script and the Appian environment are trusted.

Risk: An invalid or unquoted application identifier could lead to incorrect execution behavior.

Mitigation: Validate that the application identifier is a UUID and prefer quoted or shell-free argument passing for the runner path and UUID.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/solarspiker/skills/appian-missingdescr)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown or plain text with an inline shell command and verbatim runner output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires APPIAN_PROC_URL, APPIAN_RUNNER, node, and an Appian application UUID.]

## Skill Version(s):

1.5.10 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
