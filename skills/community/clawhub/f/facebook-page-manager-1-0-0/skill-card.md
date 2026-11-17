## Description:

Manage Facebook Pages via Meta Graph API by publishing text, photo, or link posts; listing Page posts; and listing, replying to, hiding, or deleting comments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[loui1979](https://clawhub.ai/user/loui1979)

### License/Terms of Use:


## Use Case:

External users, developers, and page operators use this skill to configure Meta OAuth, select managed Facebook Pages, publish Page content, and manage Page comments from an agent-assisted CLI workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan reports undisclosed X/Twitter-to-Facebook automation that can publish promotional content.

Mitigation: Remove or disable the X/Twitter digest scripts before use unless that automation is explicitly intended and reviewed.

Risk: The skill can post publicly, hide or delete comments, and reply on managed Facebook Pages.

Mitigation: Use test Pages first and review the exact Page, post, comment, and final public content before running write, hide, reply, or delete commands.

Risk: The skill handles Meta Page tokens and X/Twitter credentials.

Mitigation: Store credentials in a protected secret store or isolated environment, avoid broad environment variables, and verify any external executable used for X/Twitter collection.

## Reference(s):

- [Graph API Reference](references/graph-api.md)
- [Meta App Dashboard](https://developers.facebook.com/apps/)
- [Facebook Graph API v21.0](https://graph.facebook.com/v21.0)
- [ClawHub Skill Page](https://clawhub.ai/loui1979/skills/facebook-page-manager-1-0-0)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, JavaScript CLI scripts, environment configuration, and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Meta app credentials, OAuth tokens, and explicit review before public posting or comment moderation actions.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
