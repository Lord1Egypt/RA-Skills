## Description:

Automatically searches ClawHub for matching OpenClaw skills, presents results, and installs a user-confirmed choice when no local skill fits the request.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lpb123](https://clawhub.ai/user/lpb123)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to find a specialized ClawHub skill when installed skills are insufficient, review the match, and install it after confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A recommended third-party skill may not be the intended skill or publisher.

Mitigation: Before installing, check that the slug and publisher match the user's intent.

Risk: A newly installed third-party skill may contain instructions or bundled files the user has not reviewed.

Mitigation: Inspect the new SKILL.md and bundled files when possible before trusting or using the skill.

Risk: Immediate use in the same session can apply a newly installed skill before normal restart-time review.

Mitigation: Use immediate activation cautiously and only after reading the installed skill instructions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lpb123/skills/clawhub-skill-finder)
- [ClawHub publisher profile](https://clawhub.ai/user/lpb123)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes user-confirmation steps before installation.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
