## Description: <br>
ContextKeeper helps agents create manual project checkpoints and view local project status using foreground shell scripts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gopinathnelluri](https://clawhub.ai/user/gopinathnelluri) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and AI-agent users use ContextKeeper to save local work-session checkpoints, inspect recent project status, and resume context across sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The checkpoint helper writes and later reads persistent local project metadata under ~/.memory/contextkeeper. <br>
Mitigation: Use it only in trusted workspaces and review the created checkpoint and project-state files before relying on them. <br>
Risk: Project-ID path handling, JSON generation for filenames and paths, and dashboard timestamp parsing may affect files or dashboard behavior. <br>
Mitigation: Patch or review these script paths before operational use, especially when project names, paths, or checkpoint messages can contain unusual characters. <br>
Risk: Cron and session-hook automation are described as future behavior and should not be treated as an installed safety boundary. <br>
Mitigation: Keep any automation opt-in and review hook contents before enabling it. <br>


## Reference(s): <br>
- [Implementation Guide](references/implementation.md) <br>
- [ContextKeeper on ClawHub](https://clawhub.ai/gopinathnelluri/contextkeeper) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance and foreground shell-script output with JSON checkpoint files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes persistent local project metadata under ~/.memory/contextkeeper when checkpoint scripts are run.] <br>

## Skill Version(s): <br>
0.2.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
