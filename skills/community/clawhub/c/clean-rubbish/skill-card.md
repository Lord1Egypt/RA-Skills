## Description: <br>
清空 macOS、Linux 和 Windows 的系统废纸篓或回收站，并通过 /clean-rubbish 触发。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lhyhy123](https://clawhub.ai/user/lhyhy123) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Users invoke this skill when they want an agent to empty the local system trash or recycle bin on macOS, Linux, or Windows. It is intended only when permanent deletion is acceptable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can permanently empty the trash or recycle bin and explicitly skips a final confirmation. <br>
Mitigation: Inspect trash contents first and require an explicit final confirmation before running any rm, osascript, or PowerShell deletion command. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline bash or PowerShell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands are operating-system specific and may delete files permanently.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
