## Description: <br>
Cine Cog guides agents in using CellCog to create cinematic AI videos, including short films, music videos, brand films, and widescreen cinematics from prompts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nitishgargiitd](https://clawhub.ai/user/nitishgargiitd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, creators, and agent users use this skill to plan and launch CellCog cinematic video-generation jobs. It provides prompting patterns, SDK examples, format guidance, and setup notes for creating narrative films, music videos, brand videos, short films, and other AI-generated cinematics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a CellCog API key. <br>
Mitigation: Store CELLCOG_API_KEY in the environment or a secret manager, avoid exposing it in prompts or logs, and rotate it if disclosure is suspected. <br>
Risk: Creative prompts or referenced project material may be sent to the CellCog remote service. <br>
Mitigation: Avoid submitting secrets or confidential unreleased material unless CellCog terms, account controls, and project requirements allow that use. <br>
Risk: Cinematic video jobs can consume credits or billing capacity, and results may be unpredictable. <br>
Mitigation: Monitor credit and billing usage, start with scoped jobs, and review generated outputs before relying on them for production work. <br>


## Reference(s): <br>
- [Cine Cog on ClawHub](https://clawhub.ai/nitishgargiitd/cine-cog) <br>
- [CellCog homepage](https://cellcog.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with Python and shell code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and CELLCOG_API_KEY; examples invoke the remote CellCog service.] <br>

## Skill Version(s): <br>
1.0.11 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
