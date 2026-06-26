## Description: <br>
Organize and maintain agent workspace directories by initializing structure, classifying files, auditing placement, cleaning content, and suggesting expansions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhaql](https://clawhub.ai/user/zhaql) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to create, audit, and maintain organized workspace directory structures. It helps classify documents and code files, detect misplaced or duplicate content, and propose cleanup or structure changes for review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Workspace cleanup recommendations can move, rename, archive, merge, or remove files that contain unique or important information. <br>
Mitigation: Ask for a dry-run report first and review proposed changes before applying them. <br>
Risk: Cleanup of memory, preferences, SQL, or task files can affect future agent behavior or workspace correctness. <br>
Mitigation: Review these categories explicitly and prefer archiving over deletion when value is uncertain. <br>


## Reference(s): <br>
- [Document Classification Rules](references/classification-rules.md) <br>
- [Workspace Structure Templates](references/structure-templates.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with directory structures, checklists, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include proposed file moves, renames, archives, or cleanup steps for user approval.] <br>

## Skill Version(s): <br>
1.1.0 (source: release evidence and CHANGELOG, released 2026-03-25) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
