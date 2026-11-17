## Description:

Edit videos in bulk with BatchEdits - add captions, remove silences, crop to 9:16, zoom and cut long videos into clips with the BatchEdits CLI (or MCP server), then download the results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chuckwhisler](https://clawhub.ai/user/chuckwhisler)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators and teams use this skill to batch edit videos by adding captions, removing silence, reframing to 9:16, zooming on key moments, and cutting long videos into clips, then downloading the results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review had partial coverage; the referenced package and unresolved local references were not fully assessed.

Mitigation: Review the package and resolve relevant local references before installing.

Risk: Video files selected for processing are sent to BatchEdits.com.

Mitigation: Choose only videos approved for processing and confirm they may be sent to the service.

Risk: An exposed BATCHEDITS_API_KEY could allow unauthorized account access.

Mitigation: Keep the key in the environment and never include it in commands, URLs, or chat messages.

## Reference(s):

- [BatchEdits CLI documentation](https://batchedits.com/docs/cli?utm_source=clawhub&utm_medium=skill)
- [BatchEdits MCP setup guide](https://batchedits.com/docs/mcp?utm_source=clawhub&utm_medium=skill)
- [BatchEdits npm package](https://www.npmjs.com/package/batchedits)

## Skill Output:

**Output Type(s):** [Edited video files, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Video files with Markdown workflow guidance and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports batches of up to 50 videos; processing and AI clips use credits.]

## Skill Version(s):

1.0.11 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
