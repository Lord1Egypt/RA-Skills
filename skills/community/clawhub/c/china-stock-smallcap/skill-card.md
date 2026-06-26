## Description: <br>
Selects approximate China A-share small-cap stock candidates using public Eastmoney market data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[luyao-inc](https://clawhub.ai/user/luyao-inc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, financial research agents, and analysts use this skill to retrieve informational China A-share small-cap screening results from public market data. The output supports research workflows and is not investment advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill makes outbound requests to Eastmoney and depends on public market-data availability. <br>
Mitigation: Run it only where outbound access to Eastmoney is allowed, and handle API failures or unavailable data as expected runtime conditions. <br>
Risk: Financial screening output could be mistaken for investment advice. <br>
Mitigation: Treat results as informational research output and independently verify data, assumptions, and suitability before acting on them. <br>
Risk: The documented script path may need correction at runtime. <br>
Mitigation: Confirm the installed script path before invocation and adjust the command path if the runtime layout differs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/luyao-inc/china-stock-smallcap) <br>
- [Eastmoney public quote API](https://push2.eastmoney.com/api/qt/clist/get) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands] <br>
**Output Format:** [JSON] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes strategy type, status, message, and ranked stock records.] <br>

## Skill Version(s): <br>
2.0.0 (source: release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
