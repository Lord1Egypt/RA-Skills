## Description: <br>
Configure PostParam (Post-Mint Parameter / PMP) values on Art Blocks tokens using artblocks-mcp. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ryley-o](https://clawhub.ai/user/ryley-o) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and Art Blocks users use this skill to discover available PostParams for a token, validate allowed values and authorization, and prepare an unsigned transaction for post-mint configuration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on a configured artblocks-mcp service for token and transaction data. <br>
Mitigation: Install and use it only when the configured artblocks-mcp service is trusted. <br>
Risk: Wallet addresses or token identifiers may reveal activity or ownership patterns. <br>
Mitigation: Avoid submitting wallet addresses or identifiers considered private unless the lookup is acceptable to the user. <br>
Risk: A transaction can revert if the signer is not authorized for a parameter's authOption. <br>
Mitigation: Call discover_postparams first, show authOption and constraints to the user, and compare them with the signer's role before building the transaction. <br>


## Reference(s): <br>
- [Configure Postparams on ClawHub](https://clawhub.ai/ryley-o/configure-postparams) <br>
- [Publisher profile: ryley-o](https://clawhub.ai/user/ryley-o) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline tool-call examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces instructions for discovering PostParams and building unsigned configuration transactions; it does not execute or submit transactions by itself.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
