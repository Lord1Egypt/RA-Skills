## Description:

YouTube video translation workflow, download audio, launch Doubao, play audio, capture translation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[banner90](https://clawhub.ai/user/banner90)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators use this skill to translate YouTube videos by orchestrating audio download, Doubao launch, audio playback, and subtitle capture on a Windows desktop.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The plugin manifest points to a Python script outside the package, so the code that will execute is not included in the reviewed release.

Mitigation: Install only after the implementation is bundled in the package or after you personally control, inspect, and trust the external script path.

Risk: The workflow downloads YouTube audio, automates Doubao on a visible Windows desktop, plays audio, and saves local output files.

Mitigation: Run it only in an environment where the visible desktop, audio playback, network use, and Windows works directory are appropriate for the content being translated.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/banner90/skills/byt-workflow)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Files]

**Output Format:** [JSON status object with generated audio and translation file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces audio and translation files under a Windows works directory when successful.]

## Skill Version(s):

1.0.4 (source: server release metadata; artifact package metadata lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
