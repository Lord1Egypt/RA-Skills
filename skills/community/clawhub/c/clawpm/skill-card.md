## Description: <br>
Multi-project task and research management (JSON-first CLI). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[malphas-gh](https://clawhub.ai/user/malphas-gh) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to manage tasks, project context, research notes, blockers, issues, and work logs across local projects through the clawpm CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on an external local CLI package, which carries normal supply-chain risk. <br>
Mitigation: Install only if you trust the GitHub source for the CLI, and review or pin the repository in sensitive environments. <br>
Risk: The CLI creates and updates local project, task, research, issue, and work-log files. <br>
Mitigation: Use it in intended project directories and review generated or updated local state before relying on it. <br>
Risk: Task notes, research notes, blockers, and work logs may capture sensitive user-entered content. <br>
Mitigation: Avoid putting secrets into tasks, research notes, blockers, or work logs. <br>


## Reference(s): <br>
- [Clawpm homepage](https://github.com/malphas-gh/clawpm) <br>
- [ClawHub skill page](https://clawhub.ai/malphas-gh/clawpm) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with CLI command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The underlying CLI emits JSON by default and supports text output with -f text.] <br>

## Skill Version(s): <br>
0.1.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
