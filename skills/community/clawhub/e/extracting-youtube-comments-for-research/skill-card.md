## Description:

Extracts and analyzes YouTube comments for audience research using apidojo's YouTube scraper on Apify.

This skill is ready for commercial/non-commercial use.

## Publisher:

[apidojo-io](https://clawhub.ai/user/apidojo-io)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators, brand researchers, product teams, and audience insight analysts use this skill to collect YouTube comments and turn them into sentiment, question, theme, and feedback reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on a mutable third-party Apify actor for YouTube comment collection.

Mitigation: Verify the exact Apify actor before use, review its current behavior, and set explicit collection limits for each run.

Risk: The documented REST fallback places the Apify token in the request URL.

Mitigation: Prefer environment-based token handling or an approved client, use a dedicated limited Apify token, and avoid logging URLs that contain credentials.

Risk: YouTube targets and scraping parameters are sent to Apify/apidojo.

Mitigation: Use the skill only for targets appropriate for third-party processing and avoid sending sensitive research targets without approval.

Risk: Comment datasets can be noisy, spam-heavy, non-English, or coordinated.

Mitigation: Apply the documented cleaning filters, report language distribution and brigading signals, and present findings as audience research signals rather than definitive measurements.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/apidojo-io/skills/extracting-youtube-comments-for-research)
- [Apify actor: apidojo/youtube-scraper](https://apify.com/apidojo/youtube-scraper)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown report with tables and optional CSV or JSON data files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Apify actor inputs and YouTube comment fields such as text, likes, replies, username, and timestamp.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
