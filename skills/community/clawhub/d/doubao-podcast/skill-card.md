## Description:

Use when calling the Doubao/ByteDance podcast TTS API to generate audio, parse WebSocket binary frames, handle streaming audio chunks, extract audio URLs, troubleshoot generation issues, or design podcast playback architecture.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mileszhang001-boom](https://clawhub.ai/user/mileszhang001-boom)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to integrate Doubao/ByteDance podcast text-to-speech generation into agent workflows, server-side services, and browser-facing applications. It provides implementation guidance for authentication, binary WebSocket framing, streaming audio handling, caching, and operational troubleshooting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Article URLs and text are sent to the Doubao/ByteDance podcast TTS service.

Mitigation: Avoid sensitive articles or text unless the user accepts sending that content to ByteDance.

Risk: Batch generation can write MP3 files outside the selected output folder when file IDs are not validated.

Mitigation: Do not run batch JSON from untrusted sources, and validate file IDs before using them in output paths.

Risk: Generated audio files may be stored in unintended locations or depend on short-lived CDN URLs.

Mitigation: Store generated MP3s in a controlled location and download audio promptly instead of relying on expiring audio URLs.

Risk: The trigger scope is broader than the Doubao-specific implementation.

Mitigation: Use the skill for Doubao/ByteDance podcast TTS work and confirm applicability before applying it to other podcast TTS providers.

Risk: Dependencies and source provenance are not server-resolved for this release.

Mitigation: Prefer a reviewed commit and pinned dependencies before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mileszhang001-boom/skills/doubao-podcast)
- [Publisher profile](https://clawhub.ai/user/mileszhang001-boom)
- [Agent Skills](https://agentskills.io)
- [Volcengine Console](https://console.volcengine.com/)
- [Reference generator script](artifact/scripts/generate_podcast.py)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with inline code examples, command snippets, and configuration details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide agents to generate MP3 podcast files through the referenced API and local helper script.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
