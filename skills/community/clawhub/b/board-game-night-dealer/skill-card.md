## Description:

Recommends board games for a group's player count, time budget, and complexity preference, with teaching guides and fair pick rotation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[voronindenis5](https://clawhub.ai/user/voronindenis5)

### License/Terms of Use:

MIT

## Use Case:

Game-night hosts, clubs, and other groups use this skill to choose games, prepare short teaching guides, and rotate who picks fairly.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Rotation records and recent picks are saved in a local game_night.json file.

Mitigation: Review the stored group information and remove the file when you no longer need the history.

Risk: A recommended game's play and teaching time may exceed the session budget.

Mitigation: Check the displayed play and teach times against the available time before committing to a pick.

## Reference(s):

- [Game Catalog and Selection Reference](artifact/references/game-catalog.md)
- [ClawHub skill listing](https://clawhub.ai/voronindenis5/skills/board-game-night-dealer)

## Skill Output:

**Output Type(s):** [Text, JSON]

**Output Format:** [Console text for recommendations and teaching guides; local JSON for rotation history]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Recommendations explain their fit; rotation and recent picks persist in game_night.json beside the script.]

## Skill Version(s):

1.0.0 (source: skill frontmatter and ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
