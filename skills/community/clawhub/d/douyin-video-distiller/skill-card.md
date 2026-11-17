## Description:

Douyin Video Distiller helps an agent turn Douyin links, local videos, or transcripts into timestamped knowledge cards with summaries, evidence, timelines, action items, and points needing confirmation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[3378925604-a11y](https://clawhub.ai/user/3378925604-a11y)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to distill Douyin videos, local video files, or supplied transcripts into reusable knowledge-management notes. It is intended to preserve timestamps, separate source evidence from model conclusions, and report download, analysis, and cleanup status transparently.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The analyzer can upload whole media files to NVIDIA or to an endpoint configured in the environment.

Mitigation: Use only media approved for upload, avoid private or regulated content without explicit authorization, and confirm the endpoint before analysis.

Risk: A configurable endpoint could receive the NVIDIA API bearer token and encoded media if misconfigured.

Mitigation: Verify NVIDIA_ENDPOINT is unset or restricted to the intended HTTPS NVIDIA host before running the analyzer.

Risk: Downloads or analysis can fail because of access controls, missing cookies, file size limits, timeouts, or empty model responses.

Mitigation: Report incomplete steps clearly, avoid fabricating video understanding, preserve retryable inputs, and segment or compress large videos before analysis.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/3378925604-a11y/skills/douyin-video-distiller)
- [NVIDIA Build](https://build.nvidia.com)
- [NVIDIA chat completions endpoint](https://integrate.api.nvidia.com/v1/chat/completions)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Structured Markdown knowledge card with optional JSON analyzer output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include timestamps, source evidence, distilled conclusions, action items, confirmation items, and explicit failure or cleanup status.]

## Skill Version(s):

1.0.0 (source: artifact frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
