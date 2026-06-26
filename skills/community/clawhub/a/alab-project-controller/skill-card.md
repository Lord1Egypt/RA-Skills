## Description: <br>
Coordinates one existing ALab project with a project admin key, including experiment creation, configuration validation, project evidence review, and token-isolated worker handoff. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bebetterest](https://clawhub.ai/user/bebetterest) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and project operators use this skill to coordinate ALab project-level workflows, create and compare experiments, manage scoped configuration and lifecycle state, and delegate experiment work without exposing project admin credentials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide powerful project-level ALab actions, including lifecycle changes and worker delegation. <br>
Mitigation: Install only for ALab project-level workflows, review destructive lifecycle actions before force or confirm removal, and use dry-run behavior where available. <br>
Risk: Project admin keys or unrelated tokens could be exposed to experiment worker sessions if credentials are passed through prompts, argv, copied files, or inherited environments. <br>
Mitigation: Provide project admin keys only through private environment variables or secure stdin, and ensure delegated workers receive only experiment worktree tokens. <br>


## Reference(s): <br>
- [ALab Project Controller Commands](references/commands.md) <br>
- [ALab Project Controller Commands (Chinese)](references/commands_cn.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/bebetterest/alab-project-controller) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and configuration references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Project-level summaries should identify created or reused experiments, relevant runs or commits, withheld credentials, and safe follow-up artifacts.] <br>

## Skill Version(s): <br>
0.1.9 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
