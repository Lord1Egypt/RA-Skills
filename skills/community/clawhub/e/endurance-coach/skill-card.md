## Description:

Create personalized triathlon, marathon, and ultra-endurance training plans using Strava or manually provided fitness data, including sport-specific workouts, training zones, periodization, and race-day strategy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shiv19](https://clawhub.ai/user/shiv19)

### License/Terms of Use:


## Use Case:

External athletes and coaches use this skill to assess training history, validate current constraints, and produce personalized endurance plans, post-workout reviews, and race-day guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can run a mutable npm CLI and sync Strava-derived training history.

Mitigation: Pin or vet the endurance-coach package before use, and require explicit user approval before authentication, sync, or CLI execution.

Risk: The skill can persist sensitive fitness, health-adjacent, life-context, and coaching notes locally.

Mitigation: Ask before saving or updating local athlete records, minimize stored details, and keep the user informed about what will be retained.

Risk: Coach notes and preliminary analysis may be stored separately from athlete-facing reflections.

Mitigation: Require opt-in before storing hidden coaching analysis and provide a user-reviewable summary of any notes that affect future coaching.

## Reference(s):

- [Endurance Coach ClawHub Skill Page](https://clawhub.ai/shiv19/skills/endurance-coach)
- [Athlete Assessment Guide](reference/assessment.md)
- [Training Load Management](reference/load-management.md)
- [Periodization & Progressive Overload](reference/periodization.md)
- [Athlete Assessment Commands](reference/queries.md)
- [Race Execution & Nutrition Strategy](reference/race-day.md)
- [Database Schema Reference](reference/schema.md)
- [Workout Templates Reference](reference/templates.md)
- [Workout Library](reference/workouts.md)
- [Training Zones & Field Testing](reference/zones.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with YAML v2.0 plan data, shell command examples, and HTML rendering steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local athlete context, workout interview summaries, coach notes, trigger settings, and rendered training-plan files when the user approves.]

## Skill Version(s):

1.4.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
