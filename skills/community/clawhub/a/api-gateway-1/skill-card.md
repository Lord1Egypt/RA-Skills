## Description:

Connects agents to 100+ third-party APIs through Maton's managed OAuth gateway.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kdegeek](https://clawhub.ai/user/kdegeek)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use this skill to create OAuth-backed service connections and make native API calls to connected business applications such as Google Workspace, Microsoft 365, Notion, Slack, Airtable, and HubSpot.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can enable broad read, write, and delete actions across connected business applications.

Mitigation: Install only when the operator trusts Maton and grants narrowly scoped OAuth access for services the agent actually needs.

Risk: Authorized connections may include high-impact admin, financial, messaging, or publishing capabilities.

Mitigation: Require human confirmation before deletes, sends, refunds, permission changes, public posts, or other high-impact actions.

Risk: Unsafe troubleshooting or logging could expose MATON_API_KEY.

Mitigation: Do not print, paste, store, or log MATON_API_KEY, and redact it from command output and diagnostics.

## Reference(s):

- [Maton](https://maton.ai)
- [Maton API Reference](https://www.maton.ai/docs/api-reference)
- [ClawHub Skill Page](https://clawhub.ai/kdegeek/skills/api-gateway-1)
- [Provider Routing References](references/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with API examples, shell commands, and JSON response shapes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires network access, a MATON_API_KEY, and user-authorized OAuth connections for each target service.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
