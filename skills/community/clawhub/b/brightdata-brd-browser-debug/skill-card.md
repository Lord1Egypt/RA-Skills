## Description: <br>
Diagnose Bright Data Scraping Browser sessions using the Browser Sessions API, including error diagnosis, bandwidth analysis, captcha reporting, and recent-session pattern detection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[meirk-brd](https://clawhub.ai/user/meirk-brd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and scraper operators use this skill to inspect Bright Data Scraping Browser session diagnostics, explain failures, identify bandwidth or captcha patterns, and separate proxy-side issues from client-side scraper problems. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Bright Data API token. <br>
Mitigation: Use a least-privileged token, provide it through BRIGHTDATA_API_KEY, and avoid pasting the token into chat or generated reports. <br>
Risk: Broad trigger wording can cause the agent to list recent browser sessions when the user's intended scope is narrower. <br>
Mitigation: Provide a specific session ID, target domain, zone, status, or date range before requesting diagnostics. <br>
Risk: Browser-session diagnostics may expose target URLs, error messages, bandwidth usage, captcha status, and other operational metadata. <br>
Mitigation: Review diagnostic output before sharing it, and avoid running the skill against sensitive scraping activity unless that metadata is acceptable to disclose. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/meirk-brd/brightdata-brd-browser-debug) <br>
- [Publisher profile](https://clawhub.ai/user/meirk-brd) <br>
- [Bright Data API tokens](https://brightdata.com/cp/setting/users) <br>
- [GET /browser_sessions](https://docs.brightdata.com/api-reference/browser-api/get-sessions) <br>
- [GET /browser_sessions/{session_id}](https://docs.brightdata.com/api-reference/browser-api/get-session) <br>
- [Bright Data support](https://help.brightdata.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown troubleshooting report with API request guidance and session diagnostics] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires BRIGHTDATA_API_KEY; may inspect live Bright Data session metadata and should use explicit session IDs or narrow filters when available.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
