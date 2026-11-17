## Description:

Discovers podcast topics from configurable sources, structures research, generates cited scripts, verifies claims, prepares ElevenLabs audio, and uploads episodes to local or S3 storage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harshilmathur](https://clawhub.ai/user/harshilmathur)

### License/Terms of Use:

MIT

## Use Case:

Developers and content creators use this skill to automate podcast topic discovery, research scaffolding, script generation, source checking, audio preparation, and storage publication while retaining manual review points.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The auto-publishing flow and safety claims are under-scoped enough that users should review the skill before installing or running it.

Mitigation: Install only after reviewing and controlling the workflow; prefer manual mode until the pipeline is tested.

Risk: Generated podcast scripts may contain unsupported or sensitive claims even when a verification gate is present.

Mitigation: Treat generated scripts as untrusted until a human verifies sources, and do not rely on the advertised verification gate to stop auto publication without supervision or modification.

Risk: S3 publication can expose generated episodes or metadata if credentials or bucket permissions are broader than intended.

Mitigation: Keep storage local during testing and use least-privilege AWS credentials before enabling S3 upload.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/harshilmathur/skills/custom-podcast-discovery)
- [README.md](README.md)
- [DEPLOYMENT.md](DEPLOYMENT.md)
- [SECURITY.md](SECURITY.md)
- [ElevenLabs voice library](https://elevenlabs.io/voice-library)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, JSON reports, text scripts, TTS-ready text, and generated audio files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Pipeline outputs can include ranked topic JSON, research JSON, cited script text, verification JSON, TTS-ready text, MP3 audio, local files, S3 URLs, and pipeline state.]

## Skill Version(s):

1.0.1 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
