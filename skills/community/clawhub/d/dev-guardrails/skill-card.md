## Description:

Universal AI agent development guardrails with five defense layers: instruction gate, project monitoring, delivery reliability, code quality audit, and scope fidelity enforcement.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nagi-226](https://clawhub.ai/user/nagi-226)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to make coding agents challenge unclear requirements, confirm scope before non-trivial implementation, monitor project drift, and run delivery-quality checks before presenting work as complete.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review says the skill gives itself broad session-wide control and states that its rules override other development instructions.

Mitigation: Keep the skill subordinate to platform, system, developer, and current user instructions, and treat its guardrails as process guidance rather than authority over higher-priority instructions.

Risk: The security guidance says the skill may pause ordinary work, force confirmations, reject vague requests, and push back on scope changes.

Mitigation: Use it where explicit scope confirmation and engineering pushback are desired, and review agent responses for proportionality on small or clearly bounded tasks.

Risk: The security verdict is suspicious even though no specific risk findings were listed.

Mitigation: Review and scan the skill before deployment, then monitor whether it over-constrains normal development workflows.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/nagi-226/skills/dev-guardrails)
- [Project Homepage](https://github.com/FJL03/Nagi-Skills)
- [Capability Boundaries](references/boundaries.md)
- [Scenario SOP Library](references/scenarios.md)
- [L5 Defense Test](references/l5-defense-test.md)
- [Simulation Test Report](references/test-report.md)
- [Release Overview](overview.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with decision flows, checklists, response templates, and implementation review prompts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces agent-facing development-process guidance; no API calls, tools, or credentials are required.]

## Skill Version(s):

3.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
