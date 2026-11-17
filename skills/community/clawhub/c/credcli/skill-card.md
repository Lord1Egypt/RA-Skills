## Description:

Guides agents through using CredCLI to generate, render, upload, stamp, and email mail-merged digital credentials through Chainletter.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ntbooks](https://clawhub.ai/user/ntbooks)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to issue batches of personalized certificates, credentials, diplomas, badges, and claim emails with CredCLI. It helps them set up a Chainletter-backed workspace, prepare CSV recipient data, render PDF or PNG outputs, and manage public or private issuance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on an external CredCLI and Chainletter workflow with network access, package installation, uploads, email delivery, and blockchain stamping.

Mitigation: Pin and verify the CLI, restrict network access to required Chainletter and stamping service hosts, and require explicit review before upload, email delivery, or stamping.

Risk: The workflow can involve Chainletter tokens and SMTP credentials.

Mitigation: Avoid placing real tokens or SMTP passwords directly in commands or shared logs, and use scoped credentials where possible.

Risk: Public issuance can make credentials accessible and verifiable by recipients, while stamping may be irreversible.

Mitigation: Confirm public versus private issuance with the user early, review recipient data and collection assignment, and get final approval before public upload, email delivery, or blockchain stamping.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/ntbooks/skills/credcli)
- [Publisher profile](https://clawhub.ai/user/ntbooks)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with CLI command examples and configuration steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The guided workflow can result in generated PDF or PNG credentials, CSV and job files, email files, mailbox files, uploads, email delivery, and blockchain stamping when the agent runs CredCLI.]

## Skill Version(s):

0.2.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
