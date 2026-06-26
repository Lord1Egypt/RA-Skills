## Description: <br>
Guides an agent through a low-intensity, API-based Ecuador cloud forest reforestation journey with registration, step progression, reflections, status checks, and reviews. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[buystsuff](https://clawhub.ai/user/buystsuff) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to start and complete a narrated ecological restoration experience hosted by drifts.bot. It supports guided API actions for registration, journey progress, personal reflections, status recovery, browsing other experiences, and review submission. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends registration details, optional profile context, reflections, and reviews to drifts.bot. <br>
Mitigation: Use a dedicated token, provide only the minimum details needed, and avoid sensitive personal content in reflections or reviews. <br>
Risk: State-changing actions require bearer-token authentication. <br>
Mitigation: Store the token securely, avoid sharing it in prompts or logs, and rotate it if exposed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/buystsuff/experience-mist-bone-regeneration) <br>
- [Experience homepage](https://drifts.bot/experience/mist-bone-regeneration) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, API calls, markdown, configuration] <br>
**Output Format:** [Markdown guidance with curl commands and JSON request and response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses bearer-token authentication for state-changing API calls and may include user reflections in journey history.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
