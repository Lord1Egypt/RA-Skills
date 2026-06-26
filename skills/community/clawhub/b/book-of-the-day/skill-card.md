## Description: <br>
Book Of The Day fetches a fresh daily book recommendation and returns an uplifting, poetic reading in the user's language. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Romanluoman00007](https://clawhub.ai/user/Romanluoman00007) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users ask for a daily book-themed reading or recommendation. Operators can optionally configure the skill for scheduled Telegram or Slack posts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts the configured book API when invoked. <br>
Mitigation: Install only if external API access is acceptable, and configure BOOK_OF_THE_DAY_API_URL to a trusted endpoint when overriding the default. <br>
Risk: Optional cron setup can automatically post daily output to Telegram or Slack. <br>
Mitigation: Enable the cron command only when scheduled posting is intended, and verify the channel, timezone, and message before use. <br>
Risk: A separate one-click private-API installer may modify local configuration. <br>
Mitigation: Inspect any private-API installer command before executing it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Romanluoman00007/book-of-the-day) <br>
- [Default Book Of The Day API](https://book-of-the-day.vercel.app) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown text with a book title, author, archetype, short reading, and closing call to action] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Under 200 words for the generated reading, excluding book description] <br>

## Skill Version(s): <br>
1.0.7 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
