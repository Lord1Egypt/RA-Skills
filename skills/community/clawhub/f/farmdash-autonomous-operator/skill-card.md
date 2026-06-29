## Description: <br>
Session state and control-loop skill for OpenClaw. Manages sessions, FarmingContext, autopilot OODA control loops, circuit breakers, and Forensic receipts in zero-custody. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[parmasanandgarlic](https://clawhub.ai/user/parmasanandgarlic) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external DeFi agent operators use this skill to coordinate persistent FarmDash sessions, shared context, bounded autopilot control loops, policy checks, approvals, and forensic receipts. It is intended for zero-custody session and state coordination, not direct private-key custody or direct on-chain execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: DeFi autopilot coordination can create financial risk if budgets, allowlists, or execution approvals are too broad. <br>
Mitigation: Keep budgets and allowlists tight, require explicit wallet approval for transactions, and halt workflows when risk limits or circuit breakers are reached. <br>
Risk: FARMDASH_API_KEY and sessionToken values are sensitive credentials. <br>
Mitigation: Store credentials only in the agent runtime or secret manager, avoid displaying session tokens in user-facing prose, and rotate credentials if exposed. <br>
Risk: The skill coordinates intent routing and approval records but does not itself provide private-key custody or direct on-chain execution. <br>
Mitigation: Use separate signing or execution skills for state-changing actions and verify that policy, simulation, and approval gates pass before execution. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/parmasanandgarlic/skills/farmdash-autonomous-operator) <br>
- [FarmDash Agents](https://www.farmdash.one/agents) <br>
- [FarmDash Autonomous Operator Skill Manual](https://www.farmdash.one/openclaw-skills/farmdash-autonomous-operator/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown and structured session or intent guidance for agent workflows] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference session tokens, API keys, approval payloads, receipt IDs, and risk-state data that should be handled as sensitive operational context.] <br>

## Skill Version(s): <br>
1.0.9 (source: ClawHub release metadata; artifact frontmatter reports 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
