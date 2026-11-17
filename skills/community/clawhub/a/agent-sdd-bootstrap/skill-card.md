## Description:

Helps developers initialize an OpenSpec/SDD workflow in a project, configure project context, and connect native or non-native agent CLI tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nieen](https://clawhub.ai/user/nieen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to bootstrap Spec-Driven Development with OpenSpec, populate project-specific SDD configuration, and bridge generated skills or commands into agent CLI tools that OpenSpec does not natively support.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing the OpenSpec CLI globally from npm can introduce supply-chain or privilege risk.

Mitigation: Review the selected npm package version, avoid administrator privileges for the global install, and update deliberately rather than relying on an unchecked latest version.

Risk: OpenSpec initialization and configuration updates can overwrite project files or replace existing SDD configuration.

Mitigation: Commit or stage project changes before initialization, inspect generated OpenSpec and agent skill or command files, and review diffs before relying on them.

Risk: Mirroring generated skills or commands into non-native agent CLI tools can fail if the target tool uses a different schema.

Mitigation: Check the target tool's skill and command format, adapt copied files to that schema, and verify the resulting slash commands in the target tool before regular use.

## Reference(s):

- [PowerShell Command Reference](references/powershell.md)
- [OpenSpec GitHub](https://github.com/Fission-AI/OpenSpec)
- [OpenSpec npm package](https://www.npmjs.com/package/@fission-ai/openspec)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with bash, PowerShell, and YAML examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance may include file creation, whole-file configuration replacement, and command adaptation steps for different agent CLI tools.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
