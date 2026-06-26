## Description: <br>
Generates a Web3 capital markets weekly digest by fetching public financing, regulation, digital-asset treasury, M&A, and RWA project data, then producing a Markdown report for AI-assisted completion. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[baoyangispoor](https://clawhub.ai/user/baoyangispoor) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Analysts, editors, and Web3 operations teams use this skill to assemble a weekly capital operations report covering fundraising, regulation, public-company crypto treasury activity, M&A, and RWA project updates. It is intended to speed up public-data collection while leaving financial figures and narrative analysis for review before publication. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Public market, fundraising, and news sources can be incomplete, unavailable, or stale, and AI-completed commentary may introduce errors. <br>
Mitigation: Verify figures, source links, and generated analysis against the cited public sources before publication. <br>
Risk: The skill runs local Python scripts that make outbound public web requests and one standalone DAT helper may require Playwright. <br>
Mitigation: Run the scripts in an intended local workspace, review dependencies before installing them, and inspect the generated Markdown before sharing. <br>
Risk: Broad Web3 weekly-report phrasing may activate the skill even when the user expects a narrower task. <br>
Mitigation: Confirm the requested date range and report scope before running the full collection workflow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/baoyangispoor/eden-digital-web3-weekly-digest-yang) <br>
- [TechFlow RSS feed](https://www.techflowpost.com/api/client/common/rss.xml?page=1) <br>
- [Rootdata Fundraising](https://www.rootdata.com/Fundraising) <br>
- [CoinGecko public treasury API](https://api.coingecko.com/api/v3/companies/public_treasury/bitcoin) <br>
- [PANews RWA weekly column](https://www.panewslab.com/en/columns/019888d2-9a04-7e7b-97b5-5a1eac76759a) <br>
- [Coinglass Bitcoin Treasuries](https://www.coinglass.com/zh/BitcoinTreasuries) <br>
- [CryptoRank RWA news API](https://api.cryptorank.io/v0/news?lang=en&coinKeys=rwa&withFullContent=true) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown report with structured sections and marked fields for AI completion] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes a local report file; default output path is report_YYYYMMDD.md unless overridden.] <br>

## Skill Version(s): <br>
8.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
