## Description: <br>
Extracts, normalizes, and analyzes key metrics from corporate financial reports, producing ratio analysis, red-flag findings, and peer-comparison oriented summaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[boboy-j](https://clawhub.ai/user/boboy-j) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and analysts use this skill to summarize normalized company financial data, compute common financial ratios, and surface heuristic red flags for further review. It is descriptive analysis only and should not be used for stock price prediction, investment advice, or unsupported business decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release substantially overstates its financial-report analysis capabilities and may return placeholder results for unsupported report formats. <br>
Mitigation: Treat it as a local demo for pre-normalized JSON financial data unless the publisher narrows the claims or implements the missing PDF, XBRL, Excel, peer benchmarking, provenance, and audit-log functionality. <br>
Risk: Outputs could be misread as business, investment, or fraud conclusions. <br>
Mitigation: Use the output only as descriptive analysis and review red flags as signals that warrant further investigation, not as verdicts or investment advice. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/boboy-j/financial-report-analyzer-pro) <br>
- [Publisher profile](https://clawhub.ai/user/boboy-j) <br>
- [Project homepage](https://github.com/openclaw-skills/financial-report-analyzer) <br>
- [IFRS Standards](https://www.ifrs.org/issued-standards/) <br>
- [FASB Accounting Standards Codification](https://asc.fasb.org/) <br>
- [Ratio Definitions](knowledge/ratio_definitions.md) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [JSON or Markdown financial analysis report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include executive summaries, computed ratios, red-flag findings, peer-benchmark fields, and provenance fields when supported by the input data.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter, changelog, release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
