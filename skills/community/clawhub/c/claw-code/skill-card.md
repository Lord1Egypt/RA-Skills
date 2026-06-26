## Description: <br>
TypeScript runtime port of Claude Code's AI agent harness for running commands, routing prompts, managing sessions, and auditing tool and command registries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dae-xiaoe](https://clawhub.ai/user/dae-xiaoe) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to inspect and exercise a Claude Code-like agent harness, including command and tool registries, prompt routing, session bootstrapping, and parity audit reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill exposes a CLI harness and mirrored command/tool names that resemble sensitive operations, including shell, file, SSH, remote, and credential-related workflows. <br>
Mitigation: Install only when a harness or registry simulator is needed, and review command output before relying on it; server security evidence reports these behaviors as static placeholders rather than real credential, filesystem, MDM, or network access. <br>
Risk: Parity audit behavior may be incomplete when the original archive snapshot is unavailable. <br>
Mitigation: Treat parity audit output as advisory and confirm critical compatibility claims against the intended source archive. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dae-xiaoe/claw-code) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and plain text CLI output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Command outputs summarize harness state, registries, routing decisions, session records, and parity audit status.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and scripts/package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
