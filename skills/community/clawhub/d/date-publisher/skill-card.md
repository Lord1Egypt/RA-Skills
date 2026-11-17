## Description:

Prepares platform-specific drafts and approved public adult dating profile publications from one canonical showme card.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dongsheng123132](https://clawhub.ai/user/dongsheng123132)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to turn an approved dating profile card into target-specific drafts, previews, publication actions, and distribution records. It supports public and voluntary dating-profile distribution with per-target confirmation gates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Public dating-profile publication can expose personal profile details, photos, contact methods, accounts, visibility settings, and public URLs.

Mitigation: Use a dedicated public contact method, review each publication preview, and approve only targets where public visibility is acceptable.

Risk: Profile content could be published to a target the user did not intend to authorize.

Mitigation: Require explicit per-target confirmation before account creation, OAuth authorization, pull requests, posts, messages, or other publication actions.

Risk: Private contact details or sensitive data could be included in distribution records.

Mitigation: Keep distribution logs limited to approved fields, public URLs, dates, targets, and status, and exclude tokens, passwords, private messages, home addresses, work addresses, and private chat IDs.

## Reference(s):

- [Platform Modes](references/platform-modes.md)
- [ClawHub Skill Page](https://clawhub.ai/dongsheng123132/skills/date-publisher)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown, JSON snippets, and copy-ready text drafts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires explicit per-target approval before publication or account authorization.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
