## Description:

Helps deconditioned desk workers assess their mobility and strength, rebuild posture, restore movement, and progress through no-gym fitness routines for less pain and better functional capacity.

This skill is ready for commercial/non-commercial use.

## Publisher:

[howtousehumans](https://clawhub.ai/user/howtousehumans)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to guide desk workers through a starting assessment, phased mobility and strength routines, walking plans, posture resets, reminders, and progress checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review reports broad filesystem access without an explained file-use need.

Mitigation: Install only with least-privilege permissions; deny filesystem access unless the publisher documents a specific need.

Risk: The security review reports an unpinned npx install command.

Mitigation: Pin the installer or package version and verify the release before installation.

Risk: Calendar reminders can reveal or infer desk-work patterns if configured too broadly.

Mitigation: Grant only calendar access when needed and configure reminder timing explicitly.

Risk: Fitness guidance can be inappropriate for users with worsening pain, injuries, or medical constraints.

Mitigation: Follow the skill's instruction to seek medical or physical-therapy assessment when pain persists or worsens, and avoid heavy lifting, running, or high-impact exercise for deconditioned users.

## Reference(s):

- [Physical Activity Guidelines for Americans](https://health.gov/our-work/nutrition-physical-activity/physical-activity-guidelines)
- [NIH National Institute on Aging: Exercise and Physical Activity](https://www.nia.nih.gov/health/exercise-and-physical-activity)
- [Cochrane Library](https://www.cochranelibrary.com)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, configuration]

**Output Format:** [Markdown guidance with checklists, phased routines, reminder prompts, and YAML-like state snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use calendar reminders and agent state for workout scheduling, phase progression, posture resets, and progress tracking.]

## Skill Version(s):

1.0.0 (source: server release evidence and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
