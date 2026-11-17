## Description:

Convert a text or Markdown manuscript into clean, long-form spoken narration (MP3, optional MP4) fully locally with Kokoro-82M via MLX.

This skill is ready for commercial/non-commercial use.

## Publisher:

[highnoonoffice](https://clawhub.ai/user/highnoonoffice)

### License/Terms of Use:

MIT

## Use Case:

Developers, creators, and agents use this skill to prepare manuscripts for local text-to-speech narration, synthesize ordered long-form MP3/WAV outputs, optionally assemble a static-image MP4, and verify the resulting job manifest.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release security summary says the skill downplays first-run network downloads.

Mitigation: Pre-download and verify Kokoro model assets and dependencies before use in offline, sensitive, or policy-restricted environments.

Risk: The release security summary flags unpinned install commands that can change what code runs.

Mitigation: Pin dependency versions and hashes where possible, and compare against the README's verified versions before deployment.

Risk: The workflow processes user manuscripts and writes generated audio/video outputs to selected directories.

Mitigation: Run it only on manuscripts and output directories intentionally selected, and avoid committing private manuscripts, generated media, credentials, or downloaded model weights.

## Reference(s):

- [Narration quality fixes](references/FIXES.md)
- [README](README.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and generated local media/file artifacts.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The workflow can produce narration text, MP3, lossless WAV master, manifest JSON, segment files, and optional MP4 output.]

## Skill Version(s):

1.0.0 (source: frontmatter and ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
