## Description:

行李清单 Pro generates personalized travel packing lists from destination, travel dates, trip purpose, companions, and FlyAI travel search results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hello-ahang](https://clawhub.ai/user/hello-ahang)

### License/Terms of Use:

MIT-0

## Use Case:

Travelers and travel-planning agents use this skill to collect trip details and produce categorized packing lists with must-bring items, recommended items, locally purchasable items, and destination-specific reminders.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks agents to install or upgrade a global npm package and suggests sudo when permissions fail.

Mitigation: Review commands before execution, avoid sudo and global installs where possible, and use a pinned, verified CLI version in an isolated environment.

Risk: The skill directs FlyAI commands to bypass TLS certificate validation.

Mitigation: Keep TLS validation enabled and resolve certificate or network issues instead of setting NODE_TLS_REJECT_UNAUTHORIZED=0.

Risk: The skill can read and update persistent travel profile data from memory or ~/.flyai/user-profile.md.

Mitigation: Make profile use opt-in, store only necessary preferences, and provide clear review and deletion controls before writing profile data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hello-ahang/skills/flyai-packing-list)
- [FlyAI tool reference](reference/tools.md)
- [POI and attraction search reference](reference/search-poi.md)
- [Keyword search reference](reference/keyword-search.md)
- [User profile storage reference](reference/user-profile-storage.md)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Markdown checklist with categorized sections and occasional inline shell commands for travel search]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May incorporate destination search results and saved travel preferences when available.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
