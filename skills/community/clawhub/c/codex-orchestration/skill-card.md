## Description: <br>
General-purpose orchestration for Codex that uses update_plan and background PTY terminals to run parallel codex exec workers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shanelindsay](https://clawhub.ai/user/shanelindsay) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and Codex users use this skill to coordinate multi-step work, delegate scoped worker tasks, and synthesize results while retaining control of the final answer. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill coordinates background workers and shell commands, which can expand the impact of a mistaken prompt or command. <br>
Mitigation: Use it only in trusted workspaces, keep worker scopes narrow, and review worker outputs before acting on them. <br>
Risk: The documented no-approval posture can lead to unintended command execution or edits. <br>
Mitigation: Prefer read-only worker prompts unless edits are explicitly intended, and avoid exposing sensitive credentials or private data unless necessary. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/shanelindsay/codex-orchestration) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, markdown, text] <br>
**Output Format:** [Markdown guidance with inline shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Coordinates worker prompts, plan updates, and command execution patterns for Codex sessions.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
