## Description:

Publishes and schedules text, image, and link-in-comment posts to a Facebook Page through the Meta Graph API, with multilingual drafting and a required preview before publishing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aaazzzr](https://clawhub.ai/user/aaazzzr)

### License/Terms of Use:


## Use Case:

External page managers and marketing teams use this skill to draft, translate, preview, publish, and schedule content on a Facebook Page through the Meta Graph API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can publish or schedule content on a Facebook Page using long-lived Meta credentials.

Mitigation: Use a dedicated Meta app and Page token with the narrowest permissions possible, keep credential files private, and rotate the token if exposure is suspected.

Risk: A broad posting request could publish unintended content or target the wrong platform.

Mitigation: Require the documented preview and explicit user confirmation, and confirm the target platform before approving any post.

Risk: Credential setup guidance includes shell profile and shared configuration examples that may expose secrets.

Mitigation: Prefer private credential storage, avoid shared config files, and limit access to the token and app secret.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/aaazzzr/skills/fb-page-manager)
- [Facebook Page Access Token Setup](references/token-setup-guide.md)
- [Meta Developers](https://developers.facebook.com)
- [Meta App Dashboard](https://developers.facebook.com/apps/)
- [Graph API Explorer](https://developers.facebook.com/tools/explorer/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown preview text with inline shell commands and JSON status output from the posting script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js plus LONG_META_page_TOKEN, META_PAGE_ID, and META_APP_SECRET environment variables.]

## Skill Version(s):

2.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
