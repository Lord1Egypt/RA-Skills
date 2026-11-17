## Description:

Complete genviral Partner API automation. Create and schedule posts (video + slideshow) across TikTok, Instagram, and any supported platform. Includes slideshow generation, file uploads, template/pack management, analytics, and full content pipeline automation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ugenesys](https://clawhub.ai/user/ugenesys)

### License/Terms of Use:


## Use Case:

External creators, marketers, and agent operators use this skill to automate Genviral Partner API workflows for generating media, scheduling social posts, tracking analytics, and improving content strategy from performance data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The self-updater and daily update cron can replace skill instructions and scripts from a mutable branch without integrity verification.

Mitigation: Keep automatic updates disabled; update manually from pinned releases and review diffs before applying changes.

Risk: The skill uses a Genviral API key and connected social accounts to create, schedule, update, retry, and delete posts.

Mitigation: Use the least-privileged API and account access available, and review target accounts, captions, media, and destructive operations before execution.

Risk: Automated posting workflows can publish or schedule content repeatedly if cron jobs are enabled.

Mitigation: Prefer draft or scheduled review workflows, keep the visual review gate before posting, and monitor workspace logs and analytics after publication.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/ugenesys/skills/genviral-skill)
- [Genviral website](https://genviral.io)
- [Setup guide](docs/setup.md)
- [Content pipeline documentation](docs/api/pipeline.md)
- [Analytics loop reference](docs/references/analytics-loop.md)
- [Competitor research reference](docs/references/competitor-research.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON or YAML configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Genviral API key and can produce API-driven social posting actions, media workflow commands, and workspace tracking updates.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
