## Description: <br>
Batch Renamer helps users prepare and run bulk file renaming workflows with naming patterns, regular-expression replacement, preview, backup, and undo support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[utopiabenben](https://clawhub.ai/user/utopiabenben) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to organize photos, downloads, and document collections by generating or running batch rename commands with preview and undo safeguards. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The install instructions include an unverified global package path. <br>
Mitigation: Prefer reviewing and running the included Python script directly unless the package source has been independently trusted. <br>
Risk: Bulk rename operations can make broad file changes or produce unsafe paths when patterns or regex replacements are too permissive. <br>
Mitigation: Run preview mode first, test on copied folders, and avoid replacements that introduce slashes, absolute paths, or parent-directory references. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/utopiabenben/batch-renamer) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include preview-first rename commands, undo guidance, and configuration snippets.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
