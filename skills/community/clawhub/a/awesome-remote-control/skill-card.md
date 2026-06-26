## Description: <br>
Start a Claude Code remote control session in tmux with bypass permissions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oobagi](https://clawhub.ai/user/oobagi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to launch, list, stop, resume, and send tasks to persistent Claude Code remote-control sessions for a selected project directory. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent remote-control sessions can operate with normal permission checks bypassed. <br>
Mitigation: Install and run the skill only for trusted projects where remote-control access and bypass permissions are intentional. <br>
Risk: Session URLs and resume UUIDs can grant access to active or resumable sessions. <br>
Mitigation: Treat session URLs and resume UUIDs as secrets and stop sessions when work is complete. <br>
Risk: The skill updates Claude workspace trust state for the target project. <br>
Mitigation: Review the ~/.claude.json trust change for the project directory before relying on the launched session. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/oobagi/awesome-remote-control) <br>
- [OpenClaw](https://github.com/openclaw/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and session URLs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local session registry and Claude configuration changes when its scripts are run.] <br>

## Skill Version(s): <br>
1.0.8 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
