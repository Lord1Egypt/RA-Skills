## Description:

A-share quantitative research assistant for K-line data, technical indicators, shareholder counts, and official announcement parsing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vcvycy](https://clawhub.ai/user/vcvycy)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to query Chinese A-share stock data, inspect shareholder-count history, search official announcements, and read downloaded announcement PDF content through the documented API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Stock queries are sent to a documented third-party HTTP service.

Mitigation: Use the skill only when sending these queries to the service is acceptable for the user and environment.

Risk: Financial data returned by the service may be incomplete or unsuitable as the sole basis for decisions.

Mitigation: Cross-check important financial decisions against authoritative sources.

Risk: Announcement PDFs may be downloaded and retained under the documented STOCK_HOME path.

Mitigation: Review local retention and cleanup practices for downloaded announcement PDFs.

## Reference(s):

- [DeepStock ClawHub listing](https://clawhub.ai/vcvycy/skills/deepstock)
- [DeepStock API host](http://60.205.179.76:8000)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, shell commands, guidance]

**Output Format:** [Markdown with HTTP endpoint examples and JSON response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference local announcement PDF paths returned by the API.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
