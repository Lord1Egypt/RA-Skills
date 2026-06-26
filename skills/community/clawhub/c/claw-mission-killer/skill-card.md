## Description: <br>
Interrupts a running agent task and rolls back its session to before the last triggering user message. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[DorianYoung7702](https://clawhub.ai/user/DorianYoung7702) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to stop misdirected, stuck, or unintended agent work and restore the affected session to a pre-task state. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can force-stop running agent work. <br>
Mitigation: Use --dry-run first and prefer targeted --agent actions over all-agent interruption. <br>
Risk: The skill can rewrite session transcripts during rollback. <br>
Mitigation: Review the affected agent and keep the generated interrupt-log backup available for recovery. <br>
Risk: The installer and watcher can modify multiple agents' AGENTS.md files. <br>
Mitigation: Review AGENTS.md changes before applying them and avoid scheduling watch.py unless ongoing automatic integration is intended. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/DorianYoung7702/claw-mission-killer) <br>
- [AGENTS.md integration rules](references/agents-md-integration.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can direct local Python scripts that install agent integration, register running processes, interrupt agents, and roll back session transcripts.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
