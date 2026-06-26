## Description: <br>
AutoCAD/Autodesk Clean Uninstall Tool - Thoroughly remove all residues, supports multi-PC and multi-user environments, step-by-step confirmation, intelligent discovery of non-standard installation directories. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gzjohny](https://clawhub.ai/user/gzjohny) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and Windows support agents use this skill to inspect and remove AutoCAD or Autodesk leftovers after uninstall, including files, user configuration, registry entries, processes, and services. It is intended for cleanup, reinstall troubleshooting, disk-space recovery, and preparing a machine before handoff. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can make broad, irreversible Windows changes by deleting directories and registry keys and terminating Autodesk-related processes. <br>
Mitigation: Use it only when intentional Autodesk/AutoCAD removal is desired, create backups or a restore point first, and review every listed path, process, service, and registry key before approval. <br>
Risk: The one-click cleanup script supports an unattended -Auto mode that bypasses per-step confirmations. <br>
Mitigation: Prefer the step-by-step commands and do not use -Auto unless the target machine, cleanup scope, and backups have already been independently verified. <br>
Risk: Administrative cleanup of Program Files, services, and HKLM registry locations can affect system functionality or future software reinstall behavior. <br>
Mitigation: Run with administrator privileges only after confirming the detected Autodesk items are expected, and keep a recovery path available for registry or file restoration. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/gzjohny/autodesk-clean-uninstall) <br>
- [Chinese User Guide](readme中文说明.txt) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with PowerShell command blocks and step-by-step cleanup guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are Windows-focused and include environment scanning, confirmation-gated cleanup steps, registry and file deletion commands, and a one-click script with an unattended -Auto option.] <br>

## Skill Version(s): <br>
2.1.0 (source: server release evidence; artifact frontmatter reports 2.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
