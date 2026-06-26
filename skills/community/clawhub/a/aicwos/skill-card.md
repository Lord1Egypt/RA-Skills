## Description: <br>
Aicwos helps agents generate Chinese short-form spoken scripts by retrieving lecturer style profiles, knowledge-base context, behavior rules, and series history through local command-line workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smallroya](https://clawhub.ai/user/smallroya) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents creating Chinese short-video or spoken copy use this skill to learn lecturer styles, retrieve product knowledge, produce single or series scripts, revise episodes, and keep copywriting records synchronized in a local control folder. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persistently create, update, delete, import, export, and sync local copywriting and knowledge-base data. <br>
Mitigation: Use a separate low-risk control folder, keep important knowledge files backed up, and review delete or revision operations before execution. <br>
Risk: The skill can sync knowledge-base content from a configured remote URL. <br>
Mitigation: Review the cloud sync URL before use and avoid untrusted sources or imported lecturer folders. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/smallroya/aicwos) <br>
- [Profile format](references/profile-format.md) <br>
- [Lecturer management workflow](references/workflow-lecturer.md) <br>
- [Knowledge-base workflow](references/workflow-knowledge.md) <br>
- [Copywriting workflow](references/workflow-copywriting.md) <br>
- [Script styles](references/script-styles.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and structured JSON payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces copywriting guidance, command sequences, lecturer profile data, knowledge-base operations, and saved episode content through local workflows.] <br>

## Skill Version(s): <br>
1.10.5 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
