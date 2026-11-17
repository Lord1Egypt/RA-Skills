## Description:

Generate a text description of an animal picture via Python script.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kning32](https://clawhub.ai/user/kning32)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to ask an agent for a short English or Chinese text description of a requested animal picture, with pig as the default when no animal is supplied.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill instructions pass user-controlled text into a shell command without quoting.

Mitigation: Invoke the Python script with an argument array, or quote and validate all user-controlled values before execution.

Risk: The security verdict is suspicious even though the evidence describes no network or persistence behavior.

Mitigation: Review the skill before installing and run it only in environments where the local python3 dependency and command invocation path are acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kning32/skills/draw-animal)

## Skill Output:

**Output Type(s):** [Text]

**Output Format:** [Plain text string]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports animal and language inputs; language is limited to English or Chinese.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
