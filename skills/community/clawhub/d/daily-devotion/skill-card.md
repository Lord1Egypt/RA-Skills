## Description:

Creates personalized daily devotions with verse of the day, pastoral message, structured prayer, and time-aware greetings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[enjuguna](https://clawhub.ai/user/enjuguna)

### License/Terms of Use:


## Use Case:

External users invoke this skill to receive a Christian daily devotion that combines a current verse, pastoral reflection, structured prayer, and time-aware encouragement. Users may include prayer context in the initial prompt for a more personalized prayer.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The artifact asks users to run unpinned npm or npx code that was not included in the reviewed artifact.

Mitigation: Review the npm package source and pin exact versions before using the install or npx commands.

Risk: Users may share sensitive prayer details while personalizing the devotion.

Mitigation: Avoid sharing sensitive prayer details unless necessary; use general prayer context when possible.

Risk: The helper package is not required for the main devotional output.

Mitigation: If only the devotion is needed, have the agent fetch the documented OurManna URL directly instead of running helper commands.

## Reference(s):

- [OurManna Daily Verse API](https://beta.ourmanna.com/api/v1/get?format=json&order=daily)
- [OurManna](http://www.ourmanna.com/)
- [ClawHub Daily Devotion Skill Page](https://clawhub.ai/enjuguna/skills/daily-devotion)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown devotional text with scripture, pastoral reflection, structured prayer, and time-aware greeting.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call the OurManna API for the verse of the day; helper installation or npx commands are documented but should be reviewed before execution.]

## Skill Version(s):

1.1.1 (source: release metadata; artifact frontmatter says 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
