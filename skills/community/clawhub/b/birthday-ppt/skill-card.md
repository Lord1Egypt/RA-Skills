## Description: <br>
Generates customized kindergarten birthday PowerPoint decks with child details, themed decorations, photo pages, blessing text, and closing slides using python-pptx. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kukuxnd](https://clawhub.ai/user/kukuxnd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Parents, teachers, and caregivers use this skill to create birthday-themed PPTX presentations for kindergarten children, including growth photos, themed colors, decorative slides, and family blessing text. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Photo paths may point to untrusted or unavailable files, and the evidence guidance notes that URL photos should not be assumed to work unless network fetching is documented and constrained. <br>
Mitigation: Use trusted local image files and verify photo paths before generation. <br>
Risk: The generated PPTX may replace an existing file at the chosen output path. <br>
Mitigation: Choose a deliberate output path and review whether a file already exists there before running the skill. <br>


## Reference(s): <br>
- [Birthday PPT Creator on ClawHub](https://clawhub.ai/kukuxnd/birthday-ppt) <br>


## Skill Output: <br>
**Output Type(s):** [code, shell commands, configuration, guidance] <br>
**Output Format:** [Python script invocation that writes a .pptx presentation file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python-pptx and Pillow; accepts child name, birth date, photo paths, output path, and a pink, blue, purple, or yellow theme.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
