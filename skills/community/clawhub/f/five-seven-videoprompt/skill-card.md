## Description: <br>
CinePrompt helps agents create AI video prompts and storyboard scripts using a five-dimension ideation framework, seven video-language elements, single-shot and segmented output modes, role cards, style cards, and keyframe anchors. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[slfcys](https://clawhub.ai/user/slfcys) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators, marketers, video teams, and developers use this skill to turn ideas into structured AI video generation prompts, storyboard sequences, and continuity plans for single or multi-segment videos. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may activate on broad prompt-writing or storyboard terms. <br>
Mitigation: Use narrower trigger phrases when installing or routing the skill so it is selected mainly for AI video prompt and storyboard drafting tasks. <br>
Risk: Generated video prompts may include timing, style, or continuity assumptions that do not match the target video model's limits. <br>
Mitigation: Review the generated prompt against the target model's duration, aspect-ratio, and continuity constraints before production use. <br>


## Reference(s): <br>
- [Five-Dimension Thinking Framework](artifact/references/five-dimensions.md) <br>
- [Video Spectrum: Seven Elements](artifact/references/video-spectrum.md) <br>
- [Segmented Generation Rules](artifact/references/segmented-rules.md) <br>
- [Prompt Examples](artifact/references/examples.md) <br>
- [CinePrompt on ClawHub](https://clawhub.ai/slfcys/five-seven-videoprompt) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown prompt and storyboard structures with role cards, style cards, shot sequences, transitions, optional audio timing notes, and continuity tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports single-prompt and segmented-video outputs; segmented outputs repeat role and style cards and include keyframe anchors for continuity.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
