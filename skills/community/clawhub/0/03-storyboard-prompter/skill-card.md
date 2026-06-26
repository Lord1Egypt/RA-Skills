## Description: <br>
Generates consistent AI art storyboard prompts from short-drama scene objects, using local formatting without API calls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ghwyever](https://clawhub.ai/user/ghwyever) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Creators, developers, and content automation teams use this skill to convert short-drama scene lists into consistent vertical cinematic image prompts for storyboard or AI art workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Scene text may contain secrets, sensitive personal details, or private story information that could be exposed if generated prompts are shared. <br>
Mitigation: Redact sensitive details before providing scenes, and review generated prompts before sharing or publishing them. <br>
Risk: Missing scene fields can produce incomplete or unclear prompts. <br>
Mitigation: Validate that every scene object includes scene, role, action, and duration before running the skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ghwyever/03-storyboard-prompter) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON] <br>
**Output Format:** [JSON object containing a shot_list array of storyboard prompt entries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Each shot entry includes shot_id, prompt, and duration; prompts combine scene, role, action, 9:16 aspect ratio, and cinematic style terms.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
