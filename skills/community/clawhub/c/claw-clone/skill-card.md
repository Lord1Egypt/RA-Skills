## Description: <br>
Exports and imports OpenClaw agent configuration packages, including identity files, rules, selected memory, installed skill lists, and filtered configuration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Anwhere](https://clawhub.ai/user/Anwhere) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and developers use this skill to package an agent setup for sharing or to clone another agent setup into a local OpenClaw workspace. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Imported clone packages can overwrite persistent OpenClaw identity, rule, tool, memory, and configuration files. <br>
Mitigation: Import only trusted packages, inspect every file entry before applying it, and keep or review the generated backup files before continuing work. <br>
Risk: A package can request installation of additional skills chosen by the package author. <br>
Mitigation: Review the listed skills before import and install only skills from publishers and versions the user trusts. <br>
Risk: Exported packages may still contain sensitive agent identity, rules, memory, or credentials not covered by automatic filtering. <br>
Mitigation: Inspect the generated package before sharing it and reconfigure API keys, channel credentials, and other authentication details manually after import. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Files, Shell commands, Configuration] <br>
**Output Format:** [JSON clone package and terminal import/export report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Exports redact common sensitive configuration keys; imports can write workspace files, create backups, and install listed skills.] <br>

## Skill Version(s): <br>
1.0.1 (source: release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
