## Description:

Generate synchronized word-by-word animated captions and translated subtitles for video timelines.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brajendrak00068](https://clawhub.ai/user/brajendrak00068)

### License/Terms of Use:

MIT-0

## Use Case:

Video creators and editors use this skill to add synchronized word-level captions, style subtitles, and translate timeline captions through the Levea editing service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Source media is sent to Levea through publicly reachable URLs.

Mitigation: Use media you are comfortable sharing with Levea and review the service's data handling.

Risk: The Levea API key could be exposed if it is placed in an unintended location.

Mitigation: Keep the key in the intended plugin or MCP server configuration.

Risk: The separately installed plugin or MCP server implementation and service data handling were not included in this artifact review.

Mitigation: Review the plugin or MCP server and the service's data handling independently. Enable plan approval to review proposed edits before execution.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/brajendrak00068/skills/auto-captions-subtitles)
- [Levea editing service](https://livecore.ai/?openclaw=1&utm_source=clawhub&utm_medium=skill&utm_campaign=auto-captions-subtitles)

## Skill Output:

**Output Type(s):** [API Calls, Configuration instructions, Video files, Text]

**Output Format:** [Tool requests and structured status/results; edited video exported as MP4]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Levea account and API key; source media is provided through public URLs.]

## Skill Version(s):

1.0.4 (source: frontmatter, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
