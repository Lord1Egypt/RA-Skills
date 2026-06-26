## Description: <br>
Generate cute cartoon-style pet images (dogs, cats, etc.) using code. Use when user asks for cartoon pet drawings, cute animal illustrations, or simple pet avatars. No AI image API required - generates SVG and converts to PNG using Node.js and rsvg-convert. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[juliantsaiii](https://clawhub.ai/user/juliantsaiii) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill to generate simple cartoon pet avatars or illustrations as SVG-derived PNG files without calling an external image generation API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A crafted output filename could cause the script to run unintended shell commands. <br>
Mitigation: Review before installing, use only fixed and trusted output filenames in a safe directory such as /tmp, and prefer a patched version that validates paths and uses execFileSync or spawn with argument arrays instead of shell strings. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Files] <br>
**Output Format:** [Markdown guidance with shell commands that produce SVG and PNG image files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports dog, cat, rabbit, and bear pet types with color and size options.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
