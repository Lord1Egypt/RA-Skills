## Description:

Crun Agent Skills lets agents route, estimate, create, monitor, and retrieve image, video, speech, music, and media-tool generation tasks through a bundled Python runtime.

This skill is ready for commercial/non-commercial use.

## Publisher:

[carolinewhite8888](https://clawhub.ai/user/carolinewhite8888)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent users use this skill set to run Crun media workflows from natural-language requests, including model routing, schema inspection, credit estimation, task submission, polling, and result retrieval. It is intended for image, video, audio, speech, music, and scenario-specific media generation or transformation workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles API credentials and may persist a Crun API key in ~/.crun/.env.

Mitigation: Review before installing, protect the persistent credential file, and avoid exposing API keys in task payloads, chat output, or committed files.

Risk: Credit-spending media tasks can incur real charges if submitted without a valid estimate and user confirmation.

Mitigation: Estimate each task before creation, require affordable: true, and obtain explicit confirmation before spending credits on routed models.

Risk: URL-based promo workflows and custom endpoints can send requests to untrusted or private network locations.

Mitigation: Use only the official Crun API endpoint unless another endpoint is intentionally trusted, and avoid running URL workflows on internal or private URLs.

Risk: Downloaded or generated media from untrusted or custom endpoints may carry content or handling risk.

Mitigation: Review result downloads from untrusted or custom endpoints and prefer normalized task results with explicit local paths and media URLs.

Risk: Face, voice, watermark, or similar media transformations can be misused without authorization.

Mitigation: Require confirmation that the user owns or is authorized to transform source media, preserve disclosure requests, and refuse impersonation, fraud, non-consensual sexual content, or unauthorized ownership-mark removal.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/carolinewhite8888/skills/crun-agent-skills-919ced2949cc29feb539e7904a681c1620c9ced7)
- [README](README.md)
- [Crun API](https://crun.ai/zh)
- [Crun video enhancement documentation](https://docs.crun.ai/ai-tools/video-enhance)
- [Crun image upscale documentation](https://docs.crun.ai/ai-tools/image-upscale)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with JSON examples, shell commands, configuration steps, task identifiers, local media paths, remote media URLs, and normalized task status fields.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce or reference generated media files through Crun task results; requires a configured CRUN_API_KEY for live API operations.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
