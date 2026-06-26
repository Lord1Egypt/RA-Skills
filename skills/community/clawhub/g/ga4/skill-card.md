## Description: <br>
Query Google Analytics 4 (GA4) data via the Analytics Data API for website analytics such as top pages, traffic sources, users, sessions, conversions, metrics, dimensions, custom date ranges, and filters. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jdrhyne](https://clawhub.ai/user/jdrhyne) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, analysts, and site operators use this skill to query GA4 properties for traffic, page, source, user, session, conversion, and event metrics without modifying the analytics property. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses sensitive Google OAuth credentials and a refresh token. <br>
Mitigation: Keep credentials out of shared terminals and logs, use a dedicated OAuth client where possible, and verify the consent screen grants Analytics read-only access. <br>
Risk: The skill can read analytics data from the configured GA4 property. <br>
Mitigation: Install and run it only for properties where read-only access is appropriate, and review outputs before sharing analytics data. <br>
Risk: Python dependencies are installed from external package sources. <br>
Mitigation: Install google-analytics-data and google-auth-oauthlib from trusted sources in a controlled environment. <br>


## Reference(s): <br>
- [GA4 Analytics ClawHub Page](https://clawhub.ai/jdrhyne/ga4) <br>
- [Google Analytics Developer Documentation](https://developers.google.com/analytics) <br>
- [Google Analytics Data API](https://console.cloud.google.com/apis/library/analyticsdata.googleapis.com) <br>
- [Google Analytics Read-Only OAuth Scope](https://www.googleapis.com/auth/analytics.readonly) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples; query script output can be table text, JSON, or CSV.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python, GA4_PROPERTY_ID, GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, and GOOGLE_REFRESH_TOKEN.] <br>

## Skill Version(s): <br>
1.2.2 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
