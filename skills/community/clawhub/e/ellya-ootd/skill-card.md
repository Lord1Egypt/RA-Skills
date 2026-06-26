## Description: <br>
OpenClaw virtual companion skill that bootstraps character state, learns style prompts from uploaded photos, and generates prompt-based selfies or multi-pose photo series. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[laogiant](https://clawhub.ai/user/laogiant) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw agents and their operators use this skill to personalize a virtual companion, learn reusable outfit and visual-style descriptions from reference photos, and generate single images or photo series to send back in conversation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Uploaded reference photos, base images, generated outputs, and saved style text may contain sensitive appearance details. <br>
Mitigation: Use only images the user is authorized to process, avoid minors, private documents, intimate images, and non-consenting people, and review or delete saved assets, outputs, and styles after use. <br>
Risk: Reference images and prompts may be sent to third-party AI providers during analysis or generation. <br>
Mitigation: Install and run the skill only when the operator is comfortable with that provider exposure and has configured the intended provider credentials. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/laogiant/ellya-ootd) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [ANALYSIS_PROMPT.md](artifact/ANALYSIS_PROMPT.md) <br>
- [SOUL.md template](artifact/templates/SOUL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with inline shell commands; bundled scripts create style markdown files and generated image files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user-supplied reference images and configured Gemini or Minimax credentials; photo series generation accepts 1 to 10 variations.] <br>

## Skill Version(s): <br>
1.0.2 (source: target metadata and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
