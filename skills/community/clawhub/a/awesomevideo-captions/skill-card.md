## Description:

Burn styled captions onto video (MP4 + SRT/VTT/JSON) via AwesomeVideo MCP or REST. Use when an agent needs subtitles, burned captions, or a free API key for video captioning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vhmartinezm](https://clawhub.ai/user/vhmartinezm)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and creators can submit an authorized video to generate styled, burned-in captions and downloadable subtitle and transcript files. They can estimate costs before running a paid caption job.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Video sources are processed by an external captioning service.

Mitigation: Submit only videos you are authorized to share, and review the service's privacy practices before sending sensitive recordings.

Risk: Paid caption jobs use an API balance and require a bearer token.

Mitigation: Use the free estimate before a job, keep API keys out of logs and shared configuration, and approve payments yourself.

Risk: A source URL may expose a private file if it is made public for processing.

Mitigation: Do not make private files public just to provide a source URL.

## Reference(s):

- [AwesomeVideo agent recipes](https://awesomevideoeditor.com/agents)
- [Caption API documentation](https://awesomevideoeditor.com/api/captions)
- [AwesomeVideo OpenAPI specification](https://api.awesomevideoeditor.com/openapi.json)
- [AwesomeVideo MCP endpoint](https://api.awesomevideoeditor.com/mcp)

## Skill Output:

**Output Type(s):** [Video files, Subtitle files, Transcript data]

**Output Format:** [MP4 video, SRT and VTT subtitles, and JSON transcript]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Styled captions can be translated when requested.]

## Skill Version(s):

1.0.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
