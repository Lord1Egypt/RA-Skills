## Description: <br>
Bidirectional file management system for OpenClaw workspaces that organizes, indexes, and retrieves files exchanged with users via local inbox files and command-line helpers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dgkim311](https://clawhub.ai/user/dgkim311) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to save, archive, tag, search, and report on files received from or sent to users across workspace channels. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill keeps persistent local copies and metadata for exchanged files, which can expose sensitive or regulated content if used indiscriminately. <br>
Mitigation: Use it only when a persistent archive is desired, avoid registering sensitive or regulated files, and periodically review or delete archived entries. <br>
Risk: Inbound registration moves files by default, which can surprise users who expect the original path to remain intact. <br>
Mitigation: Use --copy when the original file must remain in place, especially for outbound files that still need to be sent through a channel. <br>


## Reference(s): <br>
- [Channel Integration Guide](references/integration-guide.md) <br>
- [Auto-Tagging Guide](references/tagging-guide.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/dgkim311/file-inbox) <br>
- [Publisher Profile](https://clawhub.ai/user/dgkim311) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, plus local INDEX.md, JSON metadata, and command-line text output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates and updates a persistent local inbox directory, metadata file, and human-readable index.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
