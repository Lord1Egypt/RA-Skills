## Description:

Guides agents to recommend aperture and shutter speed combinations based on desired depth of field, motion rendering, and exposure balance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bianchunhui](https://clawhub.ai/user/bianchunhui)

### License/Terms of Use:

MIT-0

## Use Case:

External photography learners and agents use this skill to choose aperture and shutter speed settings based on creative goals such as background blur, broad depth of field, freezing motion, or motion blur.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is mainly written in Chinese and may steer responses toward Chinese.

Mitigation: Preserve the user's language preference when applying the skill.

Risk: Photography parameter suggestions can be misleading if treated as fixed rules without scene context or metering.

Mitigation: Ask for the user's creative goal, depth-of-field needs, motion intent, and exposure context; present settings as starting points.

Risk: The skill may be confused with metering, ISO selection, or gear recommendation workflows.

Mitigation: Use this skill for aperture and shutter-speed tradeoffs, and route metering, ISO, and gear-selection questions to the appropriate guidance.

## Reference(s):

- [Server-resolved GitHub provenance](https://github.com/bianchunhui/nyip-photography-skills/tree/main/exposure-dual-control)
- [ClawHub skill page](https://clawhub.ai/bianchunhui/skills/exposure-dual-control)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown or plain text with aperture and shutter speed recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include concrete aperture and shutter speed pairings with a brief creative-effect rationale.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
