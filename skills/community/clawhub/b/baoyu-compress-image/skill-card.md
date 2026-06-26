## Description: <br>
Compresses images to WebP, PNG, or JPEG with automatic compressor selection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jimliu](https://clawhub.ai/user/jimliu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to compress, optimize, or convert local image files and image directories while choosing format, quality, recursion, and whether to keep originals. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The compressor can rename or replace original image files by default. <br>
Mitigation: Use --keep for important originals, test on copies before recursive directory runs, and review output paths before converting to the same format. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jimliu/baoyu-compress-image) <br>
- [Project homepage](https://github.com/JimLiu/baoyu-skills#baoyu-compress-image) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with shell commands; CLI output is plain text or JSON when --json is used.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May process one file or a directory of supported image files; supports WebP, PNG, and JPEG output.] <br>

## Skill Version(s): <br>
1.117.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
