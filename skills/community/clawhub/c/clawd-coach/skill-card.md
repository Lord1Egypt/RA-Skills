## Description:

Create personalized triathlon, marathon, and ultra-endurance training plans using Strava-synced training history or manually provided fitness data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shiv19](https://clawhub.ai/user/shiv19)

### License/Terms of Use:


## Use Case:

External athletes and coaches use this skill to assess current fitness, validate constraints and goals, and generate endurance training plans with periodization, workouts, zones, and race-day strategy.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Strava Client Secrets and OAuth redirect URLs can expose account access if pasted into shared or retained chat contexts.

Mitigation: Use a trusted local authorization flow, avoid sharing secrets or redirect URLs in chat, and revoke or rotate tokens if exposed.

Risk: Unpinned npx claude-coach commands may execute package code that the installer has not independently reviewed.

Mitigation: Pin and audit the package version before running commands, and run it only in an environment where the user is comfortable storing training data.

Risk: Strava sync may store up to two years of private activity history and tokens locally.

Mitigation: Confirm the storage location, deletion process, and token revocation path before syncing personal fitness data.

Risk: Training, testing, caffeine, hydration, and nutrition guidance may be inappropriate for some athletes or medical situations.

Mitigation: Treat recommendations as general coaching ranges, validate assessment details with the athlete, and seek qualified medical guidance for injuries or health concerns.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shiv19/skills/clawd-coach)
- [Athlete assessment guide](reference/assessment.md)
- [Training load management](reference/load-management.md)
- [Periodization and progressive overload](reference/periodization.md)
- [SQL queries for athlete assessment](reference/queries.md)
- [Race execution and nutrition strategy](reference/race-day.md)
- [Sport-specific workout library](reference/workouts.md)
- [Training zones and field testing](reference/zones.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with inline shell commands plus structured JSON training plans and HTML render instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use Strava authorization, local activity data, SQL queries, and manually entered fitness details when the user provides them.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
