## Description:

Guides agents through main-sub delegation for substantial work with bounded roles, evidence checks, and independent review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mfang0126](https://clawhub.ai/user/mfang0126)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use this skill to decide when to keep work in the main thread versus orchestrate bounded explorer, researcher, worker, tester, and reviewer roles. It is intended for multi-component, cross-cutting, risky, or context-heavy work where decomposition and independent review add value.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing with an unpinned npx command can expose users to supply-chain changes outside the reviewed artifact.

Mitigation: Install only from trusted sources and pin or review the resolved package before use.

Risk: Orchestrated subagent workflows can materially increase token or API cost compared with simple main-thread work.

Mitigation: Use the skill for bounded, verifiable work where decomposition is justified, and avoid it for simple questions or small edits.

Risk: Delegating sensitive or high-impact actions without explicit approval can exceed the user's intended authority boundary.

Mitigation: Require explicit approval for sensitive actions and keep the main agent responsible for authorization, final inspection, and user-facing claims.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mfang0126/skills/crew-contract)
- [Child brief template](references/child-brief-template.md)
- [Class playbook](references/class-playbook.md)
- [Evidence index](references/evidence-index.md)
- [Hermes mechanics](references/hermes-mechanics.md)
- [Google agent-scaling study](https://research.google/blog/towards-a-science-of-scaling-agent-systems-when-and-why-agent-systems-work/)
- [Anthropic multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system)
- [MAST multi-agent failure study](https://arxiv.org/abs/2503.13657)
- [Cognition multi-agent systems](https://cognition.ai/blog/multi-agents-working)
- [Weaver verification study](https://arxiv.org/abs/2506.18203)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration instructions]

**Output Format:** [Markdown guidance with templates, checklists, and inline command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs route-card guidance, role briefs, review expectations, risk notes, and bounded workflow instructions for an agent to apply.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
