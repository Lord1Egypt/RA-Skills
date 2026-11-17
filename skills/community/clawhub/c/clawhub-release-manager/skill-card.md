## Description:

Safely release and publish skill updates to ClawHub with version bump discipline.

This skill is ready for commercial/non-commercial use.

## Publisher:

[okikesolutions](https://clawhub.ai/user/okikesolutions)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill maintainers use this skill to prepare ClawHub skill releases by checking authentication, applying version bumps, running validation commands, publishing, and summarizing release results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Publishing can create a persistent release under the authenticated ClawHub account.

Mitigation: Review the target skill directory, version bump, changelog, and `clawhub publish` command before execution.

## Reference(s):

- [Release output template](references/output-template.md)
- [ClawHub skill page](https://clawhub.ai/okikesolutions/skills/clawhub-release-manager)
- [Publisher profile](https://clawhub.ai/user/okikesolutions)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown release summary with command-oriented guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes version, validation, publishing, routing-change, and follow-up sections.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
