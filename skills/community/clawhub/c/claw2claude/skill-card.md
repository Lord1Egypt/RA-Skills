## Description: <br>
Delegates tasks from OpenClaw to the local Claude Code CLI for discussion, execution, continuation, or background work. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[is-xins-xiaobai](https://clawhub.ai/user/is-xins-xiaobai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to hand complex work to a local Claude Code session while keeping session state, result delivery, and project context coordinated through OpenClaw. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs Claude Code unattended with skipped permission prompts. <br>
Mitigation: Install only for trusted project directories, review generated changes and logs, and use direct Claude Code sessions when interactive permission prompts are required. <br>
Risk: Background helper processes can deliver results across OpenClaw sessions when the required gateway settings are enabled. <br>
Mitigation: Enable the required OpenClaw settings only in environments where cross-session delivery is intended and avoid highly sensitive or multi-user deployments without tighter scoping. <br>
Risk: Prompts, logs, and generated files may expose sensitive project context. <br>
Mitigation: Avoid secrets in prompts and review `.claude-last-run.log`, `.claude-notify.json`, and monthly skill logs according to local retention and access policies. <br>


## Reference(s): <br>
- [Claw2Claude ClawHub release](https://clawhub.ai/is-xins-xiaobai/claw2claude) <br>
- [Claude Code](https://claude.ai/code) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown responses and generated project files produced through a delegated Claude Code session] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write project files, session state, logs, and result notification files in the configured project and skill directories.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
