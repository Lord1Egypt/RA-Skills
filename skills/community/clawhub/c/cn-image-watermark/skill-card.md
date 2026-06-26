## Description: <br>
Cn Image Watermark helps agents add text or logo watermarks to local image files, including single-image and batch workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[freedompixels](https://clawhub.ai/user/freedompixels) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, content creators, and operators use this skill to apply copyright, brand, or anti-repost watermarks to local image assets through agent-run commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Batch mode can touch many files or write outputs to an unintended folder if given a broad input directory or wrong output path. <br>
Mitigation: Review input and output paths before running batch jobs, and test on a small folder first. <br>
Risk: Server security evidence notes a reliability bug in batch mode that may affect automation. <br>
Mitigation: Avoid relying on batch mode for unattended workflows until the bug is fixed or manually verified in the target environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/freedompixels/cn-image-watermark) <br>
- [Publisher profile](https://clawhub.ai/user/freedompixels) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, JSON, files, guidance] <br>
**Output Format:** [Agent guidance with shell commands; the watermark script emits JSON status and writes image files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python 3 and Pillow; output paths should be reviewed before batch processing.] <br>

## Skill Version(s): <br>
1.2.7 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
