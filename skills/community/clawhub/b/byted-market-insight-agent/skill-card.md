## Description: <br>
Byted Market Insight Agent helps agents retrieve Volcengine market-insight tasks, AI-filtered public content, and business lead data for brand monitoring, competitor tracking, trend analysis, and opportunity research. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[volcengine-skills](https://clawhub.ai/user/volcengine-skills) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, and developers use this skill to access Volcengine market-insight data for brand sentiment monitoring, competitive intelligence, topic trend analysis, monitored-task retrieval, and AI-generated sales lead review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can look for Volcengine and Gateway credentials in shell startup files and local persisted auth state. <br>
Mitigation: Install only from a trusted publisher, use least-privileged credentials, and protect or remove persist/auth.json when access is no longer needed. <br>
Risk: The skill can make external API calls to market-insight providers using configured credentials. <br>
Mitigation: Review requested tasks and date ranges before execution, and monitor API usage under the connected account. <br>
Risk: The skill may attempt to install the Volcengine SDK during use. <br>
Mitigation: Disable automatic package installation with MARKET_INSIGHT_AUTO_PIP=0 when dependency changes should be controlled manually. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/volcengine-skills/byted-market-insight-agent) <br>
- [Usage and integration guide](references/usage.md) <br>
- [API differences](references/api-diff.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [JSON-compatible API responses with concise setup and credential guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can return paginated market insight tasks, filtered public content, parsed lead details, and credential prompts when required.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
