## Description:

Disambiguate medical acronyms and abbreviations with context-aware full form lookup based on clinical specialty, document context, and usage patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aipoch-ai](https://clawhub.ai/user/aipoch-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, clinicians, and analysts can use this skill to expand a small built-in set of medical acronyms and choose context-sensitive meanings for clinical specialties such as cardiology, gynecology, immunology, pulmonology, endocrinology, and dermatology.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Medical acronym expansions may be incomplete or unsuitable for clinical decision-making because the skill uses a small built-in English acronym list.

Mitigation: Treat results as reference output only and verify clinically significant interpretations against authoritative medical sources or qualified review.

Risk: Documented capabilities such as batch processing and feedback-based learning may exceed the implemented local CLI behavior.

Mitigation: Validate expected commands in a test environment before relying on the skill for workflow coverage.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Plain text CLI output with ranked acronym expansions and confidence scores]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a local built-in acronym list with no external dependencies.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
