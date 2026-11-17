## Description:

Recommends nearby Ele.me food delivery options based on a user's meal times, taste preferences, and location.

This skill is ready for commercial/non-commercial use.

## Publisher:

[du425](https://clawhub.ai/user/du425)

### License/Terms of Use:

MIT-0

## Use Case:

External users configure meal times, taste preferences, recommendation count, and location so an agent can fetch nearby Ele.me restaurants and return meal recommendations before breakfast, lunch, or dinner.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires an active Ele.me browser cookie and precise location data.

Mitigation: Use a limited test account where possible, avoid shared machines, do not paste real cookies into shell history, and clear or rotate the cookie after testing.

Risk: Network requests may expose sensitive account or location data if TLS verification and secret handling are not fixed.

Mitigation: Use only trusted networks, review the implementation before deployment, and require normal TLS verification and safer secret storage before routine use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/du425/skills/eleme-food-recommend)
- [Publisher profile](https://clawhub.ai/user/du425)
- [ClawHub metadata homepage](https://github.com/your-name/eleme-food-recommend)
- [Ele.me website](https://www.ele.me)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration, guidance]

**Output Format:** [JSON responses and command-line guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Recommendations depend on a valid Ele.me cookie, configured location, meal-time settings, and reachable Ele.me endpoints.]

## Skill Version(s):

1.0.0 (source: evidence release and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
