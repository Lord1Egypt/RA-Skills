## Description:

Work in your own signed-in Chrome through BrowserPair OAuth MCP, with user-controlled site and browser permissions. Activate when asked to research or operate in a connected Chrome profile.

This skill is ready for commercial/non-commercial use.

## Publisher:

[browserpair-dev](https://clawhub.ai/user/browserpair-dev)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can connect a separately authorized Chrome profile to research websites or complete browser tasks. The agent follows the active tool schema, site permissions, and human confirmations, then checks outcomes against observed browser evidence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A connected signed-in browser can access or change information on websites within its approved permissions.

Mitigation: Approve only intended browsers and sites, honor confirmation prompts and sensitive-field masking, and verify outcomes using observed browser state.

## Reference(s):

- [BrowserPair connection documentation](https://docs.browserpair.com/connect-ai-app)
- [BrowserPair security](https://browserpair.com/security)
- [BrowserPair privacy](https://browserpair.com/privacy)

## Skill Output:

**Output Type(s):** [Text, Guidance, Browser task results, Shell commands, Configuration instructions]

**Output Format:** [Text responses and observed browser task results; setup guidance in Markdown with inline shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Report task findings based on observed browser evidence.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
