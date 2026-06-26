## Description: <br>
Demo skill for practicing Cashu HTTP 402 payment flow end-to-end: detect 402, review x-cashu challenge, request permission when needed, settle payment, and retry with X-Cashu. <br>

This skill is for demonstration purposes and not for production usage. <br>

## Publisher: <br>
[robwoodgate](https://clawhub.ai/user/robwoodgate) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to practice a Cashu-gated HTTP 402 payment flow against a controlled endpoint. It guides the agent through reviewing an x-cashu challenge, obtaining human approval before spending, retrying with a Cashu token, and confirming a successful paid response. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may spend or consume a small Cashu token during the paywalled HTTP flow. <br>
Mitigation: Require human approval before spending and verify the endpoint, amount, mint, and purpose before approving payment. <br>
Risk: Installing or using wallet tooling can introduce dependency and wallet-management risk. <br>
Mitigation: Review cocod separately and ask permission before installing or using it. <br>
Risk: Handling the x-cashu header unsafely in a shell could allow unintended command interpretation. <br>
Mitigation: Pass the x-cashu value as data and avoid pasting untrusted header text into shell syntax. <br>


## Reference(s): <br>
- [Clawtar ClawHub release page](https://clawhub.ai/robwoodgate/clawtar) <br>
- [Clawtar API endpoint](https://clawtar.cashutools.dev/v1/clawtar/ask) <br>
- [Minibits Mint](https://mint.minibits.cash/Bitcoin) <br>
- [cocod wallet skill](https://clawhub.ai/Egge21M/cocod) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API calls] <br>
**Output Format:** [Markdown with JSON examples and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires human approval before spending Cashu tokens or installing wallet tooling.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
