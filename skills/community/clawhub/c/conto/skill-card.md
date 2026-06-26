## Description: <br>
Enforces fine-grained spending policies before an agent executes payments, transfers, swaps, bridges, or x402 API payments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kwattana](https://clawhub.ai/user/kwattana) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and agent operators use Conto to check payment intent against policy controls before value leaves an agent wallet. The skill also supports viewing, creating, updating, and deleting Conto policies when an admin SDK key is provided. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent high-impact authority over payment approvals, policy changes, and fund movement. <br>
Mitigation: Use a Standard SDK key for routine payment checks, keep Admin keys out of auto-running chat agents, and require explicit human confirmation before transfers or policy mutations. <br>
Risk: A payment could proceed without the intended policy protection if the approval, execution, or confirmation flow is skipped or misapplied. <br>
Mitigation: Require a Conto approval before transfer, stop on denials or expired approvals, and confirm successful transactions so spend tracking remains accurate. <br>
Risk: Credential exposure or overly broad SDK permissions could let an agent or operator bypass intended controls. <br>
Mitigation: Store CONTO_SDK_KEY only in the agent environment, prefer least-privilege SDK keys, and monitor Conto dashboard activity after use. <br>


## Reference(s): <br>
- [ClawHub Conto Skill](https://clawhub.ai/kwattana/conto) <br>
- [Conto Homepage](https://conto.finance) <br>
- [Conto SDK Docs](https://docs.conto.finance) <br>
- [Conto Policy Documentation](https://conto.finance/docs/policies) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, API calls, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, JSON API payloads, and payment status details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires CONTO_SDK_KEY and may report approvals, denials, policy violations, transaction hashes, and explorer URLs.] <br>

## Skill Version(s): <br>
1.8.0 (source: server release metadata; artifact files report 1.6.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
