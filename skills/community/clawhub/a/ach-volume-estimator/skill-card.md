## Description: <br>
Estimate Dwolla's end-of-month ACH transaction volume from daily KPI emails and PDF data by extracting transactions and business days, calculating a per-business-day rate, and projecting monthly totals with a US Federal Reserve holiday calendar. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[daveglaser0823](https://clawhub.ai/user/daveglaser0823) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees who process Dwolla ACH KPI emails use this skill to turn daily email and PDF metrics into end-of-month ACH volume projections, optional revenue forecasts, and dashboard updates for KPI reporting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses sensitive Gmail ACH KPI messages and PDF attachments. <br>
Mitigation: Install only where the named Gmail account and ACH KPI email workflow are approved, and limit access to authorized users. <br>
Risk: The bundle includes revenue forecasting and local calibration file use beyond the core ACH volume estimate. <br>
Mitigation: Confirm revenue forecasting is in scope for this release, or split it into a separate skill with explicit review and approval. <br>
Risk: Dashboard automation writes local report data and is intended for recurring cron use. <br>
Mitigation: Approve the dashboard destination, local paths, and cron schedule before enabling automated runs. <br>


## Reference(s): <br>
- [Federal Reserve Bank Holiday Schedule](https://www.federalreserve.gov/aboutthefed/k8.htm) <br>
- [FRED SOFR Data](https://fred.stlouisfed.org/series/SOFR) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [One-line ACH estimates, optional JSON forecast output, and local dashboard data updates.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use approved Gmail KPI messages, PDF attachments, local calibration files, and local dashboard HTML/JSON files.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
