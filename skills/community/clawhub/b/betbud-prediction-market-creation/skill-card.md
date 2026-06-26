## Description: <br>
Automatically creates prediction markets on betbud.live by analyzing trending crypto Twitter topics with Claude AI, selecting images, creating Base Sepolia markets, and registering them through the Betbud workflow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[SamJ12](https://clawhub.ai/user/SamJ12) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External developers and platform operators can use this agent to keep a prediction-market site populated with timely crypto-related markets. The skill monitors crypto Twitter, asks Claude to draft a yes/no market proposal, fetches an image, sends a Base Sepolia transaction, and registers the market on betbud.live. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can autonomously spend testnet wallet funds and publish prediction markets without a built-in confirmation step or clear limits. <br>
Mitigation: Run it manually first with a dedicated low-value Base Sepolia test wallet, and require confirmation showing the proposed market, contract address, deposit, gas settings, and Betbud payload before signing or posting. <br>
Risk: Scheduled or continuous operation can create repeated external actions without rate, budget, or monitoring controls. <br>
Mitigation: Avoid cron or 24/7 operation unless rate limits, budget limits, monitoring, and alerting are added. <br>
Risk: The skill requires a wallet private key and API keys in the local environment. <br>
Mitigation: Use only scoped service credentials and never use a main wallet key. Keep secrets in local environment files outside source control. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/SamJ12/betbud-prediction-market-creation) <br>
- [Publisher profile](https://clawhub.ai/user/SamJ12) <br>
- [twitterapi.io](https://twitterapi.io) <br>
- [Anthropic Console](https://console.anthropic.com) <br>
- [Unsplash Developers](https://unsplash.com/developers) <br>
- [Base Sepolia RPC](https://sepolia.base.org) <br>
- [Base Sepolia transaction explorer](https://sepolia.basescan.org) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, API Calls, Blockchain transactions, Files] <br>
**Output Format:** [Console text, JSON market proposals, HTTP requests, signed Base Sepolia transactions, and a local JSON cache] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates externally visible prediction markets and stores recent prediction questions in recent_predictions.json.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
