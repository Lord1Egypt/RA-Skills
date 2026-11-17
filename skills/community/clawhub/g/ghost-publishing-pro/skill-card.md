## Description:

Guides Ghost publishers through writing, publishing, newsletters, migrations, content audits, and search-indexing workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[highnoonoffice](https://clawhub.ai/user/highnoonoffice)

### License/Terms of Use:

MIT-0

## Use Case:

Publishers and content teams use this skill to manage Ghost posts and newsletters, migrate and audit content, and improve site discoverability through agent-guided workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Publishing or newsletter sends can reach subscribers immediately and cannot be easily undone.

Mitigation: Require explicit approval for each send and confirm the audience and content before publishing.

Risk: Bulk writes, deletes, and automated publishing can change or remove substantial site content.

Mitigation: Confirm the scope and post count, back up affected content, and require approval before bulk changes, deletes, cron jobs, or webhooks.

Risk: Ghost credentials grant broad publishing access; owner-level access and browser code injection raise additional site-wide risk.

Mitigation: Use a dedicated revocable integration key, avoid owner-level tokens, and never run browser code-injection steps autonomously.

Risk: Some workflows involve third-party services despite claims that requests stay within the Ghost site.

Mitigation: Review and approve external service calls and any data shared with them before execution.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/highnoonoffice/skills/ghost-publishing-pro)
- [Project homepage (listed in ClawHub metadata)](https://github.com/highnoonoffice/hno-skills)
- [Ghost API reference](artifact/references/api.md)
- [Ghost publishing workflows](artifact/references/workflows.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration instructions]

**Output Format:** [Markdown with API examples and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide changes to Ghost posts, images, newsletters, and publishing automation.]

## Skill Version(s):

2.6.1 (source: ClawHub release and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
