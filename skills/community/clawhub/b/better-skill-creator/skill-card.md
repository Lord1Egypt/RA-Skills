## Description: <br>
Enhanced skill creation and management tool with built-in end-to-end version control capabilities. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zzzanezhou0829](https://clawhub.ai/user/zzzanezhou0829) <br>

### License/Terms of Use: <br>
Apache 2.0 <br>


## Use Case: <br>
Developers and agents use this skill to create, modify, package, version, compare, and roll back agent skills with backup and review steps built into the workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Migration or rollback actions can overwrite or remove local skill directories after confirmation. <br>
Mitigation: Read prompts carefully, verify the target path before proceeding, and keep or inspect backups before relying on the changed skill. <br>
Risk: Generated plans, diffs, or automated modifications can introduce incorrect guidance or unwanted behavior into a skill. <br>
Mitigation: Review proposed changes, inspect diffs, and scan or test the skill before deployment. <br>


## Reference(s): <br>
- [Configuration guide](references/config.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Code, Configuration, Markdown] <br>
**Output Format:** [Markdown guidance with shell commands and generated or modified skill files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or modify local skill directories and store backups, proposals, diffs, and changelog-style records under ~/.openclaw.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
