## Description:

Digest Comunidad F100K analyzes recent Instagram or TikTok comments, identifies recurring questions and pain points, and turns the top five themes into script-ready content ideas saved to the user's idea bank and delivered through Telegram.

This skill is ready for commercial/non-commercial use.

## Publisher:

[formula100k](https://clawhub.ai/user/formula100k)

### License/Terms of Use:

MIT-0

## Use Case:

External creators and social media operators use this skill to convert recent community comments into content ideas grounded in cited audience feedback. It supports a weekly workflow that gathers comments from connected Instagram, public Apify sources, or user-provided screenshots, then prepares a private digest and updates the F100K idea bank.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may process connected social account data and private community comments.

Mitigation: Ask the user before using connected accounts or scraping tools, and proceed only with an explicit, scoped source for the digest.

Risk: Delivery instructions conflict between email, Telegram, saved reports, and idea-bank updates.

Mitigation: Use one confirmed delivery path for each run and show the planned file changes before saving handles, reports, or content ideas.

Risk: Third-party usernames and comment identifiers could be exposed beyond the private report.

Mitigation: Keep @usernames only where strictly necessary in a private local report and omit them from public scripts or content ideas.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/formula100k/skills/digest-comunidad-f100k)
- [formula100k publisher profile](https://clawhub.ai/user/formula100k)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown report, Telegram-ready message text, and appended Markdown content ideas]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires ig_handle or tiktok_handle; outputs should cite real comments and avoid public use of third-party usernames.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
