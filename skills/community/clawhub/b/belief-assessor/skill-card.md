## Description:

Belief Assessor evaluates claims against evidence and returns calibrated confidence with VERIFIED, CONTESTED, or UNCERTAIN belief states.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hqzzdsda](https://clawhub.ai/user/hqzzdsda)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to assess whether claims are trustworthy, identify contradictions, and express uncertainty before presenting conclusions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Private or sensitive claims may be sent to search or LLM providers during evidence gathering and assessment.

Mitigation: Review and redact confidential, legal, medical, financial, or business-sensitive text before using the skill.

Risk: Hostile evidence text or spoofed source URLs may influence the assessment.

Mitigation: Prefer trusted sources, inspect provenance, and treat confidence scores as advisory rather than authoritative.

Risk: Structured confidence outputs can be over-relied on for high-stakes decisions.

Mitigation: Use conservative settings for high-stakes claims and require human review before acting on results.

## Reference(s):

- [Belief Assessor on ClawHub](https://clawhub.ai/hqzzdsda/skills/belief-assessor)

## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [Markdown explanation with optional JSON assessment fields and Python snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include belief state, confidence, confidence range, feature judgments, veto reasons, and cap applied.]

## Skill Version(s):

2.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
