## Description: <br>
clawxpay helps agents make user-approved pay-per-call API requests through x402 using a Base USDC wallet for market data, on-chain data, funding intelligence, China A-share data, and AI inference. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[biggggtreee-rgb](https://clawhub.ai/user/biggggtreee-rgb) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agents use clawxpay to access paid data and AI inference endpoints without managing separate provider accounts or API keys. The skill is intended for tasks such as market lookups, technical indicators, on-chain signals, Web3 funding research, China A-share data, and model inference where the user approves spending before each paid call. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can spend USDC from the configured Base wallet across external paid services. <br>
Mitigation: Use a dedicated low-balance wallet, require explicit user approval before paid calls, and configure per-transaction caps, daily caps, and recipient allowlists before use. <br>
Risk: Requests may send prompts, files, URLs, or private data to paid external services. <br>
Mitigation: Avoid sending sensitive data unless the user intends to share it with the selected external service. <br>
Risk: The local wallet private key is sensitive and stored on disk. <br>
Mitigation: Do not print, log, transmit, or request the private key; use the wallet address for user-facing wallet information. <br>


## Reference(s): <br>
- [clawxpay homepage](https://clawxpay.com) <br>
- [clawxpay documentation](https://clawxpay.com/docs) <br>
- [ClawHub skill page](https://clawhub.ai/biggggtreee-rgb/clawxpay) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, shell commands, configuration, API calls] <br>
**Output Format:** [Markdown with JavaScript and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance centers on user-approved paid API calls, wallet balance checks, spending caps, and safe handling of the local wallet key.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
