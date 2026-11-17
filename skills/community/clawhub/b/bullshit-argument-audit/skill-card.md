## Description:

Audit text, transcripts, audio, or video for bogus proof tactics, handwaving, bad citations, and weak argument moves.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stanestane](https://clawhub.ai/user/stanestane)

### License/Terms of Use:

MIT-0

## Use Case:

External users and reviewers use this skill to audit argumentative material for unsupported claims, citation theater, semantic drift, evidence inflation, and other fake proof moves. It is suited to text, transcripts, audio, video, and mixed-media arguments when the relevant content can be inspected or transcribed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can produce blunt critiques of arguments, which may be mistaken for a determination that a claim is false rather than unsupported or overclaimed.

Mitigation: Use the skill's calibration rule to separate absence of proof from falsity and label issues as unsupported, contradicted, ambiguous, or overclaimed.

Risk: Audio, video, or citation-heavy material may be audited incompletely when transcripts or references are unavailable.

Mitigation: Provide transcripts, timestamps, and inspectable references when possible; otherwise state that the audit is limited to visible, on-screen, or user-provided context.

## Reference(s):

- [Korpi Proof Technique Map](references/korpi-proof-technique-map.md)
- [Korpi's World: 63 Methods of Mathematical Proof](https://www.korpisworld.com/Mathematics/math%20leftovers/methods_of_mathematical_proof.htm)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown argument audit with verdict, findings, claim map, and repair plan]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include short quotes, paraphrased locations, timestamps when available, severity ratings, and concrete repair steps.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
