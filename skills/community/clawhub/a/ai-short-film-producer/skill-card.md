## Description:

AI短剧制作助手 | AI Short Film Producer helps agents plan and produce low-cost AI short films by creating shot scripts, generating video and TTS assets through third-party APIs, and assembling them locally with FFmpeg and Python.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hitjcl](https://clawhub.ai/user/hitjcl)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and creative operators use this skill to turn a topic, script, or concept into an AI short film workflow with shot planning, video generation, voiceover generation, subtitles, local composition, review, and cost tracking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow uses third-party video and TTS APIs that may receive user prompts, scripts, or generated content.

Mitigation: Do not submit secrets, regulated data, private scripts, or sensitive personal information to the referenced APIs; review provider terms before use.

Risk: API keys may be exposed if copied into URLs, logs, scripts, or shared project files.

Mitigation: Pass API keys through headers or a local secret store, keep them out of URLs and logs, and avoid committing generated credentials or configuration files.

Risk: Downloaded media archives and generated assets are processed locally with Python and FFmpeg.

Mitigation: Use request timeouts, retry limits, trusted download hosts, archive size checks, and safe FFmpeg concat manifests before processing untrusted media folders.

Risk: Generated footage, TTS, or subtitles can be inaccurate, poorly synchronized, or visually defective.

Mitigation: Run the documented review workflow for audio-video sync, subtitle accuracy, duration drift, repeated loops, and visual quality before publishing.

## Reference(s):

- [AI Short Film Producer skill page](https://clawhub.ai/hitjcl/skills/ai-short-film-producer)
- [AI短剧制作流程详细参考](artifact/references/production_workflow.md)
- [速创API 接口文档与踩坑经验](artifact/references/sucuang_api.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with JSON, Python, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces workflow guidance and implementation snippets for scripts, generated media assets, subtitles, FFmpeg composition, review checks, and cost calculations.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
