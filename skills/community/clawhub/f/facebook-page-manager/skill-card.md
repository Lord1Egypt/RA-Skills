## Description:

Manage Facebook Pages through the Meta Graph API by listing pages and posts, publishing text, photo, or link content, and managing comments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[longmaba](https://clawhub.ai/user/longmaba)

### License/Terms of Use:


## Use Case:

External page managers, social media operators, and developers use this skill to configure OAuth, obtain Page tokens, publish Facebook Page content, inspect posts, and manage comments through the Meta Graph API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The Facebook Page CLI uses real Page authority and stores durable tokens locally.

Mitigation: Protect .env and tokens.json, restrict filesystem access to those files, and run the skill only in environments intended for Page administration.

Risk: Commands can publish posts, upload photos, hide comments, or delete posts and comments.

Mitigation: Require human review of page IDs, post IDs, comment IDs, and message content before running publish, hide, or delete actions.

Risk: Bundled X-to-Facebook automation uses X session cookies and can automatically publish generated promotional digest content.

Mitigation: Do not run x_digest_collect.js or x_digest_to_fb.js unless the X digest workflow is explicitly intended; consider removing or isolating those scripts for normal Facebook Page management.

## Reference(s):

- [Graph API Reference](references/graph-api.md)
- [Meta Developers Apps](https://developers.facebook.com/apps/)
- [ClawHub skill page](https://clawhub.ai/longmaba/skills/facebook-page-manager)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands; bundled CLI scripts produce terminal text or JSON status output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Meta App credentials and Facebook Page authority; scripts can publish posts, upload photos, list posts and comments, reply to comments, hide comments, and delete posts or comments.]

## Skill Version(s):

1.0.0 (source: release metadata and scripts/package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
