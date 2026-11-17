## Description: <br>
Agentvibes Skill helps agents guide Chinese-language TTS and audio-production workflows for neural voices, multi-role narration, batch audio export, effects, and background music. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, content-production teams, and automation users can use this skill to plan and operate TTS workflows for audiobooks, podcasts, training videos, game dialogue, and IVR prompts. It is intended for agent-assisted audio generation and batch export, not unrelated shell or file automation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requests broad command and file authority while its routing and data-flow instructions are generic. <br>
Mitigation: Review commands before execution, run the skill in a dedicated workspace, and limit use to TTS/audio-generation tasks. <br>
Risk: Batch export workflows can write to unintended output locations. <br>
Mitigation: Confirm output directories and filenames before running export commands. <br>
Risk: Customer text, scripts, or other sensitive content may be sent to online TTS engines. <br>
Mitigation: Avoid sending sensitive content unless the data transfer is approved for the selected engine. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/agentvibes-skill) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose TTS engine settings, license environment variables, batch export commands, and output directory choices for review before execution.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
