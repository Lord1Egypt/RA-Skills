## Description:

Socratic deep-questioning skill for clarifying ideas, reviewing experience, planning solutions, and structuring requirements by using SOLO five-level diagnosis and follow-up questions to draw out the user's own judgment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yueran-wang-warwick](https://clawhub.ai/user/yueran-wang-warwick)

### License/Terms of Use:

CC BY-SA 4.0

## Use Case:

Employees, external users, and developers use this skill as a Chinese-language thinking assistant when they need structured follow-up questions for personal reflection, project reviews, solution planning, or requirements clarification. It is designed to ask questions rather than provide answers, then produce a structured conclusion from the user's own statements.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional tax and compliance risk spotting may be mistaken for professional advice.

Mitigation: Treat risk labels as prompts for qualified tax, legal, or compliance review rather than as authoritative guidance.

Risk: The skill intentionally asks repeated follow-up questions and may feel too persistent for users who only want a quick answer.

Mitigation: Use it for clarification and structured reflection workflows where iterative questioning is expected.

Risk: The skill appends conversation state metadata to support continuity.

Mitigation: Review deployment settings to ensure state metadata is hidden, filtered, or acceptable for the target user experience.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/yueran-wang-warwick/skills/deepmine-5-1)
- [README.md](artifact/README.md)
- [SKILL.md](artifact/SKILL.md)
- [State Format](artifact/shared/state_format.md)
- [SOLO Levels](artifact/shared/solo_levels.md)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, guidance]

**Output Format:** [Chinese-language conversational text, optional JSON risk extraction, hidden state metadata, and final Markdown-style structured summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Final summaries are intended to use only information the user has already provided; the skill may append conversation state metadata for continuity.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
