## Description: <br>
DeepStock helps agents query China A-share stock basics, K-line market data, technical indicators, shareholder counts, and official announcement content through a documented HTTP API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vcvycy](https://clawhub.ai/user/vcvycy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, analysts, and agent developers use this skill to look up China A-share company information, daily market data, shareholder-count history, and official announcement text for investment research workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill calls an unauthenticated HTTP API for stock research data. <br>
Mitigation: Verify important investment information against official sources before relying on it. <br>
Risk: Announcement search endpoints may download and store PDF files locally. <br>
Mitigation: Treat downloaded PDFs as untrusted files and clean up the announcement download directory when retention or disk usage matters. <br>


## Reference(s): <br>
- [DeepStock API host](http://60.205.179.76:8000) <br>
- [DeepStock ClawHub release page](https://clawhub.ai/vcvycy/deepstock) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, API Calls, Text, JSON] <br>
**Output Format:** [Markdown instructions with HTTP GET examples and JSON response shapes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Announcement search endpoints may create stored PDF files in the configured announcement download directory.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
