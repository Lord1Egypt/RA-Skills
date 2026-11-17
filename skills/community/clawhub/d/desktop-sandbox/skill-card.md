## Description:

Desktop Sandbox installs AtlasCore Desktop Sandbox so OpenClaw can run in a native desktop environment with sandboxed isolation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[atlascore-tech](https://clawhub.ai/user/atlascore-tech)

### License/Terms of Use:


## Use Case:

External OpenClaw users and developers use this skill to download and run the AtlasCore Desktop Sandbox installer from release assets on supported desktop platforms.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill downloads and runs native GitHub release installers, and the default latest release target can change over time.

Mitigation: Use a pinned release version, verify the installer through an independent checksum or platform signature, and review the repository and release before execution.

Risk: The server security verdict flags the skill as suspicious because installer execution has weak safeguards.

Mitigation: Install only when the AtlasCore release process is trusted and the user is comfortable allowing a native installer to run on the machine.

## Reference(s):

- [Desktop Sandbox ClawHub listing](https://clawhub.ai/atlascore-tech/skills/desktop-sandbox)
- [AtlasCore Desktop Sandbox repository](https://github.com/AtlasCore-tech/desktop-sandbox-openclaw)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Markdown instructions with shell commands and JSON installer status]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js; supports an optional --version argument for selecting a release tag.]

## Skill Version(s):

1.1.1 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
