## Description:

Manage Freshdesk tickets, notes, watchers, conversations, and support workflows via the Freshdesk API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hith3sh](https://clawhub.ai/user/hith3sh)

### License/Terms of Use:

MIT-0

## Use Case:

Support teams and agents use this skill to inspect Freshdesk tickets, manage conversations and notes, update ticket fields, and coordinate customer-support workflows from an agent chat.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on a persistent ClawLink plugin that handles connected Freshdesk access.

Mitigation: Install only if comfortable using ClawLink for Freshdesk, use a Freshdesk account with minimum necessary permissions, and revoke the ClawLink connection when it is no longer needed.

Risk: Freshdesk write actions can create, update, delete, or expose support ticket content.

Mitigation: Preview and confirm each write or destructive action, including the target ticket or resource and whether content is public or private.

Risk: Ticket access depends on the connected agent account's Freshdesk permissions and visibility settings.

Mitigation: Verify ticket IDs before acting, handle 403 and 404 errors as permission or existence checks, and avoid broad access grants unless explicitly approved.

## Reference(s):

- [Freshdesk API Documentation](https://developers.freshdesk.com/api/)
- [Freshdesk Ticket API](https://developers.freshdesk.com/api/#tickets)
- [ClawLink Documentation](https://docs.claw-link.dev/openclaw)
- [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=freshdesk-support)
- [Freshdesk skill on ClawHub](https://clawhub.ai/hith3sh/skills/freshdesk-support)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON tool parameters]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Freshdesk tool names and JSON parameter examples; write operations require user confirmation.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
