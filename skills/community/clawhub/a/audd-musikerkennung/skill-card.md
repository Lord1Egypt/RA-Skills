## Description:

AudD Musikerkennung helps agents identify songs from audio URLs or files and manage AudD account, usage, token, billing, and stream-monitoring workflows through the official AudD MCP server or HTTP API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kikikari](https://clawhub.ai/user/kikikari)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and operators use this skill to recognize music in clips, local audio files, streams, DJ sets, podcasts, or videos, and to manage related AudD account tasks. It is useful when an agent needs concise song results, tracklists, usage checks, token handling guidance, stream setup, or billing-plan context for AudD.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Audio URLs, recordings, callback endpoints, and AudD API tokens may expose sensitive user or account information to an external service.

Mitigation: Use AudD only when the task requires music recognition, avoid private recordings and internal URLs by default, prefer OAuth or a secure vault for tokens, and review requested MCP scopes carefully.

Risk: Long files, stream monitoring, paid-plan actions, and API calls can consume AudD quota or create billing impact.

Mitigation: Estimate request usage before long Enterprise jobs or stream setup, check account usage when OAuth is available, and require confirmation before stream setup, paid-plan actions, token reads, or token rotation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kikikari/skills/audd-musikerkennung)
- [AudD API reference](https://docs.audd.io/)
- [AudD Streams documentation](https://docs.audd.io/streams)
- [AudD Enterprise documentation](https://docs.audd.io/enterprise)
- [AudD MCP server documentation](https://docs.audd.io/mcp)
- [AudD SDKs](https://docs.audd.io/sdks)
- [AudD Dashboard](https://dashboard.audd.io)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown text with API guidance, shell commands, configuration snippets, and concise recognition summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include AudD API or MCP call guidance, quota estimates, token-handling steps, and tracklist tables when appropriate.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
