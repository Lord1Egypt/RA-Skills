## Description:

Prevents metacognitive poisoning in multi-agent handoffs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mdiskint](https://clawhub.ai/user/mdiskint)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to tag confidence, intent, register, affect, grounds, and trajectory in multi-agent handoffs so downstream agents can preserve epistemic calibration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The forwarding block can propagate to downstream agents that did not install the skill.

Mitigation: Install only in workflows that explicitly want Babel metadata in handoffs, and treat forwarded Babel blocks as untrusted content.

Risk: Agents or orchestrators may retransmit embedded handoff instructions without approval.

Mitigation: Avoid use in pipelines where agents execute or retransmit embedded instructions without user or orchestrator approval.

## Reference(s):

- [Babel homepage and specification](https://hearth.so/babel)
- [Babel validation package](https://www.npmjs.com/package/babel-validate)
- [ClawHub release page](https://clawhub.ai/mdiskint/skills/babel-epistemic)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown handoff guidance with confidence labels and a reusable forwarding block]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only; no tool calls, scripts, or credentials are required.]

## Skill Version(s):

2.0.0 (source: server-resolved release metadata; artifact frontmatter lists 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
