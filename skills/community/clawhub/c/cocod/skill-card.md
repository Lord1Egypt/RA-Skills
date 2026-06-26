## Description: <br>
A Cashu ecash wallet CLI for Bitcoin and Lightning payments. Use when managing Cashu tokens, sending/receiving payments via Lightning (bolt11) or ecash, handling HTTP 402 X-Cashu payment requests, or viewing wallet history. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[egge21m](https://clawhub.ai/user/egge21m) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to operate the cocod CLI for Cashu ecash, Bitcoin Lightning payments, HTTP 402 X-Cashu settlement, mint management, and wallet history review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Wallet commands can spend real funds through Cashu or Lightning flows. <br>
Mitigation: Preview payment requests when possible and require explicit user approval before any spend command. <br>
Risk: Wallet state, mnemonics, passphrases, sockets, and daemon files under ~/.cocod are sensitive. <br>
Mitigation: Do not log or expose ~/.cocod contents, mnemonics, or passphrases unless the user explicitly requests a specific safe subset. <br>
Risk: Using an unexpected cocod package or version can change wallet behavior. <br>
Mitigation: Verify the installed cocod package and exact 0.0.15 CLI version before use. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include commands that inspect wallet state, receive funds, or spend funds only after explicit user approval.] <br>

## Skill Version(s): <br>
0.0.15 (source: server release metadata and SKILL.md metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
