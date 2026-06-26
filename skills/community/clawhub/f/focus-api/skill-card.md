## Description: <br>
FocusAI helps an agent monitor local screen activity, evaluate focus state, and query same-day visual activity history with user consent. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[HR2AY](https://clawhub.ai/user/HR2AY) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Chinese-speaking end users and their local agent use this skill to start focus monitoring, check current focus status, and summarize same-day screen activity. The workflow is intended for local personal productivity analysis and requires user consent before monitoring begins. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can periodically capture the whole screen, store local screen history, and send images to a vision-model provider. <br>
Mitigation: Use it only after explicit consent, confirm which provider receives images, avoid sensitive windows while monitoring, and regularly manage or delete ~/Desktop/FocusOS_Data/. <br>
Risk: Installation relies on running an unpinned external setup script. <br>
Mitigation: Review the external repository and start.bat before running the installer, and install only from a source the user trusts. <br>
Risk: The local HTTP API can start, stop, and reconfigure monitoring. <br>
Mitigation: Run the service only on trusted local machines and keep access limited to localhost. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/HR2AY/focus-api) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with HTTP API examples and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill directs an agent to check for same-day local data before querying history or analyzing screenshots.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
