## Description: <br>
Dump the current STM32 LCD framebuffer via J-Link and convert it to PNG for visual comparison with Figma. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ylongw](https://clawhub.ai/user/ylongw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and embedded UI engineers use this skill to capture the real pixels currently displayed by an STM32 LCD framebuffer and convert the raw dump into a PNG for design comparison or regression snapshots. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Framebuffer dumps, PNGs, and logs may contain sensitive information visible on the connected device screen. <br>
Mitigation: Use a private temporary directory when possible and delete raw dumps, PNGs, and logs after use if screen contents may be sensitive. <br>
Risk: Incorrect target device, framebuffer address, dimensions, dump size, or output path can produce invalid captures or read unintended device memory. <br>
Mitigation: Verify the target device, framebuffer address, size, pixel format, and output paths before running the J-Link dump workflow. <br>


## Reference(s): <br>
- [Framebuffer Dump on ClawHub](https://clawhub.ai/ylongw/framebuffer-dump) <br>
- [SEGGER J-Link Downloads](https://www.segger.com/downloads/jlink/) <br>
- [Pillow Python Package](https://pypi.org/project/Pillow/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with shell commands and parameter guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides J-Link framebuffer dumping and PNG conversion; the workflow produces a raw binary dump, log file, and PNG when executed by the user.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
