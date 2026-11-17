## Description:

Daily profession-targeted news from X (Twitter), Google News, Grok, and global media, with bilingual briefs, multi-profession subscriptions, keyword filters, and scheduled morning push.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cosmofang](https://clawhub.ai/user/cosmofang)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to register career-news preferences, manage profession subscriptions, and generate profession-targeted news query or morning brief prompts. It supports Chinese and English briefs across multiple professional categories.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores user profile text and can reuse regions or keywords in later prompts and executable command hints.

Mitigation: Avoid untrusted text, shell characters, or multiline instructions in region and keyword fields, and review generated prompts or commands before allowing an agent to run them automatically.

Risk: Scheduled morning pushes can run unattended through cron and repeatedly generate prompts from saved user preferences.

Mitigation: Review output with dry-run or manual execution before enabling scheduled runs, and disable push for users that should no longer receive automated briefs.

## Reference(s):

- [Career News on ClawHub](https://clawhub.ai/cosmofang/skills/career-news)
- [cosmofang Publisher Profile](https://clawhub.ai/user/cosmofang)
- [Skill Definition](artifact/SKILL.md)
- [Package Metadata](artifact/package.json)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and console text with inline shell commands and news-brief prompts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local user preference JSON files under data/users and prompt text for agents to execute news searches.]

## Skill Version(s):

1.1.0 (source: release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
