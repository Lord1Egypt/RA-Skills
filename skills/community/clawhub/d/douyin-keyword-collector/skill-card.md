## Description:

Accesses Douyin with browser automation, enters a keyword, and collects related search suggestions from the autocomplete prompt box.

This skill is ready for commercial/non-commercial use.

## Publisher:

[openlark](https://clawhub.ai/user/openlark)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, marketers, and content teams use this skill to collect Douyin search suggestions for SEO, topic planning, content ideation, trend analysis, and competitive keyword research.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Browser automation may expose account-personalized Douyin page content if the user logs in while collecting suggestions.

Mitigation: Use the skill logged out when possible; if login is required, use a separate low-privilege account.

Risk: Douyin login prompts or anti-crawler controls may block or alter suggestion collection.

Mitigation: Close login prompts when possible, add short waits between actions, and stop automation if Douyin requires manual login or additional verification.

## Reference(s):

- [Douyin homepage](https://www.douyin.com)
- [ClawHub skill page](https://clawhub.ai/openlark/skills/douyin-keyword-collector)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown or plain text keyword list]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Collected suggestions are organized under the entered keyword.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
