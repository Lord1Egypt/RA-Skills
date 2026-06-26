## Description: <br>
Uses CamScanner to remove visible watermarks, stamps, and translucent logos from images while preserving the underlying content and layout. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[camscanner-ai](https://clawhub.ai/user/camscanner-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to generate CamScanner API workflows for uploading an image, applying watermark removal, and saving the cleaned image locally. Use should be limited to images the user owns or is authorized to edit. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Images are sent to a CamScanner-hosted endpoint for processing, which can expose private or sensitive content. <br>
Mitigation: Use only approved, non-sensitive images and confirm that sending them to CamScanner is acceptable for the user's privacy and data-handling requirements. <br>
Risk: Removing watermarks, stamps, seals, signatures, or authenticity marks can create legal and document-integrity concerns. <br>
Mitigation: Use only on images the user owns or is authorized to edit, and avoid IDs, contracts, certificates, official records, signatures, seals, or other provenance marks. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/camscanner-ai/camscanner-image-remove-watermark) <br>
- [CamScanner homepage](https://www.camscanner.com) <br>
- [CamScanner AI tools API endpoint](https://ai-tools.camscanner.com) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, text] <br>
**Output Format:** [Markdown with inline bash and JSON code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The generated workflow can save a processed JPG image to a caller-specified local path.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence; frontmatter reports 1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
