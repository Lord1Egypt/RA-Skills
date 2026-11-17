## Description:

Get the spoken words (transcript) of a public video or audio link from the ClawGrab API, so an agent can summarize, take notes, quote, or answer questions about it.

This skill is ready for commercial/non-commercial use.

## Publisher:

[getclawgrab](https://clawhub.ai/user/getclawgrab)

### License/Terms of Use:

MIT-0

## Use Case:

People using an AI assistant can provide a single public video or audio link to get its transcript, then ask the assistant to summarize it, find quotes, make notes, translate it, or answer questions about what was said.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The transcription service receives the submitted video URL, and the skill documentation says requested URLs are written to the service log.

Mitigation: Submit only public video or audio URLs you are comfortable having processed and logged by ClawGrab.

Risk: The security evidence says the scan is incomplete because two local path references remain unresolved.

Mitigation: Review the full skill package and resolve the noted local references before relying on the security assessment.

## Reference(s):

- [ClawGrab](https://getclawgrab.com)
- [ClawGrab on ClawHub](https://clawhub.ai/getclawgrab/skills/clawgrab)
- [ClawGrab MCP server](https://github.com/getclawgrab/clawgrab-mcp-server)

## Skill Output:

**Output Type(s):** [Text]

**Output Format:** [Plain text transcript, optionally timestamped]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Transcript text from one public video or audio link; the agent can use it to prepare summaries, notes, quotations, translations, or answers.]

## Skill Version(s):

1.0.1 (source: frontmatter; release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
