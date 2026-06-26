## Description: <br>
Generate a storyboard and prompts from a scene or reference images, confirm the script with the user, then optionally submit multi-segment video generation tasks to the Volcengine Ark video API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yunni123](https://clawhub.ai/user/yunni123) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to turn scene ideas or reference images into structured video storyboards, English generation prompts, and optional Ark multi-segment video generation workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated prompts and reference-image-derived content may be sent to Volcengine Ark during execution. <br>
Mitigation: Confirm the storyboard and execution step with the user before calling the API, and avoid using sensitive prompts or images unless external processing is acceptable. <br>
Risk: Generated videos are saved under ~/.openclaw/media and the workflow may send final files through Feishu. <br>
Mitigation: Review local storage and delivery needs before execution, remove unneeded media after use, and only send files through Feishu when the user expects that delivery path. <br>
Risk: The artifact includes a default rule that represents unspecified human characters as East Asian. <br>
Mitigation: Review or replace the default character-representation rule when neutral, user-directed, or region-specific representation is required. <br>
Risk: The server security summary flags under-scoped external delivery and persistent workflow logging. <br>
Mitigation: Check the execution plan before enabling generation, delivery, or logging behavior, and keep only records needed for the workflow. <br>


## Reference(s): <br>
- [Ark Video API Notes](artifact/references/api.md) <br>
- [Storyboard Schema](artifact/references/storyboard-schema.md) <br>
- [Prompt Rules](artifact/references/prompt-rules.md) <br>
- [Examples](artifact/references/examples.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/yunni123/ark-video-storyboard) <br>
- [Publisher Profile](https://clawhub.ai/user/yunni123) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, API Calls, Files, Guidance] <br>
**Output Format:** [Markdown storyboard guidance, JSON storyboard data, shell commands, API request results, and downloaded video files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Prompts are confirmation-first; optional generation sends prompts and reference-image-derived content to Volcengine Ark and may save generated videos under ~/.openclaw/media.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
