## Description: <br>
Execute liquid staking operations on Bifrost SLPx protocol across Ethereum, Base, Optimism, and Arbitrum, including minting vETH, redeeming vETH back to ETH, and claiming completed redemptions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ark930](https://clawhub.ai/user/ark930) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to prepare and execute Bifrost vETH staking, redemption, and claim workflows across supported EVM networks. It can produce unsigned transaction details for manual wallet signing or guide opt-in agent-side signing when explicitly configured. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional agent-side signing can expose funds if a private key is used in an untrusted environment. <br>
Mitigation: Prefer manual signing. If agent-side signing is used, configure BIFROST_PRIVATE_KEY only in a trusted environment and use a dedicated low-balance wallet. <br>
Risk: Incorrect chain, contract address, amount, receiver, calldata, or gas can cause unintended on-chain transactions. <br>
Mitigation: Review the full transaction preview and verify chain, contract address, amount, receiver, calldata, and gas before confirming any write operation. <br>
Risk: Redeeming vETH starts a queued withdrawal rather than returning ETH immediately. <br>
Mitigation: Warn users before redemption, check claimable amounts before claim attempts, and only proceed after explicit confirmation. <br>


## Reference(s): <br>
- [Bifrost vETH page](https://www.bifrost.io/vtoken/veth) <br>
- [Bifrost App vETH staking](https://app.bifrost.io/vstaking/vETH) <br>
- [ClawHub skill page](https://clawhub.ai/ark930/bifrost-slpx-stake) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with transaction fields and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include chain-specific contract addresses, calldata, RPC settings, previews, warnings, and block explorer links.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata; skill metadata lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
