## Description:

Fetch YouTube video subtitles/captions using Felo YouTube Subtitling API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangzhiming1999](https://clawhub.ai/user/wangzhiming1999)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to fetch captions or transcripts from YouTube video URLs or IDs, optionally selecting a subtitle language and timestamped output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The Felo API key could be sent to an arbitrary endpoint if FELO_API_BASE is influenced.

Mitigation: Leave FELO_API_BASE unset or set it only to a trusted HTTPS Felo endpoint, and rotate the key if it may have been used with an untrusted base URL.

Risk: The unpinned global felo-ai CLI may differ from the reviewed artifact.

Mitigation: Prefer the bundled script unless the global CLI package and version have been separately reviewed.

Risk: Requested YouTube video IDs and the Felo API key are sent to Felo.

Mitigation: Use the skill only when sharing those identifiers and credentials with Felo is acceptable.

## Reference(s):

- [Felo YouTube Subtitling API](https://openapi.felo.ai/docs/api-reference/v2/youtube-subtitling.html)
- [Felo Open Platform](https://openapi.felo.ai/docs/)
- [ClawHub skill page](https://clawhub.ai/wangzhiming1999/skills/felo-youtube-subtitling)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands; script output is plain text or JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include subtitle timestamps when requested; failures are reported on stderr with a nonzero exit code.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
