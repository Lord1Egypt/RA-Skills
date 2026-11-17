## Description:

Manages publishing, distribution, and versioning of OpenClaw skills through the ClawHub registry with CLI authentication and batch sync support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hybrid1labs](https://clawhub.ai/user/hybrid1labs)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill maintainers use this skill to publish, synchronize, install, update, and manage OpenClaw skills through the ClawHub registry.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Registry-management commands can affect the wrong skill, account, or registry if run with incorrect targets.

Mitigation: Confirm the target skill path, authenticated account, registry URL, slug, and version before running publish, sync, uninstall, delete, hide, or unhide commands.

Risk: The local ClawHub token can grant publishing or management access if exposed.

Mitigation: Store the token with restrictive filesystem permissions and avoid sharing logs or files that may include credential paths or token contents.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hybrid1labs/skills/clawhub-publishing)
- [ClawHub publisher profile](https://clawhub.ai/user/hybrid1labs)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with bash command examples and registry workflow guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include commands that require authenticated ClawHub CLI access.]

## Skill Version(s):

1.0.0 (source: server release metadata and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
