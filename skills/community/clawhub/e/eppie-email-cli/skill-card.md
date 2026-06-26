## Description: <br>
Guides an agent to operate the eppie-console email CLI for account, folder, message, synchronization, sending, and vault workflows with structured automation patterns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[eppieapp](https://clawhub.ai/user/eppieapp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation agents use this skill to run eppie-console predictably for reading, sending, syncing, account setup, and local vault management. It is intended for workflows that need machine-readable CLI output and explicit standard-input contracts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill enables agents to operate real email mailboxes and local vaults, including account-changing actions. <br>
Mitigation: Require explicit user confirmation before send, reset, delete-message, and other account-changing commands. <br>
Risk: Reset and delete-message workflows can remove mailbox or vault data, including permanent deletion for messages already in Trash. <br>
Mitigation: Use disposable or isolated working directories for destructive tests and avoid high-value mailboxes until the workflow has been validated. <br>
Risk: Mailbox and provider credentials may be exposed if passed through command-line arguments or logs. <br>
Mitigation: Pass vault passwords and provider secrets through the documented stdin contracts and avoid logging raw command input. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/eppieapp/eppie-email-cli) <br>
- [Eppie CLI releases](https://github.com/Eppie-io/Eppie-CLI/releases/latest) <br>
- [Eppie CLI repository](https://github.com/Eppie-io/Eppie-CLI) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, code] <br>
**Output Format:** [Markdown with inline shell commands, JSON examples, and structured command tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Emphasizes JSON CLI output, exact stdin ordering, bounded pagination, and explicit handling of warning and error envelopes.] <br>

## Skill Version(s): <br>
0.2.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
