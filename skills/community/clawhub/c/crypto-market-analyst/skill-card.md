## Description: <br>
Analyze Bitcoin, Ethereum, and major altcoins using real-time price, on-chain signals, and macro context from the Finskills API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[finskills](https://clawhub.ai/user/finskills) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to analyze current cryptocurrency market conditions, compare Bitcoin, Ethereum, and major altcoins, and produce structured market regime and positioning guidance from Finskills API data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Finskills API key and sends crypto market requests to the Finskills service. <br>
Mitigation: Provide the key only if the deployment is approved to use Finskills, store it as a secret environment variable, and avoid including unrelated sensitive information in prompts. <br>
Risk: The skill can produce positioning guidance for highly volatile crypto assets. <br>
Mitigation: Treat outputs as research support, verify market data independently, and do not use the report as financial advice. <br>
Risk: Crypto market data may be delayed or incomplete for fast-moving market conditions. <br>
Mitigation: Check timestamps, corroborate with current market sources, and rerun analysis before acting on time-sensitive conclusions. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/finskills/crypto-market-analyst) <br>
- [Finskills Publisher Profile](https://clawhub.ai/user/finskills) <br>
- [Project Homepage](https://github.com/finskills/crypto-market-analyst) <br>
- [Finskills API](https://finskills.net) <br>
- [Finskills API Registration](https://finskills.net/register) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, analysis, guidance] <br>
**Output Format:** [Markdown report with market tables, computed metrics, and concise positioning guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires FINSKILLS_API_KEY for Finskills API access; outputs are research support, not financial advice.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
