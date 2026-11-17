## Description:

A professional storyboard skill for film, advertising, short video, and educational narrative scenarios, built around a strict 'plan first, render later' flow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dlazyai](https://clawhub.ai/user/dlazyai)

### License/Terms of Use:

MIT-0

## Use Case:

Filmmakers, advertisers, short-video creators, and educators use it to turn creative briefs into a planned storyboard with character references, shot-by-shot prompts, and delivery guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scanner review was partial and did not establish what credentials the CLI accesses or how it uses them.

Mitigation: Review the CLI login and setup behavior before installing, and use a revocable dLazy API key.

Risk: Storyboard prompts and supplied local media are sent to dLazy-hosted services for generation.

Mitigation: Send only prompts and media that are appropriate to share with that service.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/dlazyai/skills/dlazy-image-storyboard)
- [dLazy CLI source reference](https://github.com/dlazy-ai/cli)
- [dLazy CLI on npm](https://www.npmjs.com/package/@dlazy/cli)
- [dLazy](https://dlazy.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown storyboard plans, character and shot prompts, with inline CLI commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include image-generation result URLs and print/PDF delivery guidance.]

## Skill Version(s):

1.3.43 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
