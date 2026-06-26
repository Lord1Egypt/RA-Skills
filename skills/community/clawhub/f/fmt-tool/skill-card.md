## Description: <br>
Simple text formatting and reflow tool. Use for reformatting paragraphs, removing extra whitespace, and cleaning up text files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dinghaibin](https://clawhub.ai/user/dinghaibin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and other agent users can use this skill to reflow paragraphs, normalize whitespace, and clean up local text files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The helper reads local text from the file path explicitly passed to it, so an agent could expose sensitive content if it is pointed at the wrong file. <br>
Mitigation: Review file paths before invoking the formatter and avoid passing files that contain secrets, credentials, or private data. <br>
Risk: The documented -w option syntax may not match the bundled helper script's positional argument handling. <br>
Mitigation: Test the command shape in a controlled workspace or update the wrapper before relying on width flags in production workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dinghaibin/fmt-tool) <br>
- [Publisher profile](https://clawhub.ai/user/dinghaibin) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text and Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Formats a single text stream or local text file path supplied by the user.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
