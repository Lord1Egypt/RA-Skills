## Description: <br>
Process and convert images with resizing, cropping, compression, thumbnail generation, filters, and format conversion. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dinghaibin](https://clawhub.ai/user/dinghaibin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content operators use this skill to process local image files, including resizing batches, converting formats, compressing images for web use, making thumbnails, and applying simple filters. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Image processing can overwrite the input file when no separate output path is supplied. <br>
Mitigation: Pass --output for each operation or work on copies of source images. <br>
Risk: Fallback mode without Pillow may copy and rename a file instead of performing real format conversion. <br>
Mitigation: Install Pillow for conversion workflows and do not rely on fallback mode for format changes. <br>


## Reference(s): <br>
- [Image Processor ClawHub Release](https://clawhub.ai/dinghaibin/dinghaibin-image-processor) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and local file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May invoke a local Python script that writes processed image files to the requested output path.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
