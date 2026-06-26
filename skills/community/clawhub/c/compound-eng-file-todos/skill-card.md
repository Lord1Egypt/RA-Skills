## Description: <br>
File-based todo and task tracking in the todos/ directory for creating, triaging, listing, managing, and checking project work items, status, and dependencies. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[iliaal](https://clawhub.ai/user/iliaal) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to manage persistent markdown todos in a project `todos/` directory. It supports creating new todo files, triaging pending work, tracking dependencies, updating work logs, and marking items complete. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can lead an agent to create, edit, copy, or rename local markdown todo files. <br>
Mitigation: Run it in the intended project workspace and review changes under the todos/ directory before relying on them. <br>
Risk: The release has capability tags for crypto and purchases that do not match the local todo-tracking behavior described by the security evidence. <br>
Mitigation: Treat the skill as a local markdown todo manager and have the publisher correct the unrelated tags to avoid scope confusion. <br>


## Reference(s): <br>
- [Todo Workflows](references/workflows.md) <br>
- [Quick Reference Commands](references/quick-reference.md) <br>
- [Todo Template](assets/todo-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with YAML frontmatter examples and bash command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Intended outputs are local markdown todo files and status updates scoped to a project todos/ directory.] <br>

## Skill Version(s): <br>
3.0.5 (source: evidence.release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
