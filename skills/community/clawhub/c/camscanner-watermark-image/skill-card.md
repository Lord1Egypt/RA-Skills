## Description: <br>
Use CamScanner to add a tiled text watermark across an entire image with custom text, color, opacity, and font size. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[camscanner-ai](https://clawhub.ai/user/camscanner-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to upload an image to CamScanner, apply repeating diagonal watermark text such as Confidential or Draft, and download the processed image. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected images are uploaded to CamScanner servers for processing. <br>
Mitigation: Use only images approved for third-party processing, and avoid highly sensitive images unless that processing is acceptable for the use case. <br>
Risk: RGBA PNG images with an alpha channel may fail in the upstream image processor. <br>
Mitigation: Convert affected PNG files to JPEG before upload when this failure occurs. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/camscanner-ai/camscanner-watermark-image) <br>
- [CamScanner Homepage](https://www.camscanner.com) <br>
- [CamScanner AI Tools API](https://ai-tools.camscanner.com) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces command guidance for uploading an image, applying a watermark, and downloading the resulting file.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; frontmatter reports 1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
