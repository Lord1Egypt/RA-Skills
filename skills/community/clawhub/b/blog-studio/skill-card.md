## Description:

Standalone CMS for GitHub Pages Jekyll blogs - browse, edit, create posts, and deploy with one click.

This skill is ready for commercial/non-commercial use.

## Publisher:

[amrree](https://clawhub.ai/user/amrree)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content maintainers use BlogStudio to manage GitHub Pages Jekyll blog content through a local CMS UI. It supports browsing, editing, creating, previewing, syncing, and publishing posts, guides, pages, and related content to a configured GitHub repository.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles GitHub credentials and publishing authority, which could expose or misuse a user's token.

Mitigation: Run only with a narrowly scoped, revocable GitHub token for the intended repository and review token handling before installation.

Risk: The artifact can write, publish, and delete repository content through GitHub API operations.

Mitigation: Use repository permissions, branch protection, backups, and human review before publish or delete actions.

Risk: Previewing repository content before token handling, renderer sanitization, IPC validation, and destructive-action controls are fixed may increase exposure.

Mitigation: Avoid previewing untrusted repository content until those controls are reviewed and corrected.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/amrree/skills/blog-studio)
- [Publisher Profile](https://clawhub.ai/user/amrree)
- [Managed GitHub Pages Site](https://thesolai.github.io)
- [GitHub Repository API Endpoint](https://api.github.com/repos/TheSolAI/thesolai.github.io)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Configuration]

**Output Format:** [Markdown with inline shell commands, file paths, and configuration details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may guide local server startup, GitHub authentication, content editing, previewing, and publishing workflows.]

## Skill Version(s):

1.0.0 (source: frontmatter, release evidence, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
