## Description: <br>
Multi-target parallel file copy CLI that reads a source once into memory and writes to multiple USB drives concurrently. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dongsheng123132](https://clawhub.ai/user/dongsheng123132) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and agent users use FastCP to copy the same source directory to multiple mounted drives or destination directories, with options for verification, incremental copying, concurrency control, and dry-run previews. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Incorrect source or destination paths can copy data to the wrong drive or overwrite expected destination contents. <br>
Mitigation: Use --dry-run first, confirm every source and destination path, verify drive labels and free space, and review the command before execution. <br>
Risk: Installing with @latest may fetch a newer package than the reviewed release. <br>
Mitigation: Pin or review the GitHub package version before installation. <br>


## Reference(s): <br>
- [FastCP ClawHub Release](https://clawhub.ai/dongsheng123132/fastcp) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides use of a file-copy CLI; command execution writes to user-selected destination paths.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
