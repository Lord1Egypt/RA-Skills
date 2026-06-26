## Description: <br>
Use CamScanner to extract formulas from images by uploading an image to CamScanner's OCR service, detecting formula regions, and downloading a stitched PNG result. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[camscanner-ai](https://clawhub.ai/user/camscanner-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to extract mathematical formulas, equations, or expressions from photos, screenshots, and scanned documents into a clean PNG image. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected images are uploaded to CamScanner's servers for formula extraction. <br>
Mitigation: Avoid using sensitive, proprietary, medical, financial, or student-record images unless CamScanner's privacy and retention terms have been reviewed and accepted. <br>
Risk: The workflow depends on external API availability and correct handling of binary download responses. <br>
Mitigation: Check each API response before continuing and include response_mode=raw when downloading the PNG result. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/camscanner-ai/camscanner-extract-formula) <br>
- [CamScanner homepage](https://www.camscanner.com) <br>
- [CamScanner AI tools API endpoint](https://ai-tools.camscanner.com) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown with bash and JSON examples; downloaded PNG output file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and jq; sends selected images to CamScanner servers for processing.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter reports 1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
