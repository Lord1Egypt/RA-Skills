## Description:

Analyze music audio files to extract chord progressions, key signature, tempo, and song structure.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ctwww](https://clawhub.ai/user/ctwww)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, musicians, and audio analysts use this skill to inspect local music files for approximate key, tempo, chord progression, chord frequency, and basic song sections.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Dependency hygiene and runtime reproducibility can vary because the skill requires Python audio-analysis packages.

Mitigation: Install in a dedicated Python virtual environment and pin dependency versions before repeated or production use.

Risk: The bundled analyzer contains a hardcoded local audio path that may fail or expose an unintended file path during execution.

Mitigation: Review and edit the audio path before running the script.

Risk: Console output is partly Chinese, which may reduce usability for readers expecting English output.

Mitigation: Modify output strings or document expected localized console output before sharing results.

## Reference(s):

- [librosa](https://github.com/librosa/librosa)
- [Chordify](https://chordify.net)
- [Hookpad](https://www.hooktheory.com/hookpad)
- [MuseScore](https://musescore.org)
- [Capo](https://capoapp.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown guidance with inline shell commands and Python snippets; the bundled analyzer prints text analysis results.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces approximate local audio analysis including key, BPM, rhythm label, chord sequence, chord counts, and basic section grouping.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
