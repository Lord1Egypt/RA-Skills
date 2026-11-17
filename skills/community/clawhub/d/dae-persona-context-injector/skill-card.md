## Description:

Builds a reusable persona profile for AI agents through structured dialogue before planning, writing, coding, research, or advisory work.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sirsws](https://clawhub.ai/user/sirsws)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to elicit operator context and generate a reusable PersonaProfile that downstream agents can read before doing substantive work. It is useful when generic agent output needs to be grounded in a user's goals, constraints, trade-offs, decision style, and evidence-backed profile.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persona profiles can contain sensitive personal context if users share private goals, constraints, decisions, or life details.

Mitigation: Treat generated profiles as private local configuration assets, skip questions the user does not want recorded, redact unnecessary details, and only share profiles with trusted downstream agents.

Risk: The optional npx installation command is unpinned.

Mitigation: Install through the reviewed ClawHub/OpenClaw listing when available, or verify the source and use pinned revisions before running command-line installation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sirsws/skills/dae-persona-context-injector)
- [DaE Skill Prompt](references/DaE_Skill_Prompt_en.md)
- [DaE v2 Acceptance Criteria](references/DaE_v2_acceptance_criteria_en.md)
- [Skill-declared GitHub repository](https://github.com/sirsws/dae-persona-context-injector)
- [SSRN research paper](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5961054)
- [Benchmark write-up](https://github.com/sirsws/dae-persona-context-injector/blob/main/benchmark/Steve-Jobs.md)
- [Benchmark profile](https://github.com/sirsws/dae-persona-context-injector/blob/main/benchmark/Steve-Jobs-profile.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Guidance]

**Output Format:** [Markdown profile brief and long-form PersonaProfile, with JSON only when explicitly requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Major judgments should include evidence, confidence, and status; skipped or insufficient data should be marked rather than guessed.]

## Skill Version(s):

1.0.3 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
