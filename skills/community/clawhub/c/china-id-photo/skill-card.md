## Description: <br>
Generates China-standard ID, passport, visa, and other document photos with selected sizes and white, blue, or red backgrounds. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ToBeWin](https://clawhub.ai/user/ToBeWin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to turn a local personal photo into a standards-sized China ID, passport, visa, or similar document photo with the requested size, background color, and output format. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Dependency installation and first-run model setup may contact external package or model sources. <br>
Mitigation: Review the pip install command before use and install the skill in a virtual environment where possible. <br>
Risk: The skill processes personal photos. <br>
Mitigation: Only provide photos intended for local processing and keep generated output directories access-controlled. <br>
Risk: Generated photos may not satisfy every destination authority's current submission rules. <br>
Mitigation: Verify size, background, pose, and file-format requirements against the target application before submitting the result. <br>


## Reference(s): <br>
- [China ID Photo ClawHub release](https://clawhub.ai/ToBeWin/china-id-photo) <br>
- [China ID photo standard size reference](references/sizes.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Code, Files, Configuration] <br>
**Output Format:** [Markdown with inline bash and Python code blocks; generated image files are JPEG or PNG.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and installs rembg, Pillow, and opencv-python-headless when dependencies are missing.] <br>

## Skill Version(s): <br>
1.2.1 (source: server release evidence; artifact frontmatter says 1.2.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
