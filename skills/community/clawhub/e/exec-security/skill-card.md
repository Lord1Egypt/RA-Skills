## Description: <br>
Exec Security provides pre-execution validation for shell commands, flagging destructive operations, credential leaks, data exfiltration, download-and-execute patterns, injection, Unicode obfuscation, resource exhaustion, and system file tampering before an agent runs exec or bash tools. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yozu](https://clawhub.ai/user/yozu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to review non-trivial shell commands before execution, especially commands built programmatically, derived from external data, or touching destructive tools, sensitive paths, pipes, redirections, or substitutions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is advisory and does not provide sandboxing or runtime enforcement. <br>
Mitigation: Pair it with OpenClaw exec approval controls such as allowlists or deny mode, and require explicit user confirmation for high-risk commands. <br>
Risk: Pattern-based review can miss encoded, multi-step, symlink, or context-dependent attacks. <br>
Mitigation: Inspect commands in context, resolve paths before writes, avoid executing untrusted downloaded scripts directly, and prefer safe alternatives. <br>
Risk: The skill may add warnings or confirmation prompts around deletion, secret exposure, outbound transfers, remote scripts, and system-file edits. <br>
Mitigation: Treat warnings as checkpoints for review and user confirmation rather than complete proof that a command is malicious. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yozu/exec-security) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with command examples and refusal or confirmation recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Advisory pre-execution assessment; no runtime enforcement.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
