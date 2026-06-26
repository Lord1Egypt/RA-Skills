## Description: <br>
Access and manage Bitwarden/Vaultwarden passwords securely using the rbw CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Asleep123](https://clawhub.ai/user/Asleep123) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to configure rbw, authenticate to Bitwarden or Vaultwarden, sync the vault, and list, search, retrieve, or add vault items from an agent session. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Retrieved vault entries can become visible to the agent session, terminal output, logs, or conversation transcript. <br>
Mitigation: Retrieve only the secrets needed for the task, avoid printing full secret values unless necessary, and review commands before execution. <br>
Risk: The skill can run rbw commands against a Bitwarden or Vaultwarden vault after the user authorizes access. <br>
Mitigation: Use the skill only in trusted agent sessions, authenticate intentionally, and keep vault access scoped to the current task. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Asleep123/bitwarden) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the rbw CLI and user-authorized Bitwarden or Vaultwarden access for vault operations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
