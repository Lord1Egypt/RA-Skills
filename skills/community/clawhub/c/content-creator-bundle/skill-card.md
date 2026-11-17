## Description:

Content Creator Bundle helps self-media creators adapt articles for multiple platforms, plan scheduled publishing, track content trends, and draft audience interactions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[daimingvip-a11y](https://clawhub.ai/user/daimingvip-a11y)

### License/Terms of Use:

MIT-0

## Use Case:

External content creators and content operations teams use this skill to turn one source article into platform-specific drafts, organize publishing schedules, review trend signals, and prepare comment replies.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can prepare or trigger scheduled posts, bulk publishing, likes, replies, and private-message actions on live social-media accounts.

Mitigation: Use least-privilege platform credentials and require explicit confirmation or dry-run review before any account action is executed.

Risk: Platform account settings and credentials may be handled through configuration files.

Mitigation: Store secrets outside committed configuration files and review configuration before sharing or publishing it.

Risk: Installation steps and dependency versions are not fully verified by the evidence.

Mitigation: Verify installers, dependencies, and versions before running setup commands.

## Reference(s):

- [Content Creator Bundle on ClawHub](https://clawhub.ai/daimingvip-a11y/skills/content-creator-bundle)
- [Content Creator Documentation](https://docs.clawhub.com/content-creator)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance, shell commands]

**Output Format:** [Markdown with inline commands and YAML configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include platform-specific drafts, publishing plans, trend summaries, comment reply drafts, and configuration snippets.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
