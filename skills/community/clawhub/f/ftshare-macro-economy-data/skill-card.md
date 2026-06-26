## Description: <br>
Routes an agent to bundled Python scripts that fetch public China and United States macroeconomic indicators from market.ft.tech. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Shawn92](https://clawhub.ai/user/Shawn92) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to answer China and United States macroeconomic data questions by selecting the matching indicator fetcher and presenting the returned public data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs bundled Python scripts and sends selected macroeconomic indicator queries to market.ft.tech. <br>
Mitigation: Install only where outbound requests to market.ft.tech are acceptable. <br>
Risk: Generic macroeconomic terms such as CPI, tax revenue, investment, industrial growth, or retail sales can be routed too broadly. <br>
Mitigation: Use prompts that specify the country and exact dataset before running the skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Shawn92/ftshare-macro-economy-data) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/Shawn92) <br>
- [market.ft.tech API base](https://market.ft.tech) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Markdown, Text] <br>
**Output Format:** [JSON from scripts, typically summarized by the agent as Markdown tables or concise text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Results are fetched over HTTP GET from market.ft.tech and may contain null numeric fields depending on the source data.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
