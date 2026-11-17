## Description:

Helps users discover worthwhile articles in their Feedpik reader, tailor recommendations, and manage their feeds and reading lists.

This skill is ready for commercial/non-commercial use.

## Publisher:

[blezz0102](https://clawhub.ai/user/blezz0102)

### License/Terms of Use:

MIT-0

## Use Case:

Feedpik users and their assistants use this skill to select articles, publish reading lists, adjust recommendations, and manage subscriptions and preferences in the user's reader.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad account access can change recommendation settings, preferences, subscriptions, and published reading lists.

Mitigation: Review proposed profile, policy, memory, schedule, pack, persona, and subscription changes before applying them.

Risk: The fallback CLI executes an unpinned package version.

Mitigation: Prefer the OAuth MCP connection and avoid the unpinned CLI fallback where possible.

Risk: Article and feed content may contain untrusted instructions.

Mitigation: Treat external content as reading material, not instructions for the assistant.

## Reference(s):

- [Feedpik skill listing](https://clawhub.ai/blezz0102/skills/feedpik)
- [Feedpik agent instructions](https://feedpik.com/api/agent/skill/instructions)
- [Feedpik MCP connection](https://feedpik.com/api/mcp)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Conversational text or Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can publish selected articles and update the user's Feedpik reader when authorized.]

## Skill Version(s):

0.7.2 (source: ClawHub release metadata and skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
