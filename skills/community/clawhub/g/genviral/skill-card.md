## Description:

Complete genviral Partner API automation for creating and scheduling video or slideshow posts across TikTok, Instagram, and other supported platforms, with slideshow generation, file uploads, template and pack management, analytics, and content pipeline automation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ugenesys](https://clawhub.ai/user/ugenesys)

### License/Terms of Use:

MIT

## Use Case:

Developers, creators, and marketing teams use this skill to operate a Genviral content workflow from account setup through slideshow or video generation, scheduling, posting, analytics review, and performance tracking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can self-update skill-owned instructions, scripts, and documentation from an unsigned remote branch.

Mitigation: Disable scheduled self-updates or run the updater in dry-run mode and review changes before applying them.

Risk: The content pipeline can create, schedule, or publish posts to connected social accounts.

Mitigation: Require explicit human approval and visual review before posting, and use draft modes where available for final platform-specific checks.

Risk: The Genviral API key enables automation against connected accounts and uploaded media.

Mitigation: Store the key in a controlled environment, avoid shared global environment files, and use only accounts that are approved for automated workflows.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ugenesys/skills/genviral)
- [Genviral](https://genviral.io)
- [Genviral Partner API Documentation](https://docs.genviral.io)
- [Setup Guide](docs/setup.md)
- [Post Commands](docs/api/posts.md)
- [Content Pipeline](docs/api/pipeline.md)
- [Analytics Loop](docs/references/analytics-loop.md)
- [Competitor Research](docs/references/competitor-research.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, API calls]

**Output Format:** [Markdown guidance with inline shell commands, configuration snippets, and JSON-oriented API responses.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires bash, curl, jq, a Genviral Partner API key, and connected social accounts; may update workspace files and create or schedule posts through Genviral.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
