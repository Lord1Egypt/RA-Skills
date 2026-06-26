## Description: <br>
CamScanner Image HD helps agents enhance image clarity by uploading a selected image to CamScanner for auto-crop and HD filtering, with optional demoire processing only when requested. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[camscanner-ai](https://clawhub.ai/user/camscanner-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to prepare a curl and jq image-enhancement pipeline for photos or scanned documents that need clearer, sharper, higher-definition output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected images are sent to CamScanner servers for processing, so image contents are handled by a third-party service. <br>
Mitigation: Avoid sensitive IDs, medical, legal, financial, or private business documents unless CamScanner's privacy and retention terms meet the user's needs. <br>
Risk: The pipeline downloads the enhanced image to a user-specified local path. <br>
Mitigation: Confirm the input and output paths before running the commands. <br>


## Reference(s): <br>
- [CamScanner Homepage](https://www.camscanner.com) <br>
- [CamScanner AI Tools API](https://ai-tools.camscanner.com) <br>
- [ClawHub Skill Page](https://clawhub.ai/camscanner-ai/camscanner-image-hd) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and jq; output files are saved to the local path selected by the user.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
