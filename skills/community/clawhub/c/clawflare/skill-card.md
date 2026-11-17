## Description:

Publish web content to Cloudflare Pages. Supports account/project selection, new project creation, and deploying HTML or static asset directories. Primary auth via Cloudflare API Token.

This skill is ready for commercial/non-commercial use.

## Publisher:

[drodecker](https://clawhub.ai/user/drodecker)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to publish generated HTML, landing pages, documentation, or static asset directories to Cloudflare Pages, including account/project selection, deployment, and reporting live URLs and status.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can publish or update Cloudflare Pages sites when given a valid Cloudflare token.

Mitigation: Use a narrowly scoped Pages token, verify the target account, project, and branch before deployment, and require explicit confirmation for production sites.

Risk: Publishing to the wrong project or branch could update an unintended live site.

Mitigation: Clarify account, project, branch, and custom subdomain details before publishing, and surface the live URL and deployment status after deployment.

## Reference(s):

- [Server-resolved GitHub source](https://github.com/drodecker/clawflare.publish/tree/main/skill)
- [ClawHub skill page](https://clawhub.ai/drodecker/skills/clawflare)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with structured deployment results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include live deployment URL, deployment ID, success status, target account/project/branch, and concise error guidance.]

## Skill Version(s):

0.1.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
