## Description: <br>
BluOS CLI (blu) for discovery, playback, grouping, and volume. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[snazar-faberlens](https://clawhub.ai/user/snazar-faberlens) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to control BluOS and NAD speakers through the blu CLI, including device discovery, playback, grouping, TuneIn, status checks, and volume changes. The skill emphasizes confirmation and local-network privacy guardrails before state-changing actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Playback, volume, source, or grouping changes can disrupt the wrong speaker or another user's active session. <br>
Mitigation: Confirm the target speaker and acknowledge active sessions before proposing or executing state-changing blu commands. <br>
Risk: Device discovery output can expose local network and household device details. <br>
Mitigation: Keep blu discovery output local and avoid piping it to network-transmitting commands or external services. <br>
Risk: Unnecessary exhaustive discovery can reveal more local devices than the task requires. <br>
Mitigation: Limit discovery to the device or scope needed for the user's request. <br>


## Reference(s): <br>
- [blucli homepage](https://blucli.sh) <br>
- [blucli Go install module](github.com/steipete/blucli/cmd/blu@latest) <br>
- [Faberlens safety evaluation](https://faberlens.ai) <br>
- [ClawHub skill page](https://clawhub.ai/snazar-faberlens/blucli-hardened) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose blu CLI commands and JSON-oriented scripting guidance; state-changing commands require target confirmation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and target metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
