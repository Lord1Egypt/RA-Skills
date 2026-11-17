## Description:

Diagnoses Bright Data Scraping Browser sessions with the Browser Sessions API, including failure causes, bandwidth outliers, captcha activity, redirects, and whether scraper failures are proxy-side or client-side.

This skill is ready for commercial/non-commercial use.

## Publisher:

[meirk-brd](https://clawhub.ai/user/meirk-brd)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and scraping operators use this skill to investigate Bright Data Scraping Browser failures, unexpected empty results, bandwidth use, captcha activity, redirects, and session-level error patterns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can use BRIGHTDATA_API_KEY to enumerate recent Bright Data browser sessions from broad troubleshooting cues.

Mitigation: Invoke it explicitly with a session ID, zone, target domain, or date range, and avoid generic scraper-failure prompts that could trigger broad recent-session review.

Risk: Session diagnostics may surface operational details such as target URLs, bandwidth, captcha status, redirects, and error messages.

Mitigation: Review diagnostic output before sharing it and scope API calls with the documented filters when investigating a specific target or incident.

## Reference(s):

- [Bright Data Browser Sessions API - List sessions](https://docs.brightdata.com/api-reference/browser-api/get-sessions)
- [Bright Data Browser Sessions API - Get session](https://docs.brightdata.com/api-reference/browser-api/get-session)
- [Bright Data API Tokens](https://brightdata.com/cp/setting/users)
- [Bright Data Support](https://help.brightdata.com)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, shell commands, configuration, guidance]

**Output Format:** [Markdown with concise diagnostic summaries, session fields, verdicts, and occasional HTTP or shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Bright Data session IDs, target URLs, status fields, bandwidth conversions, captcha status, and error messages when returned by the Browser Sessions API.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
