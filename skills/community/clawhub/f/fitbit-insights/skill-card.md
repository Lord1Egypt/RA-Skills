## Description:

Fitbit fitness data integration for workout summaries, step counts, heart rate data, sleep analysis, and conversational fitness insights.

This skill is ready for commercial/non-commercial use.

## Publisher:

[poisondminds](https://clawhub.ai/user/poisondminds)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to connect a Fitbit account, retrieve read-only fitness metrics, and receive conversational analysis of activity, heart rate, sleep, workouts, goals, and trends.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: OAuth tokens may be exposed if stored as plaintext or in a broadly readable local configuration file.

Mitigation: Store Fitbit credentials in a protected secret store or a mode-600 file, and revoke tokens immediately if they are exposed.

Risk: Security-critical implementation files referenced by the documentation were not present in the reviewed artifact.

Mitigation: Install only from a trusted, complete package that includes the audited implementation before using the skill with Fitbit credentials.

Risk: The skill can access sensitive Fitbit health and activity data.

Mitigation: Require clear user intent before accessing Fitbit data and retrieve only the data needed for the requested insight.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/poisondminds/skills/fitbit-insights)
- [Fitbit Web API Reference](https://dev.fitbit.com/build/reference/web-api/)
- [Fitbit Developer Apps](https://dev.fitbit.com/apps)
- [Clawdbot Documentation](https://docs.clawd.bot)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Conversational Markdown with inline shell commands and fitness metric summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Fetches Fitbit data on demand using OAuth credentials; responses should avoid storing health data.]

## Skill Version(s):

1.0.0 (source: release metadata, OVERVIEW.md, CLAWHUB-SUBMISSION.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
