## Description: <br>
Creates reveal.js HTML presentations with complete word-for-word speaker scripts, presenter view, structured slide content, and optional Gemini-generated whiteboard illustrations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lewislulu](https://clawhub.ai/user/lewislulu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, employees, and developers use this skill to turn topics, notes, or markdown into presentation-ready reveal.js HTML decks with slide structure, visuals, and speaker scripts for live talks or technical sharing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Presentation content may be sent to Gemini when image generation is used. <br>
Mitigation: Use the skill only with content approved for third-party image-generation providers, and avoid confidential customer or business material unless policy permits it. <br>
Risk: Gemini API keys may be exposed if pasted into chat or stored insecurely. <br>
Mitigation: Configure the key through a secure secret mechanism such as an environment variable, and avoid sharing raw credentials in prompts or generated files. <br>
Risk: Generated slide content and speaker scripts may be inaccurate or unsuitable for the intended audience. <br>
Mitigation: Review the markdown draft, generated HTML, and speaker notes before presentation or publication. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/lewislulu/ai-ppt-presenter) <br>
- [Skill Instructions](artifact/SKILL.md) <br>
- [Reveal Template](artifact/assets/reveal-template.html) <br>
- [Gemini Image Generation Script](artifact/scripts/generate_slide_images.py) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with HTML, JSON, and bash snippets; generated artifacts can include reveal.js HTML and image files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call Gemini image-generation APIs when the user chooses to generate slide illustrations; speaker scripts are expected in reveal.js notes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
