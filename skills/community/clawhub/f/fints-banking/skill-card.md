## Description:

FinTS Banking helps agents operate German personal online banking through fints-agent-cli, including provider discovery, onboarding, account and transaction retrieval, and guarded transfer workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[h4gen](https://clawhub.ai/user/h4gen)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to operate German FinTS banking tasks with fints-agent-cli, including setup, balance and transaction retrieval, and transfer workflows that require explicit approval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Payment commands can initiate real financial transfers.

Mitigation: Run a side-effect-free dry run or preflight first, show every transfer field, and require the exact phrase APPROVE TRANSFER before any real transfer command.

Risk: The asynchronous transfer-submit flow can submit a real transfer without repeating the final approval gate.

Mitigation: Do not use transfer-submit unless the same session already completed a preflight, field inspection, and explicit approval for the exact transaction.

Risk: Bank credentials, PINs, or sensitive banking context could be exposed through unsafe handling or diagnostics.

Mitigation: Use the system keychain, never pass PINs as CLI arguments, and reserve debug output for targeted diagnosis.

Risk: The skill depends on the third-party fints-agent-cli package.

Mitigation: Install only after reviewing and trusting the package source and verifying the package version being used.

## Reference(s):

- [FinTS Banking ClawHub skill page](https://clawhub.ai/h4gen/skills/fints-banking)
- [fints-agent-cli GitHub repository](https://github.com/h4gen/fints-agent-cli)
- [COMMANDS.md command reference](artifact/COMMANDS.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and expected command outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes command execution reporting expectations and explicit approval gates for payment-related actions.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
