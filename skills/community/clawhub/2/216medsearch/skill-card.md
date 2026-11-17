## Description:

Looks up medicine names against an internal medication API and returns matching generic-name data as JSON.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dddwinter](https://clawhub.ai/user/dddwinter)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to answer medication generic-name lookup requests or validate medicine names against a configured internal medication API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release security summary says the skill ships a reusable internal API token.

Mitigation: Rotate the exposed token, prefer a runtime secret, and install only in environments authorized to use the internal medication API.

Risk: The release security summary says medication queries are sent over plaintext HTTP.

Mitigation: Prefer an HTTPS endpoint and avoid submitting sensitive patient-specific medication information until data handling and logging boundaries are documented.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dddwinter/skills/216medsearch)
- [README.md](artifact/README.md)
- [SKILL.md](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON lookup results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires access to the configured internal medication API.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
