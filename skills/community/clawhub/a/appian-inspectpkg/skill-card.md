## Description:

Inspect an Appian package ZIP against the target environment to identify errors or warnings before deploying.

This skill is ready for commercial/non-commercial use.

## Publisher:

[solarspiker](https://clawhub.ai/user/solarspiker)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and release engineers use this skill to inspect Appian package ZIP files before deployment so they can review expected object counts, errors, and warnings against the target Appian environment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An unintended or insecure Appian base URL could receive the Appian API key and package files.

Mitigation: Use only a trusted HTTPS Appian base URL and verify APPIAN_BASE_URL before running the skill.

Risk: Local appian.json files in the current or parent directories could provide unexpected credentials or endpoints.

Mitigation: Prefer injected environment variables, and check parent directories for unexpected appian.json files before running.

Risk: An Appian API key may need remediation if it was used with an untrusted endpoint.

Mitigation: Rotate the Appian API key if there is any chance it was sent to an untrusted endpoint.

## Reference(s):

- [Appian Inspect Package API](https://docs.appian.com/suite/help/25.4/Inspect_Package_API.html)
- [ClawHub Skill Page](https://clawhub.ai/solarspiker/skills/appian-inspectpkg)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text CLI output with an inspection UUID, object counts, errors, and warnings.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports Appian inspection results after polling the configured environment; no files are written by the skill.]

## Skill Version(s):

1.1.0 (source: server release evidence and script header)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
