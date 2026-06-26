## Description: <br>
Turn an uploaded photo into a printable black-and-white coloring page. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Borahm](https://clawhub.ai/user/Borahm) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to convert an uploaded JPG, PNG, or WebP photo into a printable coloring-page PNG. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill processes uploaded photos with external Gemini image processing. <br>
Mitigation: Avoid uploading sensitive personal photos unless external processing is acceptable for the user and deployment context. <br>
Risk: The skill requires a Gemini API key and may consume quota or incur billing. <br>
Mitigation: Use a dedicated Gemini API key where possible and monitor quota and billing for the account. <br>
Risk: The skill delegates execution to a referenced command and the nano-banana-pro skill. <br>
Mitigation: Confirm those dependencies come from trusted sources before installing or running the skill. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/Borahm/coloring-page) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/Borahm) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance, image file] <br>
**Output Format:** [Markdown guidance with shell command examples; generated output is a PNG image file.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Accepts raster image inputs in JPG, PNG, or WebP format and supports 1K, 2K, and 4K output resolution options.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
