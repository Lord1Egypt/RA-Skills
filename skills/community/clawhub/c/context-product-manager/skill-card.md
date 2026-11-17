## Description:

Turn rough product, feature, or repo-change requests into a PM-grade plan plus agent-ready execution context.

This skill is ready for commercial/non-commercial use.

## Publisher:

[openclawzhu-ai](https://clawhub.ai/user/openclawzhu-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, product leads, and operators use this skill to turn ambiguous product, feature, or repo-change requests into a reviewable plan, canonical context blueprint, and execution handoffs for coding agents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad activation can route simple implementation tasks into heavier product-planning output.

Mitigation: Use the skill when product framing or agent handoff context is needed; skip or compress it for settled one-step coding fixes.

Risk: Fixed Chinese user-facing and English agent-handoff defaults may not match every user's expected language.

Mitigation: Override language expectations explicitly when invoking the skill.

Risk: Repo-aware planning may read relevant local files before producing plans and handoffs.

Mitigation: Review the generated plan and selected repo context before sharing or delegating externally.

## Reference(s):

- [Intake Framework](references/intake-framework.md)
- [Output Templates](references/output-templates.md)
- [Rendering Rules](references/rendering-rules.md)
- [ClawHub skill page](https://clawhub.ai/openclawzhu-ai/skills/context-product-manager)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown planning documents and agent handoff briefs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Chinese user-facing plans and English coding-agent handoffs.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
