## Description: <br>
Merge multiple lines of text into a single line with a customizable separator using a Python command-line tool. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[freedompixels](https://clawhub.ai/user/freedompixels) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and other agent users can use this skill to convert newline-delimited text into a single line with a chosen separator. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Command-line text processing can produce unexpected output if the input text or separator is not what the user intended. <br>
Mitigation: Review the provided text and separator before running the command, and inspect the resulting single-line output before using it downstream. <br>
Risk: The release evidence security guidance is generic and references broader maintenance workflows rather than this small line-joining artifact. <br>
Mitigation: Treat evidence.security as authoritative for the release verdict, and review the artifact files directly before installing or reusing the skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/freedompixels/cn-join-lines) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, code] <br>
**Output Format:** [Plain text or Markdown with Python command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses Python standard library only; the separator defaults to a space.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
