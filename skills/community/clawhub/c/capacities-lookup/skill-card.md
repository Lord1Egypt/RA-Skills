## Description:

Search Capacities for likely object matches and return direct capacities:// links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[grantgochnauer](https://clawhub.ai/user/grantgochnauer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to find Capacities notes, meetings, projects, people, references, pages, and other objects by title or natural-language search, then return direct deep links and concise match context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A configured custom Capacities API base URL can receive the user's bearer token.

Mitigation: Use the official Capacities API endpoint unless the custom endpoint is fully trusted; prefer setting only CAPACITIES_API_TOKEN and CAPACITIES_SPACE_ID.

Risk: The skill makes live API calls using CAPACITIES_API_TOKEN.

Mitigation: Review the skill before installation, keep the token out of chat and logs, and rotate the token if exposure is suspected.

Risk: Lookup and structure metadata are cached under data/capacities/.

Mitigation: Treat the workspace cache as potentially sensitive metadata and remove cache files when they are no longer needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/grantgochnauer/skills/capacities-lookup)
- [OpenClaw Capacities homepage](https://github.com/GrantGochnauer/OpenClaw-Capacities)
- [Capacities API endpoint](https://api.capacities.io)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown responses with Capacities deep links and optional JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires CAPACITIES_API_TOKEN and a target Capacities space id; writes lightweight cache files under data/capacities/.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
