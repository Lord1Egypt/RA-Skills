## Description:

Part of the Overpowered skill suite, gear-up helps an agent create and activate the smallest temporary capability needed to close a real execution gap, measure whether it helped, and discard or nominate it for reuse.

This skill is ready for commercial/non-commercial use.

## Publisher:

[raguets](https://clawhub.ai/user/raguets)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill when an objective exposes a material, operational capability gap that current skills, tools, context, retrieval, or Academy candidates cannot reliably close. It guides the agent to choose the smallest temporary context, skill, tool, or composite artifact, validate it before use, measure its task value, and discard it or record it for later evaluation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated tools, skills, or context fragments could introduce unsafe side effects or misleading task guidance if used without review.

Mitigation: Review generated artifacts before they run on sensitive data or perform side effects, then validate syntax, dependencies, permissions, and narrow task behavior before activation.

Risk: A runtime may not support hot activation of generated capabilities, causing an agent to overstate what is available.

Mitigation: Require explicit runtime confirmation before calling an artifact active; otherwise report it as staged and ask for the smallest reload or session action needed.

Risk: Speculative capability generation can create unnecessary artifacts and broaden maintenance or review burden.

Mitigation: Apply the capability-gap gate, prefer existing skills and tools first, and create at most the smallest artifact that has an observable before-and-after value test.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/raguets/skills/gear-up)
- [Overpowered Suite](https://github.com/raguets/overpowered)
- [Academy Handoff](references/academy-handoff.md)
- [Artifact Selection](references/artifact-selection.md)
- [Capability Gap Gate](references/capability-gap-gate.md)
- [Runtime Adapter Contract](references/runtime-contract.md)
- [Runtime Manifest Example](references/runtime-manifest.example.yaml)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with optional code, shell command, YAML manifest, and configuration snippets.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce task-scoped temporary capability artifacts and validation or Academy handoff records when justified; generated executable behavior is untrusted until reviewed.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
