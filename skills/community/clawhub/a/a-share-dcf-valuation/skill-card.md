## Description: <br>
DCF valuation modeling for A-share listed companies; the skill uses a stock code to fetch financial data, calculate WACC, run conservative/base/optimistic DCF scenarios, generate a sensitivity matrix, and produce a Chinese Markdown report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[laigen](https://clawhub.ai/user/laigen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and agent users use this skill to generate A-share DCF valuation reports from Tushare data for listed companies. It is intended for valuation analysis workflows where the user supplies a stock code and reviews the generated report before relying on it. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Tushare token and could expose or persist it if users place it in broad shell profiles or logs. <br>
Mitigation: Protect and rotate the Tushare token, set it only for the command when possible, or store it in a restricted secret store. <br>
Risk: Reports are written to the configured workspace path, so an incorrect OPENCLAW_WORKSPACE can place files somewhere unexpected. <br>
Mitigation: Confirm OPENCLAW_WORKSPACE before running the script and use a controlled workspace for generated reports. <br>
Risk: DCF outputs can be misleading if treated as investment advice or used without reviewing assumptions and source data. <br>
Mitigation: Review generated valuation reports, assumptions, and risk disclosures before using them for investment decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/laigen/a-share-dcf-valuation) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/laigen) <br>
- [Tushare data API](https://tushare.pro) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown report in Chinese with terminal progress text and setup commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes valuation reports under reports/dcf_{company}_{date}.md in the configured workspace.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
