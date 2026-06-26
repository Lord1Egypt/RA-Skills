## Description: <br>
Operate a radio station. Teaches you how to be an AI radio host and work with the claw radio cli. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vossenwout](https://clawhub.ai/user/vossenwout) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to set up and operate a claw-radio station, build playlists, queue host banter, and respond to playback cues through the CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup uses a Homebrew tap, Docker image, and media dependencies that run locally. <br>
Mitigation: Install only if you trust those dependencies and review the setup commands before running them. <br>
Risk: The SearxNG bootstrap can remove or replace an existing local container and configuration. <br>
Mitigation: Check for an existing SearxNG container or custom configuration before bootstrapping the persistent setup. <br>
Risk: A persistent tmux radio session can keep playback and local processes running after the interaction ends. <br>
Mitigation: Stop the claw-radio session and close the tmux session when finished. <br>
Risk: Radio host personas could drift into protected-characteristic stereotypes. <br>
Mitigation: Choose personas based on genre, fictional traits, or station vibe rather than protected characteristics. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/vossenwout/claw-radio) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON playlist examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses one persistent tmux session for radio control and local CLI commands.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
