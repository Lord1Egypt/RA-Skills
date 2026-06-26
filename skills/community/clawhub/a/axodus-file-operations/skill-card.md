## Description: <br>
Perform safe, auditable file operations with path validation and backups. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mzfshark](https://clawhub.ai/user/mzfshark) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to ask an agent to read, write, update, delete, move, or copy files while validating paths, creating backups for destructive changes, and reporting the result. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: File operations can delete, overwrite, or move user data if an agent is not constrained to the intended workspace. <br>
Mitigation: Install only in agents constrained to the intended workspace and require explicit approval for delete, overwrite, recursive, or bulk operations. <br>
Risk: Malformed activation metadata may make automatic triggering unreliable. <br>
Mitigation: Replace malformed trigger metadata with clear trigger phrases and scope limits before relying on automatic triggering. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mzfshark/axodus-file-operations) <br>
- [file-operations.md](artifact/file-operations.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or YAML-style status summaries with affected paths, backup paths, result status, and notes.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports operation, affected paths, backup locations, result, and notes; destructive operations should be backed up when possible.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
