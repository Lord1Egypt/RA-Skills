## Description:

Audio Processor helps agents handle audio conversion, trimming, merging, feature analysis, denoising, speed and pitch changes, volume normalization, metadata work, and batch processing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kaiyuelv](https://clawhub.ai/user/kaiyuelv)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to select and run local audio-processing workflows for converting, editing, analyzing, cleaning, normalizing, and tagging audio files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Output paths can overwrite or alter valuable audio files when a user targets originals or existing files.

Mitigation: Use explicit output paths and work on copies for valuable audio files unless overwriting is intentional.

Risk: Unpinned Python dependency versions can reduce reproducibility or introduce dependency drift.

Mitigation: Install and run the skill in a virtual environment or container, and pin dependency versions when reproducibility matters.

## Reference(s):

- [Audio Formats Reference](references/audio-formats.md)
- [Effects Guide](references/effects-guide.md)
- [ClawHub skill page](https://clawhub.ai/kaiyuelv/skills/audio-processor)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash code blocks and file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Running the referenced local scripts may produce processed audio files, JSON reports, metadata output, and plots.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
