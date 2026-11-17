## Description:

Coaching supports session preparation, question generation, client progress tracking, goal setting, and between-session momentum while emphasizing local-only client confidentiality.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agistack](https://clawhub.ai/user/agistack)

### License/Terms of Use:

MIT-0

## Use Case:

Coaches and coaching-support agents use this skill to prepare for client sessions, generate coaching questions, track client goals and commitments, and maintain momentum between sessions from local client records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Confidential client records are handled locally, and the security evidence reports weak path scoping that can expose other local JSON data.

Mitigation: Validate client identifiers, enforce path containment under the coaching directory, and limit file access to the minimum coaching records needed before use with real client information.

Risk: The skill makes strong confidentiality claims while the security guidance says confidentiality and retention limits need to be made concrete.

Mitigation: Document confidentiality boundaries, retention expectations, and deletion procedures before storing or processing client records.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with coaching summaries, question lists, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use local JSON client records in the coaching memory directory.]

## Skill Version(s):

2.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
