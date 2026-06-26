## Description: <br>
Exec Tool securely executes predefined ClawHub CLI commands within controlled OpenClaw workflows while aiming to prevent unsafe or arbitrary system operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mayuran1096](https://clawhub.ai/user/mayuran1096) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to trigger approved ClawHub CLI operations from automation layers such as OpenClaw workflows, chat interfaces, VPS management flows, and CI/CD command triggers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill executes shell commands after only a weak command-prefix check, so unintended shell commands may run. <br>
Mitigation: Run it only in a sandboxed and restricted environment, and replace free-form command strings with structured parameters that allow only specific ClawHub subcommands and flags. <br>
Risk: Connecting the skill to chat bots, agents, CI/CD, or production VPS environments can expose local, account, or deployment state to command-triggered changes. <br>
Mitigation: Require human confirmation for state-changing operations and avoid production integrations unless isolation, permissions, and audit controls are in place. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mayuran1096/exec-tool) <br>
- [Publisher profile](https://clawhub.ai/user/mayuran1096) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text command output trimmed for chat-oriented interfaces] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns command output up to approximately 4000 characters.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and clawdis metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
