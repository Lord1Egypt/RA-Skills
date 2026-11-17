## Description:

Sends text notes and memos to flomo using its webhook API, with tag support and setup guidance for flomo PRO users.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qiantao1001](https://clawhub.ai/user/qiantao1001)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to configure a flomo webhook and send short text notes, links, clippings, and tagged memos from an agent workflow to their flomo inbox.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Webhook delivery sends note content to flomo servers and requires a user-specific webhook token.

Mitigation: Use only webhook values copied directly from flomo, keep tokens private, and rotate the token if it is exposed.

Risk: Persistent configuration can store the webhook token in a local .env file or a shell startup file.

Mitigation: Prefer the local .env option with restricted permissions and avoid writing the token to shell startup files.

Risk: The send script sources .env as shell configuration before sending notes.

Mitigation: Inspect or harden the scripts before use and store only trusted key-value configuration in .env.

Risk: The artifact text is inconsistent about URL Scheme fallback while the implementation is webhook-only.

Mitigation: Treat webhook delivery as the supported behavior and verify script behavior before relying on URL Scheme or image support.

## Reference(s):

- [Flomo API Reference](references/api.md)
- [flomo official API help](https://help.flomoapp.com/advance/api.html)
- [flomo incoming webhook settings](https://flomoapp.com/mine?source=incoming_webhook)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and script invocations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces webhook-based flomo note submissions; requires flomo PRO webhook configuration.]

## Skill Version(s):

1.0.0 (source: release metadata and _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
