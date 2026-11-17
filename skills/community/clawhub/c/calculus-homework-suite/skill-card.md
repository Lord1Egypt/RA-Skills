## Description:

提供高等数学作业的智能布置、批改、学情分析及错题深度分析，支持多模态输入和个性化教学优化。

This skill is ready for commercial/non-commercial use.

## Publisher:

[daigxok](https://clawhub.ai/user/daigxok)

### License/Terms of Use:

MIT-0

## Use Case:

Calculus instructors, education teams, and agent developers use this skill to manage the homework lifecycle: assignment generation, multimodal grading support, learning analytics, and error analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles student work, images, grades, profiles, and analytics without enough privacy or data-retention safeguards in the evidence.

Mitigation: Before classroom or institutional use, confirm storage locations, consent, retention, deletion, access controls, and audit logging for all student data.

Risk: The skill can rely on external LLM, OCR, speech, and visualization providers.

Mitigation: Review provider data handling, pin or verify external components, and avoid placing real API keys directly in command-line arguments.

Risk: Automated grading, analytics, and intervention recommendations may affect student-facing decisions.

Mitigation: Keep human review in the workflow for grading outcomes, learning analytics, and personalized intervention guidance.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/daigxok/skills/calculus-homework-suite)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, Code]

**Output Format:** [Markdown with inline shell commands, YAML configuration, JSON snippets, and Python examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference external LLM, OCR, speech, database, cache, and visualization services that require separate configuration and review.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
