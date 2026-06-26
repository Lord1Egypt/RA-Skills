## Description: <br>
Advanced filesystem operations - listing, searching, batch processing, and directory analysis for Clawdbot. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Lucky-2968](https://clawhub.ai/user/Lucky-2968) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, operators, and agent users use this skill to list, search, copy, visualize, and analyze local files and directories with filtering, dry-run previews, and safety checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can inspect and copy local files, so broad paths may expose or duplicate sensitive data. <br>
Mitigation: Use narrow target paths, review file patterns before execution, and avoid broad paths such as a full home directory unless necessary. <br>
Risk: Batch copy operations can overwrite or move more files than intended when patterns are too broad. <br>
Mitigation: Run copy operations with dry-run first and require explicit confirmation before overwriting files. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/Lucky-2968/clawdbot-filesystem-1-0-2) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and command-line text, with optional table, tree, JSON, and list output from filesystem operations.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and can inspect or copy local files according to the configured path, filtering, and safety options.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
