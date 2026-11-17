## Description:

Automated WordPress blog publishing with scheduling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wespeakallday](https://clawhub.ai/user/wespeakallday)

### License/Terms of Use:


## Use Case:

Developers and content operators use this skill to convert generated article JSON into WordPress posts, optionally schedule publication, assign taxonomy IDs, and log the result.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: WordPress credentials are required to publish posts.

Mitigation: Use a dedicated low-privilege WordPress application password and avoid exposing credentials through shared command histories or logs.

Risk: The skill can publish or schedule public WordPress posts to a configured destination.

Mitigation: Install and run it only for HTTPS WordPress sites you control and review destination settings before execution.

Risk: Failure handling can write local fallback output based on the article input path.

Mitigation: Keep backups of source article JSON files and review failed-output paths before reuse.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wespeakallday/skills/blog-automation)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration]

**Output Format:** [JSON publishing result, WordPress HTML content, and log text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates or schedules WordPress posts through the WordPress REST API and can save failed publication output as a local HTML file.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
