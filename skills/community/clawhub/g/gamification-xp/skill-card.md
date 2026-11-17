## Description:

Gamification & XP System provides an XP system for productivity gamification via ClawdBot, including levels, badges, streaks, achievements, and leaderboard progress.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chipagosfinest](https://clawhub.ai/user/chipagosfinest)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to let ClawdBot track productivity XP, levels, badges, streaks, achievements, and leaderboard status through a Supabase-backed gamification API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to provide a highly privileged Supabase service-role key in the agent environment.

Mitigation: Prefer a version that keeps the service-role key only in the backend service, and review the install requirements before use.

Risk: Leaderboard participation and visibility may expose multi-user progress data without clear authorization rules.

Mitigation: Confirm leaderboard participation, visibility, and authorization rules before enabling multi-user use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chipagosfinest/skills/gamification-xp)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration, Guidance]

**Output Format:** [Markdown guidance with API endpoint examples and JSON request/response snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SUPABASE_URL and SUPABASE_SERVICE_KEY environment variables and Supabase tables for gamification data.]

## Skill Version(s):

1.1.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
