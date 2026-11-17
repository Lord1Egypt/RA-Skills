## Description:

Tracks daily English study check-ins for TOEFL, IELTS, PET, New Concept, and other study types, with support for non-repeating English motivational quotes and Chinese translations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[daizongyu](https://clawhub.ai/user/daizongyu)

### License/Terms of Use:

MIT-0

## Use Case:

English learners and agents assisting them use this skill to initialize a daily study check-in workflow, record progress by study type, view status, and avoid repeating generated motivational quotes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can execute a local Python file supplied as its learning-checkin dependency path without integrity checks.

Mitigation: Install only trusted learning-checkin code, use a pinned and verified path, and avoid LEARNING_CHECKIN_PATH or --learning-checkin-path values from untrusted locations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/daizongyu/skills/english-learning-checkin)
- [learning-checkin dependency](https://clawhub.ai/daizongyu/learning-checkin)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [JSON command responses with human-facing status and guidance text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local data files for learning type and used-quote tracking; depends on a separately installed learning-checkin script.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact version text)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
