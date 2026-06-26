## Description: <br>
exec-guard provides command execution for AI agents with timeout control, an 8KB head-tail output buffer, background process management, and CLI or HTTP service modes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cypress927](https://clawhub.ai/user/cypress927) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use exec-guard when an agent needs to run shell commands, start or monitor long-running processes, collect bounded command output, or share process state through a local HTTP service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Shell commands run with the privileges and environment of the exec-guard process. <br>
Mitigation: Install only where agent-driven command execution is intentional, run under a least-privilege account, and review commands before exposing the skill to agents. <br>
Risk: HTTP service mode can expose unauthenticated command execution if reachable by untrusted clients. <br>
Mitigation: Prefer CLI mode when possible; if server mode is required, isolate it on a trusted local network and place it behind strong authentication and network controls. <br>
Risk: Inherited environment variables can expose secrets to child processes. <br>
Mitigation: Avoid starting exec-guard with sensitive environment variables and pass only the minimum required overrides for each command. <br>
Risk: Background processes can continue consuming host resources after the initiating agent moves on. <br>
Mitigation: Use timeouts and process limits, monitor background processes, and terminate unneeded processes promptly. <br>


## Reference(s): <br>
- [exec-guard Agent Guide](references/AGENT_GUIDE.md) <br>
- [exec-guard README](references/README.md) <br>
- [ClawHub skill page](https://clawhub.ai/cypress927/exec-guard) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [JSON command responses with status, exit code, stdout, stderr, and process metadata; Markdown documentation with command examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Command output is bounded by an 8KB head-tail buffer, with background process status and logs available through CLI or HTTP interfaces.] <br>

## Skill Version(s): <br>
1.0.6 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
