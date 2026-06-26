## Description: <br>
Compresses images for web use with quality reduction and resizing to fit a target size, with WebP output by default and JPEG or PNG options. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[freedompixels](https://clawhub.ai/user/freedompixels) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, designers, and content teams use this skill to prepare local images for web publishing by compressing individual files or batches while preserving the original files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Batch and recursive processing can write optimized image outputs across the selected directory tree. <br>
Mitigation: Review input and output paths before running batch or recursive mode, and run it only on image directories intended for processing. <br>
Risk: Saved outputs strip image metadata as part of compression. <br>
Mitigation: Keep original images or separate metadata records when EXIF or other embedded metadata must be retained. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/freedompixels/cn-web-image-optimizer) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown or terminal text with file paths and compression results; optimized image files are written by the helper script.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Local image processing; configurable maximum size, output format, quality ceiling, output path, and recursive batch mode.] <br>

## Skill Version(s): <br>
1.1.2 (source: server release evidence; artifact frontmatter says 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
