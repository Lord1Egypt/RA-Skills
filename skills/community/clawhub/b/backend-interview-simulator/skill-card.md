## Description:

Simulates backend engineering interviews covering system design, API design, databases, concurrency, scaling, backend-focused coding, and backend behavioral practice.

This skill is ready for commercial/non-commercial use.

## Publisher:

[phantue2002](https://clawhub.ai/user/phantue2002)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and backend engineering candidates use this skill to run mock backend interviews, practice system and API design, solve backend-focused coding problems, and receive structured feedback. It can also tailor practice from a user-provided CV without storing the raw CV text.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may read user-provided CV files and store summarized profile details locally.

Mitigation: Provide only CV files intended for interview preparation and review or remove local profile data under ~/.openclaw/backend-interview-simulator when it is no longer needed.

Risk: Broad backend phrases such as "system design" can activate interview practice behavior.

Mitigation: Use clear prompts when working outside backend interview preparation, or disable the skill in contexts where interview simulation is not desired.

Risk: Interview scores and technical feedback are coaching guidance rather than a hiring decision or authoritative assessment.

Mitigation: Treat scores as practice feedback and review important technical recommendations before relying on them.

## Reference(s):

- [Backend Interview Simulator reference](reference.md)
- [ClawHub skill page](https://clawhub.ai/phantue2002/skills/backend-interview-simulator)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown text with code blocks, scoring rubrics, interview prompts, and structured feedback]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write local profile, history, weak-area, and saved-answer JSON files under ~/.openclaw/backend-interview-simulator.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
