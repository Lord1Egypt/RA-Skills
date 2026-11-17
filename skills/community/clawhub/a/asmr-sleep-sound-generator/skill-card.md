## Description:

Interactive 3D head tapping ASMR synthesizer with material, position, and strength controls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[moroiser](https://clawhub.ai/user/moroiser)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to run a browser-based 3D ASMR sound generator, choose tapping regions and materials, arrange playback sequences, and export generated sleep-sound audio.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional LLM feature asks users to store an API key in browser localStorage.

Mitigation: Use a restricted, low-quota, revocable API key and clear browser storage when finished.

Risk: Running a local static server could expose unintended files if it is bound broadly or started from a sensitive directory.

Mitigation: Bind the server to localhost, for example with --bind 127.0.0.1, and serve only the intended project directory.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/moroiser/skills/asmr-sleep-sound-generator)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Markdown]

**Output Format:** [Markdown with inline bash commands and browser usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include local server startup commands, browser interaction steps, and LLM API configuration guidance.]

## Skill Version(s):

0.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
