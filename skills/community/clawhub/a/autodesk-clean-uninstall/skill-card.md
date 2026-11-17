## Description:

AutoCAD/Autodesk Clean Uninstall Tool - Thoroughly remove all residues, supports multi-PC and multi-user environments, step-by-step confirmation, intelligent discovery of non-standard installation directories.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gzjohny](https://clawhub.ai/user/gzjohny)

### License/Terms of Use:

MIT-0

## Use Case:

External users and IT administrators use this skill to generate and follow PowerShell-based cleanup guidance for removing Autodesk and AutoCAD installation residues, user data, services, processes, and registry entries from Windows 10/11 systems.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad, irreversible Windows file and registry deletion can remove user data, licensing information, file associations, or uninstall records.

Mitigation: Use only on a backed-up Windows system where full Autodesk removal is intended, inspect every deletion target manually, and avoid elevated execution unless the exact files and registry keys are understood.

Risk: The one-click script supports an Auto mode that bypasses confirmation prompts.

Mitigation: Avoid the -Auto option and run the step-by-step workflow so each process, service, directory, and registry deletion target can be reviewed before execution.

Risk: Stopping processes and services can interrupt active Autodesk work or related background licensing components.

Mitigation: Close active work, confirm that no needed Autodesk tasks are running, and stop only the listed targets that are intended for removal.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gzjohny/skills/autodesk-clean-uninstall)
- [Chinese usage documentation](artifact/readme中文说明.txt)
- [ClawHub manifest](artifact/claw.json)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands]

**Output Format:** [Markdown with inline PowerShell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands target Windows 10/11 systems and may require administrator privileges for protected directories and registry keys.]

## Skill Version(s):

2.1.0 (source: evidence.release.version; artifact frontmatter reports 2.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
