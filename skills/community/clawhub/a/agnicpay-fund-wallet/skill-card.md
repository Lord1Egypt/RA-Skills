## Description: <br>
Get instructions for funding an Agnic wallet with USDC on Base, including authentication, wallet address lookup, dashboard funding, direct USDC transfer, bridging, and balance verification. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[agnicpay-prog](https://clawhub.ai/user/agnicpay-prog) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill when they need agent guidance for adding USDC to an Agnic wallet, checking the wallet address, choosing a funding path, and confirming the balance on Base. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives wallet-funding guidance where an incorrect network, token, or destination address can lead to lost funds. <br>
Mitigation: Confirm the funding applies to the Agnic wallet and independently verify the Base network, USDC token, and destination address before sending funds. <br>
Risk: The skill may require wallet authentication through a browser session or AGNIC_TOKEN in headless environments. <br>
Mitigation: Use the documented Agnic authentication flow, keep tokens out of shared logs and prompts, and avoid exposing AGNIC_TOKEN beyond the active agent environment. <br>


## Reference(s): <br>
- [Agnic Dashboard](https://app.agnic.ai) <br>
- [Base Bridge](https://bridge.base.org) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes funding instructions, network warnings, authentication notes, and balance verification commands.] <br>

## Skill Version(s): <br>
2.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
