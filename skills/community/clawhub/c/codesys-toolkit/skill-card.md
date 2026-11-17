## Description:

Automates CODESYS/InoProShop PLC programming workflows, including project generation, POU export and patching, compile checks, device enumeration, and error dialog monitoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[paudyyin](https://clawhub.ai/user/paudyyin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation engineers use this skill to operate PLC project workflows for CODESYS/InoProShop environments, including generating projects from templates, exporting and modifying Structured Text files, applying incremental POU patches, and checking compilation results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can execute automation scripts that create, patch, save, and compile PLC projects.

Mitigation: Install only when the publisher and configured workspaces are trusted, review env.json paths before use, and test with backups or non-production PLC projects first.

Risk: The optional download script can fetch tool files from a remote internal GitLab location.

Mitigation: Prefer the bundled reviewed tools; run download_tools.ps1 only after verifying the exact remote contents and access path.

Risk: A workspace-level generator_override.py can replace the bundled generator during generate runs.

Mitigation: Avoid untrusted workspaces and review any generator_override.py before running generation.

Risk: The launcher may stop existing InoProShop processes before running a script.

Mitigation: Use the -NoKill option when other InoProShop sessions may be active.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/paudyyin/skills/codesys-toolkit)
- [Artifact README](artifact/README.md)
- [Artifact skill definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with PowerShell commands, JSON configuration examples, and code/file operation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Targets Windows-based InoProShop/CODESYS project workspaces and may produce or modify project, Structured Text, snapshot, task mapping, device list, and log files.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
