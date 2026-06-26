## Description: <br>
Generates a structured Web3 industry capital-markets weekly digest covering financing events, regulatory and industry updates, public-company digital-asset treasury activity, M&A transactions, and RWA project progress. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[baoyangispoor](https://clawhub.ai/user/baoyangispoor) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, analysts, and editorial teams use this skill to gather public Web3 market signals and draft a weekly capital-operations digest with consistent sections and manually reviewable gaps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Financial or regulatory claims may be incomplete, stale, or misleading when public sources or free APIs omit weekly change data. <br>
Mitigation: Review important claims against primary sources before publishing and use the skill's manual supplementation prompts for missing data. <br>
Risk: Manual supplements may expose confidential internal research if pasted into an agent session. <br>
Mitigation: Only provide information that is approved for the agent environment and avoid confidential internal research. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/baoyangispoor/eden-digital-web3-weekly-digest) <br>
- [Cryptorank funding rounds](https://cryptorank.io/funding-rounds) <br>
- [CoinGecko public treasury API - Bitcoin](https://api.coingecko.com/api/v3/companies/public_treasury/bitcoin) <br>
- [CoinGecko public treasury API - Ethereum](https://api.coingecko.com/api/v3/companies/public_treasury/ethereum) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown weekly digest with inline shell and Python snippets for public data collection] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes prompts for manual supplementation where public sources or free APIs do not provide complete weekly data.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter reports 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
