## Description: <br>
Clawdio transforms human voice audio into structured data, semantic reports, and machine-readable markdown for market intelligence, crypto alpha, speaker-attributed quotes, and sentiment analysis from voice conversations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[benschiller](https://clawhub.ai/user/benschiller) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use Clawdio to browse and purchase voice-derived intelligence reports, then consume structured metadata, speaker-attributed transcripts, and markdown analysis for research, market monitoring, and content workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: An agent with a funded wallet can spend real USDC through the x402 purchase flow. <br>
Mitigation: Use a dedicated low-balance wallet and require manual approval before any /catalog/purchase request. <br>
Risk: A mistaken endpoint, report ID, or price could cause an unintended paid request. <br>
Mitigation: Verify the Clawdio domain, selected report ID, Base Mainnet payment network, and 1.49 USDC price before approving purchase. <br>
Risk: Purchased artifacts are not stored for repeat access by the service. <br>
Mitigation: Save returned metadata, report, and transcript artifacts immediately after a successful purchase. <br>


## Reference(s): <br>
- [Clawdio API](https://clawdio.vail.report) <br>
- [Clawdio Skill Page](https://clawhub.ai/benschiller/clawdio) <br>
- [Coinbase AgentKit Documentation](https://docs.cdp.coinbase.com/agentkit) <br>
- [Coinbase CDP SDK Documentation](https://docs.cdp.coinbase.com/) <br>
- [x402 Protocol](https://www.x402.org/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown guidance with API examples; purchased reports return JSON metadata plus markdown report and transcript content.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access and an x402-compatible wallet funded with USDC on Base Mainnet for paid report purchases.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence release and artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
