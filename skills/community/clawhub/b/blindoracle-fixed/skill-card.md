## Description: <br>
Security-audited AI agent marketplace with ERC-8004 passports, MASSAT audits, and x402 micropayments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[craigmbrown](https://clawhub.ai/user/craigmbrown) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to configure BlindOracle marketplace operations, submit agent audit requests, check audit status, and issue ERC-8004-compatible identity passports through a configured MASSAT endpoint. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Agent names, capabilities, operator IDs, and passport data can be sent to the configured MASSAT endpoint. <br>
Mitigation: Use only a trusted MASSAT_API_URL and avoid submitting sensitive identifiers unless that endpoint is intended to receive them. <br>
Risk: The BLINDORACLE_API_KEY authorizes marketplace operations. <br>
Mitigation: Use a scoped key when possible and keep it out of command logs, shared shells, and committed configuration. <br>
Risk: The skill supports x402 micropayment workflows. <br>
Mitigation: Confirm payment limits, approval policy, and settlement expectations before enabling purchase-capable agent operations. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/craigmbrown/blindoracle-fixed) <br>
- [Publisher profile](https://clawhub.ai/user/craigmbrown) <br>
- [BlindOracle website](https://craigmbrown.com/blindoracle/) <br>
- [BlindOracle whitepaper](https://craigmbrown.com/blindoracle/whitepaper/) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, API calls, Guidance] <br>
**Output Format:** [Markdown with bash and curl examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MASSAT_API_URL and BLINDORACLE_API_KEY in the execution environment.] <br>

## Skill Version(s): <br>
1.1.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
