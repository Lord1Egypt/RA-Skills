## Description: <br>
Agentvibes Skill Free helps agents configure offline text-to-speech playback with voice switching, speed controls, and basic speaking styles for personal developer and creator workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, content creators, and language learners use this skill to have an agent configure local TTS playback, voice selection, speed, preview, and cache-management commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requests command execution and has broad triggers that could lead to commands outside ordinary TTS tasks. <br>
Mitigation: Limit use to TTS configuration and playback tasks, and review proposed commands before execution. <br>
Risk: The skill may automatically download TTS engines or voice files from HuggingFace. <br>
Mitigation: Verify download sources, cache locations, and network access expectations before deployment. <br>
Risk: The documentation gives inconsistent offline and API-key guidance. <br>
Mitigation: Confirm whether credentials are actually required before entering any secret. <br>
Risk: The skill includes cache cleanup behavior that may delete local audio artifacts. <br>
Mitigation: Confirm the target cache path before running cleanup commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/agentvibes-skill-free) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with slash-command examples and shell-command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose command execution for local TTS setup, voice downloads, playback, and cache cleanup.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
