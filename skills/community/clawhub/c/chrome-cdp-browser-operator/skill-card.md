## Description:

Windows-friendly Chrome automation through an existing Chrome profile via CDP, with human-like mouse and keyboard input, browser attachment checks, page navigation, search workflows, guarded drafting, and optional notifications.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ugurinanc12](https://clawhub.ai/user/ugurinanc12)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill when an agent needs to attach to a dedicated, already logged-in Chrome profile over CDP, verify browser connectivity, search X, draft reviewable replies, and optionally post replies after explicit configuration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can operate a logged-in Chrome profile, which may expose account data or perform actions as that user.

Mitigation: Use only a dedicated low-privilege Chrome profile, keep CDP bound to localhost, and avoid using the operator from a personal or privileged browser profile.

Risk: Apply mode and public replies can post from the logged-in X account when enabled.

Mitigation: Run search and run-cycle in draft mode first, review the output bundle, and enable --apply only when allowPublicReply is intentionally configured.

Risk: The operator can collect contact details from posts and send optional Telegram notifications.

Mitigation: Disable Telegram unless the destination, account, and message contents are approved for the data being handled.

## Reference(s):

- [CDP Setup](references/cdp-setup.md)
- [ClawHub release page](https://clawhub.ai/ugurinanc12/skills/chrome-cdp-browser-operator)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance, Python and PowerShell commands, JSON configuration, and JSON run outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can produce browser search bundles, draft reply bundles, state files, starter scripts, and optional notification messages.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
