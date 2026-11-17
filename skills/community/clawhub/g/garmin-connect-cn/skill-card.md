## Description:

Queries Garmin Connect China account data for health metrics including steps, distance, calories, sleep, heart rate, and recent activities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tcyxk](https://clawhub.ai/user/tcyxk)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to retrieve Garmin Connect China wellness and activity data for a requested date or recent activity window. It supports conversational questions about steps, sleep, heart rate, calories, distance, floors, and workouts.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: The skill requires a live Garmin bearer token that can access private account and health data.

Mitigation: Use a limited, current token only in trusted environments, avoid sharing it, and rotate or revoke it when exposure is suspected.

Risk: Passing the token as a command-line argument may expose it through shell history or process listings.

Mitigation: Prefer a reviewed configuration that reads the token from a safer secret source instead of command-line arguments.

Risk: The activity script includes a default user ID and documentation includes sample personal data.

Mitigation: Remove sample personal data and require the authenticated user ID to be resolved before querying account-specific endpoints.

## Reference(s):

- [Garmin Connect China](https://connect.garmin.cn)
- [Garmin Connect API Documentation](references/api.md)
- [Garmin Connect Skill Setup Guide](references/setup.md)
- [ClawHub Skill Page](https://clawhub.ai/tcyxk/skills/garmin-connect-cn)
- [Publisher Profile](https://clawhub.ai/user/tcyxk)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text command output with human-readable metrics]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Garmin Connect China JWT bearer token and optional date, user ID, or activity limit arguments.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
