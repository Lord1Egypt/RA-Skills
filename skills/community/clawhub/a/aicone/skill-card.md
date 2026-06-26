## Description: <br>
A clone and restore skill for exporting, verifying, and importing AI agent workspace configuration packages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[srchengtao2025](https://clawhub.ai/user/srchengtao2025) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, operators, and teams use this skill to package an agent workspace for transfer, backup, restore, or controlled sharing between agent environments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Clone packages can include private agent memory, user data, credentials, endpoints, or proprietary workspace files. <br>
Mitigation: Inspect packages before export, remove or exclude sensitive files, and transfer clone packages only through trusted channels. <br>
Risk: Importing a clone package can overwrite persistent agent behavior and workspace configuration. <br>
Mitigation: Verify the source, run preview and verify before import, back up the target workspace, and avoid --force unless the archive is fully trusted. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/srchengtao2025/aicone) <br>
- [AI Clone Skill README](README.md) <br>
- [AI robot cloning best practices](references/best-practices.md) <br>
- [Machine Cat clone configuration](references/machine-cat-config.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Files, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with Python CLI commands and generated ZIP clone packages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Exports clone-package ZIP files and supports preview, verification, and import workflows.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
