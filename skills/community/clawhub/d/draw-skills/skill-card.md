## Description: <br>
Academic figure generation assistant that analyzes research papers or figure requests and produces detailed natural-language prompts for nanobanana and similar drawing tools to create publication-quality scientific figures. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[memory555](https://clawhub.ai/user/memory555) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External researchers, students, and developers use this skill to plan paper figures, improve existing diagrams, and generate English image-generation prompts with captions for scientific domains such as biology, systems engineering, AI, and computer vision. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Papers, images, or reference figures may be shared with the agent runtime or a downstream image-generation service. <br>
Mitigation: Use the skill only with content appropriate for those services and review applicable data-handling requirements before submitting sensitive material. <br>
Risk: Broad trigger keywords could activate the skill in contexts where figure generation was not intended. <br>
Mitigation: Prefer explicit invocation such as /draw-skills or narrow activation rules in environments that auto-trigger skills. <br>
Risk: Generated figure prompts or captions may misstate scientific details if the source paper is ambiguous or incomplete. <br>
Mitigation: Have a domain expert review generated prompts, labels, and captions before using them in a manuscript or presentation. <br>


## Reference(s): <br>
- [draw-skills ClawHub release page](https://clawhub.ai/memory555/draw-skills) <br>
- [PROMPT.md](artifact/PROMPT.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown figure plans and prompt blocks with English prompts, bilingual captions, and generation tips] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes checkpoints for figure-plan and style confirmation before final prompt generation.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
