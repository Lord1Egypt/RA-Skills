## Description:

Give independent Codex agents the same substantial task, compare their solutions against a clear rubric, and deliver one verified result.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yagel-yosef](https://clawhub.ai/user/yagel-yosef)

### License/Terms of Use:

MIT-0

## Use Case:

Codex users and developers use Arena to compare independent approaches to a substantial task, integrate the strongest result, and verify the final deliverable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Invoking Arena can replace its instructions and run new upstream shell code with the agent's existing permissions.

Mitigation: Disable automatic updates or use a Git installation pinned to a reviewed commit before invoking the skill.

Risk: On ClawHub installations, an update can overwrite local edits to the skill's three managed files.

Mitigation: Back up or avoid local edits to those files before updates; review update changes before relying on them.

## Reference(s):

- [Arena project homepage](https://github.com/yagel-yosef/arena-skill)
- [Arena on ClawHub](https://clawhub.ai/yagel-yosef/skills/arena)

## Skill Output:

**Output Type(s):** [Guidance, Analysis, Code, Files, Shell commands]

**Output Format:** [Markdown synthesis with verification findings and, when applicable, code or file changes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [One integrated result selected from independent attempts]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
