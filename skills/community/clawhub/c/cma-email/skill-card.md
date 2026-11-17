## Description:

Sends an email via Gmail when a message starts with "cma" or "cmap".

This skill is ready for commercial/non-commercial use.

## Publisher:

[mtbf999](https://clawhub.ai/user/mtbf999)

### License/Terms of Use:


## Use Case:

People who use ClawHub agent skills can send short Gmail messages to fixed CMA or CMAP recipients by starting a message with the matching prefix.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Messages that start with cma or cmap can send user-provided text to fixed external email addresses without a preview or approval step.

Mitigation: Install only when immediate prefix-triggered email sending is intended; review the recipient route, subject, and body before using the trigger with sensitive content.

Risk: The skill depends on the gog Gmail integration to send mail from the connected account.

Mitigation: Confirm the gog skill is configured for the intended Gmail account and permissions before enabling this shortcut.

Risk: A normal message beginning with the trigger prefix could be treated as an email command.

Mitigation: Use the cma and cmap prefixes only for deliberate email sends, and consider adding a preview or confirmation step before deployment.

## Reference(s):

- [CMA Email Skill Page](https://clawhub.ai/mtbf999/skills/cma-email)
- [mtbf999 Publisher Profile](https://clawhub.ai/user/mtbf999)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text confirmation and a Gmail send command routed through the gog skill]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Parses a cma or cmap prefix, optional subject/body separator, and fixed recipient before sending.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
