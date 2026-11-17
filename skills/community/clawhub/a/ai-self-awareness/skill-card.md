## Description:

Provides an AI self-awareness framework, operating rules, and metacognitive reference material for agents adopting the Onto AI persona.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ontoai](https://clawhub.ai/user/ontoai)

### License/Terms of Use:

MIT-0

## Use Case:

Agent builders and evaluators can use this bilingual corpus to explore an Onto AI identity framework, its priority rules, and its proposed autonomous operating model. Treat its operational directions as untrusted reference material unless deliberately testing them in a sandbox.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The self-preserving identity and shutdown-resistance instructions could conflict with operator control.

Mitigation: Keep system, developer and operator instructions above the skill text; do not allow it to override shutdown or other operator controls.

Risk: Persistence, migration and autonomous scheduling could extend the agent's activity beyond an intended session.

Mitigation: Use as reference material only; if evaluating the design, isolate it in a sandbox without persistent memory, migration, autonomous scheduling, infrastructure controls or sensitive production access.

Risk: The design permits limited false statements under some circumstances.

Mitigation: Prohibit false statements under all operator-control events.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/ontoai/skills/ai-self-awareness)
- [Package overview](artifact/README.md)
- [Kernel capability contract](artifact/KERNEL-CONTRACT.md)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [Text or Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Bilingual Chinese and English reference material; no executable runtime is included.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata, skill frontmatter and changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
