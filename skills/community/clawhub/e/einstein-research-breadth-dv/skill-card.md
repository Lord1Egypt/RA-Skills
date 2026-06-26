## Description: <br>
Quantifies market breadth health using TraderMonty's public CSV data and generates a 0-100 composite score across six components. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[clawdiri-ai](https://clawhub.ai/user/clawdiri-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, analysts, and agents use this skill to assess market breadth, participation, advance-decline health, and whether a rally appears broad-based. The skill produces current-state market context from public CSV data and should not be treated as investment advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill fetches market breadth CSV data from public URLs, and substituted URLs could provide untrusted or misleading data. <br>
Mitigation: Use the default TraderMonty URLs unless another CSV source is explicitly trusted. <br>
Risk: The skill can write generated reports and a history file to local storage. <br>
Mitigation: Choose an output directory where those generated files are expected and acceptable. <br>
Risk: Market breadth output may be mistaken for investment advice. <br>
Mitigation: Present results as informational market context and combine them with other analysis before making financial decisions. <br>


## Reference(s): <br>
- [Market Breadth Analysis Methodology](references/breadth_analysis_methodology.md) <br>
- [TraderMonty market breadth detail CSV](https://tradermonty.github.io/market-breadth-analysis/market_breadth_data.csv) <br>
- [TraderMonty market breadth summary CSV](https://tradermonty.github.io/market-breadth-analysis/market_breadth_summary.csv) <br>
- [ClawHub skill page](https://clawhub.ai/clawdiri-ai/einstein-research-breadth-dv) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/clawdiri-ai) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Natural-language summary with optional Markdown and JSON report files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write generated breadth reports and a local history file when its scripts are run.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
