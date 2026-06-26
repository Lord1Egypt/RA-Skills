## Description: <br>
Provides real-time cryptocurrency prices, on-chain Ethereum data, and DeFi metrics through a unified agent-facing tool interface. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangshuniguang](https://clawhub.ai/user/wangshuniguang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to retrieve crypto market prices, Ethereum account and gas data, and DeFi TVL, yield, and stablecoin metrics for analysis and user-facing answers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The packaged runtime can load code outside the reviewed artifact. <br>
Mitigation: Review the complete upstream DataVault source that supplies the missing app/src modules before installation or production use. <br>
Risk: The skill is a networked crypto-data integration with under-declared credential and configuration needs. <br>
Mitigation: Use only low-privilege data-provider API keys and avoid exchange trading credentials. <br>
Risk: Wallet-related lookups may encourage users to provide sensitive wallet material. <br>
Mitigation: Provide public wallet addresses only; never provide private keys, seed phrases, or signing credentials. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/wangshuniguang/cyptodatavault) <br>
- [Publisher profile](https://clawhub.ai/user/wangshuniguang) <br>
- [README_OPENCLAW.md](artifact/README_OPENCLAW.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, guidance] <br>
**Output Format:** [Structured JSON-like tool responses summarized as agent text when appropriate] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Network-backed data may depend on exchange, blockchain, and DeFi provider availability.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
