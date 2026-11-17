## Description:

Search, install, and publish OpenClaw agent packages from the Clawstore registry.

This skill is ready for commercial/non-commercial use.

## Publisher:

[saba-ch](https://clawhub.ai/user/saba-ch)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to search the Clawstore registry, inspect agent packages, install or update agents, and publish OpenClaw agent packages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing the CLI or agent packages from an unverified source could introduce unwanted code.

Mitigation: Confirm the npm package source, prefer a reviewed or pinned CLI version, and inspect package details before installing agents.

Risk: Publishing a package without review could expose private files, secrets, or incorrect package contents.

Mitigation: Run validation and inspect the packed tarball before publishing.

Risk: Login, install, publish, update, and yank commands can affect user accounts, local workspaces, or published package state.

Mitigation: Review each proposed command and confirm package names, versions, and target directories before execution.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/saba-ch/skills/clawstore)
- [Clawstore Registry](https://useclawstore.com)
- [Publisher Profile](https://clawhub.ai/user/saba-ch)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance, Markdown]

**Output Format:** [Markdown with inline shell commands and concise operational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill produces command recommendations for the clawstore CLI and package-management workflows.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
