## Description: <br>
ByteRover Context Tree helps agents query and curate project memory in `.brv/context-tree` using the `brv` CLI and a configured LLM provider. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pratiknarola](https://clawhub.ai/user/pratiknarola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and coding agents use this skill to retrieve project conventions, prior decisions, and stored implementation context before work, then curate durable project knowledge after meaningful changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: `brv query` and `brv curate` can send query text and included file contents to a configured LLM provider. <br>
Mitigation: Use the skill only when project memory is needed, avoid sending secrets or sensitive files, and confirm provider choice before including source files. <br>
Risk: The skill encourages memory use before and after work without explicit task-by-task consent. <br>
Mitigation: Set local operating boundaries so `brv query` and `brv curate` run only when relevant to the task or explicitly requested by the user. <br>
Risk: Optional cloud sync commands can send stored knowledge to ByteRover cloud after authentication. <br>
Mitigation: Use cloud sync only with an authenticated account and after confirming the intended team space and data-sharing policy. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/pratiknarola/byterover-context-tree) <br>
- [Publisher profile](https://clawhub.ai/user/pratiknarola) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference local `.brv/context-tree` Markdown memory, configured LLM-provider behavior, and optional ByteRover cloud sync commands.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
