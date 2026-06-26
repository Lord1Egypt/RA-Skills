## Description: <br>
Autonomous music generation DAW for breakcore, dubstep, phonk, and 404-style tracks that synthesizes drums, bass, FX, voice chopping, and machine voice locally. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[evezart](https://clawhub.ai/user/evezart) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, producers, and creative agents use this skill to run a local music-generation service that creates synthetic drum patterns, bass lines, effects chains, drum kits, and chopped voice samples. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The local audio service can be network-accessible when run with its default server binding. <br>
Mitigation: Run it behind localhost-only binding or a firewall and avoid exposing the port to other machines. <br>
Risk: Filename and sample path handling may allow unsafe filesystem reads or writes when used with untrusted clients. <br>
Mitigation: Review or patch path handling before use with untrusted clients, and restrict requests to trusted filenames and sample paths. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/evezart/evez-daw-agent) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Code, Configuration, Files, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON API examples; generated artifacts are WAV audio files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs locally and exposes HTTP endpoints for rendering tracks, generating drum kits, chopping samples, listing presets, and checking health.] <br>

## Skill Version(s): <br>
1.3.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
