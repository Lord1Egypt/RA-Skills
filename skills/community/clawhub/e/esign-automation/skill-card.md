## Description:

Automates eSignGlobal contract signing workflows through the eSignGlobal CLI, including draft envelopes, sender links, sending, status checks, reminders, cancellation, downloads, signature verification, template rendering, contract comparison, attachments, CC recipients, and signer management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[esign-cn-open-source](https://clawhub.ai/user/esign-cn-open-source)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to send and manage e-signature workflows for PDF contracts, templates, recipients, reminders, downloads, signature validation, and document comparisons in eSignGlobal.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles contracts, signer details, PDFs, and an API key while invoking an unpinned third-party CLI.

Mitigation: Use a pinned, vetted version of the eSignGlobal CLI from a controlled source, provide a least-privilege ESIGNGLOBAL_APIKEY, and expose only the specific PDFs required for the task.

Risk: Send, template render, contract compare, and related workflows may transmit documents and recipient details to eSignGlobal.

Mitigation: Confirm user intent before actions that upload, send, compare, or modify envelopes, and use only deployments approved for the documents and recipient data involved.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/esign-cn-open-source/skills/esign-automation)
- [eSignGlobal website](https://www.esignglobal.com?source=agent)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands, JSON command arguments, URLs, and formatted status or signature summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses ESIGNGLOBAL_APIKEY and user-provided envelope IDs, file keys, signer details, and absolute PDF file paths.]

## Skill Version(s):

1.7.5 (source: release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
