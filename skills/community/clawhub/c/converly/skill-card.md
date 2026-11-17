## Description:

Set up server side conversion tracking for ad platforms (Google Ads, Meta, ChatGPT, LinkedIn, TikTok and more) without writing tracking code.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aaronbeashel](https://clawhub.ai/user/aaronbeashel)

### License/Terms of Use:

MIT No Attribution (MIT-0)

## Use Case:

Developers, marketers, and site operators use this skill to configure Converly conversion tracking, connect ad platforms, publish conversion flows, install tracking snippets, and verify delivery and capture.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can install live tracking and publish ad-platform flows that affect production conversion reporting.

Mitigation: Use staging where possible, confirm the site domain and target pages or forms, validate flows before publishing, and verify results with install status plus real conversion events.

Risk: Broad form monitoring or an incorrect conversion choice can pollute attribution data.

Mitigation: Ask the user to choose the conversion, fetch platform conversion options, and narrow tracking by page or connected-platform form options when needed.

Risk: Enhanced Conversions or server-side delivery may share hashed customer identifiers with ad platforms.

Mitigation: Get explicit approval before enabling Enhanced Conversions or any sharing of hashed customer identifiers, and confirm the relevant ad-platform terms are accepted.

Risk: Credentials or API keys could be exposed if handled through chat or command output.

Mitigation: Use browser login or the documented environment variable path, never ask users to paste tokens, and avoid printing credential values.

## Reference(s):

- [Converly Developer Documentation](https://developers.converly.io)
- [Converly Website](https://converly.io)
- [@converly/cli package](https://www.npmjs.com/package/@converly/cli)
- [Converly MCP Server](https://app.converly.io/mcp)
- [Destination specifics](references/destinations.md)
- [REST API fallback](references/rest-api.md)
- [Trigger specifics](references/triggers.md)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Code, Guidance]

**Output Format:** [Markdown guidance with inline shell commands, JSON snippets, and optional code changes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require human browser handoffs for login, ad-platform authorization, and approval before real conversion tests or destructive actions.]

## Skill Version(s):

1.1.0 (source: frontmatter and ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
