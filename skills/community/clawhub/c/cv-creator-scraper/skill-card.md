## Description:

Helps agents find and compare creators, analyze videos and account authenticity, export search results, and manage creator outreach through CreatiVault.

This skill is ready for commercial/non-commercial use.

## Publisher:

[creativault](https://clawhub.ai/user/creativault)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing teams and creator researchers use the skill to discover creators across TikTok, Instagram, and YouTube, review creator and video signals, export search results, and coordinate outreach. It can also summarize short-video content and estimate account authenticity risks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review reports exposed credentials and unsafe data handling; some components were only partially inspected.

Mitigation: Follow the review guidance to remove or rotate the shared credential before installation and review any credential handling.

Risk: The security review reports an update process that can replace skill files without independent release verification.

Mitigation: Independently verify and pin the updater and installer before installation.

Risk: Collection and outreach actions can affect external services or people.

Mitigation: Require clear user intent and confirmation before collection or outreach actions.

## Reference(s):

- [CreatiVault API Reference](artifact/references/api-reference.md)
- [Platform Parameters](artifact/references/platform-params.md)
- [Creativault Creator Scraper on ClawHub](https://clawhub.ai/creativault/skills/cv-creator-scraper)

## Skill Output:

**Output Type(s):** [Text, Markdown, CSV files, Analysis, Guidance]

**Output Format:** [Markdown summaries and tables, CSV exports, and structured audit results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results reflect data returned by CreatiVault; creator and video coverage depends on its indexed data.]

## Skill Version(s):

1.8.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
