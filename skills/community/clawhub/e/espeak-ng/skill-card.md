## Description:

TTS with espeak-ng.

This skill is ready for commercial/non-commercial use.

## Publisher:

[martianzenmonk](https://clawhub.ai/user/martianzenmonk)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to generate local speech from text through the espeak-ng command-line text-to-speech engine.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on the local espeak-ng system package and may require OS-level installation.

Mitigation: Install espeak-ng only from a trusted OS package manager or reviewed installer source.

Risk: The skill runs direct local text-to-speech shell commands.

Mitigation: Run it only with text you intend to speak and review generated commands before execution.

## Reference(s):

- [espeak-ng releases](https://github.com/espeak-ng/espeak-ng/releases)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text responses with command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local speech audio through the installed espeak-ng system package.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
