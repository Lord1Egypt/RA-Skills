## Description: <br>
Recover the local Chromium/Chrome environment for OpenClaw browser tool failures by diagnosing stale processes, CDP port conflicts, lock files, and page freezes, then running targeted cleanup before one retry. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wind0ws](https://clawhub.ai/user/wind0ws) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and developers use this skill to diagnose and recover local OpenClaw Chromium/Chrome sessions after startup, CDP connection, port, lock-file, or freeze failures. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Recovery may terminate local browser processes or services listening on common browser debug ports. <br>
Mitigation: Run check_state.sh first, inspect the listed PIDs and command lines, and prefer targeted recovery flags in an isolated OpenClaw container or workspace. <br>
Risk: Full recovery can remove browser lock and cache files from the configured OpenClaw profile. <br>
Mitigation: Avoid default full recovery on personal machines unless needed, and back up or rename the browser profile before deleting profile data. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/wind0ws/browser-recover) <br>
- [Browser Recovery Configuration](references/configuration.md) <br>
- [Safety Guidelines for Browser Recovery](references/safety.md) <br>
- [Browser Recovery Troubleshooting Guide](references/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May instruct the agent to run diagnostic and recovery scripts, inspect process and port state, and retry a browser operation once.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
