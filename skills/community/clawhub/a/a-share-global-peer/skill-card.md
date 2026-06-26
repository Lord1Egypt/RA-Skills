## Description: <br>
Finds global peer companies for A-share listed companies and produces comparison reports with product, market-share, and benchmark rationale. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[laigen](https://clawhub.ai/user/laigen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External finance analysts, investors, and researchers use this skill to identify publicly listed overseas peers for A-share companies and compare product overlap, market position, and market-share data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Financial, market-share, or peer-comparison data may be incomplete, stale, or unsuitable for investment or business decisions. <br>
Mitigation: Independently verify figures and cited sources before relying on the report. <br>
Risk: The skill may run a bundled Python helper and perform web or finance-data lookups using optional API keys. <br>
Mitigation: Review the helper before execution and provide only API keys intended for this skill's use. <br>
Risk: The bundled global leader reference table can become outdated as market leadership changes. <br>
Mitigation: Refresh peer and market-share claims with current web search and source-date labels. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/laigen/a-share-global-peer) <br>
- [Global Industry Leaders Reference Table](references/global_leaders_reference.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, JSON, Guidance] <br>
**Output Format:** [Chinese Markdown comparison report with tables and labeled data sources; the helper script can emit JSON or plain text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Limits the report to the most representative peer companies, labels data sources, includes a data timestamp, and flags estimates for verification.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
