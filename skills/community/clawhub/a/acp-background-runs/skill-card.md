## Description: <br>
Routes requests for ACP or external coding agents into non-blocking OpenClaw background ACP runs so the current conversation can continue. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ambition0802](https://clawhub.ai/user/ambition0802) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to dispatch ACP, Codex, Claude Code, Gemini CLI, or OpenCode work as background runs while keeping the current chat responsive. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Background delegation can send task context, repository paths, or sensitive instructions to an external coding agent. <br>
Mitigation: Confirm the target agent and repository path before submission, and avoid including secrets unless the selected background agent is trusted. <br>
Risk: Imprecise requests can start background work in the wrong directory or with the wrong execution mode. <br>
Mitigation: Use explicit task instructions, set a known absolute working directory when available, and reserve persistent sessions or progress streaming for explicit user requests. <br>


## Reference(s): <br>
- [ACP Background Runs on ClawHub](https://clawhub.ai/ambition0802/acp-background-runs) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, configuration] <br>
**Output Format:** [Markdown with JSON parameter examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only skill; outputs routing guidance and background-run parameter choices.] <br>

## Skill Version(s): <br>
0.1.2 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
