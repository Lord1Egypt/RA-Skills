## Description: <br>
Analyzes A-share stocks with ChanLun technical-analysis concepts, identifying fractals, strokes, segments, pivots, and MACD divergences while generating charts and reports. <br>

This skill is for research and development only. <br>

## Publisher: <br>
[laigen](https://clawhub.ai/user/laigen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and market-analysis users can run the skill to fetch A-share market data, apply ChanLun technical-analysis rules, and produce research-oriented reports and visualizations. The generated trading signals are for learning and research, not investment advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Tushare API token and contacts market-data services. <br>
Mitigation: Provide the token only for the current session or through a restricted secret store; avoid permanently appending it to shell startup files unless that is acceptable for the environment. <br>
Risk: The skill creates local report, chart, and optional JSON files. <br>
Mitigation: Run it with a dedicated output directory and review generated files before sharing or reusing them. <br>
Risk: ChanLun signals and generated conclusions may be incomplete or misleading for financial decisions. <br>
Mitigation: Treat outputs as research material and combine them with independent analysis before making any investment decision. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/laigen/chanlun-technical-analysis) <br>
- [Tushare Pro registration](https://tushare.pro/register) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Files, JSON, Guidance] <br>
**Output Format:** [Markdown report, PNG chart file, optional JSON, and terminal status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes outputs to ./outputs by default; requires TUSHARE_TOKEN and may contact Tushare or fallback market-data services.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
