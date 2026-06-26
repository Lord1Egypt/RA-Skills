## Description: <br>
Analyze Twitter Spaces and voice conversations to extract market intelligence, crypto alpha, sentiment analysis, and speaker-attributed insights. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[benschiller](https://clawhub.ai/user/benschiller) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External agents and developers use Clawdio to browse and purchase structured Twitter Spaces intelligence, including metadata, speaker-attributed Markdown reports, transcripts, sentiment, trend signals, and project mentions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Wallet-enabled agents may purchase paid reports automatically without clear per-purchase approval or spending limits. <br>
Mitigation: Use a dedicated low-balance wallet, require explicit approval before every purchase, browse the free catalog first, and verify the report ID and $1.49 USDC price before allowing payment. <br>
Risk: Purchased artifacts may contain speaker-attributed transcripts and quotes from voice conversations. <br>
Mitigation: Avoid sharing or storing speaker-attributed transcript content unless there is a clear basis to do so. <br>
Risk: Repeat access requires repurchase if report responses are not saved. <br>
Mitigation: Save purchased artifacts after retrieval and confirm storage policy before deleting or re-requesting paid content. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/benschiller/clawdio-twitter) <br>
- [Clawdio API](https://clawdio.vail.report) <br>
- [Clawdio catalog](https://clawdio.vail.report/catalog) <br>
- [API Reference](references/API-REFERENCE.md) <br>
- [Integration Guide](references/INTEGRATION.md) <br>
- [x402 protocol](https://www.x402.org/) <br>
- [Coinbase AgentKit](https://docs.cdp.coinbase.com/agentkit) <br>
- [Coinbase CDP SDK](https://docs.cdp.coinbase.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Guidance] <br>
**Output Format:** [JSON responses containing metadata and Markdown report and transcript content] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access and an x402-compatible wallet funded with USDC on Base Mainnet; each purchased report costs $1.49 USDC.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
