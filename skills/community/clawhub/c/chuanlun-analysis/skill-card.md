## Description: <br>
Uses ChanLun Theory to analyze A-share, Hong Kong, and U.S. stocks and generate visual technical-analysis outputs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[silverfoxchina-gif](https://clawhub.ai/user/silverfoxchina-gif) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analysts use this skill to fetch public stock market data, apply ChanLun technical-analysis concepts, and produce reports and charts for research-oriented review. It supports A-share, Hong Kong, and U.S. stocks, excluding markets not covered by the underlying data source. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts public stock-data endpoints during analysis. <br>
Mitigation: Run it only in environments where outbound market-data requests are acceptable. <br>
Risk: Generated ChanLun analysis may be incomplete, subjective, or mistaken if treated as investment advice. <br>
Mitigation: Use the output for research, validate conclusions independently, and combine it with other analysis before making decisions. <br>
Risk: The skill writes Markdown and PNG outputs locally. <br>
Mitigation: Use a dedicated output directory and review generated files before sharing or relying on them. <br>


## Reference(s): <br>
- [ClawHub skill page: chuanlun-analysis](https://clawhub.ai/silverfoxchina-gif/chuanlun-analysis) <br>
- [Original ClawHub skill referenced by artifact](https://clawhub.ai/laigen/chanlun-technical-analysis) <br>
- [Indicator stroke-recognition reference](https://github.com/neuks/Indicator) <br>
- [czsc_in_practise segment-recognition reference](https://github.com/jiapengwei/czsc_in_practise) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Files, Guidance] <br>
**Output Format:** [Markdown report, PNG visualization chart, optional JSON summary, and terminal status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes outputs to a local directory and may contact public stock-data endpoints during analysis.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
