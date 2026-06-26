## Description: <br>
Ampersend CLI for agent payments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[matiasedgeandnode](https://clawhub.ai/user/matiasedgeandnode) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external agents use this skill to configure Ampersend and make x402-enabled HTTP requests that can complete stablecoin payments within user-defined spending limits. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill enables delegated stablecoin payments by an agent. <br>
Mitigation: Use a dedicated low-balance account and set strict per-transaction, daily, and monthly spending limits. <br>
Risk: Automatic top-up can increase financial exposure. <br>
Mitigation: Avoid auto-topup unless it is intentionally required for the deployment. <br>
Risk: A paid request can spend funds if payment requirements are accepted. <br>
Mitigation: Use the inspect flow to review payment requirements and costs before making a payment. <br>
Risk: The installation depends on a globally installed npm package. <br>
Mitigation: Verify the npm package source and required version before installation or update. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/matiasedgeandnode/ampersend) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with bash command examples and JSON response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the ampersend CLI v0.0.14 and a configured agent account.] <br>

## Skill Version(s): <br>
1.0.14 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
