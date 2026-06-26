## Description: <br>
Orchestrates the full BMAD Method workflow across OpenClaw and Claude Code, including interactive planning phases with the user and implementation delegation through tmux. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[henrikrexed](https://clawhub.ai/user/henrikrexed) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and technical project leads use this skill to guide BMAD projects through brainstorming, product brief, PRD, architecture, implementation planning, and Claude Code-driven execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A remote Claude Code session can modify and commit project code with broad authority. <br>
Mitigation: Use a disposable VM or least-privileged account, run on a separate branch or clone, and review commits before merging. <br>
Risk: Permission-bypass modes and persistent tmux or cron monitoring can continue beyond the intended task. <br>
Mitigation: Avoid permission-bypass modes unless explicitly accepted, and confirm tmux sessions and cron monitors are removed when work finishes. <br>


## Reference(s): <br>
- [BMAD Claude Code Commands](references/bmad-commands.md) <br>
- [tmux Setup & Interaction Patterns](references/tmux-setup.md) <br>
- [ClawHub release page](https://clawhub.ai/henrikrexed/bmad-orchestrator) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands and YAML state examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces planning artifacts and orchestration instructions; delegated implementation may produce code and tests through Claude Code.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
