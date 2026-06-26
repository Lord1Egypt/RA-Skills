## Description: <br>
Eastmoney Skills helps agents screen stocks from natural-language selection criteria, query stocks or listed companies in specified sectors, and retrieve sector or index constituents through Eastmoney's Miaoxiang stock-screening API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[QQK000](https://clawhub.ai/user/QQK000) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent builders use this skill to turn Chinese natural-language stock-screening requests into Eastmoney API queries and local result files. It supports current stock, company, board, index constituent, and recommendation-style lookup workflows when an MX_APIKEY credential is available. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Stock-screening keywords are sent to Eastmoney's API. <br>
Mitigation: Avoid including unrelated sensitive information in screening queries and use the skill only when sending those keywords to Eastmoney is acceptable. <br>
Risk: Generated CSV, text description, and raw JSON files may contain sensitive query context or result sets. <br>
Mitigation: Review the output directory after use and remove generated files when the query or results should not persist locally. <br>
Risk: The skill requires an Eastmoney API key. <br>
Mitigation: Store the key only in the MX_APIKEY environment variable and avoid embedding it in prompts, command history, source files, or shared output. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/QQK000/eastmoney-select-stock) <br>
- [Eastmoney Miaoxiang Skills page](https://marketing.dfcfs.com/views/finskillshub/indexuNdYscEA) <br>


## Skill Output: <br>
**Output Type(s):** [text, CSV files, JSON files, shell commands, configuration guidance] <br>
**Output Format:** [Terminal text plus local CSV, text description, and raw JSON files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MX_APIKEY; sends stock-screening keywords to Eastmoney and writes results under /root/.openclaw/workspace/mx_data/output/ by default.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
