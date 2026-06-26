## Description: <br>
Generates a structured A-share bull-versus-bear debate report from market, technical, fund-flow, and financial data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jioup777](https://clawhub.ai/user/jioup777) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Investors, traders, and analysts use this skill to request a stock-code-specific A-share debate analysis and receive a structured investment brief. The report is intended for reference and includes a disclaimer that it is not investment advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks the agent to start an unverified mihomo proxy binary and configuration from /tmp. <br>
Mitigation: Use only after verifying the binary, configuration, and subscription source; avoid running it on shared servers unless proxy handling is hardened. <br>
Risk: The proxy shutdown step uses broad process-name matching, which could stop unrelated mihomo processes. <br>
Mitigation: Track the exact process ID for the proxy started by the skill and inspect the running process before stopping it. <br>
Risk: Stock prompts and collected market data are sent to BigModel GLM. <br>
Mitigation: Confirm this data sharing is acceptable for the user and organization before setting GLM_API_KEY or running the analysis. <br>
Risk: Generated trading recommendations may be incomplete, stale, or misleading. <br>
Mitigation: Verify the underlying market data and treat the generated report as informational analysis, not investment advice. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jioup777/a-stock-debate) <br>
- [BigModel GLM API endpoint](https://open.bigmodel.cn/api/paas/v4) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance] <br>
**Output Format:** [Markdown report with tables, debate summaries, risk notes, and executable data-collection snippets.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires GLM_API_KEY for BigModel calls and expects a local mihomo proxy binary and configuration under /tmp for proxied Eastmoney data.] <br>

## Skill Version(s): <br>
2.1.0 (source: server release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
