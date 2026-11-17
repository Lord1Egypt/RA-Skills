## Description:

Diagnoses playback and streaming problems in user-provided media files and URLs, including codec, container, HLS integrity, and live latency issues.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and media engineers use the skill to diagnose playback failures, streaming interruptions, and latency problems from a specific media file or URL. It returns a read-only diagnosis with suggested next steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Untrusted playlists can trigger requests to internal services and reads of unintended local files.

Mitigation: Use trusted playlists, or run the skill in an isolated environment without sensitive files or internal-network access. For untrusted playlists, restrict segment schemes, destinations, and redirects.

Risk: Suggested repair commands could change or re-encode user media if run without review.

Mitigation: Treat repair commands as proposals; review them and obtain a separate request before executing any repair.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sdk-team/skills/alibabacloud-media-diagnostics)
- [Media diagnostics knowledge base](artifact/references/knowledge-base.md)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Markdown, Shell commands]

**Output Format:** [Structured JSON and a plain-language diagnosis report; repair commands may be suggested as text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only analysis; repair commands are suggestions and are not executed.]

## Skill Version(s):

0.0.2 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
