## Description: <br>
AI Drama Prompt Factory converts a novel or story idea into structured Chinese prompt packages for short-drama production, including planning, design, scripts, diagnostics, storyboard image prompts, video prompts, audio specifications, and API JSON. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[huang-shao](https://clawhub.ai/user/huang-shao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Creators, developers, and production teams use this skill to turn source fiction or original short-drama ideas into a structured prompt package for downstream image, video, and audio generation tools. It supports staged planning, character and scene design, script generation, adaptation diagnostics, and final JSON prompt assembly. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bundled document tools can broadly index local files outside the intended story-material scope. <br>
Mitigation: Run the skill only in a dedicated project folder containing the novel or story files needed for the task. <br>
Risk: Generated index files may contain sensitive source-story content or private material from indexed folders. <br>
Mitigation: Treat generated indexes as sensitive artifacts and delete them when they are no longer needed. <br>
Risk: The skill generates prompt packages for downstream media tools, so outputs may need editorial and rights review before production use. <br>
Mitigation: Review generated scripts, prompts, and source adaptation choices before submitting them to external image, video, or audio systems. <br>


## Reference(s): <br>
- [Skill source](SKILL.md) <br>
- [API output schema](references/api-schema.md) <br>
- [Assembly rules](references/assembly-rules.md) <br>
- [Planning guide](references/planning-guide.md) <br>
- [Design guide](references/design-guide.md) <br>
- [Script generation guide](references/script-generation-guide.md) <br>
- [Diagnosis guide](references/diagnosis-guide.md) <br>
- [Continuity guide](references/continuity-guide.md) <br>
- [Platform adapters](references/platform-adapters.md) <br>
- [ClawHub release page](https://clawhub.ai/huang-shao/ai-drama-prompt-factory-skip) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, JSON, and Chinese natural-language prompt text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces project manifests, episode prompt packages, role and scene configuration, storyboard image prompts, video prompts, audio specifications, and optional Markdown storyboard tables.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
