## Description:

Activate when user asks how to discuss product/strategy questions, requests analysis of unfamiliar markets, or when sparse documentation might tempt extrapolation. Provides 8 principles for grounded epistemic discussion with AI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tatsuko-tsukimi](https://clawhub.ai/user/tatsuko-tsukimi)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to keep AI-assisted product, strategy, research, and technical critique discussions grounded in current evidence. It helps agents verify current-state and market-gap claims, avoid extrapolating from sparse documentation, give clearer judgments, and keep critique aligned to the right abstraction layer.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can trigger broadly in strategy or research conversations and may change the assistant's default response posture.

Mitigation: Use it where current claims, market-gap assertions, sparse documents, or critique quality are important, and follow the artifact guidance to defer when the user explicitly asks for another approach.

Risk: The skill encourages live searches before claims about what exists now, which can add latency or require network-capable tooling.

Mitigation: Apply live research to current-state or high-impact external-world claims, then keep the resulting epistemic note concise and source-grounded.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tatsuko-tsukimi/skills/epistemic-hygiene)
- [Epistemic Hygiene principles](references/principles.md)
- [Trigger patterns](references/triggers.md)
- [Anti-patterns catalog](references/anti-patterns-catalog.md)
- [Research before assertion example](examples/research-before-assertion.md)
- [Sparse evidence example](examples/sparse-evidence.md)
- [Market-gap verification example](examples/market-claim-verification.md)

## Skill Output:

**Output Type(s):** [guidance, text, markdown]

**Output Format:** [Conversational text or Markdown with brief epistemic notes when needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include sourced current-state claims, documented-versus-inferred distinctions, and concise uncertainty notes; does not produce structured files by default.]

## Skill Version(s):

0.1.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
