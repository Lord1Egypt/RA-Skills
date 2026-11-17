## Description:

Generate songs from prompts or lyrics through an ACE-Step-compatible API backend.

This skill is ready for commercial/non-commercial use.

## Publisher:

[twocode](https://clawhub.ai/user/twocode)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to generate music from prompts or lyrics through an existing ACE-Step-compatible backend, save stable audio files, and optionally route the saved result to Clawatch playback.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, lyrics, and any configured ACESTEP_API_KEY may be sent to the configured ACE-Step backend.

Mitigation: Use only trusted backends, prefer local or HTTPS endpoints, and use a narrowly scoped API key.

Risk: Backend-controlled output URLs can expose local files or bearer tokens.

Mitigation: Avoid untrusted remote or plaintext HTTP backends, and review generated output folders and manifests before reuse.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/twocode/skills/gen-music)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, files, guidance]

**Output Format:** [Markdown guidance with bash commands, saved audio file paths, and a JSON manifest]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and a separately configured ACE-Step-compatible API backend.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
