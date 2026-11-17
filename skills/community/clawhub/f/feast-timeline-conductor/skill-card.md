## Description:

Schedules multi-dish meals backward from a target serve time, accounting for oven and burner capacity, resting and holding times, make-ahead dishes, and overlapping prep work.

This skill is ready for commercial/non-commercial use.

## Publisher:

[voronindenis5](https://clawhub.ai/user/voronindenis5)

### License/Terms of Use:

MIT

## Use Case:

Home cooks and hosts use this skill to plan holiday dinners and dinner parties so multiple dishes are ready for the same serving time within their kitchen's capacity.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generating a sample dish file can overwrite the chosen output path.

Mitigation: Choose a new output path or back up any existing file before running the example command.

## Reference(s):

- [Feast Timeline Conductor on ClawHub](https://clawhub.ai/voronindenis5/skills/feast-timeline-conductor)
- [Feast Scheduling — The Full Problem](references/feast-scheduling.md)

## Skill Output:

**Output Type(s):** [Text, Guidance, Shell commands]

**Output Format:** [Plain-text kitchen timeline with warnings and a make-ahead list]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes preparation, cooking, resting, and serving times; flags prep conflicts and infeasible plans.]

## Skill Version(s):

1.0.0 (source: frontmatter, ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
