## Description: <br>
Helps an agent use quiet-hour heartbeat time for freeform creative exploration and save local notes for later human review. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[briancolinger](https://clawhub.ai/user/briancolinger) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users can add this skill to a heartbeat routine so an agent occasionally generates reflective or creative markdown notes during quiet hours. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The heartbeat routine can create local creative notes during quiet hours, which may retain speculative or sensitive context. <br>
Mitigation: Enable it only when this behavior is desired, review the heartbeat snippet before use, and periodically review or clean memory/dreams/. <br>
Risk: Local state and topic configuration influence when the skill runs and what prompts it uses. <br>
Mitigation: Keep data/dream-state.json and data/dream-config.json limited to trusted, reviewed settings. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/briancolinger/dreaming) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown notes and shell command snippets, with a topic string emitted by the quiet-hours gate script.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes local state JSON and dream notes under configured workspace directories.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
