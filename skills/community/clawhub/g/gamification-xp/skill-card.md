## Description: <br>
XP system for productivity gamification via ClawdBot - track levels, badges, streaks, and achievements. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Chipagosfinest](https://clawhub.ai/user/Chipagosfinest) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Users and productivity teams use this skill through ClawdBot to check XP, levels, badges, streaks, leaderboard position, and recent gamification progress. Operators configure Supabase-backed gamification data so task, habit, and goal milestones can award XP and achievements. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The ClawdBot backend handles a sensitive Supabase service role key. <br>
Mitigation: Install only if the ClawdBot backend is trusted; use a dedicated Supabase project or tightly separated database and avoid reusing the service key for unrelated private tables. <br>
Risk: Leaderboard participation may expose user XP, ranks, streaks, or achievement history to other users. <br>
Mitigation: Confirm the leaderboard visibility model and participant expectations before enabling multi-user gamification. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Chipagosfinest/gamification-xp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance, API endpoint guidance] <br>
**Output Format:** [Markdown guidance with API endpoint examples and JSON payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SUPABASE_URL and SUPABASE_SERVICE_KEY for the ClawdBot backend integration.] <br>

## Skill Version(s): <br>
1.1.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
