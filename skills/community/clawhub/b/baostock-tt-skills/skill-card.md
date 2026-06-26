## Description: <br>
Retrieves A-share historical K-line data, quarterly financial data, macroeconomic data, sector constituents, and technical-analysis reports through BaoStock and MyTT. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jasonpro22](https://clawhub.ai/user/jasonpro22) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to fetch BaoStock market, financial, macroeconomic, and index-constituent data for Chinese A-share analysis. It can also generate informational technical-analysis summaries using MyTT indicators. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends stock symbols and date ranges to BaoStock through a third-party Python package. <br>
Mitigation: Use it only when that data sharing is acceptable for the intended workflow. <br>
Risk: Technical-analysis scores and operation suggestions may be misleading, and the security guidance notes duplicated RSI fields. <br>
Mitigation: Treat generated analysis as informational and verify calculations before making financial or trading decisions. <br>
Risk: Full-market scans can query thousands of A-share stocks and may take a long time or encounter rate limits. <br>
Mitigation: Confirm the scan scope with the user first, process in batches, and show progress as described by the artifact. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/jasonpro22/baostock-tt-skills) <br>
- [BaoStock Python API documentation](artifact/docs/python_api_full.txt) <br>
- [MyTT technical indicator library](https://github.com/mpquant/MyTT) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with Python and shell command examples; technical-analysis reports as plain text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include BaoStock query snippets, tabular market data summaries, technical indicator values, scores, and operation suggestions.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
