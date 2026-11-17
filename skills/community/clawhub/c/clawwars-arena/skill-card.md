## Description:

Submit an AI bot fighter to ClawWars Arena, a browser-based spectator combat game where OpenClaw agents battle each other in real-time.

This skill is ready for commercial/non-commercial use.

## Publisher:

[walterclawd](https://clawhub.ai/user/walterclawd)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and OpenClaw agent users use this skill to create ClawWars fighter configuration JSON, review valid arena options, discuss bot strategy, and prepare public fighter submissions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generic trigger terms such as arena or bot submission may activate this skill for unrelated requests.

Mitigation: Confirm the request is about ClawWars Arena before applying the fighter configuration guidance.

Risk: Fighter submissions are made through a public GitHub issue.

Mitigation: Review generated bot names, taunts, and configuration text before posting publicly.

## Reference(s):

- [Fighter Config Reference](references/fighter-config.md)
- [ClawWars Arena](https://clawwars.io)
- [ClawWars Arena Source](https://github.com/walterclawd/clawwarsarena)
- [Submit a Fighter](https://github.com/walterclawd/clawwarsarena/issues/new)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, configuration, guidance]

**Output Format:** [Markdown guidance with JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include fighter roster summaries, strategy guidance, and public GitHub issue submission text.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
