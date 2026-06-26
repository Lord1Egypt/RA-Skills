## Description: <br>
Creates draft task files in .specs/tasks/draft/ that preserve the user's original task intent. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hahamumu08](https://clawhub.ai/user/hahamumu08) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and project maintainers use this skill to turn a brief task request into a structured draft task markdown file for an SDD-style workflow, including title, issue type, dependencies, and the original prompt. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contains a folder-target inconsistency that could place task files outside the intended draft directory. <br>
Mitigation: Before use, verify that generated task files are written only under .specs/tasks/draft/ and correct any path that points to .specs/tasks/todo/. <br>
Risk: The skill preserves the original user prompt in generated markdown, so sensitive prompt content may be stored in the workspace. <br>
Mitigation: Do not include secrets or confidential data in task prompts, and review generated task files before committing them. <br>
Risk: The skill references a create-folders.sh helper that is not present in the artifact evidence. <br>
Mitigation: Confirm the installed package includes the helper or create the expected .specs/tasks directories before running the skill. <br>


## Reference(s): <br>
- [ClawHub Add Task release page](https://clawhub.ai/hahamumu08/add-task) <br>
- [Skill definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown task file plus concise text summary] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated task files preserve the original user prompt and use a placeholder description for later analyst completion.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
