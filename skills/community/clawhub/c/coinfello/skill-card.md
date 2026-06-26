## Description: <br>
Interact with CoinFello using the @coinfello/agent-cli to create a smart account, sign in with SIWE, manage delegations, send prompts with server-driven ERC-20 token subdelegations, and check transaction status. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[brettcleary](https://clawhub.ai/user/brettcleary) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to operate CoinFello wallet workflows through an agent, including smart account setup, SIWE sign-in, delegation review, prompt-based ERC-20 transaction requests, and transaction status checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent crypto-signing capability. <br>
Mitigation: Install only when the user trusts CoinFello and understands that prompts may lead to wallet signing and transaction workflows. <br>
Risk: Delegation flows can authorize ERC-20 transfer scopes. <br>
Mitigation: Review each pending delegation request before running approve_delegation_request, including chain, token, recipient, amount, and justification. <br>
Risk: Using --use-unsafe-private-key stores a plaintext software private key. <br>
Mitigation: Use hardware-backed signing where available and reserve --use-unsafe-private-key for development or testing. <br>
Risk: A misconfigured CoinFello API endpoint can direct signing and delegation flows to an untrusted service. <br>
Mitigation: Verify COINFELLO_BASE_URL before delegation flows and avoid overriding it unless the target endpoint is trusted. <br>
Risk: Installing the CLI with @latest can change behavior as the package evolves. <br>
Mitigation: Consider pinning @coinfello/agent-cli to a reviewed version for repeatable deployments. <br>


## Reference(s): <br>
- [CoinFello CLI Reference](references/REFERENCE.md) <br>
- [CoinFello](https://coinfello.com) <br>
- [CoinFello API Base URL](https://app.coinfello.com/) <br>
- [ClawHub Skill Page](https://clawhub.ai/brettcleary/coinfello) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include transaction IDs, delegation review steps, account status, and troubleshooting guidance returned through CLI workflows.] <br>

## Skill Version(s): <br>
0.3.6 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
