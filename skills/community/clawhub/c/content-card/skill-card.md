## Description: <br>
Content Card turns text, URLs, or files into shareable PNG visual cards in long-form, infographic, or multi-card formats. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lovensky1992-wk](https://clawhub.ai/user/lovensky1992-wk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and content creators use this skill to convert articles, notes, analyses, and structured information into PNG cards for reading, infographics, or social-media sharing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Some mode instructions reference an unrelated local ljg-card path outside the reviewed package. <br>
Mitigation: Review and correct stale path references before use; prefer the included ~/.openclaw/skills/content-card/scripts/capture.js path from the reviewed package. <br>
Risk: The skill can process sensitive source documents and writes intermediate files and PNG outputs. <br>
Mitigation: Avoid highly sensitive inputs unless temporary files are cleaned afterward and the expected Downloads output location is acceptable. <br>


## Reference(s): <br>
- [README](README.md) <br>
- [Long Card Mode](references/mode-long.md) <br>
- [Infographic Mode](references/mode-infograph.md) <br>
- [Poster Mode](references/mode-poster.md) <br>
- [Preferences Schema](references/config/preferences-schema.md) <br>
- [Taste Guidelines](references/taste.md) <br>
- [OpenClaw](https://github.com/openclaw/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, files] <br>
**Output Format:** [Markdown guidance with HTML/CSS templates and generated PNG files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces PNG card assets, intermediate HTML, structured content files, and file paths for generated outputs.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
