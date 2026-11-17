## Description:

Fetches and displays Duolingo learning stats including streak, XP, league, level, course progress, and daily or weekly summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[elmoorish](https://clawhub.ai/user/elmoorish)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to retrieve and summarize a Duolingo learner's public or authenticated progress, including streak status, XP totals, league placement, course progress, and recent activity.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional DUOLINGO_JWT token can grant access to authenticated Duolingo account data if exposed.

Mitigation: Prefer username-only public stats when sufficient, and never paste, log, or store the JWT in shared shell profiles.

Risk: The skill uses unofficial Duolingo endpoints that may change or enforce rate limits.

Mitigation: Handle 401 and 429 responses explicitly, ask the user to refresh expired tokens, and retry rate-limited requests after a delay.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/elmoorish/skills/duolingo-tracker)
- [Publisher Profile](https://clawhub.ai/user/elmoorish)
- [Duolingo API Base Endpoint](https://www.duolingo.com/2017-06-30)
- [Duolingo Public User Endpoint](https://www.duolingo.com/users/USERNAME)
- [Duolingo Leaderboard Endpoint](https://duolingo-leaderboards-prod.duolingo.com/leaderboards/7d9f5dd1-8423-491a-91f2-2532052038d8/users/USER_ID?get_users_only=true)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, API Calls, Guidance]

**Output Format:** [Markdown summary with optional inline shell commands and compact text charts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use username-only public data or an optional DUOLINGO_JWT bearer token for richer authenticated stats.]

## Skill Version(s):

0.1.0 (source: server release metadata; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
