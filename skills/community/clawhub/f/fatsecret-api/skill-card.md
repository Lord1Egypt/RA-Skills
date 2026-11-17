## Description:

Search foods, look up nutrition, log meals, track weight, browse recipes, and manage exercises via the FatSecret API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivanvmoreno](https://clawhub.ai/user/ivanvmoreno)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to have an agent search FatSecret nutrition data, summarize food and recipe results, and manage diary, exercise, weight, saved meal, favorite, and profile records through the FatSecret API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires FatSecret API credentials and can send health-related nutrition, exercise, weight, diary, saved meal, favorite, and profile data to FatSecret.

Mitigation: Install only if FatSecret is trusted for this data and keep credentials in environment variables with least practical exposure.

Risk: Delegated operations can modify sensitive account and health records.

Mitigation: Prefer read-only operations by default and require explicit user confirmation before creating, editing, deleting, copying, or committing profile-scoped records.

Risk: The profile_get_auth operation can expose delegated authentication output.

Mitigation: Avoid invoking profile_get_auth unless necessary and do not display or persist authentication material beyond the immediate user-requested flow.

Risk: The skill depends on the pyfatsecret package for FatSecret API access.

Mitigation: Install pyfatsecret from a pinned and audited version before deployment.

## Reference(s):

- [ClawHub Fatsecret Skill](https://clawhub.ai/ivanvmoreno/skills/fatsecret-api)
- [FatSecret API Platform](https://platform.fatsecret.com/api/)
- [OpenClaw Skills Documentation](https://docs.openclaw.ai/tools/skills)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, JSON, API calls, Guidance]

**Output Format:** [Markdown summaries with inline shell commands and JSON API results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3, pyfatsecret, and FATSECRET_CLIENT_ID/FATSECRET_CLIENT_SECRET environment variables; account-changing operations should be confirmed by the user.]

## Skill Version(s):

1.0.1 (source: SKILL.md frontmatter and ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
