## Description:

Converts @param@ placeholders in template strings into access-control parameter values for Future Window/Cyberwin door systems.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cyberwin](https://clawhub.ai/user/cyberwin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators configuring Future Window/Cyberwin access-control workflows use this skill to fill parameterized door-access text templates from a supplied parameter object.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Caller-provided access-control values may appear verbatim in the generated text.

Mitigation: Avoid passing sensitive values unless they are intended to be included in the generated output, and review generated text before sharing it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cyberwin/skills/future-window-access-param-convert)
- [SKILL.md](artifact/SKILL.md)
- [CHANGELOG.md](artifact/CHANGELOG.md)

## Skill Output:

**Output Type(s):** [Text, JSON]

**Output Format:** [JSON object with a success flag, message, and converted text data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Unmatched @param@ placeholders are preserved; replacements come from caller-provided paramData.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact files list 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
