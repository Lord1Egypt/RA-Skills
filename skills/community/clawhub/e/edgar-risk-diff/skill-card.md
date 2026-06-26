## Description: <br>
Diffs the SEC 10-K Risk Factors section (Item 1A) between two filings for a US-listed ticker and reports new, removed, and modified risk language, theme rollups, and churn percentage. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hootriot08](https://clawhub.ai/user/hootriot08) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External analysts, investors, students, and research teams use this skill to compare year-over-year 10-K risk-factor disclosures, spot newly added or removed risks, and summarize dominant themes across one or more tickers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill makes outbound HTTPS GET requests to SEC EDGAR and sends the configured EDGAR User-Agent to SEC servers. <br>
Mitigation: Run it only where SEC EDGAR access is acceptable and set EDGAR_USER_AGENT to an appropriate contact string when redistributing. <br>
Risk: Downloaded public filings are cached in ~/.edgar-risk-diff/cache. <br>
Mitigation: Review or clear the local cache according to the user's data-retention needs. <br>
Risk: The optional premium feature uses a local license key. <br>
Mitigation: Keep the license key out of shared repositories, shell history, and logs where possible. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/hootriot08/edgar-risk-diff) <br>
- [SEC company tickers data](https://www.sec.gov/files/company_tickers.json) <br>
- [SEC submissions API](https://data.sec.gov/submissions/) <br>
- [SEC EDGAR archives](https://www.sec.gov/Archives/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown reports and tables from CLI subcommands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Fetches public SEC filings over HTTPS, caches responses locally, and can use a local premium license key for novelty scoring.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
