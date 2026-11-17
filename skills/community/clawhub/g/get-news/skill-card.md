## Description:

Fetches BlockBeats crypto flash news, filters items by keyword, and returns cleaned, timestamp-normalized JSON for downstream agent workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leesen86](https://clawhub.ai/user/leesen86)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to collect recent crypto news from BlockBeats, filter by one or more keywords, and pass structured JSON into follow-on automation such as summarization, translation, or notification workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The package includes under-disclosed scripts that can send Feishu messages through a local OpenClaw gateway using a credential embedded in source.

Mitigation: Run the documented news-fetching script only unless Feishu delivery is intentional; before using messaging scripts, rotate or replace the exposed token and confirm the target recipient and gateway permissions.

Risk: Additional package behavior and dependency hygiene need review, including a shell execution issue and an unused ws dependency identified by the security guidance.

Mitigation: Review push-news.js and send-feishu.js before execution, fix the shell execution issue, and remove or update the unused dependency before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/leesen86/skills/get-news)
- [ClawHub publisher profile](https://clawhub.ai/user/leesen86)
- [BlockBeats open flash API](https://api.theblockbeats.news/v1/open-api/open-flash)

## Skill Output:

**Output Type(s):** [json, shell commands, text]

**Output Format:** [JSON array written to stdout, with optional shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Items may include cleaned text fields, formatted timestamp fields, original timestamp values with _raw suffixes, titles, IDs, and links.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
