## Description: <br>
A fast and user-friendly alternative to 'find' - simple syntax, smart defaults, respects gitignore. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Arnarsson](https://clawhub.ai/user/Arnarsson) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to find files and directories quickly with fd, including filtering by name, type, extension, size, modification time, and path patterns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Deletion and bulk-operation examples can affect more files than intended when search scope or patterns are too broad. <br>
Mitigation: Run the fd search alone first, review the matched files, and narrow the directory or filters before using rm, xargs, -x, or bulk copy commands. <br>
Risk: The skill depends on the fd binary being installed from the local operating system package ecosystem. <br>
Mitigation: Install fd from a trusted package manager and confirm the fd command is available before following the command examples. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Arnarsson/fd-find) <br>
- [fd GitHub repository](https://github.com/sharkdp/fd) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes command examples for fd searches, filters, execution flags, and integrations with command-line tools.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
