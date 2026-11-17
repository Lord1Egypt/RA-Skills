## Description:

Sends Gmail messages from an operator-controlled Chrome debug session using Chrome DevTools Protocol automation, with support for plain-text bodies and attachments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[joustonhuang](https://clawhub.ai/user/joustonhuang)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and operators use this skill to send Gmail messages from a local, visible Chrome debug session when a recipient, optional body text, and optional attachments are provided. It is intended for controlled email delivery workflows that require manual session visibility and Sent-folder verification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Gmail automation could delete or alter an unrelated existing draft in the debug browser session.

Mitigation: Use a dedicated Chrome debug profile for this skill and confirm there are no unrelated Gmail drafts open before running the send flow.

Risk: Attachments or messages could be sent to the wrong recipient if compose-field validation fails or the wrong draft is active.

Mitigation: Manually confirm the recipient, unique subject, and all requested attachment filenames in the visible compose draft before sending, then verify the Sent folder by unique subject.

Risk: Sensitive or blocked attachments may be mishandled by repeated upload attempts or provider security filters.

Mitigation: Avoid sensitive files unless necessary, preflight Gmail attachment limits and blocked file classes, and use the documented Drive fallback only after verifying sharing permissions.

Risk: Runtime dependency installation can introduce supply-chain exposure.

Mitigation: Review dependency installation before use and prefer a pinned, local runtime install for puppeteer-core.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/joustonhuang/skills/cdp-gmail-delivery)
- [Google Drive Fallback Delivery](references/drive-fallback.md)
- [Troubleshooting](references/troubleshooting.md)
- [Receipts](references/receipts.md)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and plain-text command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports plain-text email bodies plus optional attachments; success should be reported only after command output and Sent-folder verification by unique subject.]

## Skill Version(s):

1.0.8 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
