## Description:

Plans an optimized multi-stop errand route with distance and travel-time estimates, opening-hours windows, dwell time, ETAs, wait time, and closing-time violation flags.

This skill is ready for commercial/non-commercial use.

## Publisher:

[voronindenis5](https://clawhub.ai/user/voronindenis5)

### License/Terms of Use:

MIT-0

## Use Case:

People planning local errands use this skill to choose a stop order, estimate arrival and departure times, and check whether time-window constraints such as store closing times can be met. It is intended for small personal or operational multi-stop routes, not live turn-by-turn navigation or fleet optimization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Errand inputs may contain private location details.

Mitigation: Review input JSON or stop details before running the skill, and avoid sharing sensitive locations unnecessarily.

Risk: Route timing is approximate because the bundled planner does not use live traffic, road closures, one-way streets, or parking conditions.

Mitigation: Keep schedule buffer for important stops and verify the final route with an appropriate navigation tool before traveling.

## Reference(s):

- [Errand Routing Model & Math Reference](references/routing-model.md)
- [ClawHub Skill Page](https://clawhub.ai/voronindenis5/skills/errand-router)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, guidance]

**Output Format:** [Markdown guidance with CLI examples and optional JSON itinerary output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces ordered stops, leg distances, drive time, wait time, dwell time, ETAs, totals, and closing-time violation flags.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
