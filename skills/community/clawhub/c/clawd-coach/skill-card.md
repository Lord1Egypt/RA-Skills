## Description: <br>
Creates personalized triathlon, marathon, and ultra-endurance training plans from Strava-synced or manually provided fitness data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shiv19](https://clawhub.ai/user/shiv19) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External athletes use this skill to assess endurance fitness, set training zones, and generate structured race preparation plans. It supports triathlon, marathon, and ultra-endurance planning using either Strava activity history or manually supplied training context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Strava account linking asks users to provide sensitive OAuth material in chat, including a Client Secret or redirect URL. <br>
Mitigation: Prefer manual data entry or a safer OAuth flow when possible; if connecting Strava, avoid sharing secrets beyond setup and review local token and database storage before proceeding. <br>
Risk: Training, nutrition, caffeine, and field-test guidance can be inappropriate for some health conditions, medications, injuries, heat exposure, or limited training history. <br>
Mitigation: Treat outputs as coaching suggestions, validate zones and volume conservatively, and seek qualified medical or coaching advice for health-sensitive decisions. <br>
Risk: Plans based on incomplete manual data or stale activity history can overestimate current capacity. <br>
Mitigation: Validate the assessment with the athlete, confirm injuries and constraints, refresh Strava data when used, and start with conservative volume when uncertain. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/shiv19/clawd-coach) <br>
- [SQL Queries for Athlete Assessment](reference/queries.md) <br>
- [Athlete Assessment Guide](reference/assessment.md) <br>
- [Training Zones & Field Testing](reference/zones.md) <br>
- [Training Load Management](reference/load-management.md) <br>
- [Periodization & Progressive Overload](reference/periodization.md) <br>
- [Sport-Specific Workout Library](reference/workouts.md) <br>
- [Race Execution & Nutrition Strategy](reference/race-day.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands, structured JSON training plans, and HTML render instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local JSON and HTML plan files and may guide local Strava data sync through claude-coach commands.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
