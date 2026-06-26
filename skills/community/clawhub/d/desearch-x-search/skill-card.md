## Description: <br>
Search X (Twitter) in real time by keyword, user, or hashtag; retrieve user timelines, replies, retweeters, and specific posts by ID or URL with filters for dates, language, engagement, verification, and media type. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[okradze](https://clawhub.ai/user/okradze) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users, developers, and analysts use this skill to search and inspect X/Twitter posts and user activity through Desearch-backed CLI commands. It supports monitoring topics, fetching post details, reviewing user timelines, and gathering reply or retweeter data when a Desearch API key is configured. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries, post identifiers, URLs, usernames, and related investigative context are sent to Desearch during normal use. <br>
Mitigation: Use the skill only when Desearch is trusted for the intended data, and avoid submitting secrets, regulated investigative terms, or sensitive identifiers as queries. <br>
Risk: The skill requires a Desearch API key for authenticated requests. <br>
Mitigation: Use a dedicated, revocable API key stored in the DESEARCH_API_KEY environment variable, rotate it when needed, and avoid embedding it in prompts, files, or command history. <br>
Risk: Desearch privacy and retention terms determine how submitted searches and identifiers may be handled. <br>
Mitigation: Review Desearch's privacy and retention terms before using the skill for sensitive or regulated workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/okradze/desearch-x-search) <br>
- [Desearch homepage](https://desearch.ai) <br>
- [Desearch API reference](https://desearch.ai/docs/api-reference) <br>
- [Desearch Console](https://console.desearch.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text summaries, JSON API responses, and Markdown documentation with bash examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires DESEARCH_API_KEY; sends X/Twitter search terms, post identifiers, URLs, and usernames to Desearch as part of normal operation.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
