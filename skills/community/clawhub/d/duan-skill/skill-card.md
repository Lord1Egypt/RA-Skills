## Description: <br>
Creates presentation workflows by structuring content, selecting visual styles, generating AI illustrations or HTML slides, and exporting PPTX files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lifenglei](https://clawhub.ai/user/lifenglei) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to turn a short prompt or source material into Chinese slide outlines, visual direction, AI-generated imagery or editable HTML slides, and PPTX deliverables for business, education, training, pitch, and reporting scenarios. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, slide text, reference images, or personal photos may be processed by Gemini. <br>
Mitigation: Use the skill only when external Gemini processing is acceptable; avoid confidential decks and personal photos unless approved. <br>
Risk: A local Gemini API key is used by the image-generation helper. <br>
Mitigation: Use a limited API key and keep credentials out of generated decks, prompts, and shared outputs. <br>
Risk: Helper scripts could be resolved from an unintended matching skill directory. <br>
Mitigation: Verify the resolved scripts directory before running generation or PPTX conversion commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lifenglei/duan-skill) <br>
- [Prompt templates](references/prompt-templates.md) <br>
- [Proven styles gallery](references/proven-styles-gallery.md) <br>
- [Design principles](references/design-principles.md) <br>
- [Design movements](references/design-movements.md) <br>
- [Snoopy style guide](references/proven-styles-snoopy.md) <br>
- [Ten Simple Rules for Effective Presentation Slides](https://pmc.ncbi.nlm.nih.gov/articles/PMC8638955/) <br>
- [Assertion-Evidence research](https://writing.engr.psu.edu/ae_comprehension.pdf) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with slide outlines, HTML/CSS slide code, image-generation prompts, shell commands, PNG assets, and PPTX files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use Gemini image generation and local PPTX conversion scripts; Path A keeps slide text editable, while Path B produces image-based slides.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and target metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
