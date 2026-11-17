## Description:

A Chinese-language development guide for creating, modifying, troubleshooting, debugging, and packaging EasiNote 5 native .NET 6/WPF plugins.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lindexi](https://clawhub.ai/user/lindexi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers building EasiNote 5 native plugins use this skill to set up projects, extend Cloud and Shell UI surfaces, call host APIs, manage lifecycle readiness, integrate WPF visuals, restart the host safely, and package plugin outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Native plugins run in-process and can affect EasiNote UI, content, telemetry, packaging, and restart behavior.

Mitigation: Review generated plugin code before use and validate behavior in the intended Cloud, Edit, or Display host scenario.

Risk: Plugin outputs could accidentally include secrets, private paths, or unnecessary user data.

Mitigation: Check generated code, telemetry, package contents, and launch settings before packaging or sharing.

Risk: Host APIs and internal resources may vary by EasiNote version.

Mitigation: Build against the target SDK and verify internal API, resource, and UI behavior on the installed target EasiNote version.

## Reference(s):

- [Project Setup and Debug Configuration](references/project-setup.md)
- [Lifecycle, Process Modes, and Container Readiness](references/lifecycle-and-container.md)
- [Common API Recipes](references/api-recipes.md)
- [HeadToolBarItem and Subject Tool Entries](references/head-toolbar-and-subject-tools.md)
- [WPF Visual Integration](references/wpf-visual-integration.md)
- [Safe EasiNote Exit and Restart](references/safe-host-restart.md)
- [Complete Development Examples](references/complete-examples.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with C#, XML, JSON, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only skill; generated plugin changes should be reviewed and validated against the target EasiNote version.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
