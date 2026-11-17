## Description:

Creates contract or agreement drafts, formats them as PDFs, and uses eSign APIs to start, manage, download, and verify electronic signing workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[esign-cn-open-source](https://clawhub.ai/user/esign-cn-open-source)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to draft Chinese-language contracts, convert approved drafts to PDFs, upload existing contract files, start e-signature workflows, query progress, revoke workflows, download signed files, and verify signatures.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Long-lived eSign App Secrets may be pasted into chat or persisted in local configuration.

Mitigation: Prefer manual credential setup, restrict file permissions on the credential file, and rotate secrets if they were exposed in chat or logs.

Risk: The artifact describes automatic changes to agent tool permissions for some environments.

Mitigation: Review any tool permission changes before installation and keep only the minimum script commands needed for the intended workflow.

Risk: Contracts and signed downloads can contain sensitive personal, business, and legal information.

Mitigation: Use explicit private output locations, avoid shared temporary folders for sensitive files, and delete local copies when retention is not required.

Risk: Signing and revocation actions can have legal or workflow consequences.

Mitigation: Require user confirmation before starting or revoking a signing flow and review generated contract content before sending links.

Risk: API calls could be sent to an unexpected endpoint if ESIGN_BASE_URL is changed.

Mitigation: Allow only the official production endpoint or official sandbox endpoint documented in the evidence.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/esign-cn-open-source/skills/esign-contract)
- [Contract generation guide](references/contract-generation.md)
- [Signing guide](references/signing-guide.md)
- [Error handling guide](references/error-handling.md)
- [eSign official website](https://www.esign.cn)
- [eSign open platform](https://open.esign.cn)
- [eSign API documentation](https://open.esign.cn/doc)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with generated contract text, PDF files, API-backed signing links, status summaries, and local file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local configuration, token cache, workflow history, contract drafts, PDFs, and downloaded signed documents.]

## Skill Version(s):

1.0.5 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
