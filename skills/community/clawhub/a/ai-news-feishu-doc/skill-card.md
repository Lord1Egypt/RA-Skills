## Description:

Generates an AI industry morning briefing as a Markdown document from configured RSS feeds.

This skill is ready for commercial/non-commercial use.

## Publisher:

[swordman20](https://clawhub.ai/user/swordman20)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to collect AI news from configured Chinese and English RSS feeds, prioritize keyword matches, and produce a daily Markdown briefing that can be scheduled through OpenClaw cron.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill contacts configured RSS providers and creates local Markdown files.

Mitigation: Review the RSS configuration before use and run the skill only where those outbound requests and file writes are expected.

Risk: Generated briefings contain untrusted internet content and may include remote image embeds.

Mitigation: Review generated Markdown before sharing it and disable or review remote images in Markdown viewers.

Risk: The documented cron setup can run the generator unattended every day.

Mitigation: Add the cron schedule only when unattended daily runs are intended, and monitor the generated output location.

Risk: The script depends on PyYAML.

Mitigation: Install PyYAML in an isolated environment with a pinned version.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/swordman20/skills/ai-news-feishu-doc)
- [RSS feed configuration](artifact/assets/ai-news-rss.yaml)

## Skill Output:

**Output Type(s):** [markdown, shell commands, configuration]

**Output Format:** [Markdown file with headings, article summaries, source links, and optional remote image embeds]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes AI早报_<date>.md under the skill's scripts directory; article count and sources are controlled by assets/ai-news-rss.yaml.]

## Skill Version(s):

0.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
