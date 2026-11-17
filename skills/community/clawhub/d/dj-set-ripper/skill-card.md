## Description:

DJ Set Ripper extracts tracklists from DJ set or mix links, downloads available individual tracks through the dj-mp3-sourcer workflow, can optionally download the full mix, and writes a timestamped status log.

This skill is ready for commercial/non-commercial use.

## Publisher:

[robinnnnn](https://clawhub.ai/user/robinnnnn)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to turn an authorized DJ set, mix URL, or pasted tracklist into individual downloaded tracks, an optional full-mix backup, and a per-track status log.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Untrusted page text can influence automated track downloads and filename changes.

Mitigation: Prefer trusted tracklist sources or pasted tracklists, inspect extracted tracklists before acting on them, and review proposed downloads and renames before unattended use.

Risk: The workflow can be misused to download music without proper rights.

Mitigation: Use the skill only for music the user is authorized to download, and respect copyright rules in the user's jurisdiction.

Risk: Filename normalization and temporary tracklist handling can be risky in shared or privileged environments.

Mitigation: Do not run with elevated privileges, avoid shared temporary directories for sensitive batches, and harden filename and temporary-file handling before relying on the skill for unattended runs.

## Reference(s):

- [DJ Set Ripper on ClawHub](https://clawhub.ai/robinnnnn/skills/dj-set-ripper)
- [dj-mp3-sourcer dependency](https://clawhub.ai/Robinnnnn/dj-mp3-sourcer)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files, Guidance]

**Output Format:** [Markdown guidance with JSON examples, bash commands, downloaded audio files, renamed filenames, and a log file.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces per-set output under a Downloads subfolder and uses a JSON tracklist as the source of truth for filename normalization.]

## Skill Version(s):

1.0.1 (source: server release metadata, created 2026-02-17)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
