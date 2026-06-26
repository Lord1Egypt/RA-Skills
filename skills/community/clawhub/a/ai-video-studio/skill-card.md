## Description: <br>
FableForge AI Video Studio is a command-level executable SOP for producing management allegory and promotional videos from concept generation through scripting, TTS narration, media preparation, HyperFrames rendering, and publishing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lucas-kay8](https://clawhub.ai/user/lucas-kay8) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, creators, and content operations teams use this skill to guide an agent through a structured AI video production workflow, including storyboard creation, voice narration, visual asset generation, timeline assembly, rendering, and publication preparation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow can use cloned-voice narration. <br>
Mitigation: Require explicit approval before voice-clone use and keep voice samples out of published repositories. <br>
Risk: The setup and media workflow can download dependencies and external files. <br>
Mitigation: Review dependency and media sources, inspect downloaded files, and prefer pinned or verified sources before execution. <br>
Risk: The publishing workflow can alter a git repository or publish changes. <br>
Mitigation: Inspect git diffs before commits and do not run git push unless publishing to the remote branch is intentional. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/lucas-kay8/ai-video-studio) <br>
- [FableForge AI Agent SOP](artifact/SKILL.en.md) <br>
- [Environment setup stage](artifact/resources/stages/stage_0_env.md) <br>
- [Creative production stage](artifact/resources/stages/stage_1_creatives.md) <br>
- [Timeline mapping stage](artifact/resources/stages/stage_2_timeline.md) <br>
- [Static layout stage](artifact/resources/stages/stage_3_static.md) <br>
- [Animation and render stage](artifact/resources/stages/stage_4_animation.md) <br>
- [Publishing stage](artifact/resources/stages/stage_5_publish.md) <br>
- [Visual style bible](artifact/resources/style_bible.md) <br>
- [Voice sample guide](artifact/resources/voice-model/README.md) <br>
- [Troubleshooting manual](artifact/resources/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with checklists, shell commands, and HTML/CSS/JavaScript snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces staged operating instructions and project file guidance for an agent-driven video workflow.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
