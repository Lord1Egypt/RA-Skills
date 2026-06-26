## Description: <br>
Feishu Requirement Manager helps agents create requirements, split them into tasks, track progress, and support custom fields in Feishu bitable workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[maoxiaohei2026-tech](https://clawhub.ai/user/maoxiaohei2026-tech) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external collaborators, and developers can use this skill to manage Feishu-based requirement intake, task decomposition, assignment, status tracking, and progress review with extensible fields. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create or update Feishu workspace records. <br>
Mitigation: Require user confirmation before setup, table creation, or record updates, and use a Feishu account authorized for the target workspace. <br>
Risk: Stored table identifiers may be reused from shared memory without clear user or workspace scoping. <br>
Mitigation: Scope stored Feishu table identifiers to the current user or workspace and verify the target app and table before modifying records. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/maoxiaohei2026-tech/feishu-requirement-manager) <br>
- [Usage examples](artifact/references/examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, configuration, guidance] <br>
**Output Format:** [Markdown guidance with structured Feishu bitable field mappings and JSON-like API call examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update Feishu requirement, task, and project records when connected to appropriate Feishu tools.] <br>

## Skill Version(s): <br>
3.1.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
