## Description: <br>
Universal AI agent development guardrails with five defense layers: instruction gate, project monitoring, delivery reliability, code quality audit, and scope fidelity enforcement. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nagi-226](https://clawhub.ai/user/nagi-226) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to make coding agents challenge ambiguous, unrealistic, or unsafe development requests before implementation. It supports scope confirmation, project-drift monitoring, delivery reliability checks, quality auditing, and over-engineering prevention during software work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can make an agent more conservative and may slow straightforward development tasks with extra confirmation steps. <br>
Mitigation: Use the documented micro-task exception for small, unambiguous changes and keep confirmations focused on scope, approach, and key decisions. <br>
Risk: The skill may refuse, narrow, or redirect oversized or vague development requests. <br>
Mitigation: Ask the agent to state the capability boundary, offer scaled alternatives, and proceed only after the user confirms a feasible scope. <br>
Risk: Because the skill is text-only, it depends on the host agent consistently applying the guardrail behavior. <br>
Mitigation: Review the agent's plans and delivery notes for explicit scope checks, regression checks, and quality-audit outcomes before relying on generated code. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nagi-226/dev-guardrails) <br>
- [Project homepage](https://github.com/FJL03/Nagi-Skills) <br>
- [Capability Boundaries](references/boundaries.md) <br>
- [Scenario SOP Library](references/scenarios.md) <br>
- [L5 Defense Test](references/l5-defense-test.md) <br>
- [Simulation Test Report](references/test-report.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration, text] <br>
**Output Format:** [Markdown and text guidance, with code, shell commands, or configuration when the guarded development task requires them] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Behavioral guardrail for coding-agent sessions; no hidden execution, data collection, or destructive behavior found in security evidence.] <br>

## Skill Version(s): <br>
3.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
