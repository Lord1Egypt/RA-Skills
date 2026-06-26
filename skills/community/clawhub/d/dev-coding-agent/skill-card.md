## Description: <br>
Enhanced coding agent for development workflows. Optimized for building features, fixing bugs, and code refactoring with OpenCode integration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rogerwengch](https://clawhub.ai/user/rogerwengch) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to run OpenCode for feature development, bug fixing, refactoring, testing, and related project maintenance tasks in a Git repository. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can run OpenCode on user-selected projects and may modify code. <br>
Mitigation: Use it only in a Git repository you are willing to let an agent edit, preferably on a branch or clean worktree. <br>
Risk: Background OpenCode runs can continue while project files change. <br>
Mitigation: Monitor background runs and review generated diffs before committing or deploying changes. <br>
Risk: Generated database migrations can affect persistent data or schema behavior. <br>
Mitigation: Review migration files carefully and test them in a non-production environment before applying them. <br>


## Reference(s): <br>
- [Development Coding Agent on ClawHub](https://clawhub.ai/rogerwengch/dev-coding-agent) <br>
- [Publisher profile: rogerwengch](https://clawhub.ai/user/rogerwengch) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May invoke OpenCode in a user-selected Git repository and may modify project files when the user runs the generated shell commands.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
