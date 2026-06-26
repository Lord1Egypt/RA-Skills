## Description: <br>
Dispatches prompts to Claude Code on a configured remote machine through FastAPI, Redis, or SSH screen channels with retry handling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zzz123hash](https://clawhub.ai/user/zzz123hash) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to send explicit Claude Code tasks to a configured remote machine and check their execution status and results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad remote execution paths can run Claude Code on a target project if the API, Redis queue, or SSH path is exposed. <br>
Mitigation: Install only when remote execution is intentional, add API and Redis authentication plus network restrictions, and limit access to trusted operators. <br>
Risk: Permission bypass and screen fallback behavior can execute changes without normal interactive approval. <br>
Mitigation: Remove bypassPermissions or require explicit approval, disable the screen fallback unless it is needed, and review task prompts before submission. <br>
Risk: Background worker and API services may continue accepting work after setup or testing. <br>
Mitigation: Run services under a dedicated low-privilege account and document how to start, stop, monitor, and remove them. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/zzz123hash/cc-remote) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Command-line text output and remote Claude Code task results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a configured remote host, Redis queue, FastAPI service, SSH access, and Claude Code on the target machine.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
