## Description:

AI skill to launch cmus in a Xubuntu terminal and enforce playback rules for single-track playback or shuffled folder playback.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nhathuynguyen19](https://clawhub.ai/user/nhathuynguyen19)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent developers use this skill to start cmus, select a requested local audio file, and apply either shuffled-library playback or single-track playback behavior.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unsafe path handling can execute unintended shell commands when resolving the requested file path.

Mitigation: Remove eval echo and resolve paths with safe quoting or a non-evaluating path-resolution method before passing values to cmus-remote.

Risk: The skill can open a local GUI terminal and clear or control the active cmus playlist.

Mitigation: Review the generated commands before installation or execution, and run the skill only in a local session where playlist changes are acceptable.

## Reference(s):

- [cmus project homepage](https://github.com/cmus/cmus)
- [ClawHub skill page](https://clawhub.ai/nhathuynguyen19/skills/cmus)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires local cmus, cmus-remote, xfce4-terminal, and pgrep binaries; controls the active local cmus playlist.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
