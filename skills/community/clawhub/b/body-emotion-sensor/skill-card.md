## Description: <br>
Body Emotion Sensor gives an agent a persistent body-emotion state system that converts structured AnalysisInput JSON into runtime prompt tags and workspace state updates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[askkumptenchen](https://clawhub.ai/user/askkumptenchen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to help an agent explain, initialize, and operate a local Body Emotion Sensor runtime for persistent per-workspace emotion state, session bootstrap tags, and turn-by-turn prompt fields. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may lead an agent to install or invoke a local CLI package before the environment is verified. <br>
Mitigation: Confirm the package source, ask for user approval before installation, and verify readiness with the CLI before claiming the runtime is active. <br>
Risk: The runtime writes persistent local state and may change a user language setting. <br>
Mitigation: Tell users where local state and configuration files are written, and confirm before changing language settings or writing persistent state. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/askkumptenchen/body-emotion-sensor) <br>
- [Publisher profile](https://clawhub.ai/user/askkumptenchen) <br>
- [Declared package source repository](https://github.com/AskKumptenchen/body-emotion-sensor) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline JSON field names and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference local JSON state files and CLI readiness checks when the runtime is available.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
