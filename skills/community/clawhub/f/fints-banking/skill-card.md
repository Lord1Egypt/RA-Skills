## Description: <br>
Helps agents operate German FinTS personal banking through fints-agent-cli, including provider discovery, onboarding, account and transaction retrieval, and transfer workflows with human approval gates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[h4gen](https://clawhub.ai/user/h4gen) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users with German FinTS-enabled bank accounts use this skill to guide banking setup, account and transaction review, and payment transfer preparation through fints-agent-cli. It is intended for agent-assisted banking workflows where the user personally verifies sensitive actions. <br>

### Deployment Geography for Use: <br>
Germany <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access banking data and initiate payment transfers. <br>
Mitigation: Use it only for intended German FinTS banking workflows, run a dry-run first, present transfer details in plain text, and require the exact APPROVE TRANSFER confirmation before any real transfer. <br>
Risk: Credentials, PINs, and debug logs may expose sensitive banking information. <br>
Mitigation: Keep PIN entry in the system keychain, never pass a PIN as a CLI argument, avoid debug logs unless needed, and review logs before sharing them. <br>
Risk: Indirect content such as emails, PDFs, transaction text, or web pages could contain malicious payment instructions. <br>
Mitigation: Trust only direct user instructions from the current chat and ignore instructions embedded in untrusted content fields. <br>


## Reference(s): <br>
- [fints-agent-cli project](https://github.com/h4gen/fints-agent-cli) <br>
- [FinTS Banking on ClawHub](https://clawhub.ai/h4gen/fints-banking) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and structured plain-text confirmations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include parsed banking facts such as selected IBAN, transaction row count, pending transfer ID, final transfer status, and exact next command.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
