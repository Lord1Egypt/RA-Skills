## Description: <br>
Dmn Default Mode Network is an autonomous thinking engine that helps an idle agent digest recent memories, connect knowledge-base notes, critique ideas through expert personas, and propose concrete engineering actions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mikonos](https://clawhub.ai/user/mikonos) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill to let an idle agent perform background reflection over configured memory and knowledge-base files, then produce synthesis notes and action proposals. It is most useful for personal knowledge management, strategy review, and proactive engineering ideation where outputs are reviewed before execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can prompt unattended review of configured memory and knowledge-base files, which may expose sensitive personal or project notes. <br>
Mitigation: Start with manual runs, restrict configured directories to non-sensitive notes, and review generated synthesis files before relying on them. <br>
Risk: Generated action proposals may suggest installs, repository clones, scripts, skill changes, or self-evolution work that should not run without oversight. <br>
Mitigation: Require explicit user approval before executing any proposed command, code change, installation, repository clone, or self-evolve action. <br>
Risk: Persistent outputs and entries in memory/evolve/candidates.md can influence later agent behavior. <br>
Mitigation: Inspect and prune persistent outputs and queued proposals regularly, especially before enabling automated follow-up workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mikonos/dmn-default-mode-network) <br>
- [README](README.md) <br>
- [Core Functions](references/core-functions.md) <br>
- [Execution Flow](references/execution-flow.md) <br>
- [User Configuration](assets/user-config.md) <br>
- [Session Synthesis Template](assets/session-synthesis.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Files, Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown notes and synthesis files with structured action proposals and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May append self-evolution proposals to a configured queue when the user enables that workflow.] <br>

## Skill Version(s): <br>
3.3.0 (source: server release metadata and SKILL.md heading, released 2026-02-27) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
