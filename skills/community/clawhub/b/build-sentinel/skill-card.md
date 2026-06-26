## Description: <br>
Security scanning and transaction simulation for Solana AI agents <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[buildsentinel-dev](https://clawhub.ai/user/buildsentinel-dev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and Solana AI agents use Sentinel to scan user requests for prompt or fraud threats and to simulate Solana transactions against policy before signing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks the agent to rely on an undeclared local `sentinel` command for financial transaction safety decisions. <br>
Mitigation: Install and use it only after verifying the exact CLI source, version, and local policy file. <br>
Risk: Transaction approval may be treated as authoritative even when scanner or simulator provenance is unknown. <br>
Mitigation: Limit use to Solana transaction or wallet-security contexts and keep human review in the signing flow for high-value or unusual transactions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/buildsentinel-dev/build-sentinel) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON-result interpretation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a local sentinel CLI and policy configuration; transaction approval depends on verified executable source, version, and policy.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
