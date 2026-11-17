## Description:

Manages Facebook Page publishing workflows through the Facebook Graph API, including text, photo, carousel, video, Reels, Stories, scheduled posts, and selected post-management actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mcbaivn](https://clawhub.ai/user/mcbaivn)

### License/Terms of Use:

MIT-0

## Use Case:

External social media operators and developers use this skill to prepare commands and configuration for publishing and managing Facebook Page content through the Graph API. It is suited for agent-assisted workflows that need posts, media uploads, scheduled publishing, and selected Page engagement actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Facebook Page tokens can grant broad posting and engagement capabilities.

Mitigation: Use the least-privileged Page token that supports the intended action, store it outside plaintext config when possible, and rotate or revoke it regularly.

Risk: Delete and reschedule operations can alter public Page content.

Mitigation: Manually confirm post IDs and scheduled times before executing delete or reschedule commands.

Risk: Advertised comment-management commands may not be reliable in this version.

Mitigation: Do not depend on comment-management behavior unless the implementation is updated and tested for those commands.

## Reference(s):

- [Facebook Page Manager API Reference](references/api-reference.md)
- [Facebook Page Access Token Guide](references/get-token.md)
- [Meta for Developers](https://developers.facebook.com/)
- [Graph API Explorer](https://developers.facebook.com/tools/explorer/)
- [Facebook Graph API Changelog](https://developers.facebook.com/docs/graph-api/changelog)
- [ClawHub Skill Page](https://clawhub.ai/mcbaivn/skills/facebook-management-skills-by-mcbai)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands, JSON configuration examples, and Python command usage]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands require a Facebook Page ID, a Page access token, and any media files referenced by the requested operation.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
