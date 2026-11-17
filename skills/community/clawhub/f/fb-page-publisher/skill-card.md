## Description:

Publish posts, upload photos, schedule content, read insights, and manage comments on Facebook Pages via the Graph API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jaimin-345](https://clawhub.ai/user/jaimin-345)

### License/Terms of Use:

MIT-0

## Use Case:

External Page managers, marketers, and developers use this skill to let an agent publish, schedule, inspect, and moderate Facebook Page content through configured Page credentials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can perform live public Facebook Page actions, including publishing, replying, scheduling, and deleting content.

Mitigation: Install only for Pages where agent action is acceptable and require human confirmation outside the skill before publish, reply, schedule, or delete actions.

Risk: The skill relies on a powerful long-lived Facebook Page access token.

Mitigation: Use a least-privilege Page token, keep it out of shared config files and version control, and rotate it if exposed.

Risk: Production use may depend on unreviewed dependency versions or package execution paths.

Mitigation: Use a reviewed lockfile and pinned npx/package versions before production use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jaimin-345/skills/fb-page-publisher)
- [Facebook Developers](https://developers.facebook.com)
- [Facebook Graph API Explorer](https://developers.facebook.com/tools/explorer/)
- [Facebook Graph API v21.0](https://graph.facebook.com/v21.0)

## Skill Output:

**Output Type(s):** [text, API calls, guidance]

**Output Format:** [Plain text responses from MCP tools; actions are performed through Facebook Graph API calls.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires FB_PAGE_ID and FB_ACCESS_TOKEN environment variables.]

## Skill Version(s):

1.0.0 (source: server release metadata, SKILL.md frontmatter, pyproject.toml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
