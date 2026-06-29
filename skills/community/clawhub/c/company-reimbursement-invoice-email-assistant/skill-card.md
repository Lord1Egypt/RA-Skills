## Description: <br>
This skill helps an agent process company reimbursement invoice emails by scanning a configured mailbox, downloading invoice attachments or links, extracting invoice fields, generating ledgers, and archiving invoice PDFs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[peter-zx](https://clawhub.ai/user/peter-zx) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Finance operations users and their agents use this skill to collect company reimbursement invoice emails, extract invoice details, produce reviewable ledgers, and organize PDF invoice archives. It is scoped to invoice-related mailbox workflows and excludes general email reading or correspondence analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles mailbox credentials while processing invoice email. <br>
Mitigation: Use a dedicated mailbox or app password, keep credentials local, and do not echo or commit secrets. <br>
Risk: Generated scan results, ledgers, and archives can contain sensitive financial data. <br>
Mitigation: Run the skill in a restricted local workspace and treat scan-results/ and archive/ as confidential outputs. <br>
Risk: Email links and attachment downloads may be unsafe or overbroad when run on untrusted mailboxes or large date ranges. <br>
Mitigation: Review before installing, prefer narrow date ranges, and improve link allowlisting before broad operational use. <br>
Risk: TLS certificate rejection is configured as false in the artifact's example environment. <br>
Mitigation: Set IMAP_REJECT_UNAUTHORIZED to true unless there is a controlled test reason to disable certificate validation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/peter-zx/company-reimbursement-invoice-email-assistant) <br>
- [Artifact README](artifact/README.md) <br>
- [Agent workflow](artifact/docs/AGENT_WORKFLOW.md) <br>
- [Project design](artifact/docs/PROJECT_DESIGN.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with inline shell commands and generated local files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [When run against a configured mailbox, the skill can produce Excel and CSV ledgers, JSON records, manual task lists, HTML archive indexes, and organized invoice PDF archives.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
