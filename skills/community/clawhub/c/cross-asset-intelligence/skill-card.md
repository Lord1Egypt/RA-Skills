## Description: <br>
Cross-asset financial analysis API combining crypto and traditional markets, with BTC-equity correlation, cross-market risk scoring, crypto news impact analysis, macro reports, token contract risk evaluation, and daily market briefings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sugacrypto](https://clawhub.ai/user/sugacrypto) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to request paid cross-market crypto and traditional finance analysis, including correlation checks, market risk scores, token safety checks, macro outlooks, and daily briefings in English or Japanese. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses paid x402 endpoints that can spend USDC from an agent wallet. <br>
Mitigation: Use a dedicated Base wallet with only the USDC budget you are willing to spend, keep WALLET_SIGNING_KEY out of source control, and require confirmation for paid or higher-tier requests where possible. <br>
Risk: The API returns market research and token safety analysis that could be mistaken for financial advice. <br>
Mitigation: Treat outputs as research inputs, review the included disclaimers and data freshness, and make financial decisions only after independent validation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sugacrypto/cross-asset-intelligence) <br>
- [x402 Bankr API endpoint](https://x402.bankr.bot/0x98ee945dfa6bb8e9ed9f9b6ae56eb82bcc82f0aa/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with HTTP GET examples and structured API response descriptions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include market analysis, correlation coefficients, risk scores, token safety verdicts, data-source freshness metadata, upgrade links, and financial-advice disclaimers.] <br>

## Skill Version(s): <br>
1.0.2 (source: server evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
