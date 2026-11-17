## Description:

Establish and use architectural guardrails for AI-assisted coding to prevent architecture collapse, feature regression, and drift across long multi-turn iterations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hgvgfgvh](https://clawhub.ai/user/hgvgfgvh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to establish repository guardrails for AI-assisted coding, including design-intent docs, architecture acceptance rules, automated constraints, and golden-rule review loops.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may propose or update architecture guardrail documents and tests in a repository.

Mitigation: Keep documentation and test changes scoped to the project, and review them before adopting them as constraints.

Risk: Overbroad architecture rules can freeze reasonable design evolution or encode incorrect assumptions.

Mitigation: Start with a minimal guardrail set, preserve human-maintained design intent, and classify uncertain drift for human decision.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hgvgfgvh/skills/ai-architecture-harness-en)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with optional code and shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update project documentation and tests when the user asks to apply guardrails.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
