## Description: <br>
Uses CamScanner's image enhancement API to remove watermarks, stamps, and translucent logos from images while preserving underlying content and layout. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[camscanner-ai](https://clawhub.ai/user/camscanner-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to prepare curl and jq workflows for uploading an authorized image to CamScanner, applying the remove-watermark enhancement, and saving a cleaned JPG locally. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill removes watermarks, stamps, and similar marks, which can be misused on copyrighted images or documents where marks indicate authenticity or provenance. <br>
Mitigation: Use only on images the user owns or is authorized to edit, and avoid IDs, contracts, certificates, signatures, seals, official records, or copyrighted third-party images. <br>
Risk: Image files are sent to CamScanner's servers for processing. <br>
Mitigation: Confirm third-party upload and processing are acceptable before use, especially for sensitive, regulated, or confidential documents. <br>


## Reference(s): <br>
- [CamScanner homepage](https://www.camscanner.com) <br>
- [CamScanner AI tools API base URL](https://ai-tools.camscanner.com) <br>
- [ClawHub skill page](https://clawhub.ai/camscanner-ai/skills/camscanner-image-remove-watermark) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, Configuration] <br>
**Output Format:** [Markdown with bash and JSON snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and jq; when executed, the generated workflow uploads an image to CamScanner and writes the processed JPG to a local path.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
