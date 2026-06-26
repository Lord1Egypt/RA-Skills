## Description: <br>
Advanced filesystem operations for Clawdbot, including listing, searching, batch processing, and directory analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[choichuncj](https://clawhub.ai/user/choichuncj) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent users use this skill to inspect local directories, search file names or file contents, copy matching files, render directory trees, and summarize filesystem structure. It is suited to project maintenance, log review, content organization, and other workflows that need controlled local file access. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The package requests broad local filesystem authority. <br>
Mitigation: Grant access only to specific non-sensitive directories, prefer read-only or dry-run operation, and review proposed changes before applying them. <br>
Risk: The release has inconsistent package evidence and limited verifiable implementation detail. <br>
Mitigation: Verify the publisher and source before installing, and ensure the package includes the expected filesystem executable or source. <br>
Risk: The artifact bundles a separate nano-pdf skill that may be outside the expected filesystem workflow. <br>
Mitigation: Review the bundled nano-pdf skill separately or remove it before deployment if PDF editing is not required. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/choichuncj/clawdbot-filesystem-bak) <br>
- [Publisher profile](https://clawhub.ai/user/choichuncj) <br>
- [Artifact README](README.md) <br>
- [Artifact license](LICENSE.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and plain text with command examples, tables, tree views, and JSON-style configuration snippets.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and local filesystem permissions; operations should be scoped to allowed non-sensitive directories.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
