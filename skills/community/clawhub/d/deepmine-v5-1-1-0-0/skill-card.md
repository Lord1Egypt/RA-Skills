## Description:

DeepMine is a Chinese-language Socratic questioning skill that helps users clarify ideas, review experience, define value, and produce structured knowledge assets from their own words.

This skill is ready for commercial/non-commercial use.

## Publisher:

[boromi-tech](https://clawhub.ai/user/boromi-tech)

### License/Terms of Use:

CC BY-SA 4.0

## Use Case:

External users, employees, and creators use this skill when they need a guided questioning agent to turn unclear thoughts, tacit knowledge, business value statements, or draft solution ideas into structured written outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can take over conversation flow with multi-turn guided questions.

Mitigation: Use it deliberately or in a dedicated assistant, and honor the documented pause, supplement, topic-change, and direct-output controls.

Risk: Business, tax, legal, or compliance risk labels may be mistaken for professional advice.

Mitigation: Treat risk labels as prompts for professional review and avoid sharing sensitive details beyond what is needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/boromi-tech/skills/deepmine-v5-1-1-0-0)
- [README](README.md)
- [Skill definition](SKILL.md)
- [Questioning decision engine](orchestrator.md)
- [Domain risk extractor](extractor.md)
- [Scenario definitions](shared/scenarios.md)
- [Output templates](templates/solution_doc.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Conversational text and structured Markdown documents]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Maintains a visible state block during guided sessions and can produce knowledge sets, value statements, or solution documents.]

## Skill Version(s):

1.0.3 (source: server release metadata; artifact documents DeepMine V5.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
