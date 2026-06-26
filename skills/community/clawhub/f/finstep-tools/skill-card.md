## Description: <br>
FinStep Tools provides A-share financial data access for real-time quotes, sector data, company information, macroeconomic indicators, research reports, news, and announcements. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zacbai](https://clawhub.ai/user/zacbai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and financial-data users can use this skill to query FinStep for market quotes, sector rankings, company fundamentals, macroeconomic indicators, financial news, reports, announcements, and trading calendars. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: FINSTEP_SIGNATURE and financial queries are sent to the FinStep service, and the security evidence reports that the required API signature is sent in URL parameters over plain HTTP. <br>
Mitigation: Install only if the publisher and service are trusted, treat FINSTEP_SIGNATURE as a secret, avoid confidential queries, and prefer a version that uses HTTPS with credentials sent through an Authorization header or managed secret store. <br>
Risk: The security verdict is suspicious because credential handling is unsafe, even though the skill appears to provide legitimate financial-data functionality. <br>
Mitigation: Use a review-before-execution posture, inspect generated shell commands before running them, and rotate the FinStep signature if exposure is suspected. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/zacbai/finstep-tools) <br>
- [FinStep API base URL](http://fintool-mcp.finstep.cn) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, JSON, guidance] <br>
**Output Format:** [Markdown command guidance and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires FINSTEP_SIGNATURE; some API endpoints may be rate limited or return endpoint-specific errors.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and user changelog) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
