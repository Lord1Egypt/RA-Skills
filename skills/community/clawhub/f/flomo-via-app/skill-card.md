## Description:

Sends text notes and tagged memos to flomo through a configured webhook, with setup guidance for storing a flomo PRO webhook token.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qiantao1001](https://clawhub.ai/user/qiantao1001)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent users use this skill to capture thoughts, links, clipboard text, and tagged notes into a flomo inbox from shell commands or agent workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends note content through a flomo webhook.

Mitigation: Install and use it only when sending the note content to flomo is acceptable, and inspect the destination webhook before saving or using it.

Risk: Webhook tokens may be persisted in local files or shell profile configuration.

Mitigation: Treat the token as a secret, prefer the permission-restricted local .env configuration, and rotate the token if it is exposed.

Risk: The package documentation and scripts are inconsistent about URL Scheme support and webhook-only behavior.

Mitigation: Rely on the current script behavior and review the package before installation until the documentation is aligned with the implementation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qiantao1001/skills/flomo-via-app)
- [flomo webhook settings](https://flomoapp.com/mine?source=incoming_webhook)
- [flomo API reference](https://help.flomoapp.com/advance/api.html)
- [Bundled API reference](artifact/references/api.md)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires flomo PRO webhook configuration; sends note content to flomo servers over HTTPS.]

## Skill Version(s):

1.0.8 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
