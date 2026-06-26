## Description: <br>
Session state and control-loop skill for OpenClaw DeFi agents. Manages persistent sessions, FarmingContext, event stream snapshots, heartbeats, delegation checks, and bounded autopilot coordination without holding private keys or bypassing user confirmations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[parmasanandgarlic](https://clawhub.ai/user/parmasanandgarlic) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and OpenClaw agents use this skill to coordinate FarmDash DeFi sessions, maintain shared context, check delegation state, and run bounded autopilot planning while keeping state-changing execution in separate user-confirmed skills. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: DeFi coordination can lead to financial loss if an agent acts on stale context, weak limits, or misunderstood intent. <br>
Mitigation: Use bounded budgets and allowlists, refresh event and context state before proposing action, and require explicit user confirmation or local wallet signing before any companion skill executes trades or other on-chain actions. <br>
Risk: Session tokens and the optional FARMDASH_API_KEY are sensitive credentials. <br>
Mitigation: Keep credentials private in the agent runtime and avoid displaying session tokens in normal user-facing prose. <br>
Risk: Autonomous operation can compound mistakes across repeated cycles. <br>
Mitigation: Log decisions, honor halted risk status, re-run sense phases when freshness is stale, and keep autopilot cycles constrained by explicit risk settings. <br>


## Reference(s): <br>
- [FarmDash Agents](https://www.farmdash.one/agents) <br>
- [FarmDash Homepage](https://www.farmdash.one) <br>
- [FarmDash Autonomous Operator Skill Source](https://www.farmdash.one/openclaw-skills/farmdash-autonomous-operator/SKILL.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/parmasanandgarlic/farmdash-autonomous-operator) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Configuration, Guidance, API Calls] <br>
**Output Format:** [Markdown and JSON-like structured guidance for session state, context patches, event snapshots, delegation checks, and autopilot coordination.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include session tokens, FarmingContext state, event stream snapshots, activity traces, delegation status, autopilot configuration, and resolved DeFi intent parameters.] <br>

## Skill Version(s): <br>
1.0.6 (source: release evidence; artifact frontmatter lists 1.0.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
