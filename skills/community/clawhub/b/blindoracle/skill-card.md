## Description: <br>
Privacy-first agent infrastructure for forecasting markets, credential verification, multi-rail settlement, and cross-rail transfers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[craigmbrown](https://clawhub.ai/user/craigmbrown) <br>

### License/Terms of Use: <br>
Proprietary <br>


## Use Case: <br>
Developers and agent operators use BlindOracle to let agents create forecasts, verify credentials, check balances, request settlement, and initiate cross-rail transfers through x402-paid services. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can trigger paid x402/USDC, settlement, swap, withdrawal, and credential-minting workflows. <br>
Mitigation: Use scoped payment credentials, low transaction limits, and manual approval for every paid or value-moving action. <br>
Risk: The security evidence says generic rail terminology is used for crypto and USDC payment activity. <br>
Mitigation: Treat settlement, transfer, and rail actions as crypto payment operations during review and user consent. <br>
Risk: Financial actions are delegated to external handler modules that were not included in the reviewed artifact. <br>
Mitigation: Inspect and approve those modules before installing or trusting the skill with funds. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/craigmbrown/blindoracle) <br>
- [BlindOracle Homepage](https://craigmbrown.com/blindoracle) <br>


## Skill Output: <br>
**Output Type(s):** [API responses, Payment requests, Settlement and transfer results, Credential verification results] <br>
**Output Format:** [JSON responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Responses may include x402 payment requirements, security details, balances, forecasts, credential results, quotes, or transfer outcomes.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
