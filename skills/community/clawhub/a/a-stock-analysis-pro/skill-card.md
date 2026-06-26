## Description: <br>
Generates Chinese A-share stock strategy research reports in HTML/PDF format from public market, financial, fund-flow, industry, and event data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bill-lib](https://clawhub.ai/user/bill-lib) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and analysts use this skill to ask an agent for structured Chinese A-share company research, including public market data collection, valuation context, scenario analysis, risks, and HTML report generation. It is intended to support research workflows, not to replace independent verification or investment judgment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The generated stock report may contain stale, incomplete, or misleading market data or conclusions. <br>
Mitigation: Ask the agent to confirm ambiguous stock identifiers, verify public market data against source sites, and independently review conclusions before making investment decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bill-lib/a-stock-analysis-pro) <br>
- [Data source specification](artifact/references/data-sources.md) <br>
- [Analysis prompt templates](artifact/references/analysis-prompts.md) <br>
- [HTML report template and quality checklist](artifact/references/report-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Code, Files, Guidance] <br>
**Output Format:** [HTML report content with optional PDF export guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses public A-share market data sources and should be checked against current source data before decisions are made.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
